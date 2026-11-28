"""Deterministic STEP-020 Connected-Component Patient Graph & Leakage-Safe Splitter.

Constructs an undirected equivalence graph (`UD10`) across frozen `LBL0001–LBL0005`
cohorts connecting:
1. `(DatasetID, PatientGroupID)` identity links
2. Non-empty DICOM header `DICOMPatientIDHash` and `DICOMStudyUIDHash` links
3. Exact / pixel-clone duplicate clusters (`ExactDupCluster`, e.g., CMMD `D1-0202<->D2-0284`,
   `D1-0808<->D1-1292`, BMCD `Normal_40<->Suspicious_16`, DMID `IMG019/021/034` clones)
4. Left/Right bilateral pairs in `DS0001 MIAS` (`mdb001/002`, ..., `mdb321/322`)

Partitions `DS0003 CMMD` (primary internal biopsy FFDM track) atomically by connected
component into stratified `70% train / 15% val / 15% internal_test` plus deterministic
`5-fold` CV over `train+val` only (`internal_test` sealed custody), keeps `DS0006`,
`DS0005`, `DS0002`, and `DS0001` cleanly isolated as zero-shot external evaluation
cohorts (with intra-cohort patient-grouped `cohort_subsplit` on `DS0006`), and fails
loudly on any injected cross-partition overlap.
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import networkx as nx
import yaml

from bc_xai.labels.freeze import COHORT_TO_LBL_ID, sha256_file

DEFAULT_SPLIT_SEED = 20261128
PRIMARY_INTERNAL_DATASET = "DS0003"
EXTERNAL_PARTITION_BY_DATASET: dict[str, str] = {
    "DS0006": "external_eval_loc",
    "DS0005": "external_test_bmcd",
    "DS0002": "external_test_dmid",
    "DS0001": "external_test_mias_sfm",
}
SPLIT_MANIFEST_FIELDS: list[str] = [
    "SplitID",
    "ImageID",
    "DatasetID",
    "LabelReleaseID",
    "PatientGroupID",
    "ComponentID",
    "primary_partition",
    "dev_fold_5",
    "cohort_subsplit",
    "custody_tier",
    "eligible_for_modeling",
    "BinaryTarget",
    "LabelClass",
    "LabelProvenanceTier",
    "SubTrackA_BiopsyEligible",
    "SubTrackB_ScreeningEligible",
    "LesionTrack_BenignVsMalignant",
    "LocalizationEligible",
    "ViewPosition",
    "Laterality",
    "DensityACR",
    "MorphologyType",
    "MultiLesionConflict",
    "AnomalyFlags",
]


class LeakageError(ValueError):
    """Raised loudly whenever connected components, patients, or clones bridge partitions."""


@dataclass(frozen=True)
class SplitConfig:
    """Deterministic `SPLIT####` partitioning and custody specification (`UD10–UD11`)."""

    split_id: str = "SPLIT0001"
    seed: int = DEFAULT_SPLIT_SEED
    primary_internal_dataset: str = PRIMARY_INTERNAL_DATASET
    train_ratio: float = 0.70
    val_ratio: float = 0.15
    test_ratio: float = 0.15
    dev_folds: int = 5


@dataclass
class ComponentRecord:
    """Aggregate attributes of one atomic connected patient/clone component."""

    component_id: str
    dataset_id: str
    image_ids: list[str]
    non_excluded_image_ids: list[str]
    patient_group_ids: list[str]
    max_target: str
    has_bilateral_discordance: bool
    dominant_morphology: str
    has_subtrack_a: bool
    has_loc_lesion_mask: bool


def _load_qc_identity_map(qc_dir: Path, datasets: list[str]) -> dict[tuple[str, str], dict[str, str]]:
    """Load `(DatasetID, ImageID) -> QC identity tags` without exposing raw file paths."""
    out: dict[tuple[str, str], dict[str, str]] = {}
    for ds_id in datasets:
        qp = qc_dir / f"{ds_id}_qc_details.csv"
        if not qp.is_file():
            continue
        with qp.open("r", encoding="utf-8", newline="") as fp:
            for row in csv.DictReader(fp):
                if row.get("RoleTrack", "") != "primary_image":
                    continue
                out[(ds_id, row["ImageID"].strip())] = {
                    "DICOMPatientIDHash": row.get("DICOMPatientIDHash", "").strip(),
                    "DICOMStudyUIDHash": row.get("DICOMStudyUIDHash", "").strip(),
                    "ExactDupCluster": row.get("ExactDupCluster", "").strip(),
                    "SHA256": row.get("SHA256", "").strip(),
                }
    return out


def _mias_bilateral_pair_token(source_stem: str) -> str:
    """Map `mdb001l`/`mdb002r` -> `MIAS_PAIR_001` cleanly (`161` paired women)."""
    stem = source_stem.strip().lower()
    if stem.startswith("mdb") and len(stem) >= 6 and stem[3:6].isdigit():
        num = int(stem[3:6])
        pair_idx = (num - 1) // 2 + 1
        return f"MIAS_PAIR_{pair_idx:03d}"
    return f"MIAS_SOLO_{stem}"


def build_equivalence_graph(
    manifest_rows: list[dict[str, str]],
    qc_identity: dict[tuple[str, str], dict[str, str]] | None = None,
) -> tuple[nx.Graph, dict[tuple[str, str], str]]:
    """Construct undirected patient/study/bilateral/clone graph across all images (`UD10`)."""
    g = nx.Graph()
    qc_identity = qc_identity or {}

    for row in manifest_rows:
        ds_id = row["DatasetID"].strip()
        img_id = row["ImageID"].strip()
        pat_id = row["PatientGroupID"].strip()
        img_node = f"IMG::{ds_id}::{img_id}"
        g.add_node(img_node, kind="image", dataset_id=ds_id, image_id=img_id)

        if pat_id and pat_id not in {"PAT_UNRESOLVED", "unknown", "none"}:
            g.add_edge(img_node, f"PAT::{ds_id}::{pat_id}")

        if ds_id == "DS0001" and row.get("SourceStem"):
            pair_tok = _mias_bilateral_pair_token(row["SourceStem"])
            g.add_edge(img_node, f"MIAS_PAIR::{pair_tok}")

        qmeta = qc_identity.get((ds_id, img_id), {})
        for key, prefix in [
            ("DICOMPatientIDHash", "DPID"),
            ("DICOMStudyUIDHash", "DSTUDY"),
            ("ExactDupCluster", "DUP"),
            ("SHA256", "FILE_SHA"),
        ]:
            val = qmeta.get(key, "").strip()
            if val and val not in {"none", "not_reported", "null", ""}:
                scope = "GLOBAL" if prefix in {"DUP", "FILE_SHA"} else ds_id
                g.add_edge(img_node, f"{prefix}::{scope}::{val}")

        # Also honor explicit optional duplicate cluster column in synthetic test inputs
        for opt_col, prefix in [("ExactDupCluster", "DUP"), ("StudyGroupID", "STUDY")]:
            val = row.get(opt_col, "").strip()
            if val and val not in {"none", "not_reported", "DUP_NONE", ""}:
                scope = "GLOBAL" if prefix == "DUP" else ds_id
                g.add_edge(img_node, f"{prefix}::{scope}::{val}")

    raw_comps: list[tuple[str, str, list[tuple[str, str]]]] = []
    for comp in nx.connected_components(g):
        img_keys = sorted(
            (g.nodes[n]["dataset_id"], g.nodes[n]["image_id"])
            for n in comp
            if g.nodes[n].get("kind") == "image"
        )
        if not img_keys:
            continue
        ds_set = {k[0] for k in img_keys}
        if len(ds_set) > 1:
            raise LeakageError(
                f"Cross-cohort duplicate/identity cluster detected across {sorted(ds_set)}: {img_keys[:5]}"
            )
        ds_id = next(iter(ds_set))
        raw_comps.append((ds_id, img_keys[0][1], img_keys))

    raw_comps.sort(key=lambda t: (t[0], t[1]))
    comp_id_by_img: dict[tuple[str, str], str] = {}
    counters: collections.Counter[str] = collections.Counter()
    for ds_id, _, img_keys in raw_comps:
        counters[ds_id] += 1
        cid = f"COMP_{ds_id}_{counters[ds_id]:04d}"
        for k in img_keys:
            comp_id_by_img[k] = cid
    return g, comp_id_by_img


def _summarize_components(
    manifest_rows: list[dict[str, str]],
    comp_id_by_img: dict[tuple[str, str], str],
) -> dict[str, ComponentRecord]:
    """Summarize each atomic component's non-excluded clinical stratification attributes."""
    grouped: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    for row in manifest_rows:
        cid = comp_id_by_img[(row["DatasetID"].strip(), row["ImageID"].strip())]
        grouped[cid].append(row)

    out: dict[str, ComponentRecord] = {}
    for cid, rows in sorted(grouped.items()):
        ds_id = rows[0]["DatasetID"].strip()
        non_ex = [r for r in rows if r["BinaryTarget"] != "Excluded"]
        t_set = {r["BinaryTarget"] for r in non_ex}
        if "1" in t_set:
            max_t = "1"
        elif "0" in t_set:
            max_t = "0"
        else:
            max_t = "Excluded"
        bilat_disc = any("BilateralDiscordantPatient" in r.get("AnomalyFlags", "") for r in non_ex)
        morphs = [r.get("MorphologyType", "none") for r in non_ex]
        if any(m == "both" for m in morphs) or ("mass" in morphs and "calcification" in morphs):
            dom_m = "both"
        elif any("calc" in m for m in morphs):
            dom_m = "calcification"
        elif any(m != "none" for m in morphs):
            dom_m = "mass_or_other"
        else:
            dom_m = "none"

        out[cid] = ComponentRecord(
            component_id=cid,
            dataset_id=ds_id,
            image_ids=[r["ImageID"].strip() for r in rows],
            non_excluded_image_ids=[r["ImageID"].strip() for r in non_ex],
            patient_group_ids=sorted({r["PatientGroupID"].strip() for r in rows}),
            max_target=max_t,
            has_bilateral_discordance=bilat_disc,
            dominant_morphology=dom_m,
            has_subtrack_a=any(r["SubTrackA_BiopsyEligible"] == "True" for r in non_ex),
            has_loc_lesion_mask=any(
                r["LocalizationEligible"] == "True" and r["LabelClass"] != "Normal_Control" for r in non_ex
            ),
        )
    return out


def _stratified_group_buckets(
    comps: list[ComponentRecord],
    bucket_targets: dict[str, float],
    seed: int,
    strat_key_fn: Any,
) -> dict[str, str]:
    """Deterministically allocate components across named buckets honoring target ratios."""
    if not comps:
        return {}
    rng = random.Random(seed)
    bucket_names = list(bucket_targets.keys())
    total_non_ex_imgs = sum(len(c.non_excluded_image_ids) for c in comps)
    desired_imgs = {b: total_non_ex_imgs * bucket_targets[b] for b in bucket_names}
    desired_comps = {b: len(comps) * bucket_targets[b] for b in bucket_names}

    assigned_imgs: collections.Counter[str] = collections.Counter()
    assigned_comps: collections.Counter[str] = collections.Counter()
    strata: dict[Any, list[ComponentRecord]] = collections.defaultdict(list)
    for c in comps:
        strata[strat_key_fn(c)].append(c)

    result: dict[str, str] = {}
    for skey in sorted(strata.keys()):
        group_list = sorted(strata[skey], key=lambda c: c.component_id)
        rng.shuffle(group_list)
        # Assign larger components first within stratum to minimize count drift
        group_list.sort(key=lambda c: len(c.non_excluded_image_ids), reverse=True)
        for comp in group_list:
            n_imgs = len(comp.non_excluded_image_ids)
            best_b = max(
                bucket_names,
                key=lambda b: (
                    (desired_imgs[b] - assigned_imgs[b]) / max(desired_imgs[b], 1.0),
                    (desired_comps[b] - assigned_comps[b]) / max(desired_comps[b], 1.0),
                    -bucket_names.index(b),
                ),
            )
            result[comp.component_id] = best_b
            assigned_imgs[best_b] += n_imgs
            assigned_comps[best_b] += 1
    return result


def assert_zero_leakage(split_rows: list[dict[str, str]]) -> None:
    """Fail loudly with `LeakageError` if any component or patient crosses partitions."""
    comp_to_parts: dict[str, set[str]] = collections.defaultdict(set)
    pat_to_parts: dict[tuple[str, str], set[str]] = collections.defaultdict(set)
    img_seen: set[tuple[str, str]] = set()
    comp_to_subsplits: dict[str, set[str]] = collections.defaultdict(set)

    for r in split_rows:
        ds_id = r["DatasetID"]
        img_id = r["ImageID"]
        key = (ds_id, img_id)
        if key in img_seen:
            raise LeakageError(f"Duplicate image entry in split manifest: {key}")
        img_seen.add(key)

        part = r["primary_partition"]
        if part == "excluded":
            continue
        cid = r["ComponentID"]
        pid = r["PatientGroupID"]
        comp_to_parts[cid].add(part)
        if pid not in {"PAT_UNRESOLVED", "unknown", "none"}:
            pat_to_parts[(ds_id, pid)].add(part)
        sub = r.get("cohort_subsplit", "none")
        if sub not in {"none", "excluded", ""}:
            comp_to_subsplits[cid].add(sub)

    bad_comps = {c: sorted(ps) for c, ps in comp_to_parts.items() if len(ps) > 1}
    if bad_comps:
        raise LeakageError(f"Connected component bridges multiple partitions: {list(bad_comps.items())[:5]}")
    bad_pats = {p: sorted(ps) for p, ps in pat_to_parts.items() if len(ps) > 1}
    if bad_pats:
        raise LeakageError(f"PatientGroupID bridges multiple partitions: {list(bad_pats.items())[:5]}")
    bad_subs = {c: sorted(ss) for c, ss in comp_to_subsplits.items() if len(ss) > 1}
    if bad_subs:
        raise LeakageError(f"Connected component bridges cohort_subsplits: {list(bad_subs.items())[:5]}")

    # Enforce sealed custody: internal_test must never appear inside dev_fold_5
    for r in split_rows:
        if r["primary_partition"] == "internal_test" and str(r["dev_fold_5"]) not in {"-1", "none", ""}:
            raise LeakageError(f"Sealed internal_test row assigned dev_fold_5={r['dev_fold_5']} ({r['ImageID']})")


def audit_external_split_overlap(
    official_split_by_img: dict[str, str],
    comp_id_by_img: dict[tuple[str, str], str],
    dataset_id: str,
) -> dict[str, Any]:
    """Audit an external/official split table for connected-component leakage."""
    comp_parts: dict[str, set[str]] = collections.defaultdict(set)
    for img_id, official_part in official_split_by_img.items():
        cid = comp_id_by_img.get((dataset_id, img_id))
        if cid:
            comp_parts[cid].add(official_part)
    leaking = {c: sorted(ps) for c, ps in comp_parts.items() if len(ps) > 1}
    return {
        "dataset_id": dataset_id,
        "audited_components": len(comp_parts),
        "leaking_component_count": len(leaking),
        "leaking_examples": dict(list(leaking.items())[:10]),
    }


def generate_split_release(
    manifest_rows: list[dict[str, str]],
    qc_identity: dict[tuple[str, str], dict[str, str]] | None = None,
    cfg: SplitConfig | None = None,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    """Build deterministic zero-leakage `SPLIT####` assignment table and summary metrics."""
    cfg = cfg or SplitConfig()
    _, comp_id_by_img = build_equivalence_graph(manifest_rows, qc_identity=qc_identity)
    comp_map = _summarize_components(manifest_rows, comp_id_by_img)

    # Separate active non-excluded components per cohort
    active_by_ds: dict[str, list[ComponentRecord]] = collections.defaultdict(list)
    for c in comp_map.values():
        if c.non_excluded_image_ids:
            active_by_ds[c.dataset_id].append(c)

    # 1. Primary internal track (`DS0003 CMMD`): 70% train / 15% val / 15% internal_test
    cmmd_comps = active_by_ds.get(cfg.primary_internal_dataset, [])
    cmmd_targets = {"train": cfg.train_ratio, "val": cfg.val_ratio, "internal_test": cfg.test_ratio}
    cmmd_part_by_comp = _stratified_group_buckets(
        cmmd_comps,
        bucket_targets=cmmd_targets,
        seed=cfg.seed,
        strat_key_fn=lambda c: (c.max_target, c.has_bilateral_discordance, c.dominant_morphology),
    )

    # Deterministic 5-fold CV STRICTLY inside `train + val` components (`never internal_test`)
    cmmd_dev_comps = [c for c in cmmd_comps if cmmd_part_by_comp[c.component_id] in {"train", "val"}]
    fold_targets = {str(i): 1.0 / cfg.dev_folds for i in range(cfg.dev_folds)}
    cmmd_fold_by_comp = _stratified_group_buckets(
        cmmd_dev_comps,
        bucket_targets=fold_targets,
        seed=cfg.seed + 101,
        strat_key_fn=lambda c: (c.max_target, c.has_bilateral_discordance),
    )

    # 2. Secondary localization cohort (`DS0006 CDD-CESM LE`): untouched in primary_split (`external_eval_loc`),
    #    plus intra-cohort patient-grouped `70/15/15` `cohort_subsplit` for secondary nested studies.
    cdd_comps = active_by_ds.get("DS0006", [])
    cdd_subsplit_by_comp = _stratified_group_buckets(
        cdd_comps,
        bucket_targets={"train": 0.70, "val": 0.15, "internal_test": 0.15},
        seed=cfg.seed + 202,
        strat_key_fn=lambda c: (c.max_target, c.has_subtrack_a, c.has_loc_lesion_mask),
    )

    split_rows: list[dict[str, str]] = []
    sorted_rows = sorted(manifest_rows, key=lambda r: (r["DatasetID"], r["ImageID"]))
    for r in sorted_rows:
        ds_id = r["DatasetID"].strip()
        img_id = r["ImageID"].strip()
        cid = comp_id_by_img[(ds_id, img_id)]
        is_excluded = r["BinaryTarget"] == "Excluded"

        if is_excluded:
            prim_part = "excluded"
            dev_fold = "-1"
            subsplit = "excluded"
            custody = "excluded_non_modeling"
            eligible = "False"
        elif ds_id == cfg.primary_internal_dataset:
            prim_part = cmmd_part_by_comp[cid]
            dev_fold = cmmd_fold_by_comp.get(cid, "-1")
            subsplit = prim_part
            custody = "sealed_until_G11" if prim_part == "internal_test" else "open_dev"
            eligible = "True"
        elif ds_id in EXTERNAL_PARTITION_BY_DATASET:
            prim_part = EXTERNAL_PARTITION_BY_DATASET[ds_id]
            dev_fold = "-1"
            subsplit = cdd_subsplit_by_comp.get(cid, "external_only") if ds_id == "DS0006" else "external_only"
            custody = "sealed_external_until_G11_G12"
            eligible = "True"
        else:
            raise ValueError(f"Unassigned cohort in split engine: {ds_id}")

        split_rows.append(
            {
                "SplitID": cfg.split_id,
                "ImageID": img_id,
                "DatasetID": ds_id,
                "LabelReleaseID": r["LabelReleaseID"],
                "PatientGroupID": r["PatientGroupID"],
                "ComponentID": cid,
                "primary_partition": prim_part,
                "dev_fold_5": dev_fold,
                "cohort_subsplit": subsplit,
                "custody_tier": custody,
                "eligible_for_modeling": eligible,
                "BinaryTarget": r["BinaryTarget"],
                "LabelClass": r["LabelClass"],
                "LabelProvenanceTier": r["LabelProvenanceTier"],
                "SubTrackA_BiopsyEligible": r["SubTrackA_BiopsyEligible"],
                "SubTrackB_ScreeningEligible": r["SubTrackB_ScreeningEligible"],
                "LesionTrack_BenignVsMalignant": r["LesionTrack_BenignVsMalignant"],
                "LocalizationEligible": r["LocalizationEligible"],
                "ViewPosition": r["ViewPosition"],
                "Laterality": r["Laterality"],
                "DensityACR": r["DensityACR"],
                "MorphologyType": r["MorphologyType"],
                "MultiLesionConflict": r["MultiLesionConflict"],
                "AnomalyFlags": r["AnomalyFlags"],
            }
        )

    assert_zero_leakage(split_rows)

    summary = _build_split_summary(cfg, split_rows, comp_map)
    return split_rows, summary


def _build_split_summary(
    cfg: SplitConfig,
    split_rows: list[dict[str, str]],
    comp_map: dict[str, ComponentRecord],
) -> dict[str, Any]:
    """Compute exact partition image, patient-component, target, ROI-mask, and subgroup counts."""
    part_stats: dict[str, dict[str, Any]] = {}
    by_part: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    for r in split_rows:
        by_part[r["primary_partition"]].append(r)

    for part, rows in sorted(by_part.items()):
        comps = {r["ComponentID"] for r in rows}
        part_stats[part] = {
            "images": len(rows),
            "components": len(comps),
            "datasets": dict(sorted(collections.Counter(r["DatasetID"] for r in rows).items())),
            "binary_targets": dict(sorted(collections.Counter(r["BinaryTarget"] for r in rows).items())),
            "subtrack_a": sum(1 for r in rows if r["SubTrackA_BiopsyEligible"] == "True"),
            "subtrack_b": sum(1 for r in rows if r["SubTrackB_ScreeningEligible"] == "True"),
            "loc_masks_total": sum(1 for r in rows if r["LocalizationEligible"] == "True"),
            "loc_masks_lesion": sum(
                1 for r in rows if r["LocalizationEligible"] == "True" and r["LabelClass"] != "Normal_Control"
            ),
            "views": dict(sorted(collections.Counter(r["ViewPosition"] for r in rows).items())),
            "morphology": dict(sorted(collections.Counter(r["MorphologyType"] for r in rows).items())),
            "density_acr": dict(sorted(collections.Counter(r["DensityACR"] for r in rows).items())),
        }

    # Nested DS0006 cohort_subsplit breakdown
    cdd_sub: dict[str, Any] = {}
    for sub in ["train", "val", "internal_test"]:
        srows = [r for r in split_rows if r["DatasetID"] == "DS0006" and r["cohort_subsplit"] == sub]
        cdd_sub[sub] = {
            "images": len(srows),
            "components": len({r["ComponentID"] for r in srows}),
            "binary_targets": dict(sorted(collections.Counter(r["BinaryTarget"] for r in srows).items())),
            "subtrack_a": sum(1 for r in srows if r["SubTrackA_BiopsyEligible"] == "True"),
            "loc_masks_lesion": sum(
                1 for r in srows if r["LocalizationEligible"] == "True" and r["LabelClass"] != "Normal_Control"
            ),
        }

    # Verify component isolation count check
    cmmd_active_comps = sum(
        1 for c in comp_map.values() if c.dataset_id == cfg.primary_internal_dataset and c.non_excluded_image_ids
    )
    return {
        "split_id": cfg.split_id,
        "seed": cfg.seed,
        "total_rows": len(split_rows),
        "total_components": len(comp_map),
        "cmmd_active_components": cmmd_active_comps,
        "zero_leakage_verified": True,
        "partitions": part_stats,
        "ds0006_cohort_subsplit": cdd_sub,
    }


def write_split_artifacts(root: Path, cfg: SplitConfig | None = None) -> dict[str, Any]:
    """Load `LBL0001–LBL0005` frozen manifests, run `split`, and write `03_Datasets/splits/SPLIT####/`."""
    cfg = cfg or SplitConfig()
    exports_dir = root / "04_Labels_XAI_Governance" / "exports"
    qc_dir = root / "03_Datasets" / "cache" / "qc"
    split_dir = root / "03_Datasets" / "splits" / cfg.split_id
    split_dir.mkdir(parents=True, exist_ok=True)

    manifest_rows: list[dict[str, str]] = []
    ds_ids: list[str] = []
    lbl_hashes: dict[str, str] = {}
    for ds_id, lbl_id in sorted(COHORT_TO_LBL_ID.items()):
        mpath = exports_dir / lbl_id / f"{lbl_id}_manifest.csv"
        if not mpath.is_file():
            raise FileNotFoundError(f"Missing frozen LBL manifest: {mpath}")
        lbl_hashes[lbl_id] = sha256_file(mpath)
        ds_ids.append(ds_id)
        with mpath.open("r", encoding="utf-8", newline="") as fp:
            manifest_rows.extend(csv.DictReader(fp))

    qc_id_map = _load_qc_identity_map(qc_dir, ds_ids)
    split_rows, summary = generate_split_release(manifest_rows, qc_identity=qc_id_map, cfg=cfg)

    out_manifest = split_dir / "manifest.csv"
    with out_manifest.open("w", encoding="utf-8", newline="\n") as fp:
        writer = csv.DictWriter(fp, fieldnames=SPLIT_MANIFEST_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(split_rows)

    cfg_dict = asdict(cfg)
    cfg_dict["input_label_manifest_sha256"] = lbl_hashes
    cfg_path = split_dir / "config.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg_dict, sort_keys=False), encoding="utf-8")

    manifest_sha = sha256_file(out_manifest)
    cfg_sha = sha256_file(cfg_path)
    summary["manifest_path"] = out_manifest.as_posix()
    summary["manifest_sha256"] = manifest_sha
    summary["config_path"] = cfg_path.as_posix()
    summary["config_sha256"] = cfg_sha
    summary["input_label_manifest_sha256"] = lbl_hashes

    summary_path = split_dir / "private_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for STEP-020 `SPLIT0001` generation and zero-leakage check."""
    parser = argparse.ArgumentParser(description="STEP-020 Connected-Component Leakage-Safe Splitter")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--split-id", type=str, default="SPLIT0001")
    parser.add_argument("--seed", type=int, default=DEFAULT_SPLIT_SEED)
    args = parser.parse_args(argv)

    cfg = SplitConfig(split_id=args.split_id, seed=args.seed)
    summ = write_split_artifacts(args.root.resolve(), cfg=cfg)
    print(f"[SPLIT DONE] {summ['split_id']} manifest SHA256={summ['manifest_sha256']}")
    for part, st in summ["partitions"].items():
        print(
            f"  {part}: imgs={st['images']}, comps={st['components']}, "
            f"targets={st['binary_targets']}, loc_lesion={st['loc_masks_lesion']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

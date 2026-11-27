"""Immutable STEP-018 Diagnostic Label & Post-Hoc ROI-Mask Release Freezer (`LBL####`).

Consumes verified `STEP-017` full-corpus label tables (`DS####_full_labels.csv`),
cross-checks 100% `ImageID` parity against `G04`-locked `DS####_private_linkage.csv` and
`03_Datasets/datasets.csv`, re-extracts & pixel-verifies every `LocalizationEligible`
binary `{0, 1}` ROI mask into deterministic SHA-256-locked Tier-2 `.zip` archives,
and emits canonical Tier-1 `04_Labels_XAI_Governance/label_map.json`.
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import re
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pandas as pd

from bc_xai.labels.verify import (
    LabelCohortSpec,
    default_label_specs,
    extract_bmcd_gt_channels,
    extract_dmid_rgba_mask,
    load_linkage_and_qc,
    rasterize_cdd_cesm_shapes,
    rasterize_mias_circle,
)

PROTOCOL_VERSION = "T09_v1.0.1 + ADJ-017-02_Option_B"
CANONICAL_TARGET_MAP: dict[str, str] = {"0": "Benign", "1": "Malignant"}
FIXED_ZIP_DATE_TIME = (2026, 11, 28, 0, 0, 0)

# Deterministic cohort -> LBL#### assignment for G04-approved Batch A CC-BY cohorts.
COHORT_TO_LBL_ID: dict[str, str] = {
    "DS0001": "LBL0001",
    "DS0002": "LBL0002",
    "DS0003": "LBL0003",
    "DS0005": "LBL0004",
    "DS0006": "LBL0005",
}

FROZEN_MANIFEST_FIELDS: list[str] = [
    "LabelReleaseID",
    "DatasetID",
    "ImageID",
    "PatientGroupID",
    "SourceStem",
    "DispositionQC",
    "Paradigm",
    "BinaryTarget",
    "LabelClass",
    "LabelProvenanceTier",
    "SubTrackA_BiopsyEligible",
    "SubTrackB_ScreeningEligible",
    "LesionTrack_BenignVsMalignant",
    "MultiLesionConflict",
    "ViewPosition",
    "Laterality",
    "DensityACR",
    "MorphologyType",
    "BIRADSScore",
    "ClinicalConcStatus",
    "LocalizationEligible",
    "MaskSourceType",
    "MaskStatus",
    "MaskWidth",
    "MaskHeight",
    "ImageWidth",
    "ImageHeight",
    "MaskForegroundPixels",
    "MaskCoveragePct",
    "MaskComponentCount",
    "AnomalyFlags",
    "RawRelativePath",
    "MaskRelativePath",
    "MaskArchiveMember",
    "MaskSHA256",
]


@dataclass
class FrozenCohortResult:
    """Cryptographic and reconciled count summary for one frozen `LBL####` release."""

    lbl_id: str
    dataset_id: str
    display_name: str
    paradigm: str
    parent_manifest_hash: str
    primary_acquired: int
    qc_retained: int
    binary_0_count: int
    binary_1_count: int
    excluded_count: int
    subtrack_a_count: int
    subtrack_b_count: int
    lesion_track_count: int
    localization_eligible_count: int
    localization_malignant_count: int
    localization_benign_count: int
    localization_normal_count: int
    frozen_manifest_path: str
    frozen_manifest_sha256: str
    masks_bundle_path: str
    masks_bundle_sha256: str
    masks_checksums_path: str
    masks_checksums_sha256: str


def sha256_bytes(data: bytes) -> str:
    """Return lowercase hexadecimal SHA-256 digest of raw bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    """Return lowercase hexadecimal SHA-256 digest of a file streamed cleanly."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _parse_bool_flag(val: str) -> bool:
    """Parse serialized CSV boolean string strictly."""
    norm = str(val).strip().lower()
    if norm == "true":
        return True
    if norm == "false":
        return False
    raise ValueError(f"Expected boolean flag True/False, got: {val!r}")


def _encode_binary_mask_png(mask: np.ndarray) -> bytes:
    """Encode binary `{0, 1}` uint8 array deterministically as lossless 8-bit PNG."""
    u8 = (mask > 0).astype(np.uint8)
    ok, buf = cv2.imencode(".png", u8, [int(cv2.IMWRITE_PNG_COMPRESSION), 1])
    if not ok:
        raise RuntimeError("cv2.imencode PNG failed while freezing ROI mask.")
    return buf.tobytes()


def _load_cdd_shapes_lookup(raw_dir: Path) -> dict[str, list[dict[str, Any]]]:
    """Load VIA hand-drawn shape attributes keyed by base image filename once per cohort."""
    seg_csv = raw_dir / "metadata" / "Radiology_hand_drawn_segmentations_v2.csv"
    if not seg_csv.is_file():
        seg_csv = raw_dir / "Radiology_hand_drawn_segmentations_v2.csv"
    if not seg_csv.is_file():
        raise FileNotFoundError(f"Missing CDD-CESM segmentation CSV inside {raw_dir}")
    seg_df = pd.read_csv(seg_csv)
    by_name: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for _, r in seg_df.iterrows():
        fname = str(r["#filename"]).strip()
        attr = json.loads(str(r["region_shape_attributes"]))
        by_name[fname].append(attr)
    return by_name


def _extract_verified_binary_mask(
    spec: LabelCohortSpec,
    row: dict[str, str],
    cdd_shapes: dict[str, list[dict[str, Any]]] | None,
) -> np.ndarray:
    """Re-extract binary `{0, 1}` uint8 ROI mask and enforce exact `STEP-017` pixel match."""
    h = int(row["ImageHeight"])
    w = int(row["ImageWidth"])
    expected_px = int(row["MaskForegroundPixels"])
    ds_id = spec.dataset_id

    if ds_id == "DS0006":
        assert cdd_shapes is not None
        fname = Path(row["RawRelativePath"]).name
        shapes = cdd_shapes.get(fname, [])
        if not shapes:
            raise ValueError(f"Missing VIA shapes for LocalizationEligible DS0006 row {row['ImageID']}")
        mask, _, _ = rasterize_cdd_cesm_shapes(shapes, h, w)
    elif ds_id == "DS0002":
        mask, _ = extract_dmid_rgba_mask(spec.raw_dir / row["MaskRelativePath"])
    elif ds_id == "DS0005":
        mask, _ = extract_bmcd_gt_channels(
            spec.raw_dir / row["MaskRelativePath"],
            target_h=h,
            target_w=w,
            mode="lesion_red_blue",
        )
    elif ds_id == "DS0001":
        tuples = re.findall(r"\(([\d.]+),\s*([\d.]+),\s*([\d.]+)\)", row["ExtraMaskTelemetry"])
        if not tuples:
            raise ValueError(f"Missing MIAS circle telemetry on DS0001 row {row['ImageID']}")
        circles = [(float(x), float(y), float(r)) for x, y, r in tuples]
        mask = rasterize_mias_circle(circles, h, w, y_from_bottom=True)
    else:
        raise ValueError(f"Unexpected ROI mask extraction request on dataset {ds_id}")

    if mask.shape != (h, w):
        raise ValueError(
            f"Mask dimension mismatch on {ds_id} {row['ImageID']}: expected {(h, w)}, got {mask.shape}"
        )
    actual_px = int((mask > 0).sum())
    if actual_px != expected_px or actual_px <= 0:
        raise ValueError(
            f"Frozen mask pixel mismatch on {ds_id} {row['ImageID']}: "
            f"expected {expected_px}, got {actual_px}"
        )
    return (mask > 0).astype(np.uint8)


def _assert_cohort_integrity(
    ds_id: str,
    full_rows: list[dict[str, str]],
    linkage_rows: list[dict[str, str]],
    expected_retained_count: int | None,
) -> None:
    """Assert 100% ImageID correspondence, valid binary targets, and post-hoc mask invariants."""
    full_ids = [r["ImageID"].strip() for r in full_rows]
    link_ids = [r["ImageID"].strip() for r in linkage_rows]
    if len(full_ids) != len(set(full_ids)):
        raise ValueError(f"Duplicate ImageID(s) found in {ds_id} full labels CSV.")
    if set(full_ids) != set(link_ids) or len(full_ids) != len(link_ids):
        missing = sorted(set(link_ids) - set(full_ids))[:5]
        orphan = sorted(set(full_ids) - set(link_ids))[:5]
        raise ValueError(
            f"ImageID linkage mismatch on {ds_id}: missing={missing}, orphan={orphan}"
        )

    retained_rows = sum(1 for r in full_rows if r["DispositionQC"] == "Retained")
    if expected_retained_count is not None and retained_rows != expected_retained_count:
        raise ValueError(
            f"G04 retained count mismatch on {ds_id}: "
            f"datasets.csv={expected_retained_count}, full_labels={retained_rows}"
        )

    for r in full_rows:
        bt = r["BinaryTarget"]
        if bt not in {"0", "1", "Excluded"}:
            raise ValueError(f"Invalid BinaryTarget {bt!r} on {ds_id} {r['ImageID']}")
        is_excluded = bt == "Excluded"
        if is_excluded and r["LabelProvenanceTier"] != "Excluded":
            raise ValueError(f"Excluded row {r['ImageID']} has non-Excluded provenance tier")
        if _parse_bool_flag(r["SubTrackA_BiopsyEligible"]):
            if is_excluded or r["LabelProvenanceTier"] != "TierA_Biopsy" or r["DispositionQC"] != "Retained":
                raise ValueError(f"SubTrackA invariant violated on {ds_id} {r['ImageID']}")
        if _parse_bool_flag(r["SubTrackB_ScreeningEligible"]) and is_excluded:
            raise ValueError(f"Excluded row {r['ImageID']} flagged SubTrackB eligible")
        if _parse_bool_flag(r["LocalizationEligible"]):
            if is_excluded or r["MaskStatus"] != "ok_nonempty" or int(r["MaskForegroundPixels"]) <= 0:
                raise ValueError(f"Mask eligibility invariant violated on {ds_id} {r['ImageID']}")
            if ds_id == "DS0003":
                raise ValueError(f"DS0003 CMMD must never mark LocalizationEligible=True ({r['ImageID']})")


def freeze_cohort_release(
    spec: LabelCohortSpec,
    lbl_id: str,
    full_labels_csv: Path,
    exports_dir: Path,
    restricted_masks_dir: Path,
    parent_manifest_hash: str,
    expected_retained_count: int | None = None,
) -> FrozenCohortResult:
    """Verify and freeze one cohort into immutable Tier-2 manifest + SHA-256 mask zip."""
    if not full_labels_csv.is_file():
        raise FileNotFoundError(f"Missing STEP-017 full labels CSV: {full_labels_csv}")

    linkage_rows = load_linkage_and_qc(spec)
    with full_labels_csv.open("r", encoding="utf-8", newline="") as fp:
        full_rows = list(csv.DictReader(fp))

    _assert_cohort_integrity(spec.dataset_id, full_rows, linkage_rows, expected_retained_count)
    full_rows.sort(key=lambda r: r["ImageID"])

    cdd_shapes = _load_cdd_shapes_lookup(spec.raw_dir) if spec.dataset_id == "DS0006" else None
    cohort_export_dir = exports_dir / lbl_id
    cohort_export_dir.mkdir(parents=True, exist_ok=True)
    restricted_masks_dir.mkdir(parents=True, exist_ok=True)

    loc_rows = [r for r in full_rows if _parse_bool_flag(r["LocalizationEligible"])]
    masks_zip_path = restricted_masks_dir / f"{lbl_id}_masks.zip"
    masks_sha_path = cohort_export_dir / f"{lbl_id}_masks_checksums.sha256"

    member_by_img: dict[str, tuple[str, str]] = {}
    if loc_rows:
        sha_lines: list[str] = []
        with zipfile.ZipFile(masks_zip_path, "w", compression=zipfile.ZIP_STORED) as zf:
            for r in loc_rows:
                mask_u8 = _extract_verified_binary_mask(spec, r, cdd_shapes)
                png_bytes = _encode_binary_mask_png(mask_u8)
                digest = sha256_bytes(png_bytes)
                member = f"masks/{r['ImageID']}.png"
                zi = zipfile.ZipInfo(filename=member, date_time=FIXED_ZIP_DATE_TIME)
                zi.compress_type = zipfile.ZIP_STORED
                zi.external_attr = 0o644 << 16
                zf.writestr(zi, png_bytes)
                member_by_img[r["ImageID"]] = (member, digest)
                sha_lines.append(f"{digest}  {member}")
        masks_sha_path.write_text("\n".join(sha_lines) + "\n", encoding="utf-8")
        bundle_rel = masks_zip_path.as_posix()
        bundle_hash = sha256_file(masks_zip_path)
        sha_rel = masks_sha_path.as_posix()
        sha_hash = sha256_file(masks_sha_path)
    else:
        masks_sha_path.write_text("# No native ROI masks eligible for this cohort\n", encoding="utf-8")
        bundle_rel = "none"
        bundle_hash = "none"
        sha_rel = masks_sha_path.as_posix()
        sha_hash = sha256_file(masks_sha_path)

    manifest_path = cohort_export_dir / f"{lbl_id}_manifest.csv"
    with manifest_path.open("w", encoding="utf-8", newline="\n") as fp:
        writer = csv.DictWriter(fp, fieldnames=FROZEN_MANIFEST_FIELDS, lineterminator="\n")
        writer.writeheader()
        for r in full_rows:
            member, mhash = member_by_img.get(r["ImageID"], ("", ""))
            out_row = {col: r.get(col, "") for col in FROZEN_MANIFEST_FIELDS}
            out_row["LabelReleaseID"] = lbl_id
            out_row["MaskArchiveMember"] = member
            out_row["MaskSHA256"] = mhash
            writer.writerow(out_row)
    manifest_sha = sha256_file(manifest_path)

    b0 = sum(1 for r in full_rows if r["BinaryTarget"] == "0")
    b1 = sum(1 for r in full_rows if r["BinaryTarget"] == "1")
    bex = sum(1 for r in full_rows if r["BinaryTarget"] == "Excluded")
    sub_a = sum(1 for r in full_rows if _parse_bool_flag(r["SubTrackA_BiopsyEligible"]))
    sub_b = sum(1 for r in full_rows if _parse_bool_flag(r["SubTrackB_ScreeningEligible"]))
    les_t = sum(1 for r in full_rows if _parse_bool_flag(r["LesionTrack_BenignVsMalignant"]))
    loc_m = sum(1 for r in loc_rows if r["BinaryTarget"] == "1")
    loc_b = sum(1 for r in loc_rows if r["BinaryTarget"] == "0" and r["LabelClass"] != "Normal_Control")
    loc_n = sum(1 for r in loc_rows if r["LabelClass"] == "Normal_Control")
    retained_cnt = sum(1 for r in full_rows if r["DispositionQC"] == "Retained")
    paradigms = sorted({r["Paradigm"] for r in full_rows if r["Paradigm"]})

    return FrozenCohortResult(
        lbl_id=lbl_id,
        dataset_id=spec.dataset_id,
        display_name=spec.display_name or spec.dataset_id,
        paradigm=";".join(paradigms),
        parent_manifest_hash=parent_manifest_hash,
        primary_acquired=len(full_rows),
        qc_retained=retained_cnt,
        binary_0_count=b0,
        binary_1_count=b1,
        excluded_count=bex,
        subtrack_a_count=sub_a,
        subtrack_b_count=sub_b,
        lesion_track_count=les_t,
        localization_eligible_count=len(loc_rows),
        localization_malignant_count=loc_m,
        localization_benign_count=loc_b,
        localization_normal_count=loc_n,
        frozen_manifest_path=manifest_path.as_posix(),
        frozen_manifest_sha256=manifest_sha,
        masks_bundle_path=bundle_rel,
        masks_bundle_sha256=bundle_hash,
        masks_checksums_path=sha_rel,
        masks_checksums_sha256=sha_hash,
    )


def _load_parent_datasets_meta(datasets_csv: Path) -> dict[str, tuple[str, int]]:
    """Read `(ManifestHash, ImageCount)` per DatasetID from `03_Datasets/datasets.csv`."""
    if not datasets_csv.is_file():
        return {}
    out: dict[str, tuple[str, int]] = {}
    with datasets_csv.open("r", encoding="utf-8", newline="") as fp:
        for row in csv.DictReader(fp):
            ds_id = row["DS"].strip()
            out[ds_id] = (row["ManifestHash"].strip(), int(row["ImageCount"].strip()))
    return out


def freeze_all_releases(
    specs: list[LabelCohortSpec],
    root: Path,
    native_dir: Path | None = None,
    exports_dir: Path | None = None,
    restricted_masks_dir: Path | None = None,
    label_map_path: Path | None = None,
    freeze_date: str = "2026-11-28",
) -> dict[str, Any]:
    """Run STEP-018 freeze across all cohorts and write `label_map.json` + `freeze_summary.json`."""
    gov_dir = root / "04_Labels_XAI_Governance"
    native_dir = native_dir or (gov_dir / "native")
    exports_dir = exports_dir or (gov_dir / "exports")
    restricted_masks_dir = restricted_masks_dir or (gov_dir / "restricted_masks")
    label_map_path = label_map_path or (gov_dir / "label_map.json")

    ds_meta = _load_parent_datasets_meta(root / "03_Datasets" / "datasets.csv")
    results: list[FrozenCohortResult] = []
    for spec in specs:
        if spec.dataset_id not in COHORT_TO_LBL_ID:
            raise ValueError(f"DatasetID missing in COHORT_TO_LBL_ID mapping: {spec.dataset_id}")
        lbl_id = COHORT_TO_LBL_ID[spec.dataset_id]
        parent_hash, exp_ret = ds_meta.get(spec.dataset_id, ("not reported", None))
        print(f"[LABEL-FREEZE] Freezing {lbl_id} ({spec.dataset_id}: {spec.display_name})...", flush=True)
        res = freeze_cohort_release(
            spec=spec,
            lbl_id=lbl_id,
            full_labels_csv=native_dir / f"{spec.dataset_id}_full_labels.csv",
            exports_dir=exports_dir,
            restricted_masks_dir=restricted_masks_dir,
            parent_manifest_hash=parent_hash,
            expected_retained_count=exp_ret,
        )
        results.append(res)

    label_map_payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "protocol_version": PROTOCOL_VERSION,
        "frozen_date": freeze_date,
        "target_mapping": CANONICAL_TARGET_MAP,
        "excluded_token": "Excluded",
        "track_semantics": {
            "SubTrackA_BiopsyEligible": "TierA_Biopsy only (DS0003 CMMD + DS0005 BMCD recent + DS0006 CDD-CESM LE benign/malignant)",
            "SubTrackB_ScreeningEligible": "Biopsy/Lesion plus disclosed Normal_Control cohorts separated by Cohort & Provenance",
            "LesionTrack_BenignVsMalignant": "Abnormal lesions excluding Normal_Control",
            "LocalizationEligible": "Strictly post-hoc verified ok_nonempty binary {0, 1} masks; filter LabelClass != Normal_Control for lesion localization",
        },
        "releases": {
            r.lbl_id: {
                "dataset_id": r.dataset_id,
                "display_name": r.display_name,
                "paradigm": r.paradigm,
                "parent_ds_manifest_hash": r.parent_manifest_hash,
                "frozen_manifest_sha256": r.frozen_manifest_sha256,
                "masks_bundle_sha256": r.masks_bundle_sha256,
                "masks_checksums_sha256": r.masks_checksums_sha256,
                "primary_acquired": r.primary_acquired,
                "qc_retained": r.qc_retained,
                "binary_0_count": r.binary_0_count,
                "binary_1_count": r.binary_1_count,
                "excluded_count": r.excluded_count,
                "subtrack_a_count": r.subtrack_a_count,
                "subtrack_b_count": r.subtrack_b_count,
                "lesion_track_count": r.lesion_track_count,
                "localization_eligible_count": r.localization_eligible_count,
                "localization_lesion_count": r.localization_malignant_count + r.localization_benign_count,
                "localization_malignant_count": r.localization_malignant_count,
                "localization_benign_count": r.localization_benign_count,
                "localization_normal_count": r.localization_normal_count,
            }
            for r in results
        },
    }
    label_map_path.parent.mkdir(parents=True, exist_ok=True)
    label_map_path.write_text(json.dumps(label_map_payload, indent=2) + "\n", encoding="utf-8")
    label_map_sha256 = sha256_file(label_map_path)

    summary_payload = {
        "generated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "freeze_date": freeze_date,
        "protocol_version": PROTOCOL_VERSION,
        "label_map_path": label_map_path.as_posix(),
        "label_map_sha256": label_map_sha256,
        "totals": {
            "primary_acquired": sum(r.primary_acquired for r in results),
            "qc_retained": sum(r.qc_retained for r in results),
            "binary_0_count": sum(r.binary_0_count for r in results),
            "binary_1_count": sum(r.binary_1_count for r in results),
            "excluded_count": sum(r.excluded_count for r in results),
            "subtrack_a_count": sum(r.subtrack_a_count for r in results),
            "subtrack_b_count": sum(r.subtrack_b_count for r in results),
            "lesion_track_count": sum(r.lesion_track_count for r in results),
            "localization_eligible_count": sum(r.localization_eligible_count for r in results),
            "localization_lesion_count": sum(r.localization_malignant_count + r.localization_benign_count for r in results),
            "localization_malignant_count": sum(r.localization_malignant_count for r in results),
            "localization_benign_count": sum(r.localization_benign_count for r in results),
            "localization_normal_count": sum(r.localization_normal_count for r in results),
        },
        "releases": [asdict(r) for r in results],
    }
    summary_path = native_dir / "freeze_summary.json"
    summary_path.write_text(json.dumps(summary_payload, indent=2) + "\n", encoding="utf-8")
    return summary_payload


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for STEP-018 immutable label & ROI-mask freeze."""
    parser = argparse.ArgumentParser(description="STEP-018 Immutable LBL#### Label & Mask Freezer")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--freeze-date", type=str, default="2026-11-28")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    payload = freeze_all_releases(
        specs=default_label_specs(root),
        root=root,
        freeze_date=args.freeze_date,
    )
    print(f"[FREEZE DONE] label_map.json SHA256={payload['label_map_sha256']}")
    for rel in payload["releases"]:
        print(
            f"[FROZEN] {rel['lbl_id']} ({rel['dataset_id']}): "
            f"0={rel['binary_0_count']}, 1={rel['binary_1_count']}, Excl={rel['excluded_count']}, "
            f"Masks={rel['localization_eligible_count']} | ManifestSHA={rel['frozen_manifest_sha256']} | "
            f"BundleSHA={rel['masks_bundle_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

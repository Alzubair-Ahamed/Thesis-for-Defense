"""Unit and leak-injection tests for STEP-020 connected-component patient splitter."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from bc_xai.data.split import (  # noqa: E402
    LeakageError,
    SplitConfig,
    assert_zero_leakage,
    audit_external_split_overlap,
    build_equivalence_graph,
    generate_split_release,
)


def _row(
    img_id: str,
    ds_id: str = "DS0003",
    pat_id: str = "PAT1",
    btarget: str = "1",
    stem: str = "",
    dup: str = "",
    study: str = "",
) -> dict[str, str]:
    return {
        "ImageID": img_id,
        "DatasetID": ds_id,
        "LabelReleaseID": "LBL0003" if ds_id == "DS0003" else "LBL0001",
        "PatientGroupID": pat_id,
        "SourceStem": stem or img_id,
        "BinaryTarget": btarget,
        "LabelClass": "Malignant" if btarget == "1" else ("Benign_Biopsy" if btarget == "0" else "Excluded"),
        "LabelProvenanceTier": "TierA_Biopsy" if btarget != "Excluded" else "Excluded",
        "SubTrackA_BiopsyEligible": "True" if ds_id == "DS0003" and btarget != "Excluded" else "False",
        "SubTrackB_ScreeningEligible": "True" if btarget != "Excluded" else "False",
        "LesionTrack_BenignVsMalignant": "True" if btarget != "Excluded" else "False",
        "LocalizationEligible": "True" if ds_id == "DS0006" and btarget != "Excluded" else "False",
        "ViewPosition": "CC",
        "Laterality": "L",
        "DensityACR": "not_reported",
        "MorphologyType": "mass",
        "MultiLesionConflict": "False",
        "AnomalyFlags": "",
        "ExactDupCluster": dup,
        "StudyGroupID": study,
    }


def test_equivalence_graph_merges_clones_mias_pairs_and_catches_cross_cohort() -> None:
    """Equivalence graph must merge clones, study IDs, and MIAS odd/even L-R pairs atomically."""
    rows = [
        # CMMD clone cluster across two patient IDs
        _row("IMG01", "DS0003", "PAT_A", "1", dup="DUP_CLONE_1"),
        _row("IMG02", "DS0003", "PAT_A", "0"),
        _row("IMG03", "DS0003", "PAT_B", "0", dup="DUP_CLONE_1"),
        # Distinct CMMD study link without shared PatientGroupID
        _row("IMG04", "DS0003", "PAT_UNRESOLVED", "1", study="ST_99"),
        _row("IMG05", "DS0003", "PAT_C", "1", study="ST_99"),
        # MIAS bilateral pair mdb001l + mdb002r -> 1 component
        _row("IMG06", "DS0001", "PAT_M1", "0", stem="mdb001lm"),
        _row("IMG07", "DS0001", "PAT_M2", "1", stem="mdb002rl"),
    ]
    _, comp_map = build_equivalence_graph(rows)
    assert comp_map[("DS0003", "IMG01")] == comp_map[("DS0003", "IMG02")] == comp_map[("DS0003", "IMG03")]
    assert comp_map[("DS0003", "IMG04")] == comp_map[("DS0003", "IMG05")]
    assert comp_map[("DS0001", "IMG06")] == comp_map[("DS0001", "IMG07")]

    # Official split leakage check catches shared component across split buckets
    official = {"IMG01": "train", "IMG02": "train", "IMG03": "test", "IMG04": "train", "IMG05": "train"}
    audit = audit_external_split_overlap(official, comp_map, "DS0003")
    assert audit["leaking_component_count"] == 1

    # Cross-cohort clone edge must crash loudly
    cross_rows = rows + [_row("IMG99", "DS0002", "PAT_D2", "1", dup="DUP_CLONE_1")]
    with pytest.raises(LeakageError, match="Cross-cohort"):
        build_equivalence_graph(cross_rows)


def test_deterministic_split_reproducibility_and_leak_injection() -> None:
    """Repeated split runs must be identical and assert_zero_leakage must catch injected splits."""
    rows: list[dict[str, str]] = []
    for idx in range(40):
        pid = f"PAT{idx:03d}"
        bt = "1" if idx % 2 == 0 else "0"
        rows.append(_row(f"C_{idx:03d}_CC", "DS0003", pid, bt))
        rows.append(_row(f"C_{idx:03d}_MLO", "DS0003", pid, bt))
    # Add an external DS0006 cohort
    for idx in range(10):
        rows.append(_row(f"E_{idx:03d}", "DS0006", f"EPAT{idx:03d}", "1" if idx % 2 == 0 else "0"))

    cfg = SplitConfig(split_id="SPLIT_TEST", seed=20261128)
    s1, sum1 = generate_split_release(rows, cfg=cfg)
    s2, sum2 = generate_split_release(rows, cfg=cfg)

    assert s1 == s2
    assert sum1["partitions"]["internal_test"]["images"] > 0
    assert sum1["partitions"]["external_eval_loc"]["images"] == 10

    # Leak injection #1: move one view of a CMMD patient component into a different partition
    leaked_part = copy.deepcopy(s1)
    c0_rows = [r for r in leaked_part if r["DatasetID"] == "DS0003" and r["PatientGroupID"] == "PAT000"]
    assert len(c0_rows) == 2
    other_part = "val" if c0_rows[0]["primary_partition"] != "val" else "train"
    c0_rows[0]["primary_partition"] = other_part
    with pytest.raises(LeakageError, match="Component|PatientGroupID|bridges"):
        assert_zero_leakage(leaked_part)

    # Leak injection #2: assign a dev_fold_5 to a sealed internal_test image
    leaked_fold = copy.deepcopy(s1)
    test_row = next(r for r in leaked_fold if r["primary_partition"] == "internal_test")
    test_row["dev_fold_5"] = "0"
    with pytest.raises(LeakageError, match="Sealed internal_test"):
        assert_zero_leakage(leaked_fold)

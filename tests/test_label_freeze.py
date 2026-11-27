"""Unit tests for STEP-018 immutable LBL#### label & post-hoc ROI-mask freezing."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from bc_xai.data.inventory import build_inventory  # noqa: E402
from bc_xai.labels.freeze import freeze_all_releases  # noqa: E402
from bc_xai.labels.verify import LabelCohortSpec, audit_cohort_labels  # noqa: E402


def _setup_synthetic_cdd_and_cmmd(tmp_path: Path) -> tuple[list[LabelCohortSpec], Path]:
    """Create minimal synthetic DS0006 (with masks) and DS0003 (no masks) for freeze tests."""
    root = tmp_path / "repo"
    raw6 = root / "03_Datasets" / "raw" / "DS0006_CDD_CESM"
    le_dir = raw6 / "Low energy images of CDD-CESM"
    meta_dir = raw6 / "metadata"
    le_dir.mkdir(parents=True)
    meta_dir.mkdir(parents=True)

    img = np.full((64, 64), 75, dtype=np.uint8)
    for stem in ["P1_L_DM_CC", "P2_R_DM_MLO"]:
        Image.fromarray(img, mode="L").convert("RGB").save(le_dir / f"{stem}.jpg")

    all_df = pd.DataFrame([
        {"Image_name": "P1_L_DM_CC", "Patient_ID": 1, "Side": "L", "Type": "DM", "Breast density (ACR)": "C", "BIRADS": 4, "Findings": "Mass", "View": "CC", "Pathology Classification/ Follow up": "Malignant"},
        {"Image_name": "P2_R_DM_MLO", "Patient_ID": 2, "Side": "R", "Type": "DM", "Breast density (ACR)": "B", "BIRADS": 1, "Findings": "Normal", "View": "MLO", "Pathology Classification/ Follow up": "Normal"},
    ])
    empty_df = pd.DataFrame(columns=["Image_name", "Type"])
    with pd.ExcelWriter(meta_dir / "Radiology-manual-annotations.xlsx") as xl:
        all_df.to_excel(xl, sheet_name="all", index=False)
        empty_df.to_excel(xl, sheet_name="postoperative", index=False)
        empty_df.to_excel(xl, sheet_name="postneoajuvant chemotherapy", index=False)
    pd.DataFrame([
        {"#filename": "P1_L_DM_CC.jpg", "region_shape_attributes": json.dumps({"name": "circle", "cx": 32, "cy": 32, "r": 10})}
    ]).to_csv(meta_dir / "Radiology_hand_drawn_segmentations_v2.csv", index=False)

    man = root / "03_Datasets" / "manifests"
    rep = root / "03_Datasets" / "reports"
    build_inventory(raw6, "DS0006", man / "DS0006_images.csv", man / "DS0006_private_linkage.csv", rep / "r6.md")
    spec6 = LabelCohortSpec("DS0006", raw6, man / "DS0006_private_linkage.csv", None, "CDD-CESM (LE)")
    native = root / "04_Labels_XAI_Governance" / "native"
    overlays = root / "04_Labels_XAI_Governance" / "restricted_masks" / "pilot_overlays"
    audit_cohort_labels(spec6, native, overlays, mode="full")
    return [spec6], root


def test_freeze_all_releases_deterministic_hashes_and_binary_zip(tmp_path: Path) -> None:
    """Freezing must produce deterministic SHA-256 digests and lossless {0, 1} PNG masks."""
    specs, root = _setup_synthetic_cdd_and_cmmd(tmp_path)
    s1 = freeze_all_releases(specs, root=root, freeze_date="2026-11-28")
    s2 = freeze_all_releases(specs, root=root, freeze_date="2026-11-28")

    assert s1["label_map_sha256"] == s2["label_map_sha256"]
    rel1 = s1["releases"][0]
    rel2 = s2["releases"][0]
    assert rel1["lbl_id"] == "LBL0005"
    assert rel1["frozen_manifest_sha256"] == rel2["frozen_manifest_sha256"]
    assert rel1["masks_bundle_sha256"] == rel2["masks_bundle_sha256"]
    assert rel1["localization_eligible_count"] == 1
    assert rel1["binary_0_count"] == 1 and rel1["binary_1_count"] == 1

    label_map = json.loads((root / "04_Labels_XAI_Governance" / "label_map.json").read_text(encoding="utf-8"))
    assert label_map["target_mapping"] == {"0": "Benign", "1": "Malignant"}

    manifest_rows = list(csv.DictReader(Path(rel1["frozen_manifest_path"]).open(encoding="utf-8")))
    loc_rows = [r for r in manifest_rows if r["LocalizationEligible"] == "True"]
    assert len(loc_rows) == 1
    member = loc_rows[0]["MaskArchiveMember"]
    expected_sha = loc_rows[0]["MaskSHA256"]
    with zipfile.ZipFile(rel1["masks_bundle_path"], "r") as zf:
        raw_png = zf.read(member)
    assert hashlib.sha256(raw_png).hexdigest() == expected_sha
    decoded = cv2.imdecode(np.frombuffer(raw_png, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    assert set(np.unique(decoded).tolist()) == {0, 1}
    assert int(decoded.sum()) == int(loc_rows[0]["MaskForegroundPixels"])


def test_freeze_rejects_orphan_or_tampered_pixel_count(tmp_path: Path) -> None:
    """Freezer must fail loudly on orphan ImageID or mismatched mask pixel counts."""
    specs, root = _setup_synthetic_cdd_and_cmmd(tmp_path)
    full_csv = root / "04_Labels_XAI_Governance" / "native" / "DS0006_full_labels.csv"
    orig_df = pd.read_csv(full_csv)

    tampered = orig_df.copy()
    tampered.loc[tampered["LocalizationEligible"].astype(str) == "True", "MaskForegroundPixels"] = 999999
    tampered.to_csv(full_csv, index=False)
    with pytest.raises(ValueError, match="pixel mismatch"):
        freeze_all_releases(specs, root=root, freeze_date="2026-11-28")

    orphan_df = orig_df.copy()
    orphan_df.loc[0, "ImageID"] = "IMG99999999"
    orphan_df.to_csv(full_csv, index=False)
    with pytest.raises(ValueError, match="ImageID linkage mismatch"):
        freeze_all_releases(specs, root=root, freeze_date="2026-11-28")

"""Synthetic unit tests for S08 label harmonization & ROI-mask verification (`src/bc_xai/labels/verify.py`)."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import pydicom
import pytest
from PIL import Image
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, SecondaryCaptureImageStorage

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from bc_xai.data.inventory import build_inventory  # noqa: E402
from bc_xai.labels.verify import (  # noqa: E402
    LabelCohortSpec,
    audit_cohort_labels,
    extract_bmcd_gt_channels,
    extract_dmid_rgba_mask,
    rasterize_cdd_cesm_shapes,
    rasterize_mias_circle,
    run_label_verification,
)


def _save_test_dicom(
    path: Path,
    arr: np.ndarray,
    patient_id: str,
    laterality: str = "L",
    view_pos: str = "CC",
    view_snomed: str | None = None,
) -> None:
    """Create minimal valid synthetic DICOM with PatientID, ImageLaterality, and ViewPosition."""
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = FileMetaDataset()
    meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds = FileDataset(str(path), {}, file_meta=meta, preamble=b"\0" * 128)
    ds.PatientID = patient_id
    ds.PatientName = patient_id
    ds.ImageLaterality = laterality
    if view_pos:
        ds.ViewPosition = view_pos
    if view_snomed:
        item = pydicom.Dataset()
        item.CodeValue = view_snomed
        ds.ViewCodeSequence = pydicom.Sequence([item])
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = meta.MediaStorageSOPInstanceUID
    ds.Modality = "MG"
    ds.Rows, ds.Columns = arr.shape[:2]
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = arr.tobytes()
    ds.save_as(str(path), enforce_file_format=True)


def test_cdd_cesm_all_five_via_primitives_and_exclusions(tmp_path: Path) -> None:
    """Verify VIA polygon/ellipse/circle/polyline/point union, $ BI-RADS & NAC/postop exclusions."""
    # Direct geometry primitive check
    shapes = [
        {"name": "polygon", "all_points_x": [10, 30, 30, 10], "all_points_y": [10, 10, 30, 30]},
        {"name": "ellipse", "cx": 60, "cy": 60, "rx": 8, "ry": 5, "theta": 0.0},
        {"name": "circle", "cx": 85, "cy": 25, "r": 6},
        {"name": "polyline", "all_points_x": [10, 20, 20, 10], "all_points_y": [60, 60, 75, 75]},
        {"name": "point", "cx": 50, "cy": 85},
    ]
    mask, names, oob = rasterize_cdd_cesm_shapes(shapes, height=100, width=100)
    assert not oob
    assert set(names) == {"polygon", "ellipse", "circle", "polyline", "point"}
    assert mask[20, 20] == 1 and mask[60, 60] == 1 and mask[25, 85] == 1
    assert mask[68, 15] == 1 and mask[85, 50] == 1
    assert mask[0, 0] == 0

    # End-to-end synthetic DS0006 cohort check
    raw = tmp_path / "raw" / "DS0006"
    le_dir = raw / "Low energy images of CDD-CESM"
    cm_dir = raw / "Subtracted images of CDD-CESM"
    meta_dir = raw / "metadata"
    le_dir.mkdir(parents=True)
    cm_dir.mkdir(parents=True)
    meta_dir.mkdir(parents=True)

    img = np.full((120, 120), 80, dtype=np.uint8)
    for stem in ["P1_L_DM_CC", "P2_R_DM_MLO", "P3_L_DM_CC", "P4_R_DM_CC", "P5_L_DM_CC", "P6_R_DM_CC"]:
        Image.fromarray(img, mode="L").convert("RGB").save(le_dir / f"{stem}.jpg")
    Image.fromarray(img, mode="L").convert("RGB").save(cm_dir / "P1_L_CM_CC.jpg")

    all_df = pd.DataFrame(
        [
            {"Image_name": "P1_L_DM_CC", "Patient_ID": 1, "Side": "L", "Type": "DM", "Breast density (ACR)": "C", "BIRADS": "3$2", "Findings": "Mass", "View": "CC", "Pathology Classification/ Follow up": "Malignant"},
            {"Image_name": "P2_R_DM_MLO", "Patient_ID": 2, "Side": "R", "Type": "DM", "Breast density (ACR)": "B", "BIRADS": 2, "Findings": "Macrocalcification", "View": "MLO", "Pathology Classification/ Follow up": "Benign"},
            {"Image_name": "P3_L_DM_CC", "Patient_ID": 3, "Side": "L", "Type": "DM", "Breast density (ACR)": "A", "BIRADS": 4, "Findings": "Cleared asymmetry", "View": "CC", "Pathology Classification/ Follow up": "Normal"},
            {"Image_name": "P4_R_DM_CC", "Patient_ID": 4, "Side": "R", "Type": "DM", "Breast density (ACR)": "D", "BIRADS": 6, "Findings": "Post NAC", "View": "CC", "Pathology Classification/ Follow up": "Normal"},
            {"Image_name": "P5_L_DM_CC", "Patient_ID": 5, "Side": "L", "Type": "DM", "Breast density (ACR)": "B", "BIRADS": 2, "Findings": "Scar", "View": "CC", "Pathology Classification/ Follow up": "Benign"},
            {"Image_name": "P6_R_DM_CC", "Patient_ID": 6, "Side": "R", "Type": "DM", "Breast density (ACR)": "C", "BIRADS": 1, "Findings": "Normal", "View": "CC", "Pathology Classification/ Follow up": "Malignant"},
        ]
    )
    postop_df = pd.DataFrame([{"Image_name": "P5_L_DM_CC", "Type": "DM"}])
    nac_df = pd.DataFrame([{"Image_name": "P4_R_DM_CC", "Type": "DM"}])
    with pd.ExcelWriter(meta_dir / "Radiology-manual-annotations.xlsx") as xl:
        all_df.to_excel(xl, sheet_name="all", index=False)
        postop_df.to_excel(xl, sheet_name="postoperative", index=False)
        nac_df.to_excel(xl, sheet_name="postneoajuvant chemotherapy", index=False)

    seg_rows = [
        {"#filename": "P1_L_DM_CC.jpg", "region_shape_attributes": json.dumps({"name": "ellipse", "cx": 60, "cy": 60, "rx": 12, "ry": 10})},
        {"#filename": "P2_R_DM_MLO.jpg", "region_shape_attributes": json.dumps({"name": "circle", "cx": 40, "cy": 40, "r": 8})},
    ]
    pd.DataFrame(seg_rows).to_csv(meta_dir / "Radiology_hand_drawn_segmentations_v2.csv", index=False)

    man = tmp_path / "manifests"
    rep = tmp_path / "reports"
    build_inventory(raw, "DS0006", man / "DS0006_images.csv", man / "DS0006_private_linkage.csv", rep / "r6.md")

    spec = LabelCohortSpec("DS0006", raw, man / "DS0006_private_linkage.csv", None, "CDD-CESM")
    summary, recs = audit_cohort_labels(spec, tmp_path / "native", tmp_path / "overlays", mode="full")
    by_stem = {r.SourceStem: r for r in recs}

    assert summary.arithmetic_closure_ok
    assert by_stem["P1_L_DM_CC"].BinaryTarget == "1"
    assert by_stem["P1_L_DM_CC"].BIRADSScore == "3"
    assert by_stem["P1_L_DM_CC"].LocalizationEligible is True
    assert by_stem["P2_R_DM_MLO"].BinaryTarget == "0"
    assert by_stem["P2_R_DM_MLO"].SubTrackA_BiopsyEligible is True
    assert by_stem["P3_L_DM_CC"].LabelClass == "Normal_Control"
    assert "DM_BIRADS_4_ClearedNormal" in by_stem["P3_L_DM_CC"].AnomalyFlags
    assert by_stem["P3_L_DM_CC"].SubTrackA_BiopsyEligible is False
    assert by_stem["P3_L_DM_CC"].SubTrackB_ScreeningEligible is True
    assert by_stem["P4_R_DM_CC"].LabelClass == "Excluded_PostNAC_BIRADS6"
    assert by_stem["P5_L_DM_CC"].LabelClass == "Excluded_PostOperative"
    assert by_stem["P6_R_DM_CC"].BinaryTarget == "1"
    assert "OccultOnDM_BIRADS_1" in by_stem["P6_R_DM_CC"].AnomalyFlags


def test_dmid_rgba_contour_fill_n_token_contradictions_and_ban(tmp_path: Path) -> None:
    """Verify DMID contour filling, 'N' & [B,M] rules, report contradictions, and ROI Masks ban."""
    # Must raise loudly if ROI Masks/*.tif path is ever touched
    with pytest.raises(ValueError, match="hard ban"):
        extract_dmid_rgba_mask(tmp_path / "DS0002_DMID" / "ROI Masks" / "IMG001.tif")

    raw = tmp_path / "raw" / "DS0002"
    (raw / "DICOM Images").mkdir(parents=True)
    (raw / "Pixel-level annotation").mkdir(parents=True)
    (raw / "Reports").mkdir(parents=True)

    arr = np.full((100, 100), 60, dtype=np.uint8)
    for stem, lat, vp in [("IMG001", "L", "CC"), ("IMG002", "R", "MLO"), ("IMG003", "L", "CC"), ("IMG004", "R", "CC"), ("IMG005", "L", "MLO")]:
        _save_test_dicom(raw / "DICOM Images" / f"{stem}.dcm", arr, patient_id="", laterality=lat, view_pos=vp)

    # Hollow red square contour for IMG001 and IMG005 (IMG005 will be excluded by Option B report discordance)
    rgba = np.zeros((100, 100, 4), dtype=np.uint8)
    rgba[..., :3] = 60
    rgba[..., 3] = 255
    cv2.rectangle(rgba, (20, 20), (50, 50), (220, 20, 20, 255), thickness=2)
    Image.fromarray(rgba, mode="RGBA").save(raw / "Pixel-level annotation" / "IMG001.tif")
    Image.fromarray(rgba, mode="RGBA").save(raw / "Pixel-level annotation" / "IMG005.tif")

    # Build Metadata.xlsx matching DMID header offset structure
    meta_rows = [[f"header row {i}", None, None, None, None, None, None, None] for i in range(5)]
    meta_rows.extend([
        ["IMG001 ", "CCLRT ", "G ", "MISC", "M ", 35, 35, 15],
        ["IMG001 ", "CCLRT ", "G ", "CIRC", "B", 70, 70, 8],
        ["IMG002", "MLORT", "F", "NORM", np.nan, np.nan, np.nan, np.nan],
        ["IMG003", "CCLT", "D", "CIRC", "N ", 40, 40, 10],
        ["IMG004", "CCRT", "G", "ASYM", "N", 40, 40, 10],
        ["IMG005", "MLOLT", "G", "ARCH", "M", 35, 35, 10],
    ])
    # Deliberate extra Benign row paired with N on IMG004 to verify mixed [B, N] exclusion
    meta_rows.append(["IMG004", "CCRT", "G", "CALC", "B", 50, 50, 5])
    pd.DataFrame(meta_rows).to_excel(raw / "Metadata.xlsx", header=False, index=False)

    (raw / "Reports" / "Img001.txt").write_text("Breast Composition: (ACR B)\nBIRADS: 3 and 5\n", encoding="utf-8")
    # Deliberate XLS-vs-TXT contradiction on IMG002 (`NORM` yet `BIRADS: 4a`) and IMG005 (`M` yet `BIRADS: 1`)
    (raw / "Reports" / "Img002.txt").write_text("Breast Composition: (ACR A)\nBIRADS: 4a\n", encoding="utf-8")
    (raw / "Reports" / "Img003.txt").write_text("BIRADS: 4a\n", encoding="utf-8")
    (raw / "Reports" / "Img004.txt").write_text("BIRADS: 3\n", encoding="utf-8")
    (raw / "Reports" / "Img005.txt").write_text("BIRADS: 1\n", encoding="utf-8")

    man = tmp_path / "manifests"
    rep = tmp_path / "reports"
    build_inventory(raw, "DS0002", man / "DS0002_images.csv", man / "DS0002_private_linkage.csv", rep / "r2.md")
    spec = LabelCohortSpec("DS0002", raw, man / "DS0002_private_linkage.csv", None, "DMID")
    summary, recs = audit_cohort_labels(spec, tmp_path / "native", tmp_path / "overlays", mode="full")
    by_stem = {r.SourceStem: r for r in recs}

    assert summary.arithmetic_closure_ok
    assert by_stem["IMG001"].BinaryTarget == "1"
    assert by_stem["IMG001"].MultiLesionConflict is True
    assert "MultiLesionBM_MalignantDominance" in by_stem["IMG001"].AnomalyFlags
    assert "UpstreamViewTypo_CCLRT" in by_stem["IMG001"].AnomalyFlags
    # Solid filled square 31x31 = 961 pixels (far above outline thickness 2)
    assert by_stem["IMG001"].MaskForegroundPixels > 800
    assert by_stem["IMG002"].BinaryTarget == "Excluded"
    assert by_stem["IMG002"].LabelClass == "Excluded_ReportMetadataDiscordance"
    assert by_stem["IMG002"].SubTrackB_ScreeningEligible is False
    assert by_stem["IMG002"].MaskStatus == "not_applicable"
    assert "Discordant_NORM_vs_RepBIRADS_4" in by_stem["IMG002"].AnomalyFlags
    assert by_stem["IMG003"].LabelClass == "Excluded_AmbiguousClassToken_N"
    assert by_stem["IMG004"].LabelClass == "Excluded_AmbiguousClassToken_N"
    assert by_stem["IMG004"].MultiLesionConflict is True
    assert by_stem["IMG005"].BinaryTarget == "Excluded"
    assert by_stem["IMG005"].LabelClass == "Excluded_ReportMetadataDiscordance"
    assert by_stem["IMG005"].SubTrackB_ScreeningEligible is False
    assert by_stem["IMG005"].LesionTrack_BenignVsMalignant is False
    assert by_stem["IMG005"].MaskStatus == "excluded_by_protocol"
    assert by_stem["IMG005"].LocalizationEligible is False
    assert "Discordant_M_vs_LowBIRADS_1" in by_stem["IMG005"].AnomalyFlags


def test_bmcd_rgb_channel_separation_prior_recent_and_aspect_check(tmp_path: Path) -> None:
    """Verify BMCD excludes green normal lines, isolates red/blue calc marks, and enforces prior rule."""
    # Direct GT image color separation check
    gt_norm = np.full((120, 100, 3), 90, dtype=np.uint8)
    # Green pectoral outline in Normal_cases must be ignored!
    cv2.line(gt_norm, (10, 10), (40, 110), (35, 160, 35), 3)
    norm_gt_path = tmp_path / "norm_GT.jpg"
    Image.fromarray(gt_norm, mode="RGB").save(norm_gt_path)
    mask_n, info_n = extract_bmcd_gt_channels(norm_gt_path, target_h=240, target_w=200)
    assert info_n["green_px"] > 50 and info_n["red_px"] == 0 and info_n["blue_px"] == 0
    assert mask_n.shape == (240, 200) and int(mask_n.sum()) == 0

    # Suspicious case blue hollow circle must fill cleanly
    gt_susp = gt_norm.copy()
    cv2.circle(gt_susp, (65, 60), 15, (20, 30, 230), 2)
    susp_gt_path = tmp_path / "susp_GT.jpg"
    Image.fromarray(gt_susp, mode="RGB").save(susp_gt_path)
    mask_s, info_s = extract_bmcd_gt_channels(susp_gt_path, target_h=240, target_w=200)
    assert info_s["blue_px"] > 40 and int(mask_s.sum()) > 1000

    # Full cohort path test
    raw = tmp_path / "raw" / "DS0005"
    norm_d = raw / "Dataset" / "Normal_cases" / "1"
    susp_d = raw / "Dataset" / "Suspicious_cases" / "1"
    dcm_arr = np.full((240, 200), 80, dtype=np.uint8)
    _save_test_dicom(norm_d / "CC_recent.dcm", dcm_arr, patient_id="N1")
    _save_test_dicom(susp_d / "CC_prior.dcm", dcm_arr, patient_id="S1")
    _save_test_dicom(susp_d / "CC_recemt.dcm", dcm_arr, patient_id="S1")
    Image.fromarray(gt_norm, mode="RGB").save(norm_d / "CC_recent_GT.jpg")
    Image.fromarray(gt_norm, mode="RGB").save(susp_d / "CC_prior_GT.jpg")
    Image.fromarray(gt_susp, mode="RGB").save(susp_d / "CC_recent_GT.jpg")

    with pd.ExcelWriter(raw / "Description.xlsx") as xl:
        pd.DataFrame(
            [
                ["Normal Cases", None, None, None, None, None, None],
                ["Folder #", "Breast (Right/Left)", "Age", "BI-RADS categories for breast density", "BI-RADS categories for classification", "Follow-up Results"],
                [1, "Left", 55, "b", 1, "NOT AVAILABLE"],
            ]
        ).to_excel(xl, sheet_name="Normal_cases", header=False, index=False)
        pd.DataFrame(
            [
                ["Suspicious Cases", None, None, None, None, None],
                ["Folder #", "Breast (Right/Left)", "Age", "BI-RADS categories for breast density", "BI-RADS categories for classification", "Biopsy Results"],
                [1, "Right", 60, "c", "4b", "DCIS"],
            ]
        ).to_excel(xl, sheet_name="Suspicious_cases", header=False, index=False)

    man = tmp_path / "manifests"
    rep = tmp_path / "reports"
    build_inventory(raw, "DS0005", man / "DS0005_images.csv", man / "DS0005_private_linkage.csv", rep / "r5.md")
    spec = LabelCohortSpec("DS0005", raw, man / "DS0005_private_linkage.csv", None, "BMCD")
    _, recs = audit_cohort_labels(spec, tmp_path / "native", tmp_path / "overlays", mode="full")
    by_stem = {r.SourceStem: r for r in recs}

    assert by_stem["Normal_cases/1/CC_recent"].LabelClass == "Normal_Control"
    assert by_stem["Normal_cases/1/CC_recent"].MaskStatus == "ok_expected_empty"
    assert by_stem["Suspicious_cases/1/CC_prior"].LabelClass == "Excluded_PriorScreeningRound"
    assert by_stem["Suspicious_cases/1/CC_recemt"].BinaryTarget == "1"
    assert by_stem["Suspicious_cases/1/CC_recemt"].LocalizationEligible is True
    assert "UpstreamFilenameTypo_CC_recemt" in by_stem["Suspicious_cases/1/CC_recemt"].AnomalyFlags

    # Bottom-margin red artifact bar must trigger LocalizationEligible = False (`ADJ-016-02`)
    gt_bar = np.full((120, 100, 3), 90, dtype=np.uint8)
    gt_bar[108:116, 20:80] = (230, 15, 15)
    Image.fromarray(gt_bar, mode="RGB").save(susp_d / "CC_recent_GT.jpg")
    _, recs_bar = audit_cohort_labels(spec, tmp_path / "native_bar", tmp_path / "overlays_bar", mode="full")
    bar_rec = {r.SourceStem: r for r in recs_bar}["Suspicious_cases/1/CC_recemt"]
    assert bar_rec.MaskStatus == "flagged_border_red_bar"
    assert bar_rec.LocalizationEligible is False
    assert "BMCD_GT_BottomMarginRedBar" in bar_rec.AnomalyFlags


def test_cmmd_bilateral_discordant_contralateral_and_conflict_exclusion(tmp_path: Path) -> None:
    """Verify CMMD patient+laterality join, contralateral exclusion & D1-0808 conflict block."""
    raw = tmp_path / "raw" / "DS0003"
    arr = np.full((64, 64), 90, dtype=np.uint8)
    _save_test_dicom(raw / "dicoms" / "D1-0001" / "01.dcm", arr, patient_id="D1-0001", laterality="L", view_pos="", view_snomed="399162004")
    _save_test_dicom(raw / "dicoms" / "D1-0001" / "02.dcm", arr, patient_id="D1-0001", laterality="R", view_pos="", view_snomed="399368009")
    _save_test_dicom(raw / "dicoms" / "D1-0002" / "01.dcm", arr, patient_id="D1-0002", laterality="L", view_pos="CC")
    _save_test_dicom(raw / "dicoms" / "D1-0002" / "02.dcm", arr, patient_id="D1-0002", laterality="R", view_pos="CC")
    _save_test_dicom(raw / "dicoms" / "D1-0808" / "01.dcm", arr, patient_id="D1-0808", laterality="R", view_pos="CC")

    pd.DataFrame(
        [
            {"ID1": "D1-0001", "LeftRight": "L", "Age": 45, "number": 2, "abnormality": "mass", "classification": "Malignant", "subtype": np.nan},
            {"ID1": "D1-0001", "LeftRight": "R", "Age": 45, "number": 2, "abnormality": "calcification", "classification": "Benign", "subtype": np.nan},
            {"ID1": "D1-0002", "LeftRight": "L", "Age": 50, "number": 2, "abnormality": "mass", "classification": "Benign", "subtype": np.nan},
            {"ID1": "D1-0808", "LeftRight": "R", "Age": 45, "number": 2, "abnormality": "mass", "classification": "Benign", "subtype": np.nan},
        ]
    ).to_excel(raw / "CMMD_clinicaldata_revision.xlsx", index=False)

    man = tmp_path / "manifests"
    rep = tmp_path / "reports"
    build_inventory(raw, "DS0003", man / "DS0003_images.csv", man / "DS0003_private_linkage.csv", rep / "r3.md", patient_pattern=r"(D\d-\d+)")
    spec = LabelCohortSpec("DS0003", raw, man / "DS0003_private_linkage.csv", None, "CMMD")
    summary, recs = audit_cohort_labels(spec, tmp_path / "native", tmp_path / "overlays", mode="full")
    by_rel = {r.RawRelativePath: r for r in recs}

    assert summary.arithmetic_closure_ok
    assert by_rel["dicoms/D1-0001/01.dcm"].BinaryTarget == "1"
    assert by_rel["dicoms/D1-0001/01.dcm"].ViewPosition == "CC"
    assert by_rel["dicoms/D1-0001/02.dcm"].BinaryTarget == "0"
    assert by_rel["dicoms/D1-0001/02.dcm"].ViewPosition == "MLO"
    assert "BilateralDiscordantPatient" in by_rel["dicoms/D1-0001/01.dcm"].AnomalyFlags
    assert by_rel["dicoms/D1-0002/02.dcm"].LabelClass == "Excluded_UnlabeledContralateral"
    assert by_rel["dicoms/D1-0808/01.dcm"].LabelClass == "Excluded_CrossLabelClonePatient"


def test_mias_yflip_and_pipeline_orchestration(tmp_path: Path) -> None:
    """Verify MIAS bottom-left Y-flip rasterization and end-to-end Tier-1-safe summary JSON."""
    mask_flip = rasterize_mias_circle([(20.0, 20.0, 8.0)], height=100, width=100, y_from_bottom=True)
    # y=20 from bottom of height=100 -> row=80
    assert mask_flip[80, 20] == 1 and mask_flip[20, 20] == 0

    raw = tmp_path / "raw" / "DS0001"
    raw.mkdir(parents=True)
    img = np.full((100, 100), 50, dtype=np.uint8)
    Image.fromarray(img, mode="L").save(raw / "mdb001lm.pgm")
    Image.fromarray(img, mode="L").save(raw / "mdb002rl.pgm")
    Image.fromarray(img, mode="L").save(raw / "mdb059l.pgm")
    (raw / "00README.txt").write_text(
        "mdb001lm G CIRC B 40 25 10\n"
        "mdb002rl F NORM\n"
        "mdb059l D ARCH M\n",
        encoding="utf-8",
    )

    man = tmp_path / "manifests"
    rep = tmp_path / "reports"
    build_inventory(raw, "DS0001", man / "DS0001_images.csv", man / "DS0001_private_linkage.csv", rep / "r1.md")
    payload = run_label_verification(
        specs=[LabelCohortSpec("DS0001", raw, man / "DS0001_private_linkage.csv", None, "MIAS")],
        tier2_native_dir=tmp_path / "native",
        tier2_overlays_dir=tmp_path / "overlays",
        mode="pilot",
        seed=20261128,
    )
    c1 = payload["cohorts"][0]
    assert c1["arithmetic_closure_ok"] is True
    assert c1["mask_status_counts"].get("ok_nonempty") == 1
    assert c1["mask_status_counts"].get("excluded_by_protocol") == 1
    assert c1["anomaly_flag_counts"].get("Excluded_NoRadiusForROI") == 1
    assert Path(c1["tier2_overlay_png"]).is_file()
    # Ensure Tier-1 discrepancy summary contains zero raw relative filenames
    assert "mdb059l" not in json.dumps(c1["discrepancies"])

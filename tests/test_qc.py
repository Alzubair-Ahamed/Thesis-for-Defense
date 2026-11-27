"""Unit tests for STEP-013 read-only mammogram QC engine (src/bc_xai/data/qc.py)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pydicom
from PIL import Image
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, SecondaryCaptureImageStorage

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from bc_xai.data.inventory import build_inventory, verify_manifest_integrity  # noqa: E402
from bc_xai.data.qc import CohortSpec, audit_cohort, run_all_qc  # noqa: E402


def _write_synthetic_dicom(
    path: Path,
    arr: np.ndarray,
    photometric: str = "MONOCHROME2",
    patient_id: str = "PAT001",
    patient_name: str = "PAT001",
    institution: str = "",
) -> None:
    """Create a valid minimal DICOM image on disk for read-only QC testing."""
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = FileMetaDataset()
    meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds = FileDataset(str(path), {}, file_meta=meta, preamble=b"\0" * 128)
    ds.PatientID = patient_id
    ds.PatientName = patient_name
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = meta.MediaStorageSOPInstanceUID
    ds.Modality = "MG"
    if institution:
        ds.InstitutionName = institution
    ds.Rows, ds.Columns = arr.shape[:2]
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = photometric
    ds.BitsAllocated = 16 if arr.dtype == np.uint16 else 8
    ds.BitsStored = 12 if arr.dtype == np.uint16 else 8
    ds.HighBit = ds.BitsStored - 1
    ds.PixelRepresentation = 0
    ds.PixelData = arr.tobytes()
    ds.save_as(str(path), enforce_file_format=True)


def test_qc_handles_monochrome1_blank_corrupt_and_preserves_hashes(tmp_path: Path) -> None:
    """QC must flag MONOCHROME1, quarantine flat frames, exclude corrupt files & preserve hashes."""
    raw_dir = tmp_path / "raw" / "DS9001"
    rng = np.random.default_rng(123)
    good_img = rng.integers(50, 3900, size=(128, 128), dtype=np.uint16)
    blank_img = np.zeros((128, 128), dtype=np.uint16)

    _write_synthetic_dicom(raw_dir / "P01" / "valid_m1.dcm", good_img, photometric="MONOCHROME1", patient_id="P01", patient_name="P01")
    _write_synthetic_dicom(raw_dir / "P02" / "blank_m2.dcm", blank_img, photometric="MONOCHROME2", patient_id="P02", patient_name="P02", institution="TEST_HOSP")
    (raw_dir / "P03").mkdir(parents=True, exist_ok=True)
    (raw_dir / "P03" / "corrupt.dcm").write_bytes(b"NOT_A_REAL_DICOM_FILE")
    (raw_dir / "desktop.ini").write_text("[ViewState]\n", encoding="utf-8")

    manifest_out = tmp_path / "manifests" / "DS9001_images.csv"
    linkage_out = tmp_path / "manifests" / "DS9001_private_linkage.csv"
    receipt_out = tmp_path / "reports" / "DS9001_intake_receipt.md"
    build_inventory(raw_dir, "DS9001", manifest_out, linkage_out, receipt_out, patient_pattern=r"(P\d+)")

    spec = CohortSpec("DS9001", raw_dir, linkage_out, "SynthDICOM")
    summary, recs = audit_cohort(
        spec,
        tier2_cache_dir=tmp_path / "cache" / "qc",
        contact_sheets_dir=tmp_path / "images" / "qc_contact_sheets",
    )

    assert summary.total_raw_files == 4
    assert summary.primary_acquired == 3
    assert summary.primary_retained == 1
    assert summary.primary_quarantined == 1
    assert summary.primary_excluded == 1
    assert summary.photometric_counts.get("MONOCHROME1") == 1
    assert summary.non_pseudonym_phi_counts.get("InstitutionName") == 1
    assert summary.pseudonym_echo_counts.get("PatientName") == 2
    assert summary.integrity_errors_pre == 0 and summary.integrity_errors_post == 0
    assert Path(summary.contact_sheet_path).is_file()
    assert verify_manifest_integrity(raw_dir, linkage_out) == []

    # Tier-1 report must never leak institution string or raw paths
    report_txt = Path(summary.tier2_detail_csv).read_text(encoding="utf-8")
    assert "TEST_HOSP" not in report_txt


def test_qc_cdd_cesm_isolation_and_cross_cohort_duplicates(tmp_path: Path) -> None:
    """QC must isolate DS0006 LE vs subtracted CESM and catch identical images across cohorts."""
    rng = np.random.default_rng(999)
    shared = rng.integers(0, 255, size=(96, 96), dtype=np.uint8)
    unique_a = rng.integers(0, 255, size=(96, 96), dtype=np.uint8)

    raw1 = tmp_path / "raw" / "DS0001"
    raw6 = tmp_path / "raw" / "DS0006"
    raw1.mkdir(parents=True)
    (raw6 / "Low energy images of CDD-CESM").mkdir(parents=True)
    (raw6 / "Subtracted images of CDD-CESM").mkdir(parents=True)
    (raw6 / "Medical reports").mkdir(parents=True)

    Image.fromarray(shared, mode="L").save(raw1 / "P1_shared.png")
    Image.fromarray(unique_a, mode="L").save(raw1 / "P2_unique.png")
    Image.fromarray(shared, mode="L").save(raw6 / "Low energy images of CDD-CESM" / "P1_L_DM_CC.png")
    Image.fromarray(unique_a, mode="L").save(raw6 / "Subtracted images of CDD-CESM" / "P1_L_CM_CC.png")
    (raw6 / "Medical reports" / "~$P54.docx").write_bytes(b"lock")
    (raw6 / "Low energy images of CDD-CESM" / "desktop.ini").write_text("x", encoding="utf-8")

    man = tmp_path / "manifests"
    rep = tmp_path / "reports"
    build_inventory(raw1, "DS0001", man / "DS0001_images.csv", man / "DS0001_private_linkage.csv", rep / "r1.md")
    build_inventory(raw6, "DS0006", man / "DS0006_images.csv", man / "DS0006_private_linkage.csv", rep / "r6.md")

    payload = run_all_qc(
        specs=[
            CohortSpec("DS0001", raw1, man / "DS0001_private_linkage.csv", "CohortA"),
            CohortSpec("DS0006", raw6, man / "DS0006_private_linkage.csv", "CDD-CESM"),
        ],
        reports_dir=rep,
        tier2_cache_dir=tmp_path / "cache" / "qc",
        contact_sheets_dir=tmp_path / "images" / "qc_contact_sheets",
    )

    c6 = [c for c in payload["cohorts"] if c["dataset_id"] == "DS0006"][0]
    assert c6["primary_acquired"] == 1
    assert c6["primary_retained"] == 1
    assert c6["disposition_counts"]["Excluded_SubtractedCESM_RF15"] == 1
    assert c6["disposition_counts"]["Excluded_WordTempLock"] == 1
    assert c6["disposition_counts"]["Excluded_OSSystemFile"] == 1
    assert payload["cross_cohort_exact_count"] == 1
    assert (rep / "DS0001_quality.md").is_file()
    assert (rep / "DS0006_quality.md").is_file()


def test_qc_catches_reencoded_header_pixel_clone(tmp_path: Path) -> None:
    """Identical uncompressed pixels with distinct DICOM UIDs/SHA256 must be quarantined."""
    rng = np.random.default_rng(77)
    arr = rng.integers(10, 240, size=(96, 96), dtype=np.uint8)
    raw_dir = tmp_path / "raw" / "DS9002"
    _write_synthetic_dicom(raw_dir / "PAT_A" / "scan1.dcm", arr, patient_id="PAT_A", patient_name="PAT_A")
    _write_synthetic_dicom(raw_dir / "PAT_B" / "scan2.dcm", arr, patient_id="PAT_B", patient_name="PAT_B")

    man = tmp_path / "manifests"
    rep = tmp_path / "reports"
    build_inventory(raw_dir, "DS9002", man / "DS9002_images.csv", man / "DS9002_private_linkage.csv", rep / "r.md", patient_pattern=r"(PAT_[AB])")
    spec = CohortSpec("DS9002", raw_dir, man / "DS9002_private_linkage.csv", "CloneTest")
    summary, _ = audit_cohort(spec, tmp_path / "cache" / "qc", tmp_path / "images" / "qc")

    assert summary.primary_acquired == 2
    assert summary.primary_retained == 1
    assert summary.primary_quarantined == 1
    assert summary.disposition_counts.get("Quarantined_PixelCloneAcrossPatients") == 1

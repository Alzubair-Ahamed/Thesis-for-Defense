"""Unit tests for STEP-012 read-only SHA-256 mammogram inventory (src/bc_xai/data/inventory.py)."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from bc_xai.data.inventory import (  # noqa: E402
    build_inventory,
    classify_file,
    main,
    verify_manifest_integrity,
)


def _create_synthetic_raw_tree(raw_dir: Path) -> None:
    """Populate a realistic multi-format raw directory including edge-case files."""
    (raw_dir / "P_0001").mkdir(parents=True, exist_ok=True)
    (raw_dir / "P_0002" / "masks").mkdir(parents=True, exist_ok=True)
    (raw_dir / "P_0001" / "scan_lcc.dcm").write_bytes(b"DICM_SYNTH_1")
    (raw_dir / "P_0002" / "scan_rmlo.tif").write_bytes(b"TIFF_SYNTH_2")
    (raw_dir / "P_0002" / "masks" / "roi_mask_01.png").write_bytes(b"MASK_SYNTH_3")
    (raw_dir / "P_0002" / "contour.xml").write_text("<roi><point>1,2</point></roi>", encoding="utf-8")
    (raw_dir / "metadata.csv").write_text("patient,label\nP_0001,benign\n", encoding="utf-8")
    (raw_dir / "corrupt_empty.dcm").write_bytes(b"")


def test_inventory_hashes_all_files_and_segregates_linkage(tmp_path: Path) -> None:
    """Every file must be hashed untouched while private paths stay segregated from manifest."""
    raw_dir = tmp_path / "raw" / "DS0001"
    _create_synthetic_raw_tree(raw_dir)
    manifest_out = tmp_path / "manifests" / "DS0001_images.csv"
    linkage_out = tmp_path / "manifests" / "DS0001_private_linkage.csv"
    receipt_out = tmp_path / "reports" / "DS0001_intake_receipt.md"

    summary = build_inventory(
        raw_dir=raw_dir,
        dataset_id="DS0001",
        manifest_out=manifest_out,
        linkage_out=linkage_out,
        receipt_out=receipt_out,
        expected_count=6,
        patient_pattern=r"(P_\d+)",
        source_url="https://example.org/ds0001",
        source_version="v1.0",
    )

    assert summary.total_files == 6
    assert summary.unique_patient_tokens == 2
    assert summary.unreadable_files == 0
    assert manifest_out.is_file() and linkage_out.is_file() and receipt_out.is_file()

    with manifest_out.open(encoding="utf-8") as fp:
        m_rows = list(csv.DictReader(fp))
    assert len(m_rows) == 6
    # Pseudonymous manifest must never expose raw directory/patient names directly
    manifest_text = manifest_out.read_text(encoding="utf-8")
    assert "P_0001" not in manifest_text
    assert "scan_lcc" not in manifest_text

    zero_byte_row = [r for r in m_rows if r["SizeBytes"] == "0"][0]
    assert zero_byte_row["ReadStatus"] == "empty_zero_bytes"
    assert verify_manifest_integrity(raw_dir, linkage_out) == []


def test_inventory_fails_loudly_on_expected_count_mismatch(tmp_path: Path) -> None:
    """CLI and builder must fail loudly when acquired file count != expected count."""
    raw_dir = tmp_path / "raw" / "DS0002"
    _create_synthetic_raw_tree(raw_dir)
    manifest_out = tmp_path / "manifests" / "DS0002_images.csv"
    linkage_out = tmp_path / "manifests" / "DS0002_private_linkage.csv"
    receipt_out = tmp_path / "reports" / "DS0002_intake_receipt.md"

    with pytest.raises(ValueError, match="Transfer file count mismatch"):
        build_inventory(
            raw_dir=raw_dir,
            dataset_id="DS0002",
            manifest_out=manifest_out,
            linkage_out=linkage_out,
            receipt_out=receipt_out,
            expected_count=10,
        )

    exit_code = main(
        [
            "--raw-dir", str(raw_dir),
            "--dataset-id", "DS0002",
            "--manifest-out", str(manifest_out),
            "--linkage-out", str(linkage_out),
            "--receipt-out", str(receipt_out),
            "--expected-count", "99",
        ]
    )
    assert exit_code == 1


def test_verify_manifest_integrity_detects_tampering(tmp_path: Path) -> None:
    """Any post-intake byte alteration or missing file must be caught immediately."""
    raw_dir = tmp_path / "raw" / "DS0003"
    _create_synthetic_raw_tree(raw_dir)
    manifest_out = tmp_path / "manifests" / "DS0003_images.csv"
    linkage_out = tmp_path / "manifests" / "DS0003_private_linkage.csv"
    receipt_out = tmp_path / "reports" / "DS0003_intake_receipt.md"

    build_inventory(
        raw_dir=raw_dir,
        dataset_id="DS0003",
        manifest_out=manifest_out,
        linkage_out=linkage_out,
        receipt_out=receipt_out,
    )

    # Mutate one byte inside raw tree
    (raw_dir / "P_0001" / "scan_lcc.dcm").write_bytes(b"TAMPERED_BYTE")
    errs = verify_manifest_integrity(raw_dir, linkage_out)
    assert any("SHA-256 mismatch" in e for e in errs)


def test_classify_file_distinguishes_masks_and_metadata() -> None:
    """Verify non-destructive path classification across mammogram types."""
    assert classify_file(Path("A/img01.dcm")) == "image_dicom"
    assert classify_file(Path("A/masks/roi_01.png")) == "roi_mask_image"
    assert classify_file(Path("A/roi_contour.xml")) == "roi_xml_or_metadata"
    assert classify_file(Path("metadata/calc_case.csv")) == "metadata_table"
    assert classify_file(Path("bundle.zip")) == "archive_bundle"


def test_gitignore_blocks_ds_manifests_and_private_linkage() -> None:
    """Live .gitignore must keep DS####_private_linkage.csv and DS####_images.csv out of Git."""
    for dummy in [
        "03_Datasets/manifests/DS0001_private_linkage.csv",
        "03_Datasets/manifests/DS0001_images.csv",
        "03_Datasets/raw/DS0001/scan.dcm",
    ]:
        res = subprocess.run(
            ["git", "check-ignore", "-q", dummy],
            cwd=str(ROOT),
            capture_output=True,
        )
        assert res.returncode == 0, f"Path not ignored by .gitignore: {dummy}"

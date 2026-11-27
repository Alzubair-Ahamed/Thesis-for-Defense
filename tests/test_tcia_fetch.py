"""Unit tests for resumable TCIA NBIA collection downloader (src/bc_xai/data/tcia_fetch.py)."""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from bc_xai.data.tcia_fetch import (  # noqa: E402
    download_one_series,
    filter_series,
    parse_args,
    parse_series_records,
    prune_verified_archives,
    series_extract_dir,
    series_zip_path,
    verify_zip_archive,
)


def test_parse_and_filter_cbis_series_descriptions() -> None:
    """Filtering by SeriesDescription must cleanly isolate full mammograms vs ROI masks."""
    sample = json.dumps(
        [
            {
                "Collection": "CBIS-DDSM",
                "PatientID": "P_0001",
                "StudyInstanceUID": "1.2.3",
                "SeriesInstanceUID": "1.2.3.1",
                "SeriesDescription": "full mammogram images",
                "ImageCount": 1,
                "FileSize": 30000000,
            },
            {
                "Collection": "CBIS-DDSM",
                "PatientID": "P_0001",
                "StudyInstanceUID": "1.2.3",
                "SeriesInstanceUID": "1.2.3.2",
                "SeriesDescription": "ROI mask images",
                "ImageCount": 2,
                "FileSize": 15000000,
            },
            {
                "Collection": "CBIS-DDSM",
                "PatientID": "P_0002",
                "StudyInstanceUID": "1.2.4",
                "SeriesInstanceUID": "1.2.4.1",
                "SeriesDescription": "cropped images",
                "ImageCount": 1,
                "FileSize": 500000,
            },
        ]
    )
    recs = parse_series_records(sample)
    assert len(recs) == 3

    full_only = filter_series(recs, descriptions=["full mammogram images"])
    assert [r.series_uid for r in full_only] == ["1.2.3.1"]

    masks_only = filter_series(recs, descriptions=["ROI mask images", "cropped images"])
    assert [r.series_uid for r in masks_only] == ["1.2.3.2", "1.2.4.1"]


def test_verify_zip_archive_rejects_corrupt_and_accepts_valid(tmp_path: Path) -> None:
    """Valid DICOM ZIP passes verification while truncated/empty ZIP fails."""
    good_zip = tmp_path / "good.zip"
    with zipfile.ZipFile(good_zip, "w") as zf:
        zf.writestr("1-1.dcm", b"DICM_DATA")
    assert verify_zip_archive(good_zip) is True

    bad_zip = tmp_path / "bad.zip"
    bad_zip.write_bytes(b"NOT_A_VALID_ZIP")
    assert verify_zip_archive(bad_zip) is False

    empty_zip = tmp_path / "empty.zip"
    with zipfile.ZipFile(empty_zip, "w"):
        pass
    assert verify_zip_archive(empty_zip) is False


def test_series_paths_preserve_patient_and_series_uids(tmp_path: Path) -> None:
    """Archive and extract directories keep PatientID and SeriesInstanceUID deterministic."""
    rec = parse_series_records(
        json.dumps(
            [
                {
                    "Collection": "CMMD",
                    "PatientID": "D1-0001",
                    "StudyInstanceUID": "1.2",
                    "SeriesInstanceUID": "1.2.99",
                    "SeriesDescription": "Mammo View",
                    "ImageCount": 2,
                    "FileSize": 1000,
                }
            ]
        )
    )[0]
    assert series_zip_path(tmp_path, rec) == tmp_path / "archives" / "Mammo_View" / "D1-0001" / "1.2.99.zip"
    assert series_extract_dir(tmp_path, rec) == tmp_path / "dicoms" / "Mammo_View" / "D1-0001" / "1.2.99"


def test_cleanup_zip_and_prune_require_verified_extraction(tmp_path: Path) -> None:
    """Verified extracted series remove redundant ZIPs and stay skipped on resume."""
    import pytest

    rec = parse_series_records(
        json.dumps(
            [
                {
                    "Collection": "CBIS-DDSM",
                    "PatientID": "P_0003",
                    "StudyInstanceUID": "1.2",
                    "SeriesInstanceUID": "1.2.3.4",
                    "SeriesDescription": "ROI mask images",
                    "ImageCount": 1,
                    "FileSize": 512,
                }
            ]
        )
    )[0]

    zpath = series_zip_path(tmp_path, rec)
    zpath.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("1-1.dcm", b"DICM_PAYLOAD")

    with pytest.raises(ValueError, match="cleanup_zip=True requires extract=True"):
        download_one_series(rec, tmp_path, extract=False, cleanup_zip=True)

    status1, _ = download_one_series(rec, tmp_path, extract=True, cleanup_zip=True)
    edir = series_extract_dir(tmp_path, rec)
    assert status1 == "downloaded"
    assert (edir / "1-1.dcm").read_bytes() == b"DICM_PAYLOAD"
    assert (edir / ".extracted_ok").is_file()
    assert not zpath.exists()

    # Resume must treat already-extracted series as skipped even after ZIP cleanup.
    status2, _ = download_one_series(rec, tmp_path, extract=True, cleanup_zip=True)
    assert status2 == "skipped"

    # Re-create verified (marked read-only) vs unverified ZIPs to test prune_verified_archives safety.
    import os
    import stat

    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("1-1.dcm", b"DICM_PAYLOAD")
    os.chmod(zpath, stat.S_IREAD)

    unverified_rec = parse_series_records(
        json.dumps(
            [
                {
                    "Collection": "CBIS-DDSM",
                    "PatientID": "P_0004",
                    "StudyInstanceUID": "1.3",
                    "SeriesInstanceUID": "1.3.4.5",
                    "SeriesDescription": "ROI mask images",
                    "ImageCount": 1,
                    "FileSize": 512,
                }
            ]
        )
    )[0]
    uzpath = series_zip_path(tmp_path, unverified_rec)
    uzpath.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(uzpath, "w") as zf:
        zf.writestr("1-1.dcm", b"KEEP_ME")

    removed, freed = prune_verified_archives(tmp_path)
    assert removed == 1
    assert freed > 0
    assert not zpath.exists()
    assert uzpath.exists()

    args = parse_args(["--out-dir", str(tmp_path), "--prune-only"])
    assert args.prune_only is True

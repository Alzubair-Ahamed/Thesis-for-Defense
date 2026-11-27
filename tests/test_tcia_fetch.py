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
    filter_series,
    parse_series_records,
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

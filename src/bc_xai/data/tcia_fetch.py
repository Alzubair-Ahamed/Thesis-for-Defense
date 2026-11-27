"""Resumable multi-threaded TCIA NBIA REST API downloader for cleared public collections.

Supports collection metadata caching, optional SeriesDescription filtering (to split
CBIS-DDSM full mammograms vs ROI masks across drives safely), atomic `.part` -> `.zip`
writes with ZIP CRC integrity verification, optional extraction into immutable STEP-012
trees, and idempotent resume without re-downloading verified series.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import http.client
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

TCIA_BASE_URL = "https://services.cancerimagingarchive.net/nbia-api/services/v1"


@dataclass(frozen=True)
class SeriesRecord:
    """Subset of TCIA getSeries metadata fields used for filtered retrieval."""

    collection: str
    patient_id: str
    study_uid: str
    series_uid: str
    series_description: str
    image_count: int
    file_size_bytes: int


def sanitize_segment(value: str) -> str:
    """Return filesystem-safe path segment preserving readability."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return cleaned or "unknown"


def parse_series_records(raw_json: str) -> list[SeriesRecord]:
    """Parse raw TCIA getSeries JSON response into sorted SeriesRecord items."""
    payload = json.loads(raw_json)
    records: list[SeriesRecord] = []
    for item in payload:
        records.append(
            SeriesRecord(
                collection=str(item.get("Collection", "")).strip(),
                patient_id=str(item.get("PatientID", "unknown")).strip(),
                study_uid=str(item.get("StudyInstanceUID", "unknown")).strip(),
                series_uid=str(item["SeriesInstanceUID"]).strip(),
                series_description=str(item.get("SeriesDescription", "unspecified")).strip(),
                image_count=int(item.get("ImageCount") or 0),
                file_size_bytes=int(item.get("FileSize") or 0),
            )
        )
    records.sort(key=lambda r: (r.patient_id, r.series_description, r.series_uid))
    return records


def filter_series(
    records: Sequence[SeriesRecord],
    descriptions: Sequence[str] | None = None,
    limit: int | None = None,
) -> list[SeriesRecord]:
    """Filter series by exact SeriesDescription (case-insensitive) and optional limit."""
    selected = list(records)
    if descriptions:
        allowed = {d.strip().lower() for d in descriptions if d.strip()}
        selected = [r for r in selected if r.series_description.lower() in allowed]
    if limit is not None and limit >= 0:
        selected = selected[:limit]
    return selected


def fetch_collection_series(collection: str, manifest_cache: Path, timeout: int = 60) -> list[SeriesRecord]:
    """Fetch or load cached TCIA getSeries metadata for a collection."""
    if manifest_cache.is_file() and manifest_cache.stat().st_size > 2:
        return parse_series_records(manifest_cache.read_text(encoding="utf-8"))

    url = f"{TCIA_BASE_URL}/getSeries?Collection={urllib.parse.quote(collection)}"
    req = urllib.request.Request(url, headers={"User-Agent": "BC-XAI-Research/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw_text = resp.read().decode("utf-8")
    manifest_cache.parent.mkdir(parents=True, exist_ok=True)
    manifest_cache.write_text(raw_text, encoding="utf-8")
    return parse_series_records(raw_text)


def verify_zip_archive(zip_path: Path) -> bool:
    """Return True if zip_path is a valid non-empty ZIP passing CRC check."""
    if not zip_path.is_file() or zip_path.stat().st_size == 0:
        return False
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            return bool(names) and zf.testzip() is None
    except (zipfile.BadZipFile, OSError):
        return False


def series_zip_path(out_dir: Path, rec: SeriesRecord) -> Path:
    """Compute canonical archive destination path under out_dir/archives/."""
    desc_dir = sanitize_segment(rec.series_description)
    pat_dir = sanitize_segment(rec.patient_id)
    uid = sanitize_segment(rec.series_uid)
    return out_dir / "archives" / desc_dir / pat_dir / f"{uid}.zip"


def series_extract_dir(out_dir: Path, rec: SeriesRecord) -> Path:
    """Compute canonical extracted DICOM directory under out_dir/dicoms/."""
    desc_dir = sanitize_segment(rec.series_description)
    pat_dir = sanitize_segment(rec.patient_id)
    uid = sanitize_segment(rec.series_uid)
    return out_dir / "dicoms" / desc_dir / pat_dir / uid


def download_one_series(
    rec: SeriesRecord,
    out_dir: Path,
    extract: bool = True,
    timeout: int = 120,
    retries: int = 3,
) -> tuple[str, str]:
    """Download and verify a single TCIA series ZIP (idempotent resume)."""
    zpath = series_zip_path(out_dir, rec)
    edir = series_extract_dir(out_dir, rec)
    done_marker = edir / ".extracted_ok"

    if extract and done_marker.is_file():
        return ("skipped", rec.series_uid)
    if not extract and verify_zip_archive(zpath):
        return ("skipped", rec.series_uid)

    if not verify_zip_archive(zpath):
        zpath.parent.mkdir(parents=True, exist_ok=True)
        part_path = zpath.with_suffix(".zip.part")
        url = f"{TCIA_BASE_URL}/getImage?SeriesInstanceUID={urllib.parse.quote(rec.series_uid)}"
        last_err: Exception | None = None
        for _ in range(retries):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "BC-XAI-Research/1.0"})
                with urllib.request.urlopen(req, timeout=timeout) as resp, part_path.open("wb") as fp:
                    while True:
                        chunk = resp.read(1024 * 512)
                        if not chunk:
                            break
                        fp.write(chunk)
                if not verify_zip_archive(part_path):
                    raise zipfile.BadZipFile(f"Corrupted ZIP downloaded for {rec.series_uid}")
                part_path.replace(zpath)
                last_err = None
                break
            except (urllib.error.URLError, http.client.HTTPException, zipfile.BadZipFile, TimeoutError, OSError) as exc:
                last_err = exc
                if part_path.exists():
                    part_path.unlink(missing_ok=True)
        if last_err is not None:
            raise RuntimeError(f"Failed downloading {rec.series_uid}: {last_err}") from last_err

    if extract and not done_marker.is_file():
        edir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zpath, "r") as zf:
            for member in zf.infolist():
                member_name = Path(member.filename).name
                if not member_name or member.is_dir():
                    continue
                target = edir / member_name
                with zf.open(member, "r") as src, target.open("wb") as dst:
                    dst.write(src.read())
        done_marker.write_text("ok\n", encoding="utf-8")

    return ("downloaded", rec.series_uid)


def run_collection_download(
    collection: str,
    out_dir: Path,
    descriptions: Sequence[str] | None = None,
    workers: int = 6,
    limit: int | None = None,
    extract: bool = True,
) -> dict[str, int]:
    """Download filtered TCIA collection series concurrently with progress reporting."""
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_path = out_dir / f"_{sanitize_segment(collection)}_series_manifest.json"
    all_records = fetch_collection_series(collection, cache_path)
    targets = filter_series(all_records, descriptions=descriptions, limit=limit)
    total_bytes = sum(r.file_size_bytes for r in targets)
    print(
        f"TCIA Fetch {collection}: {len(targets)} target series "
        f"({total_bytes / (1024 ** 3):.2f} GiB uncompressed), workers={workers}"
    )

    counts = {"downloaded": 0, "skipped": 0, "failed": 0}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(download_one_series, rec, out_dir, extract): rec
            for rec in targets
        }
        for idx, fut in enumerate(concurrent.futures.as_completed(futures), start=1):
            try:
                status, _ = fut.result()
                counts[status] += 1
            except Exception as exc:
                counts["failed"] += 1
                print(f"ERROR [{idx}/{len(targets)}]: {exc}", file=sys.stderr)
            if idx % 50 == 0 or idx == len(targets):
                print(
                    f"Progress [{idx}/{len(targets)}]: "
                    f"downloaded={counts['downloaded']} skipped={counts['skipped']} failed={counts['failed']}",
                    flush=True,
                )
    return counts


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for TCIA collection downloader."""
    parser = argparse.ArgumentParser(description="Resumable TCIA NBIA collection downloader")
    parser.add_argument("--collection", required=True, help="TCIA Collection name (e.g., CMMD, CBIS-DDSM)")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--descriptions", type=str, default="", help="Comma-separated SeriesDescription filter")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--no-extract", action="store_true")
    return parser.parse_args(list(argv) if argv is not None else None)


def main(argv: Iterable[str] | None = None) -> int:
    """CLI entrypoint returning nonzero if any series fails download/verification."""
    args = parse_args(argv)
    descs = [d.strip() for d in args.descriptions.split(",") if d.strip()] if args.descriptions else None
    counts = run_collection_download(
        collection=args.collection,
        out_dir=args.out_dir,
        descriptions=descs,
        workers=args.workers,
        limit=args.limit,
        extract=not args.no_extract,
    )
    return 1 if counts["failed"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

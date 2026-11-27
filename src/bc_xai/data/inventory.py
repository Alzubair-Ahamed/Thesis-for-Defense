"""Read-only SHA-256 mammogram inventory and pseudonymous manifest builder (STEP-012).

Preserves every acquired raw file untouched (images, ROI masks, metadata CSV/XML,
archives, and unreadable files), emits segregated pseudonymous manifests alongside
restricted private linkage tables, computes deterministic manifest hashes, and fails
loudly on transfer count mismatches or raw-byte tampering.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import stat
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

CHUNK_SIZE_BYTES = 1024 * 1024  # 1 MiB streaming buffer

IMAGE_DICOM_EXTS = {".dcm", ".dicom"}
IMAGE_RASTER_EXTS = {".png", ".tif", ".tiff", ".pgm", ".jpg", ".jpeg", ".bmp", ".ljpeg"}
MASK_HINT_TOKENS = ("mask", "roi", "seg", "contour", "annotation", "overlay")
META_TABLE_EXTS = {".csv", ".tsv", ".xlsx", ".xls", ".json", ".txt"}
META_XML_EXTS = {".xml"}
ARCHIVE_EXTS = {".zip", ".tar", ".gz", ".tgz", ".bz2", ".7z", ".rar"}

MANIFEST_COLUMNS = [
    "ImageID",
    "DatasetID",
    "PatientGroupID",
    "RelativePathHash",
    "Extension",
    "SizeBytes",
    "SHA256",
    "FileCategory",
    "ReadStatus",
]

LINKAGE_COLUMNS = [
    "ImageID",
    "DatasetID",
    "PatientGroupID",
    "SourcePatientToken",
    "RawRelativePath",
    "SizeBytes",
    "SHA256",
    "FileCategory",
]


@dataclass(frozen=True)
class InventorySummary:
    """Aggregate summary returned after a read-only intake inventory run."""

    dataset_id: str
    raw_dir: Path
    total_files: int
    total_bytes: int
    unreadable_files: int
    unique_patient_tokens: int
    manifest_hash: str
    manifest_path: Path
    linkage_path: Path
    receipt_path: Path


def sha256_file(path: Path, chunk_size: int = CHUNK_SIZE_BYTES) -> str:
    """Compute lowercase hexadecimal SHA-256 digest of a file via streaming reads."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    """Return lowercase hexadecimal SHA-256 digest of UTF-8 text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def classify_file(rel_path: Path) -> str:
    """Classify an acquired file by extension and non-destructive path hints."""
    ext = rel_path.suffix.lower()
    lower_str = rel_path.as_posix().lower()
    if ext in ARCHIVE_EXTS or lower_str.endswith(".tar.gz"):
        return "archive_bundle"
    if ext in META_XML_EXTS:
        return "roi_xml_or_metadata" if any(tok in lower_str for tok in MASK_HINT_TOKENS) else "metadata_xml"
    if ext in META_TABLE_EXTS:
        return "metadata_table"
    if ext in IMAGE_DICOM_EXTS or ext in IMAGE_RASTER_EXTS:
        if any(tok in lower_str for tok in MASK_HINT_TOKENS):
            return "roi_mask_image"
        return "image_dicom" if ext in IMAGE_DICOM_EXTS else "image_raster"
    return "other_or_unexpected"


def infer_source_patient_token(
    rel_path: Path,
    patient_regex: re.Pattern[str] | None = None,
) -> str:
    """Extract conservative patient/case grouping token from relative path without guessing."""
    posix = rel_path.as_posix()
    if patient_regex is not None:
        match = patient_regex.search(posix)
        if match:
            token = match.group(1) if match.groups() else match.group(0)
            if token.strip():
                return token.strip()
    parts = rel_path.parts
    if len(parts) > 1 and re.search(r"[A-Za-z0-9]{2,}", parts[0]):
        first = parts[0]
        if re.match(r"^(?:P(?:at)?|Case|Sub|mdb|D1|D2|Calc|Mass|INbreast|[A-Za-z]+[-_]\d+)", first, re.I):
            return first
    stem_match = re.match(r"^([A-Za-z]+[-_]\d+|mdb\d+|\d{4,})", rel_path.stem, re.I)
    if stem_match:
        return stem_match.group(1)
    return "PAT_UNRESOLVED"


def set_tree_read_only(root: Path) -> int:
    """Apply read-only permissions across existing files without touching file contents."""
    changed = 0
    for path in sorted(root.rglob("*")):
        if path.is_file():
            mode = path.stat().st_mode
            new_mode = mode & ~stat.S_IWRITE & ~stat.S_IWGRP & ~stat.S_IWOTH
            if new_mode != mode:
                os.chmod(path, new_mode)
                changed += 1
    return changed


def build_inventory(
    raw_dir: Path,
    dataset_id: str,
    manifest_out: Path,
    linkage_out: Path,
    receipt_out: Path,
    expected_count: int | None = None,
    patient_pattern: str | None = None,
    source_url: str = "not reported",
    source_version: str = "not reported",
    make_readonly: bool = False,
) -> InventorySummary:
    """Walk raw_dir read-only, hash all files, emit pseudonymous & private manifests."""
    raw_dir = raw_dir.resolve()
    if not raw_dir.is_dir():
        raise FileNotFoundError(f"Raw dataset directory does not exist: {raw_dir}")
    if not re.fullmatch(r"DS\d{4}", dataset_id):
        raise ValueError(f"DatasetID must follow DS#### format, got: {dataset_id}")

    files: list[Path] = sorted(p for p in raw_dir.rglob("*") if p.is_file())
    if not files:
        raise ValueError(f"Raw dataset directory contains zero files: {raw_dir}")
    if expected_count is not None and len(files) != expected_count:
        raise ValueError(
            f"Transfer file count mismatch for {dataset_id}: expected {expected_count}, observed {len(files)}"
        )

    pat_regex = re.compile(patient_pattern) if patient_pattern else None
    pat_map: dict[str, str] = {}
    next_pat_idx = 1

    manifest_rows: list[list[str]] = []
    linkage_rows: list[list[str]] = []
    digest_lines: list[str] = []
    category_counts: dict[str, int] = {}
    total_bytes = 0
    unreadable_files = 0

    for idx, fpath in enumerate(files, start=1):
        rel = fpath.relative_to(raw_dir)
        rel_posix = rel.as_posix()
        image_id = f"IMG{idx:08d}"
        ext = fpath.suffix.lower() or "(none)"
        category = classify_file(rel)
        category_counts[category] = category_counts.get(category, 0) + 1

        try:
            size_bytes = fpath.stat().st_size
            file_hash = sha256_file(fpath)
            read_status = "empty_zero_bytes" if size_bytes == 0 else "ok"
            total_bytes += size_bytes
        except OSError as exc:
            size_bytes = -1
            file_hash = "UNREADABLE"
            read_status = f"unreadable:{type(exc).__name__}"
            unreadable_files += 1

        src_token = infer_source_patient_token(rel, pat_regex)
        if src_token == "PAT_UNRESOLVED":
            patient_group_id = "PAT_UNRESOLVED"
        else:
            if src_token not in pat_map:
                pat_map[src_token] = f"PAT{next_pat_idx:08d}"
                next_pat_idx += 1
            patient_group_id = pat_map[src_token]

        rel_hash = sha256_text(f"{dataset_id}::{rel_posix}")
        manifest_rows.append(
            [
                image_id,
                dataset_id,
                patient_group_id,
                rel_hash,
                ext,
                str(size_bytes),
                file_hash,
                category,
                read_status,
            ]
        )
        linkage_rows.append(
            [
                image_id,
                dataset_id,
                patient_group_id,
                src_token,
                rel_posix,
                str(size_bytes),
                file_hash,
                category,
            ]
        )
        digest_lines.append(f"{image_id}|{rel_hash}|{size_bytes}|{file_hash}|{category}")

    manifest_hash = sha256_text("\n".join(digest_lines))

    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    with manifest_out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(MANIFEST_COLUMNS)
        writer.writerows(manifest_rows)

    linkage_out.parent.mkdir(parents=True, exist_ok=True)
    with linkage_out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(LINKAGE_COLUMNS)
        writer.writerows(linkage_rows)

    if make_readonly:
        set_tree_read_only(raw_dir)

    receipt_out.parent.mkdir(parents=True, exist_ok=True)
    cat_lines = "\n".join(
        f"| `{k}` | `{v}` |" for k, v in sorted(category_counts.items())
    )
    receipt_text = (
        f"# Raw Dataset Intake Receipt — `{dataset_id}` (`STEP-012`)\n\n"
        f"- **DatasetID:** `{dataset_id}`\n"
        f"- **Intake Date:** `{date.today().isoformat()}`\n"
        f"- **Source URL / DOI:** {source_url}\n"
        f"- **Authorized Version:** `{source_version}`\n"
        f"- **Restricted Raw Directory:** `{raw_dir.as_posix()}` *(gitignored Tier-2)*\n"
        f"- **Total Files Inventoried:** `{len(files)}`\n"
        f"- **Total Size (Bytes):** `{total_bytes}` (`{total_bytes / (1024 ** 2):.2f} MiB`)\n"
        f"- **Unreadable Files:** `{unreadable_files}`\n"
        f"- **Resolved Source Patient Tokens:** `{len(pat_map)}` "
        f"(`{'PAT_UNRESOLVED present' if any(r[2] == 'PAT_UNRESOLVED' for r in manifest_rows) else 'all resolved'}`)\n"
        f"- **Deterministic Manifest SHA-256 (`ManifestHash`):** `{manifest_hash}`\n"
        f"- **Pseudonymous Manifest:** `{manifest_out.as_posix()}` *(gitignored Tier-2)*\n"
        f"- **Private Linkage Table:** `{linkage_out.as_posix()}` *(strictly gitignored Tier-2)*\n\n"
        f"## Inventoried File Categories\n\n"
        f"| Category | Count |\n|---|---|\n{cat_lines}\n"
    )
    receipt_out.write_text(receipt_text, encoding="utf-8")

    return InventorySummary(
        dataset_id=dataset_id,
        raw_dir=raw_dir,
        total_files=len(files),
        total_bytes=total_bytes,
        unreadable_files=unreadable_files,
        unique_patient_tokens=len(pat_map),
        manifest_hash=manifest_hash,
        manifest_path=manifest_out,
        linkage_path=linkage_out,
        receipt_path=receipt_out,
    )


def verify_manifest_integrity(raw_dir: Path, linkage_csv: Path) -> list[str]:
    """Re-verify raw file existence and SHA-256 hashes against recorded linkage table."""
    errors: list[str] = []
    raw_dir = raw_dir.resolve()
    recorded_paths: set[str] = set()

    with linkage_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rel_posix = row["RawRelativePath"]
            recorded_paths.add(rel_posix)
            fpath = raw_dir / rel_posix
            if not fpath.is_file():
                errors.append(f"Missing raw file: {rel_posix}")
                continue
            actual_hash = sha256_file(fpath)
            if actual_hash != row["SHA256"]:
                errors.append(
                    f"SHA-256 mismatch on {rel_posix}: expected {row['SHA256']}, got {actual_hash}"
                )

    actual_paths = {p.relative_to(raw_dir).as_posix() for p in raw_dir.rglob("*") if p.is_file()}
    unexpected = sorted(actual_paths - recorded_paths)
    for rel_posix in unexpected:
        errors.append(f"Uninventoried raw file present: {rel_posix}")
    return errors


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for STEP-012 dataset inventory execution."""
    parser = argparse.ArgumentParser(description="STEP-012 immutable mammogram raw inventory")
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--dataset-id", required=True, help="Canonical DS#### identifier")
    parser.add_argument("--manifest-out", type=Path, required=True)
    parser.add_argument("--linkage-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=None)
    parser.add_argument("--patient-pattern", type=str, default=None)
    parser.add_argument("--source-url", type=str, default="not reported")
    parser.add_argument("--source-version", type=str, default="not reported")
    parser.add_argument("--make-readonly", action="store_true")
    return parser.parse_args(list(argv) if argv is not None else None)


def main(argv: Iterable[str] | None = None) -> int:
    """CLI entrypoint failing loudly on count mismatch or empty archive."""
    args = parse_args(argv)
    try:
        summary = build_inventory(
            raw_dir=args.raw_dir,
            dataset_id=args.dataset_id,
            manifest_out=args.manifest_out,
            linkage_out=args.linkage_out,
            receipt_out=args.receipt_out,
            expected_count=args.expected_count,
            patient_pattern=args.patient_pattern,
            source_url=args.source_url,
            source_version=args.source_version,
            make_readonly=args.make_readonly,
        )
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"INVENTORY FAILED: {exc}", file=sys.stderr)
        return 1

    print(
        f"INVENTORY PASSED ({summary.dataset_id}): {summary.total_files} files "
        f"({summary.total_bytes} bytes), {summary.unique_patient_tokens} patient tokens, "
        f"ManifestHash={summary.manifest_hash}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

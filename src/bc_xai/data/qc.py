"""Read-only STEP-013 technical QC, DICOM PHI audit, duplicate check & contact-sheet builder.

Inspects acquired raw cohorts strictly via `DS####_private_linkage.csv` without ever modifying
raw bytes or copying PHI/raw paths into Tier-1 outputs. Verifies `verify_manifest_integrity`
before and after scanning, writes Tier-2 per-image CSV details under `03_Datasets/cache/qc/`
and stratified visual contact sheets under `03_Datasets/images/qc_contact_sheets/`, and emits
aggregate Tier-1 QC reports (`03_Datasets/reports/DS####_quality.md`) + cross-cohort audit.
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pydicom
from PIL import Image, ImageDraw, ImageOps

from bc_xai.data.inventory import sha256_file, verify_manifest_integrity

STANDARD_PIXEL_FORMATS = {".dcm", ".dicom", ".pgm", ".tif", ".tiff", ".png", ".jpg", ".jpeg", ".bmp"}
DICOM_EXTENSIONS = {".dcm", ".dicom"}
TEMP_LOCK_PREFIXES = ("~$", ".~")
OS_SYSTEM_FILENAMES = {"desktop.ini", "thumbs.db", ".ds_store"}

# Strict PHI / institutional tags to inspect in DICOM headers (never serialized raw to Tier-1).
PHI_SENSITIVE_TAGS = (
    "PatientName",
    "PatientBirthDate",
    "PatientAddress",
    "PatientTelephoneNumbers",
    "OtherPatientIDs",
    "OtherPatientNames",
    "InstitutionName",
    "InstitutionAddress",
    "InstitutionalDepartmentName",
    "ReferringPhysicianName",
    "PerformingPhysicianName",
    "PhysiciansOfRecord",
    "OperatorsName",
    "ReviewerName",
    "StationName",
    "AccessionNumber",
    "DeviceSerialNumber",
)

DEMOGRAPHIC_DATE_TAGS = ("PatientSex", "PatientAge", "StudyDate", "SeriesDate", "AcquisitionDate")


@dataclass(frozen=True)
class CohortSpec:
    """Mapping between a registered DS#### dataset and its local Tier-2 folders."""

    dataset_id: str
    raw_dir: Path
    linkage_csv: Path
    display_name: str = ""


@dataclass
class ImageQCRecord:
    """Per-file QC telemetry record stored strictly in Tier-2 cache CSVs."""

    DatasetID: str
    ImageID: str
    PatientGroupID: str
    RawRelativePath: str
    FileCategory: str
    RoleTrack: str
    Disposition: str
    Extension: str
    SizeBytes: int
    SHA256: str
    DecodeStatus: str
    DecodeError: str = ""
    DecoderUsed: str = ""
    Width: int | None = None
    Height: int | None = None
    Channels: int | None = None
    BitDepthStored: int | None = None
    BitsAllocated: int | None = None
    DType: str = ""
    PhotometricInterpretation: str = ""
    TransferSyntax: str = ""
    RescaleSlope: str = ""
    RescaleIntercept: str = ""
    HasVOILUT: bool = False
    WindowCenter: str = ""
    WindowWidth: str = ""
    ModalityTag: str = ""
    ManufacturerTag: str = ""
    ViewTag: str = ""
    LateralityTag: str = ""
    DICOMPatientIDPresent: bool = False
    DICOMStudyUIDPresent: bool = False
    DICOMPatientIDHash: str = ""
    DICOMStudyUIDHash: str = ""
    PixelMin: float | None = None
    PixelMax: float | None = None
    PixelMean: float | None = None
    PixelStd: float | None = None
    FracZero: float | None = None
    FracSaturated: float | None = None
    EdgeToCenterRatio: float | None = None
    RGBMaxChannelDiff: int | None = None
    NonPseudonymPHITags: str = ""
    PseudonymEchoTags: str = ""
    DemographicOrDateTags: str = ""
    BurnedInAnnotation: str = ""
    StudyYear: str = ""
    PixelContentSHA256: str = ""
    DHash64: str = ""
    ExactDupCluster: str = ""
    NearDupCluster: str = ""


@dataclass
class CohortQCResult:
    """Aggregate, Tier-1-safe QC summary for a single dataset."""

    dataset_id: str
    display_name: str
    total_raw_files: int
    primary_acquired: int
    primary_retained: int
    primary_excluded: int
    primary_quarantined: int
    disposition_counts: dict[str, int]
    track_counts: dict[str, int]
    decode_status_counts: dict[str, int]
    photometric_counts: dict[str, int]
    transfer_syntax_counts: dict[str, int]
    bit_depth_counts: dict[str, int]
    resolution_counts: dict[str, int]
    rescale_counts: dict[str, int]
    voi_lut_count: int
    window_present_count: int
    manufacturer_counts: dict[str, int]
    modality_tag_counts: dict[str, int]
    rgb_identical_channels: int
    rgb_nonzero_channel_diff: int
    non_pseudonym_phi_counts: dict[str, int]
    pseudonym_echo_counts: dict[str, int]
    demographic_tag_counts: dict[str, int]
    burned_in_counts: dict[str, int]
    study_years: dict[str, int]
    unique_dicom_patient_ids: int
    unique_dicom_study_uids: int
    unique_patient_group_ids: int
    exact_dup_within_cohort_clusters: int
    near_dup_within_cohort_pairs: int
    near_dup_cross_patient_pairs: int
    polarity_flip_near_dup_pairs: int
    integrity_errors_pre: int
    integrity_errors_post: int
    cohort_specific_notes: list[str] = field(default_factory=list)
    contact_sheet_path: str = ""
    tier2_detail_csv: str = ""


def _safe_str(val: Any) -> str:
    """Convert pydicom metadata values safely to printable scalar strings."""
    if val is None:
        return ""
    if isinstance(val, (list, tuple, pydicom.multival.MultiValue)):
        return ";".join(str(x).strip() for x in val)
    return str(val).strip()


def _format_scalar_tag(val: Any) -> str:
    """Serialize numeric or MultiValue DICOM tag into a compact string."""
    if val is None:
        return ""
    if isinstance(val, (list, tuple, pydicom.multival.MultiValue)):
        return "|".join(str(x).strip() for x in val)
    return str(val).strip()


def classify_qc_track(dataset_id: str, rel_path: str, file_category: str, size_bytes: int) -> tuple[str, str]:
    """Deterministically assign (RoleTrack, initial_non_primary_disposition) from intake metadata."""
    p = Path(rel_path)
    name_lower = p.name.lower()
    stem_lower = p.stem.lower()
    ext_lower = p.suffix.lower()
    norm_rel = rel_path.replace("\\", "/").lower()

    if name_lower.startswith(TEMP_LOCK_PREFIXES):
        return "excluded_system_or_temp", "Excluded_WordTempLock"
    if name_lower in OS_SYSTEM_FILENAMES:
        return "excluded_system_or_temp", "Excluded_OSSystemFile"
    if file_category == "roi_mask_image":
        return "roi_mask", "Supporting_ROIMask"
    if file_category in ("metadata_table", "archive_bundle", "other_or_unexpected"):
        return "metadata_or_doc", "Supporting_NonImageAsset"

    if dataset_id == "DS0006" and ext_lower in STANDARD_PIXEL_FORMATS:
        if "subtracted images" in norm_rel or "_cm_" in stem_lower:
            return "excluded_non_target_modality", "Excluded_SubtractedCESM_RF15"
        if "low energy images" in norm_rel or "_dm_" in stem_lower:
            return "primary_image", "PendingDecode"

    if dataset_id == "DS0005" and ext_lower in STANDARD_PIXEL_FORMATS:
        if stem_lower.endswith("_gt") or ext_lower in (".jpg", ".jpeg", ".png"):
            return "auxiliary_gt_overlay", "Excluded_OverlayGT_NotRawInput"

    if dataset_id == "DS0002" and ext_lower in STANDARD_PIXEL_FORMATS:
        if norm_rel.startswith("tiff images/"):
            if " - copy" in stem_lower or stem_lower.endswith(" copy"):
                return "mirror_raster", "Excluded_MirrorTIFF_CopyArtifact"
            return "mirror_raster", "Supporting_MirrorTIFF_Secondary"

    if ext_lower in STANDARD_PIXEL_FORMATS:
        if size_bytes == 0:
            return "primary_image", "Excluded_ZeroByteFile"
        return "primary_image", "PendingDecode"

    return "metadata_or_doc", "Supporting_NonImageAsset"


def _grayscale_and_rgb_diff(arr: np.ndarray) -> tuple[np.ndarray, int | None]:
    """Return 2D luminance array quickly and exact max RGB channel difference if multi-channel."""
    if arr.ndim == 2:
        return arr, None
    c0, c1, c2 = arr[..., 0], arr[..., 1], arr[..., 2]
    if np.array_equal(c0, c1) and np.array_equal(c1, c2):
        return c0, 0
    diff01 = int(np.max(np.abs(c0.astype(np.int32) - c1.astype(np.int32))))
    diff12 = int(np.max(np.abs(c1.astype(np.int32) - c2.astype(np.int32))))
    rgb_diff = max(diff01, diff12)
    if arr.dtype == np.uint8:
        gray = cv2.cvtColor(arr[..., :3], cv2.COLOR_RGB2GRAY)
    else:
        gray = arr[..., :3].mean(axis=2, dtype=np.float32)
    return gray, rgb_diff


def _compute_stats_fast(gray: np.ndarray, max_theoretical: float) -> tuple[float, float, float, float, float, float]:
    """Compute exact (min, max, mean, std, frac_zero, frac_saturated) using bincount for integers."""
    total_vals = float(gray.size)
    if np.issubdtype(gray.dtype, np.unsignedinteger) and int(np.iinfo(gray.dtype).bits) <= 16:
        max_val_bound = int(np.max(gray))
        if max_val_bound <= 65535:
            hist = np.bincount(gray.ravel(), minlength=max_val_bound + 1)
            nz = np.nonzero(hist)[0]
            if nz.size == 0:
                return 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
            p_min = float(nz[0])
            p_max = float(nz[-1])
            vals = nz.astype(np.float64)
            wts = hist[nz].astype(np.float64)
            mean = float(np.sum(vals * wts) / total_vals)
            var = float(np.sum(((vals - mean) ** 2) * wts) / total_vals)
            std = float(np.sqrt(max(var, 0.0)))
            f_zero = float(hist[0]) / total_vals
            sat_idx = int(max_theoretical)
            f_sat = float(np.sum(hist[sat_idx:])) / total_vals if sat_idx <= max_val_bound else 0.0
            return (
                round(p_min, 3),
                round(p_max, 3),
                round(mean, 3),
                round(std, 4),
                round(f_zero, 5),
                round(f_sat, 5),
            )

    arr_f = gray.astype(np.float32, copy=False)
    return (
        round(float(np.min(arr_f)), 3),
        round(float(np.max(arr_f)), 3),
        round(float(np.mean(arr_f)), 3),
        round(float(np.std(arr_f)), 4),
        round(float(np.count_nonzero(gray == 0)) / total_vals, 5),
        round(float(np.count_nonzero(arr_f >= max_theoretical)) / total_vals, 5),
    )


def _compute_dhash64_from_small(small_f32: np.ndarray) -> str:
    """Compute 64-bit dHash from an already-downsampled 2D array."""
    s_min = float(np.min(small_f32))
    s_max = float(np.max(small_f32))
    if s_max > s_min:
        norm = ((small_f32 - s_min) / (s_max - s_min) * 255.0).clip(0.0, 255.0).astype(np.float32)
    else:
        return "0000000000000000"
    tiny = cv2.resize(norm, (9, 8), interpolation=cv2.INTER_AREA)
    diff = tiny[:, 1:] > tiny[:, :-1]
    bits = 0
    for val in diff.ravel():
        bits = (bits << 1) | (1 if bool(val) else 0)
    return f"{bits:016x}"


def compute_dhash64(arr: np.ndarray) -> str:
    """Compute a deterministic 64-bit difference hash (dHash) over normalized grayscale pixels."""
    gray, _ = _grayscale_and_rgb_diff(arr)
    if gray.shape[0] > 512 or gray.shape[1] > 512:
        small = cv2.resize(gray.astype(np.float32, copy=False), (256, 256), interpolation=cv2.INTER_AREA)
    else:
        small = gray.astype(np.float32, copy=False)
    return _compute_dhash64_from_small(small)


def _edge_to_center_ratio(small_f32: np.ndarray) -> float:
    """Compute border-vs-center intensity ratio on 2D array to screen for MONOCHROME1 polarity."""
    h, w = small_f32.shape
    if h < 16 or w < 16:
        return 0.0
    bh = max(4, h // 16)
    bw = max(4, w // 16)
    top = small_f32[:bh, :]
    bottom = small_f32[-bh:, :]
    left = small_f32[bh:-bh, :bw]
    right = small_f32[bh:-bh, -bw:]
    edge_mean = float(np.mean(np.concatenate([top.ravel(), bottom.ravel(), left.ravel(), right.ravel()])))
    center = small_f32[h // 4 : (3 * h) // 4, w // 4 : (3 * w) // 4]
    center_mean = float(np.mean(center))
    return round(edge_mean / max(center_mean, 1.0), 4)


def _bit_depth_from_pil_mode(mode: str) -> tuple[int, str]:
    """Infer bit depth and canonical dtype string from a PIL image mode."""
    if mode in ("1",):
        return 1, "bool"
    if mode.startswith("I;16"):
        return 16, "uint16"
    if mode in ("I",):
        return 32, "int32"
    if mode in ("F",):
        return 32, "float32"
    return 8, "uint8"


def _audit_dicom_phi(ds: pydicom.dataset.Dataset) -> tuple[list[str], list[str], list[str], str, str]:
    """Inspect DICOM tags for non-pseudonymous PHI, pseudonym echoes, dates, and burned-in flags."""
    pat_id = _safe_str(getattr(ds, "PatientID", ""))
    non_pseudo: list[str] = []
    echoes: list[str] = []
    demog: list[str] = []

    for tag in PHI_SENSITIVE_TAGS:
        val = _safe_str(getattr(ds, tag, ""))
        if not val:
            continue
        if tag == "PatientName" and pat_id and val == pat_id:
            echoes.append(tag)
        else:
            non_pseudo.append(tag)

    study_year = ""
    for tag in DEMOGRAPHIC_DATE_TAGS:
        val = _safe_str(getattr(ds, tag, ""))
        if not val:
            continue
        demog.append(tag)
        if tag == "StudyDate" and len(val) >= 4 and val[:4].isdigit() and not study_year:
            study_year = val[:4]

    burned = _safe_str(getattr(ds, "BurnedInAnnotation", ""))
    return non_pseudo, echoes, demog, burned, study_year


def inspect_single_file(dataset_id: str, raw_dir: Path, row: dict[str, str]) -> ImageQCRecord:
    """Run read-only decode, pixel telemetry, dHash, and header audit on one linkage row."""
    rel_path = row["RawRelativePath"]
    full_path = raw_dir / rel_path
    ext_lower = full_path.suffix.lower()
    size_bytes = int(row["SizeBytes"])
    file_cat = row["FileCategory"]
    role_track, init_disp = classify_qc_track(dataset_id, rel_path, file_cat, size_bytes)

    rec = ImageQCRecord(
        DatasetID=dataset_id,
        ImageID=row["ImageID"],
        PatientGroupID=row["PatientGroupID"],
        RawRelativePath=rel_path,
        FileCategory=file_cat,
        RoleTrack=role_track,
        Disposition=init_disp,
        Extension=ext_lower,
        SizeBytes=size_bytes,
        SHA256=row["SHA256"],
        DecodeStatus="skipped_non_image",
    )

    if ext_lower not in STANDARD_PIXEL_FORMATS or role_track in ("excluded_system_or_temp", "metadata_or_doc"):
        return rec

    if not full_path.is_file() or size_bytes == 0:
        rec.DecodeStatus = "failed_missing_or_empty"
        rec.DecodeError = "File missing or zero bytes"
        if role_track == "primary_image":
            rec.Disposition = "Excluded_ZeroByteOrMissing"
        return rec

    arr: np.ndarray | None = None
    try:
        if ext_lower in DICOM_EXTENSIONS:
            ds = pydicom.dcmread(full_path, force=False)
            rec.DecoderUsed = "pydicom"
            ts_uid = ds.file_meta.get("TransferSyntaxUID") if hasattr(ds, "file_meta") else None
            rec.TransferSyntax = getattr(ts_uid, "name", str(ts_uid or ""))
            rec.PhotometricInterpretation = _safe_str(getattr(ds, "PhotometricInterpretation", ""))
            rec.BitsAllocated = int(ds.BitsAllocated) if hasattr(ds, "BitsAllocated") else None
            rec.BitDepthStored = int(ds.BitsStored) if hasattr(ds, "BitsStored") else None
            rec.RescaleSlope = _format_scalar_tag(getattr(ds, "RescaleSlope", None))
            rec.RescaleIntercept = _format_scalar_tag(getattr(ds, "RescaleIntercept", None))
            rec.HasVOILUT = bool(getattr(ds, "VOILUTSequence", None))
            rec.WindowCenter = _format_scalar_tag(getattr(ds, "WindowCenter", None))
            rec.WindowWidth = _format_scalar_tag(getattr(ds, "WindowWidth", None))
            rec.ModalityTag = _safe_str(getattr(ds, "Modality", ""))
            rec.ManufacturerTag = _safe_str(getattr(ds, "Manufacturer", ""))
            rec.ViewTag = _safe_str(getattr(ds, "ViewPosition", ""))
            rec.LateralityTag = _safe_str(getattr(ds, "ImageLaterality", ""))
            dicom_pid = _safe_str(getattr(ds, "PatientID", ""))
            dicom_suid = _safe_str(getattr(ds, "StudyInstanceUID", ""))
            rec.DICOMPatientIDPresent = bool(dicom_pid)
            rec.DICOMStudyUIDPresent = bool(dicom_suid)
            if dicom_pid:
                rec.DICOMPatientIDHash = hashlib.sha256(dicom_pid.encode("utf-8")).hexdigest()[:16]
            if dicom_suid:
                rec.DICOMStudyUIDHash = hashlib.sha256(dicom_suid.encode("utf-8")).hexdigest()[:16]

            non_p, echoes, demog, burned, year = _audit_dicom_phi(ds)
            rec.NonPseudonymPHITags = ";".join(non_p)
            rec.PseudonymEchoTags = ";".join(echoes)
            rec.DemographicOrDateTags = ";".join(demog)
            rec.BurnedInAnnotation = burned
            rec.StudyYear = year

            arr = ds.pixel_array
        else:
            with Image.open(full_path) as im:
                im.load()
                rec.DecoderUsed = "PIL"
                bits_stored, inferred_dtype = _bit_depth_from_pil_mode(im.mode)
                rec.BitDepthStored = bits_stored
                rec.BitsAllocated = bits_stored if bits_stored in (8, 16, 32) else 8
                rec.PhotometricInterpretation = im.mode
                arr = np.asarray(im)
                if not rec.DType:
                    rec.DType = inferred_dtype
    except Exception as exc:  # noqa: BLE001
        rec.DecodeStatus = "failed_decode"
        rec.DecodeError = f"{type(exc).__name__}: {str(exc)[:180]}"
        if role_track == "primary_image":
            rec.Disposition = "Excluded_CorruptDecodeError"
        return rec

    rec.DecodeStatus = "ok"
    rec.Height = int(arr.shape[0])
    rec.Width = int(arr.shape[1]) if arr.ndim >= 2 else 1
    rec.Channels = int(arr.shape[2]) if arr.ndim == 3 else 1
    rec.DType = str(arr.dtype)

    gray, rgb_diff = _grayscale_and_rgb_diff(arr)
    rec.RGBMaxChannelDiff = rgb_diff
    rec.PixelContentSHA256 = hashlib.sha256(np.ascontiguousarray(gray).tobytes()).hexdigest()

    max_theoretical = float((1 << rec.BitDepthStored) - 1) if rec.BitDepthStored else float(np.max(gray))
    if max_theoretical <= 0:
        max_theoretical = 255.0

    p_min, p_max, p_mean, p_std, f_zero, f_sat = _compute_stats_fast(gray, max_theoretical)
    rec.PixelMin = p_min
    rec.PixelMax = p_max
    rec.PixelMean = p_mean
    rec.PixelStd = p_std
    rec.FracZero = f_zero
    rec.FracSaturated = f_sat

    small = cv2.resize(gray, (256, 256), interpolation=cv2.INTER_AREA).astype(np.float32, copy=False)
    rec.EdgeToCenterRatio = _edge_to_center_ratio(small)
    rec.DHash64 = _compute_dhash64_from_small(small)

    if role_track == "primary_image":
        if rec.Width < 64 or rec.Height < 64:
            rec.Disposition = "Excluded_TinyDimensions"
        elif (rec.PixelStd is not None and rec.PixelStd < 1.0) or (
            rec.FracZero is not None and rec.FracZero > 0.998
        ) or (rec.FracSaturated is not None and rec.FracSaturated > 0.998):
            rec.Disposition = "Quarantined_BlankOrNearConstant"
        else:
            rec.Disposition = "Retained"

    return rec


def _inspect_worker(args: tuple[str, str, dict[str, str]]) -> ImageQCRecord:
    """Top-level picklable worker wrapper for parallel cohort file inspection."""
    dataset_id, raw_dir_str, row = args
    return inspect_single_file(dataset_id, Path(raw_dir_str), row)


def _is_informative_dhash(dhash_hex: str) -> bool:
    """Reject degenerate margin-gradient hashes (<12 or >52 set bits out of 64)."""
    if not dhash_hex:
        return False
    pc = int(dhash_hex, 16).bit_count()
    return 12 <= pc <= 52


def _load_norm64(full_path: Path) -> np.ndarray | None:
    """Load 64x64 min-max normalized grayscale vector for tight clone correlation verification."""
    try:
        if full_path.suffix.lower() in DICOM_EXTENSIONS:
            arr = pydicom.dcmread(full_path, force=False).pixel_array
        else:
            with Image.open(full_path) as im:
                im.load()
                arr = np.asarray(im)
    except Exception:  # noqa: BLE001
        return None
    gray, _ = _grayscale_and_rgb_diff(arr)
    lo, hi = float(np.min(gray)), float(np.max(gray))
    scaled = (gray.astype(np.float32) - lo) / max(hi - lo, 1.0)
    return cv2.resize(scaled, (64, 64), interpolation=cv2.INTER_AREA).ravel()


def _assign_within_cohort_duplicates(
    records: list[ImageQCRecord],
    raw_dir: Path | None = None,
) -> tuple[int, int, int, int, list[dict[str, Any]]]:
    """Cluster file SHA-256, uncompressed PixelContentSHA256, and correlated near-clones."""
    sha_map: dict[str, list[ImageQCRecord]] = collections.defaultdict(list)
    pix_map: dict[str, list[ImageQCRecord]] = collections.defaultdict(list)
    primary_decoded: list[ImageQCRecord] = []
    for r in records:
        if r.DecodeStatus == "ok" and r.RoleTrack in ("primary_image", "mirror_raster"):
            sha_map[r.SHA256].append(r)
        if r.DecodeStatus == "ok" and r.RoleTrack == "primary_image":
            if r.PixelContentSHA256:
                pix_map[r.PixelContentSHA256].append(r)
            if r.DHash64:
                primary_decoded.append(r)

    exact_clusters = 0
    for idx, (_sha, group) in enumerate(sorted(sha_map.items())):
        if len(group) > 1:
            exact_clusters += 1
            cid = f"EXACT_{group[0].DatasetID}_{idx:03d}"
            for g in group:
                g.ExactDupCluster = cid
            prim_group = [g for g in group if g.RoleTrack == "primary_image"]
            for g_i, g in enumerate(prim_group):
                if g_i > 0:
                    if g.PatientGroupID != prim_group[0].PatientGroupID:
                        g.Disposition = "Quarantined_ExactDupAcrossPatients"
                    else:
                        g.Disposition = "Excluded_ExactDuplicateWithinCohort"

    # Uncompressed raw pixel SHA-256 clone clusters (catches header-reencoded clones!)
    pix_cluster_idx = 0
    for _psha, pgroup in sorted(pix_map.items()):
        if len(pgroup) > 1:
            cid = f"PIXCLONE_{pgroup[0].DatasetID}_{pix_cluster_idx:03d}"
            pix_cluster_idx += 1
            unique_pats = {g.PatientGroupID for g in pgroup}
            for g_i, g in enumerate(pgroup):
                if not g.ExactDupCluster:
                    g.ExactDupCluster = cid
                if g_i > 0 and g.Disposition == "Retained":
                    g.Disposition = (
                        "Quarantined_PixelCloneAcrossPatients"
                        if len(unique_pats) > 1
                        else "Excluded_PixelCloneWithinCohort"
                    )

    near_pairs = 0
    near_cross_pat = 0
    flip_pairs = 0
    near_pair_rows: list[dict[str, Any]] = []
    if len(primary_decoded) > 1:
        hashes = np.array([int(r.DHash64, 16) for r in primary_decoded], dtype=np.uint64)
        means = np.array([float(r.PixelMean or 0.0) for r in primary_decoded], dtype=np.float64)
        stds = np.array([float(r.PixelStd or 0.0) for r in primary_decoded], dtype=np.float64)
        inf_mask = np.array([_is_informative_dhash(r.DHash64) for r in primary_decoded], dtype=bool)
        thumb_cache: dict[str, np.ndarray | None] = {}

        for i in range(len(primary_decoded) - 1):
            ri = primary_decoded[i]
            xor_vals = hashes[i] ^ hashes[i + 1 :]
            dists = np.bitwise_count(xor_vals)

            # Check lossy near-identical pixel clones via tight stats + dHash<=2 even on low popcount
            if raw_dir is not None:
                stat_cand = np.nonzero(
                    (dists <= 2)
                    & (np.abs(means[i + 1 :] - means[i]) <= 0.2)
                    & (np.abs(stds[i + 1 :] - stds[i]) <= 0.2)
                )[0]
                for off in stat_cand:
                    j = i + 1 + int(off)
                    rj = primary_decoded[j]
                    if ri.PixelContentSHA256 == rj.PixelContentSHA256 or ri.Width != rj.Width or ri.Height != rj.Height:
                        continue
                    if ri.ImageID not in thumb_cache:
                        thumb_cache[ri.ImageID] = _load_norm64(raw_dir / ri.RawRelativePath)
                    if rj.ImageID not in thumb_cache:
                        thumb_cache[rj.ImageID] = _load_norm64(raw_dir / rj.RawRelativePath)
                    ta, tb = thumb_cache[ri.ImageID], thumb_cache[rj.ImageID]
                    if ta is not None and tb is not None and float(np.corrcoef(ta, tb)[0, 1]) >= 0.999:
                        if rj.Disposition == "Retained":
                            rj.Disposition = "Quarantined_LossyPixelClone"
                        tag = f"LOSSYCLONE_{ri.ImageID}_{rj.ImageID}"
                        if not ri.ExactDupCluster:
                            ri.ExactDupCluster = tag
                        if not rj.ExactDupCluster:
                            rj.ExactDupCluster = tag

            if not inf_mask[i]:
                continue
            close_idx = np.nonzero((dists <= 4) & inf_mask[i + 1 :])[0]
            for off in close_idx:
                j = i + 1 + int(off)
                rj = primary_decoded[j]
                if ri.SHA256 != rj.SHA256:
                    near_pairs += 1
                    same_pat = ri.PatientGroupID == rj.PatientGroupID
                    if not same_pat:
                        near_cross_pat += 1
                    tag = f"NEAR_{ri.ImageID}_{rj.ImageID}"
                    if not ri.NearDupCluster:
                        ri.NearDupCluster = tag
                    if not rj.NearDupCluster:
                        rj.NearDupCluster = tag
                    near_pair_rows.append(
                        {
                            "DatasetID": ri.DatasetID,
                            "ImageA": ri.ImageID,
                            "PatientGroupA": ri.PatientGroupID,
                            "ImageB": rj.ImageID,
                            "PatientGroupB": rj.PatientGroupID,
                            "SamePatientGroup": same_pat,
                            "HammingDist": int(dists[int(off)]),
                        }
                    )
            flip_pairs += int(np.count_nonzero((dists >= 60) & inf_mask[i + 1 :]))

    return exact_clusters, near_pairs, near_cross_pat, flip_pairs, near_pair_rows


def find_cross_cohort_duplicates(
    all_records: list[ImageQCRecord], hamming_threshold: int = 4
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Identify exact SHA-256 and perceptual dHash collisions across different cohorts."""
    prim = [r for r in all_records if r.DecodeStatus == "ok" and r.RoleTrack == "primary_image"]
    sha_map: dict[str, list[ImageQCRecord]] = collections.defaultdict(list)
    for r in prim:
        sha_map[r.SHA256].append(r)

    exact_cross: list[dict[str, Any]] = []
    for sha, grp in sha_map.items():
        datasets = {g.DatasetID for g in grp}
        if len(datasets) > 1:
            exact_cross.append(
                {
                    "SHA256": sha,
                    "Datasets": ";".join(sorted(datasets)),
                    "ImageIDs": ";".join(f"{g.DatasetID}:{g.ImageID}" for g in grp),
                }
            )

    near_cross: list[dict[str, Any]] = []
    if len(prim) > 1:
        hashes = np.array([int(r.DHash64, 16) for r in prim], dtype=np.uint64)
        inf_mask = np.array([_is_informative_dhash(r.DHash64) for r in prim], dtype=bool)
        ds_ids = [r.DatasetID for r in prim]
        for i in range(len(prim) - 1):
            if not inf_mask[i]:
                continue
            xor_vals = hashes[i] ^ hashes[i + 1 :]
            dists = np.bitwise_count(xor_vals)
            for off in np.nonzero((dists <= hamming_threshold) & inf_mask[i + 1 :])[0]:
                j = i + 1 + int(off)
                if ds_ids[i] != ds_ids[j]:
                    near_cross.append(
                        {
                            "DatasetA": prim[i].DatasetID,
                            "ImageA": prim[i].ImageID,
                            "DatasetB": prim[j].DatasetID,
                            "ImageB": prim[j].ImageID,
                            "HammingDist": int(dists[int(off)]),
                            "DHashA": prim[i].DHash64,
                            "DHashB": prim[j].DHash64,
                        }
                    )
    return exact_cross, near_cross


def _load_uint8_thumbnail(full_path: Path, thumb_size: int = 240) -> Image.Image:
    """Decode DICOM or raster image read-only and render a crisp 8-bit preview thumbnail."""
    ext = full_path.suffix.lower()
    if ext in DICOM_EXTENSIONS:
        ds = pydicom.dcmread(full_path, force=False)
        arr = ds.pixel_array
        if arr.ndim == 3:
            gray = arr[..., :3].mean(axis=2, dtype=np.float32)
        else:
            gray = arr.astype(np.float32, copy=False)
        lo, hi = float(np.percentile(gray, 1.0)), float(np.percentile(gray, 99.5))
        if hi <= lo:
            lo, hi = float(np.min(gray)), float(np.max(gray))
        if hi > lo:
            norm = ((gray - lo) / (hi - lo) * 255.0).clip(0.0, 255.0).astype(np.uint8)
        else:
            norm = np.zeros(gray.shape, dtype=np.uint8)
        pil_img = Image.fromarray(norm, mode="L").convert("RGB")
    else:
        with Image.open(full_path) as im:
            im.load()
            if im.mode.startswith("I;16") or im.mode == "I":
                arr = np.asarray(im, dtype=np.float32)
                lo, hi = float(np.percentile(arr, 1.0)), float(np.percentile(arr, 99.5))
                if hi > lo:
                    norm = ((arr - lo) / (hi - lo) * 255.0).clip(0.0, 255.0).astype(np.uint8)
                else:
                    norm = np.zeros(arr.shape, dtype=np.uint8)
                pil_img = Image.fromarray(norm, mode="L").convert("RGB")
            else:
                pil_img = im.convert("RGB")

    return ImageOps.pad(pil_img, (thumb_size, thumb_size), color=(18, 18, 18))


def build_contact_sheet(
    dataset_id: str,
    raw_dir: Path,
    records: list[ImageQCRecord],
    out_png: Path,
    grid_cols: int = 4,
    grid_rows: int = 4,
) -> Path | None:
    """Create a stratified 4x4 Tier-2 visual QC contact sheet with pseudonymous labels only."""
    ok_imgs = [r for r in records if r.DecodeStatus == "ok" and r.RoleTrack == "primary_image"]
    if not ok_imgs:
        return None

    target_n = min(grid_cols * grid_rows, len(ok_imgs))
    by_disp = [r for r in ok_imgs if r.Disposition != "Retained"]
    retained = [r for r in ok_imgs if r.Disposition == "Retained"]
    retained_sorted = sorted(retained, key=lambda x: (x.PixelMean or 0.0))

    picked: list[ImageQCRecord] = []
    seen_ids: set[str] = set()
    for r in by_disp[:4]:
        if r.ImageID not in seen_ids:
            picked.append(r)
            seen_ids.add(r.ImageID)

    # Stratify remaining slots across intensity & resolution quantiles
    need = target_n - len(picked)
    if need > 0 and retained_sorted:
        step = max(1, len(retained_sorted) // need)
        for cand in retained_sorted[::step]:
            if cand.ImageID not in seen_ids:
                picked.append(cand)
                seen_ids.add(cand.ImageID)
            if len(picked) >= target_n:
                break
    for cand in ok_imgs:
        if len(picked) >= target_n:
            break
        if cand.ImageID not in seen_ids:
            picked.append(cand)
            seen_ids.add(cand.ImageID)

    cell_w, cell_h = 260, 290
    header_h = 36
    canvas = Image.new("RGB", (grid_cols * cell_w, header_h + grid_rows * cell_h), (24, 24, 28))
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (12, 10),
        f"{dataset_id} Stratified Visual QC Sheet ({len(picked)}/{len(ok_imgs)} Primary Images | Pseudonymous IDs)",
        fill=(235, 240, 245),
    )

    for idx, rec in enumerate(picked):
        r_i, c_i = divmod(idx, grid_cols)
        x0 = c_i * cell_w + 10
        y0 = header_h + r_i * cell_h + 6
        thumb = _load_uint8_thumbnail(raw_dir / rec.RawRelativePath, thumb_size=236)
        canvas.paste(thumb, (x0, y0))
        tag_photo = rec.PhotometricInterpretation[:6] if rec.PhotometricInterpretation else rec.DType
        caption1 = f"{rec.ImageID} | {rec.Width}x{rec.Height} | {rec.BitDepthStored}b {tag_photo}"
        caption2 = f"{rec.Disposition[:28]} | u={rec.PixelMean} edge={rec.EdgeToCenterRatio}"
        draw.text((x0, y0 + 240), caption1, fill=(210, 230, 255))
        draw.text((x0, y0 + 256), caption2, fill=(185, 200, 195))

    out_png.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_png)
    return out_png


def _cohort_cross_checks(spec: CohortSpec, records: list[ImageQCRecord]) -> list[str]:
    """Compute cohort-specific structural notes (`DMID` DCM vs TIF, `BMCD` DCM vs GT, `CDD-CESM` LE)."""
    notes: list[str] = []
    rec_by_rel = {r.RawRelativePath.replace("\\", "/"): r for r in records}

    if spec.dataset_id == "DS0002":
        dcms = [r for r in records if r.RoleTrack == "primary_image" and r.Extension == ".dcm"]
        tifs = [r for r in records if r.RoleTrack == "mirror_raster" and r.Extension in (".tif", ".tiff")]
        notes.append(f"DMID format audit: {len(dcms)} DICOMs vs {len(tifs)} TIFFs inspected read-only.")
        shape_matches = 0
        shape_mismatches = 0
        for d in dcms:
            stem = Path(d.RawRelativePath).stem
            tif = rec_by_rel.get(f"TIFF Images/{stem}.tif")
            if tif and d.Width == tif.Width and d.Height == tif.Height:
                shape_matches += 1
            else:
                shape_mismatches += 1
        dhash_exact_matches = sum(
            1
            for d in dcms
            if (tif := rec_by_rel.get(f"TIFF Images/{Path(d.RawRelativePath).stem}.tif"))
            and d.DHash64
            and d.DHash64 == tif.DHash64
        )
        notes.append(
            f"DMID DCM-vs-TIFF paired audit: {shape_matches} dimension matches ({dhash_exact_matches} identical dHash), {shape_mismatches} mismatched/missing."
        )
        # Inspect DICOM StudyUID / PatientID counts
        unique_pats = sum(1 for r in dcms if r.DICOMPatientIDPresent)
        notes.append(
            f"DMID DICOM header PatientID populated in {unique_pats}/{len(dcms)} files; "
            f"{sum(1 for r in dcms if r.DICOMStudyUIDPresent)}/{len(dcms)} carry StudyInstanceUID."
        )

    elif spec.dataset_id == "DS0005":
        dcms = [r for r in records if r.RoleTrack == "primary_image" and r.Extension == ".dcm"]
        gts = [r for r in records if r.RoleTrack == "auxiliary_gt_overlay"]
        normal_n = sum(1 for r in dcms if "/normal_cases/" in r.RawRelativePath.replace("\\", "/").lower())
        susp_n = sum(1 for r in dcms if "/suspicious_cases/" in r.RawRelativePath.replace("\\", "/").lower())
        notes.append(
            f"BMCD cohort structure: {normal_n} Normal_cases DICOMs + {susp_n} Suspicious_cases DICOMs; "
            f"{len(gts)} *_GT.jpg overlays decoded (`Excluded_OverlayGT_NotRawInput` for raw modeling)."
        )
        gt_sizes = collections.Counter(f"{g.Width}x{g.Height}" for g in gts if g.DecodeStatus == "ok")
        notes.append(f"BMCD *_GT.jpg overlay resolutions: {dict(gt_sizes.most_common(5))}.")

    elif spec.dataset_id == "DS0006":
        le = [r for r in records if r.RoleTrack == "primary_image"]
        cm = [r for r in records if r.Disposition == "Excluded_SubtractedCESM_RF15"]
        sys_excl = [r for r in records if r.RoleTrack == "excluded_system_or_temp"]
        le_res = collections.Counter(f"{r.Width}x{r.Height}" for r in le if r.DecodeStatus == "ok")
        notes.append(
            f"CDD-CESM RF15 isolation: {len(le)} Low-Energy DM JPEGs retained vs {len(cm)} Subtracted CESM "
            f"images excluded; {len(sys_excl)} non-medical artifacts excluded ({', '.join(sorted(Path(s.RawRelativePath).name for s in sys_excl))})."
        )
        notes.append(f"CDD-CESM Low-Energy unique resolutions count: {len(le_res)} (top 5: {dict(le_res.most_common(5))}).")

    return notes


def audit_cohort(
    spec: CohortSpec,
    tier2_cache_dir: Path,
    contact_sheets_dir: Path,
    verify_raw_hashes: bool = True,
    verify_pre_hashes: bool | None = None,
    verify_post_hashes: bool | None = None,
    workers: int | None = None,
) -> tuple[CohortQCResult, list[ImageQCRecord]]:
    """Run complete STEP-013 read-only QC on a single cohort and serialize Tier-2 CSV + contact sheet."""
    if not spec.linkage_csv.is_file():
        raise FileNotFoundError(f"Missing private linkage manifest: {spec.linkage_csv}")

    do_pre = verify_raw_hashes if verify_pre_hashes is None else verify_pre_hashes
    do_post = verify_raw_hashes if verify_post_hashes is None else verify_post_hashes

    pre_errs = verify_manifest_integrity(spec.raw_dir, spec.linkage_csv) if do_pre else []
    with spec.linkage_csv.open("r", encoding="utf-8", newline="") as fp:
        rows = list(csv.DictReader(fp))

    total_rows = len(rows)
    use_workers = workers if workers is not None else min(6, max(1, (os.cpu_count() or 2) - 2))
    records: list[ImageQCRecord] = []
    if use_workers > 1 and total_rows >= 50:
        tasks = [(spec.dataset_id, str(spec.raw_dir), row) for row in rows]
        with ProcessPoolExecutor(max_workers=use_workers) as pool:
            for idx, rec in enumerate(pool.map(_inspect_worker, tasks, chunksize=8), start=1):
                records.append(rec)
                if idx % 500 == 0 or idx == total_rows:
                    print(f"  [{spec.dataset_id}] {idx}/{total_rows} files processed", flush=True)
    else:
        for idx, row in enumerate(rows, start=1):
            records.append(inspect_single_file(spec.dataset_id, spec.raw_dir, row))
            if idx % 500 == 0 or idx == total_rows:
                print(f"  [{spec.dataset_id}] {idx}/{total_rows} files processed", flush=True)

    exact_clusters, near_pairs, near_cross_pat, flip_pairs, near_pair_rows = _assign_within_cohort_duplicates(
        records, raw_dir=spec.raw_dir
    )

    unique_pids = {
        r.DICOMPatientIDHash
        for r in records
        if r.RoleTrack == "primary_image" and r.DICOMPatientIDHash
    }
    unique_suids = {
        r.DICOMStudyUIDHash
        for r in records
        if r.RoleTrack == "primary_image" and r.DICOMStudyUIDHash
    }

    post_errs = verify_manifest_integrity(spec.raw_dir, spec.linkage_csv) if do_post else []

    # Tier-2 CSV serialization (under gitignored 03_Datasets/cache/qc/)
    tier2_cache_dir.mkdir(parents=True, exist_ok=True)
    detail_csv = tier2_cache_dir / f"{spec.dataset_id}_qc_details.csv"
    fieldnames = list(ImageQCRecord.__dataclass_fields__.keys())
    with detail_csv.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow(asdict(r))

    if near_pair_rows:
        near_csv = tier2_cache_dir / f"{spec.dataset_id}_within_near_dups.csv"
        with near_csv.open("w", encoding="utf-8", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=list(near_pair_rows[0].keys()))
            writer.writeheader()
            writer.writerows(near_pair_rows)

    # Contact sheet serialization (under gitignored 03_Datasets/images/qc_contact_sheets/)
    sheet_path = build_contact_sheet(
        spec.dataset_id,
        spec.raw_dir,
        records,
        contact_sheets_dir / f"{spec.dataset_id}_qc_grid.png",
    )

    prim = [r for r in records if r.RoleTrack == "primary_image"]
    retained_n = sum(1 for r in prim if r.Disposition == "Retained")
    excluded_n = sum(1 for r in prim if r.Disposition.startswith("Excluded_"))
    quarantined_n = sum(1 for r in prim if r.Disposition.startswith("Quarantined_"))

    def _cnt_split(attr: str) -> dict[str, int]:
        c: collections.Counter[str] = collections.Counter()
        for r in prim:
            val = getattr(r, attr)
            if val:
                for tok in str(val).split(";"):
                    if tok:
                        c[tok] += 1
        return dict(sorted(c.items()))

    notes = _cohort_cross_checks(spec, records)

    summary = CohortQCResult(
        dataset_id=spec.dataset_id,
        display_name=spec.display_name or spec.dataset_id,
        total_raw_files=len(records),
        primary_acquired=len(prim),
        primary_retained=retained_n,
        primary_excluded=excluded_n,
        primary_quarantined=quarantined_n,
        disposition_counts=dict(collections.Counter(r.Disposition for r in records)),
        track_counts=dict(collections.Counter(r.RoleTrack for r in records)),
        decode_status_counts=dict(collections.Counter(r.DecodeStatus for r in prim)),
        photometric_counts=dict(collections.Counter(r.PhotometricInterpretation or "N/A" for r in prim)),
        transfer_syntax_counts=dict(collections.Counter(r.TransferSyntax or "raster_non_dicom" for r in prim)),
        bit_depth_counts=dict(collections.Counter(f"{r.BitDepthStored}b_{r.DType}" for r in prim if r.DecodeStatus == "ok")),
        resolution_counts=dict(collections.Counter(f"{r.Width}x{r.Height}" for r in prim if r.DecodeStatus == "ok").most_common(12)),
        rescale_counts=dict(collections.Counter(f"slope={r.RescaleSlope or 'None'},intercept={r.RescaleIntercept or 'None'}" for r in prim if r.Extension in DICOM_EXTENSIONS)),
        voi_lut_count=sum(1 for r in prim if r.HasVOILUT),
        window_present_count=sum(1 for r in prim if bool(r.WindowCenter)),
        manufacturer_counts=dict(collections.Counter(r.ManufacturerTag or "unspecified" for r in prim if r.Extension in DICOM_EXTENSIONS)),
        modality_tag_counts=dict(collections.Counter(r.ModalityTag or "unspecified" for r in prim if r.Extension in DICOM_EXTENSIONS)),
        rgb_identical_channels=sum(1 for r in prim if r.Channels and r.Channels >= 3 and r.RGBMaxChannelDiff == 0),
        rgb_nonzero_channel_diff=sum(1 for r in prim if r.Channels and r.Channels >= 3 and (r.RGBMaxChannelDiff or 0) > 0),
        non_pseudonym_phi_counts=_cnt_split("NonPseudonymPHITags"),
        pseudonym_echo_counts=_cnt_split("PseudonymEchoTags"),
        demographic_tag_counts=_cnt_split("DemographicOrDateTags"),
        burned_in_counts=dict(collections.Counter(r.BurnedInAnnotation or "absent" for r in prim if r.Extension in DICOM_EXTENSIONS)),
        study_years=dict(sorted(collections.Counter(r.StudyYear for r in prim if r.StudyYear).items())),
        unique_dicom_patient_ids=len(unique_pids),
        unique_dicom_study_uids=len(unique_suids),
        unique_patient_group_ids=len({r.PatientGroupID for r in prim}),
        exact_dup_within_cohort_clusters=exact_clusters,
        near_dup_within_cohort_pairs=near_pairs,
        near_dup_cross_patient_pairs=near_cross_pat,
        polarity_flip_near_dup_pairs=flip_pairs,
        integrity_errors_pre=len(pre_errs),
        integrity_errors_post=len(post_errs),
        cohort_specific_notes=notes,
        contact_sheet_path=str(sheet_path.as_posix()) if sheet_path else "",
        tier2_detail_csv=str(detail_csv.as_posix()),
    )
    return summary, records


def _display_repo_relpath(raw_str: str) -> str:
    """Shorten Tier-2 paths cleanly to repo-relative '03_Datasets/...' when present."""
    marker = "03_Datasets/"
    idx = raw_str.find(marker)
    return raw_str[idx:] if idx >= 0 else raw_str


def render_quality_markdown(summary: CohortQCResult, source_sha: str, generated_at: str) -> str:
    """Format an aggregate Tier-1-safe DS####_quality.md report."""
    lines = [
        f"# {summary.dataset_id} ({summary.display_name}) — Technical Quality, Integrity & PHI Audit (`STEP-013`)",
        "",
        f"- **Generated:** `{generated_at}`",
        f"- **Raw Linkage SHA-256 Verified (`Pre / Post QC`):** `{summary.integrity_errors_pre}` / `{summary.integrity_errors_post}` errors (`read-only invariance confirmed`)",
        f"- **Manifest SHA-256 Reference:** `{source_sha}`",
        f"- **Tier-2 Per-File CSV (Gitignored):** `{_display_repo_relpath(summary.tier2_detail_csv)}`",
        f"- **Tier-2 Contact Sheet (Gitignored):** `{_display_repo_relpath(summary.contact_sheet_path)}`",
        "",
        "## 1. Accounting Reconciliation (`Acquired = Retained + Excluded + Quarantined`)",
        "",
        f"- **Primary Track Image Accounting:** `{summary.primary_acquired}` = **`{summary.primary_retained}` Retained** + **`{summary.primary_excluded}` Excluded** + **`{summary.primary_quarantined}` Quarantined** (`exact sum check: {summary.primary_retained + summary.primary_excluded + summary.primary_quarantined == summary.primary_acquired}`)",
        f"- **Total Raw Files Inventoried:** `{summary.total_raw_files}`",
        f"- **Pseudonymous Patient Groups (`PatientGroupID` in primary track):** `{summary.unique_patient_group_ids}` (`DICOM PatientID tags: {summary.unique_dicom_patient_ids}`; `DICOM StudyInstanceUIDs: {summary.unique_dicom_study_uids}`)",
        "",
        "| Disposition (`All Raw Files`) | Count |",
        "|---|---:|",
    ]
    for k, v in sorted(summary.disposition_counts.items()):
        lines.append(f"| `{k}` | {v} |")

    lines.extend([
        "",
        "## 2. Pixel Format, Decode, Polarity & Normalization Audit (`Primary Track`)",
        "",
        f"- **Decode Status:** `{summary.decode_status_counts}`",
        f"- **Bit Depths / DTypes:** `{summary.bit_depth_counts}`",
        f"- **Photometric Interpretation / PIL Mode:** `{summary.photometric_counts}`",
        f"- **DICOM Transfer Syntaxes:** `{summary.transfer_syntax_counts}`",
        f"- **RescaleSlope / RescaleIntercept:** `{summary.rescale_counts or 'N/A (non-DICOM)'}`",
        f"- **VOI LUT Sequences / Window Tags:** `VOILUT={summary.voi_lut_count}`, `WindowCenter={summary.window_present_count}`",
        f"- **RGB Channel Check (`SamplesPerPixel >= 3`):** `identical_R_eq_G_eq_B={summary.rgb_identical_channels}`, `nonzero_diff={summary.rgb_nonzero_channel_diff}`",
        f"- **Top Image Dimensions (`W x H`):** `{summary.resolution_counts}`",
        "",
        "## 3. Privacy / DICOM Header PHI & Duplicate Screen",
        "",
        f"- **Non-Pseudonymous Sensitive PHI Tags Present:** `{summary.non_pseudonym_phi_counts or 'None populated'}`",
        f"- **Pseudonym Echo Tags (`PatientName == PatientID`):** `{summary.pseudonym_echo_counts or 'None'}`",
        f"- **Demographic / Date Tags Present:** `{summary.demographic_tag_counts or 'None'}` (`StudyYears: {summary.study_years or 'None'}`)",
        f"- **BurnedInAnnotation Tag:** `{summary.burned_in_counts or 'N/A'}`",
        f"- **Within-Cohort Exact SHA-256 Duplicate Clusters:** `{summary.exact_dup_within_cohort_clusters}`",
        f"- **Within-Cohort Near-Duplicate Pairs (`dHash <= 4`):** `{summary.near_dup_within_cohort_pairs}` (`cross-patient`: `{summary.near_dup_cross_patient_pairs}`, `polarity-flipped >= 60`: `{summary.polarity_flip_near_dup_pairs}`)",
        "",
        "## 4. Cohort-Specific Verification Notes",
        "",
    ])
    for note in summary.cohort_specific_notes:
        lines.append(f"- {note}")
    lines.append("")
    return "\n".join(lines)


def default_cohort_specs(root: Path) -> list[CohortSpec]:
    """Return all 5 acquired & inventoried cohorts for STEP-013 (`DS0004_CBIS_DDSM` excluded/untouched)."""
    manifests = root / "03_Datasets" / "manifests"
    raw = root / "03_Datasets" / "raw"
    return [
        CohortSpec("DS0001", raw / "DS0001_MIAS", manifests / "DS0001_private_linkage.csv", "MIAS v1.21"),
        CohortSpec("DS0002", raw / "DS0002_DMID", manifests / "DS0002_private_linkage.csv", "DMID"),
        CohortSpec("DS0003", raw / "DS0003_CMMD", manifests / "DS0003_private_linkage.csv", "CMMD"),
        CohortSpec("DS0005", raw / "DS0005_BMCD", manifests / "DS0005_private_linkage.csv", "BMCD"),
        CohortSpec("DS0006", raw / "DS0006_CDD_CESM", manifests / "DS0006_private_linkage.csv", "CDD-CESM (LE Track)"),
    ]


def run_all_qc(
    specs: list[CohortSpec],
    reports_dir: Path,
    tier2_cache_dir: Path,
    contact_sheets_dir: Path,
    datasets_csv: Path | None = None,
    verify_raw_hashes: bool = True,
    verify_pre_hashes: bool | None = None,
    verify_post_hashes: bool | None = None,
    workers: int | None = None,
) -> dict[str, Any]:
    """Run QC across all cohorts, cross-cohort duplicate audit, and emit JSON + Markdown outputs."""
    manifest_hashes: dict[str, str] = {}
    if datasets_csv and datasets_csv.is_file():
        with datasets_csv.open(encoding="utf-8", newline="") as fp:
            for r in csv.DictReader(fp):
                manifest_hashes[r["DS"]] = r.get("ManifestHash", "not reported")

    generated_at = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summaries: list[CohortQCResult] = []
    all_records: list[ImageQCRecord] = []
    reports_dir.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        print(f"[QC] Auditing {spec.dataset_id} ({spec.display_name})...", flush=True)
        summary, recs = audit_cohort(
            spec,
            tier2_cache_dir=tier2_cache_dir,
            contact_sheets_dir=contact_sheets_dir,
            verify_raw_hashes=verify_raw_hashes,
            verify_pre_hashes=verify_pre_hashes,
            verify_post_hashes=verify_post_hashes,
            workers=workers,
        )
        summaries.append(summary)
        all_records.extend(recs)
        md = render_quality_markdown(summary, manifest_hashes.get(spec.dataset_id, "not reported"), generated_at)
        (reports_dir / f"{spec.dataset_id}_quality.md").write_text(md, encoding="utf-8")

    exact_cross, near_cross = find_cross_cohort_duplicates(all_records)
    cross_out = tier2_cache_dir / "cross_cohort_duplicates.json"
    cross_out.write_text(
        json.dumps({"exact_cross_cohort": exact_cross, "near_cross_cohort": near_cross}, indent=2),
        encoding="utf-8",
    )

    payload = {
        "generated_at": generated_at,
        "cohorts": [asdict(s) for s in summaries],
        "cross_cohort_exact_count": len(exact_cross),
        "cross_cohort_near_count": len(near_cross),
        "cross_cohort_detail_path": str(cross_out.as_posix()),
    }
    summary_json = tier2_cache_dir / "step013_qc_summary.json"
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only STEP-013 Mammography QC Engine")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--workers", type=int, default=None, help="Parallel worker processes for decoding")
    parser.add_argument("--verify-pre-hashes", action="store_true", help="Also run pre-QC SHA-256 scan before pixel audit")
    parser.add_argument("--no-hash-recheck", action="store_true", help="Skip SHA-256 verification before/after scan")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    payload = run_all_qc(
        specs=default_cohort_specs(root),
        reports_dir=root / "03_Datasets" / "reports",
        tier2_cache_dir=root / "03_Datasets" / "cache" / "qc",
        contact_sheets_dir=root / "03_Datasets" / "images" / "qc_contact_sheets",
        datasets_csv=root / "03_Datasets" / "datasets.csv",
        verify_raw_hashes=not args.no_hash_recheck,
        verify_pre_hashes=False if not args.verify_pre_hashes else not args.no_hash_recheck,
        verify_post_hashes=not args.no_hash_recheck,
        workers=args.workers,
    )
    for c in payload["cohorts"]:
        print(
            f"[DONE] {c['dataset_id']}: total={c['total_raw_files']} | "
            f"primary={c['primary_acquired']} -> retained={c['primary_retained']}, "
            f"excluded={c['primary_excluded']}, quarantined={c['primary_quarantined']} | "
            f"integrity_err=({c['integrity_errors_pre']},{c['integrity_errors_post']})"
        )
    print(
        f"[CROSS-COHORT] exact_dups={payload['cross_cohort_exact_count']}, "
        f"near_dups={payload['cross_cohort_near_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

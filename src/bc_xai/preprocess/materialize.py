"""STEP-021: Training-only preprocessing fitting and immutable REL#### materialization."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import csv
from dataclasses import asdict, dataclass
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import cv2
import numpy as np
from PIL import Image, ImageDraw
import pydicom

from bc_xai.data.inventory import verify_manifest_integrity
from bc_xai.labels.freeze import COHORT_TO_LBL_ID, sha256_bytes, sha256_file
from bc_xai.preprocess.transforms import (
    PreprocessConfig,
    PreprocessOutput,
    TrainFitState,
    compute_safe_foreground_crop,
    load_preprocess_config,
    preprocess_sample_pair,
    standardize_intensity_and_polarity,
    validate_config_safety,
)

RELEASE_MANIFEST_COLUMNS: list[str] = [
    "ReleaseID",
    "PreprocessingID",
    "SplitID",
    "DatasetID",
    "LabelReleaseID",
    "ImageID",
    "PatientGroupID",
    "ComponentID",
    "primary_partition",
    "dev_fold_5",
    "BinaryTarget",
    "LabelClass",
    "LabelProvenanceTier",
    "SubTrackA_BiopsyEligible",
    "SubTrackB_ScreeningEligible",
    "LesionTrack_BenignVsMalignant",
    "LocalizationEligible",
    "PhotometricInterpretation",
    "BitsStored",
    "orig_h",
    "orig_w",
    "crop_x0",
    "crop_y0",
    "crop_x1",
    "crop_y1",
    "resized_h",
    "resized_w",
    "pad_top",
    "pad_bottom",
    "pad_left",
    "pad_right",
    "target_size",
    "scale_x",
    "scale_y",
    "ForegroundCoveragePct",
    "ImageMin01",
    "ImageMax01",
    "ImageMean01",
    "ImageStd01",
    "OrigMaskPixels",
    "PostCropMaskPixels",
    "ProcessedMaskPixels",
    "ImageRelPath",
    "ImageSHA256",
    "MaskRelPath",
    "MaskSHA256",
]


@dataclass(frozen=True)
class SampleInputRecord:
    """Joined split and label metadata identifying one modeling-eligible scan."""

    split_id: str
    dataset_id: str
    label_release_id: str
    image_id: str
    patient_group_id: str
    component_id: str
    primary_partition: str
    dev_fold_5: str
    binary_target: str
    label_class: str
    label_provenance_tier: str
    subtrack_a: str
    subtrack_b: str
    lesion_track: str
    localization_eligible: bool
    raw_path: Path
    mask_zip_path: Path | None
    mask_archive_member: str
    mask_expected_sha256: str


@dataclass(frozen=True)
class RawLoadedImage:
    """Decoded raw mammogram array and source pixel-encoding metadata."""

    array: np.ndarray
    photometric_interpretation: str
    bits_stored: int | None
    rescale_slope: float
    rescale_intercept: float


@dataclass(frozen=True)
class FitSummary:
    """Serialized training-only intensity fit state and quantile diagnostics."""

    state: TrainFitState
    fit_state_npz_path: Path
    fit_state_npz_hash: str
    fit_state_json_path: Path
    fit_state_json_hash: str
    stats_payload: dict[str, object]


@dataclass(frozen=True)
class MaterializeSummary:
    """Complete release materialization metrics and integrity verification outputs."""

    release_id: str
    preprocessing_id: str
    split_id: str
    config_hash: str
    code_revision: str
    total_images: int
    total_patients_or_components: int
    roi_mask_count: int
    partition_counts: dict[str, int]
    cohort_counts: dict[str, int]
    bit_depth_counts: dict[str, int]
    fit_summary: FitSummary
    manifest_path: Path
    manifest_hash: str
    summary_json_path: Path
    qc_plate_paths: list[Path]
    raw_integrity_verified: bool
    raw_manifest_hashes_before: dict[str, str]
    raw_manifest_hashes_after: dict[str, str]


def _resolve_raw_dir_map(datasets_csv: Path) -> dict[str, Path]:
    with datasets_csv.open("r", encoding="utf-8", newline="") as handle:
        return {row["DS"]: Path(row["RestrictedLocation"]) for row in csv.DictReader(handle)}


def _load_label_lookup(
    label_exports_dir: Path,
) -> dict[tuple[str, str], dict[str, str]]:
    lookup: dict[tuple[str, str], dict[str, str]] = {}
    for dataset_id, lbl_id in sorted(COHORT_TO_LBL_ID.items()):
        manifest_path = label_exports_dir / lbl_id / f"{lbl_id}_manifest.csv"
        if not manifest_path.is_file():
            continue
        with manifest_path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                lookup[(row["DatasetID"], row["ImageID"])] = row
    return lookup


def load_eligible_samples(
    split_manifest: Path,
    datasets_csv: Path,
    label_exports_dir: Path,
    masks_dir: Path,
) -> list[SampleInputRecord]:
    """Load all modeling-eligible samples from SPLIT#### joined to LBL#### paths."""
    raw_dirs = _resolve_raw_dir_map(datasets_csv)
    label_lookup = _load_label_lookup(label_exports_dir)
    records: list[SampleInputRecord] = []

    with split_manifest.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["eligible_for_modeling"] != "True" or row["primary_partition"] == "excluded":
                continue

            ds_id = row["DatasetID"]
            img_id = row["ImageID"]
            lbl_row = label_lookup.get((ds_id, img_id))
            if lbl_row is None:
                raise KeyError(f"Missing label manifest entry for ({ds_id}, {img_id})")
            if lbl_row["DispositionQC"] != "Retained":
                raise ValueError(
                    f"Eligible split row ({ds_id}, {img_id}) has DispositionQC={lbl_row['DispositionQC']}"
                )

            loc_split = row["LocalizationEligible"] == "True"
            loc_lbl = lbl_row["LocalizationEligible"] == "True"
            if loc_split != loc_lbl:
                raise ValueError(
                    f"LocalizationEligible mismatch on ({ds_id}, {img_id}): "
                    f"split={loc_split} vs label={loc_lbl}"
                )

            if ds_id not in raw_dirs:
                raise KeyError(f"DatasetID {ds_id} missing from {datasets_csv}")
            raw_path = raw_dirs[ds_id] / lbl_row["RawRelativePath"]
            if not raw_path.is_file():
                raise FileNotFoundError(f"Raw image missing for ({ds_id}, {img_id}): {raw_path}")

            lbl_id = row["LabelReleaseID"]
            mask_zip: Path | None = None
            mask_member = ""
            mask_sha = ""
            if loc_split:
                if lbl_row["MaskStatus"] != "ok_nonempty":
                    raise ValueError(
                        f"LocalizationEligible scan ({ds_id}, {img_id}) has MaskStatus={lbl_row['MaskStatus']}"
                    )
                mask_zip = masks_dir / f"{lbl_id}_masks.zip"
                mask_member = lbl_row["MaskArchiveMember"]
                mask_sha = lbl_row["MaskSHA256"]
                if not mask_zip.is_file():
                    raise FileNotFoundError(f"Missing frozen mask zip archive: {mask_zip}")

            records.append(
                SampleInputRecord(
                    split_id=row["SplitID"],
                    dataset_id=ds_id,
                    label_release_id=lbl_id,
                    image_id=img_id,
                    patient_group_id=row["PatientGroupID"],
                    component_id=row["ComponentID"],
                    primary_partition=row["primary_partition"],
                    dev_fold_5=row["dev_fold_5"],
                    binary_target=row["BinaryTarget"],
                    label_class=row["LabelClass"],
                    label_provenance_tier=row["LabelProvenanceTier"],
                    subtrack_a=row["SubTrackA_BiopsyEligible"],
                    subtrack_b=row["SubTrackB_ScreeningEligible"],
                    lesion_track=row["LesionTrack_BenignVsMalignant"],
                    localization_eligible=loc_split,
                    raw_path=raw_path,
                    mask_zip_path=mask_zip,
                    mask_archive_member=mask_member,
                    mask_expected_sha256=mask_sha,
                )
            )

    records.sort(key=lambda r: (r.dataset_id, r.image_id))
    return records


def load_raw_image(raw_path: Path) -> RawLoadedImage:
    """Decode DICOM or raster (PGM/JPEG/PNG) mammogram with pixel metadata."""
    if raw_path.suffix.lower() == ".dcm":
        ds = pydicom.dcmread(raw_path)
        arr = ds.pixel_array
        pi = str(getattr(ds, "PhotometricInterpretation", "MONOCHROME2")).strip()
        raw_bits = getattr(ds, "BitsStored", None)
        bits_stored = int(raw_bits) if raw_bits is not None else None
        raw_slope = getattr(ds, "RescaleSlope", None)
        raw_intercept = getattr(ds, "RescaleIntercept", None)
        slope = float(raw_slope) if raw_slope is not None else 1.0
        intercept = float(raw_intercept) if raw_intercept is not None else 0.0
        return RawLoadedImage(
            array=arr,
            photometric_interpretation=pi,
            bits_stored=bits_stored,
            rescale_slope=slope,
            rescale_intercept=intercept,
        )

    with Image.open(raw_path) as im:
        arr = np.asarray(im)
    bits = 16 if arr.dtype == np.uint16 else 8
    return RawLoadedImage(
        array=arr,
        photometric_interpretation="MONOCHROME2",
        bits_stored=bits,
        rescale_slope=1.0,
        rescale_intercept=0.0,
    )


def load_verified_mask_from_bytes(
    raw_bytes: bytes,
    expected_sha256: str,
    expected_shape: tuple[int, int],
) -> np.ndarray:
    """Verify frozen mask digest, validate binary {0, 1} domain, and match shape."""
    if expected_sha256:
        actual_sha = sha256_bytes(raw_bytes)
        if actual_sha != expected_sha256:
            raise ValueError(
                f"Mask archive member SHA-256 mismatch: expected {expected_sha256}, got {actual_sha}"
            )

    with Image.open(io.BytesIO(raw_bytes)) as im:
        mask = np.asarray(im)
    if mask.ndim != 2:
        raise ValueError(f"Expected 2D binary mask, got shape {mask.shape}")
    if mask.shape != expected_shape:
        raise ValueError(
            f"Mask shape mismatch: expected {expected_shape}, got {mask.shape}"
        )
    uniq = np.unique(mask)
    if not np.isin(uniq, [0, 1]).all():
        raise ValueError(f"Mask contains non-binary values outside {{0, 1}}: {uniq.tolist()}")
    if int(mask.sum()) <= 0:
        raise ValueError("LocalizationEligible mask has zero foreground pixels")
    return mask.astype(np.uint8, copy=False)


def _write_deterministic_npz(path: Path, arrays: dict[str, np.ndarray]) -> None:
    """Write numpy archive with fixed zip timestamps for bit-reproducible SHA-256."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as zf:
        for name in sorted(arrays):
            buf = io.BytesIO()
            np.save(buf, arrays[name], allow_pickle=False)
            info = zipfile.ZipInfo(f"{name}.npy", date_time=(2026, 1, 1, 0, 0, 0))
            zf.writestr(info, buf.getvalue())


def _init_worker() -> None:
    """Restrict OpenCV internal threads inside multiprocessing workers to prevent contention."""
    cv2.setNumThreads(1)


def _fit_one_worker(
    task: tuple[SampleInputRecord, PreprocessConfig],
) -> tuple[np.ndarray, float, float, int]:
    rec, cfg = task
    if rec.primary_partition != "train":
        raise AssertionError(f"Leakage block: attempted train fit on {rec.primary_partition}")
    loaded = load_raw_image(rec.raw_path)
    out = preprocess_sample_pair(
        loaded.array,
        cfg,
        photometric_interpretation=loaded.photometric_interpretation,
        bits_stored=loaded.bits_stored,
        rescale_slope=loaded.rescale_slope,
        rescale_intercept=loaded.rescale_intercept,
        roi_mask=None,
        fit_state=None,
    )
    img01 = np.clip(out.image_01, 0.0, 1.0)
    if not np.isfinite(img01).all():
        raise ValueError(f"Non-finite pixel detected during train fit: {rec.dataset_id}/{rec.image_id}")
    q_u16 = np.round(img01 * 65535.0).astype(np.uint16)
    local_hist = np.bincount(q_u16.ravel(), minlength=65536)
    fg = img01[img01 > 0.0]
    return (
        local_hist,
        float(fg.sum(dtype=np.float64)),
        float(np.square(fg, dtype=np.float64).sum()),
        int(fg.size),
    )


def fit_training_state(
    records: list[SampleInputRecord],
    cfg: PreprocessConfig,
    fit_state_npz_path: Path,
    fit_state_json_path: Path,
    workers: int = 6,
) -> FitSummary:
    """Fit intensity statistics strictly on primary_partition == 'train' scans."""
    validate_config_safety(cfg)
    if cfg.fit_partition_required != "train":
        raise ValueError(f"fit_partition_required must be 'train', got {cfg.fit_partition_required!r}")

    train_records = [rec for rec in records if rec.primary_partition == cfg.fit_partition_required]
    if not train_records:
        raise ValueError("Zero training records found for FitPartition='train'")
    if any(rec.primary_partition != "train" for rec in train_records):
        raise AssertionError("Non-train partition detected inside training fit pool")

    split_id = train_records[0].split_id
    hist_bins = 65536
    hist_accum = np.zeros(hist_bins, dtype=np.int64)
    fg_sum = 0.0
    fg_sq = 0.0
    fg_count = 0

    tasks = [(rec, cfg) for rec in train_records]
    if workers > 1 and len(tasks) > 4:
        with ProcessPoolExecutor(max_workers=workers, initializer=_init_worker) as pool:
            for idx, (h_local, f_s, f_sq, f_n) in enumerate(pool.map(_fit_one_worker, tasks, chunksize=16), start=1):
                hist_accum += h_local
                fg_sum += f_s
                fg_sq += f_sq
                fg_count += f_n
                if idx % 1000 == 0 or idx == len(tasks):
                    print(f"[{cfg.preprocessing_id}] train fit {idx}/{len(tasks)}", flush=True)
    else:
        for t in tasks:
            h_local, f_s, f_sq, f_n = _fit_one_worker(t)
            hist_accum += h_local
            fg_sum += f_s
            fg_sq += f_sq
            fg_count += f_n

    total_pixels = int(hist_accum.sum())
    bin_vals = np.arange(hist_bins, dtype=np.float64) / 65535.0
    global_mean = float(np.dot(hist_accum, bin_vals) / total_pixels)
    global_var = float(np.dot(hist_accum, np.square(bin_vals - global_mean)) / total_pixels)
    global_std = float(np.sqrt(max(global_var, 1e-12)))

    cdf = np.cumsum(hist_accum) / total_pixels
    quantiles = {
        "q01": float(np.searchsorted(cdf, 0.01) / 65535.0),
        "q05": float(np.searchsorted(cdf, 0.05) / 65535.0),
        "q50": float(np.searchsorted(cdf, 0.50) / 65535.0),
        "q95": float(np.searchsorted(cdf, 0.95) / 65535.0),
        "q99": float(np.searchsorted(cdf, 0.99) / 65535.0),
    }

    fg_mean = float(fg_sum / fg_count) if fg_count > 0 else 0.0
    fg_var = float(fg_sq / fg_count - fg_mean * fg_mean) if fg_count > 0 else 0.0
    fg_std = float(np.sqrt(max(fg_var, 1e-12)))

    state = TrainFitState(
        fit_partition="train",
        mean=round(global_mean, 8),
        std=round(global_std, 8),
        sample_count=len(train_records),
        split_id=split_id,
    )

    _write_deterministic_npz(
        fit_state_npz_path,
        {
            "mean": np.array([state.mean], dtype=np.float64),
            "std": np.array([state.std], dtype=np.float64),
            "fg_mean": np.array([fg_mean], dtype=np.float64),
            "fg_std": np.array([fg_std], dtype=np.float64),
            "sample_count": np.array([state.sample_count], dtype=np.int64),
            "quantiles": np.array(
                [quantiles["q01"], quantiles["q05"], quantiles["q50"], quantiles["q95"], quantiles["q99"]],
                dtype=np.float64,
            ),
            "histogram_u16": hist_accum,
        },
    )
    npz_hash = sha256_file(fit_state_npz_path)

    payload: dict[str, object] = {
        "preprocessing_id": cfg.preprocessing_id,
        "preprocessing_name": cfg.name,
        "split_id": split_id,
        "fit_partition": state.fit_partition,
        "sample_count": state.sample_count,
        "train_cohort_ids": sorted({r.dataset_id for r in train_records}),
        "excluded_partitions_from_fit": sorted(
            {r.primary_partition for r in records if r.primary_partition != "train"}
        ),
        "global_mean_01": round(global_mean, 8),
        "global_std_01": round(global_std, 8),
        "foreground_mean_01": round(fg_mean, 8),
        "foreground_std_01": round(fg_std, 8),
        "quantiles_01": {k: round(v, 6) for k, v in quantiles.items()},
        "normalization_policy": cfg.normalization_policy,
        "model_norm_mean_rgb": list(cfg.norm_mean),
        "model_norm_std_rgb": list(cfg.norm_std),
        "fit_state_npz_sha256": npz_hash,
    }
    fit_state_json_path.parent.mkdir(parents=True, exist_ok=True)
    fit_state_json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    json_hash = sha256_file(fit_state_json_path)

    return FitSummary(
        state=state,
        fit_state_npz_path=fit_state_npz_path,
        fit_state_npz_hash=npz_hash,
        fit_state_json_path=fit_state_json_path,
        fit_state_json_hash=json_hash,
        stats_payload=payload,
    )


def _snapshot_dataset_manifest_hashes(manifests_dir: Path, dataset_ids: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for ds_id in sorted(dataset_ids):
        img_manifest = manifests_dir / f"{ds_id}_images.csv"
        if img_manifest.is_file():
            out[ds_id] = sha256_file(img_manifest)
    return out


def _verify_one_cohort(task: tuple[str, Path, Path]) -> list[str]:
    ds_id, raw_dir, linkage_csv = task
    errs = verify_manifest_integrity(raw_dir, linkage_csv)
    return [f"[{ds_id}] {e}" for e in errs[:5]]


def _verify_all_raw_integrity(
    datasets_csv: Path,
    manifests_dir: Path,
    dataset_ids: list[str],
) -> None:
    raw_dirs = _resolve_raw_dir_map(datasets_csv)
    cohort_tasks: list[tuple[str, Path, Path]] = []
    for ds_id in sorted(dataset_ids):
        linkage_csv = manifests_dir / f"{ds_id}_private_linkage.csv"
        if not linkage_csv.is_file():
            raise FileNotFoundError(f"Missing linkage table for {ds_id}: {linkage_csv}")
        cohort_tasks.append((ds_id, raw_dirs[ds_id], linkage_csv))
    with ThreadPoolExecutor(max_workers=min(5, len(cohort_tasks))) as pool:
        for errs in pool.map(_verify_one_cohort, cohort_tasks):
            if errs:
                raise ValueError(f"Raw integrity check failed: {errs}")


def _write_png_lossless(path: Path, arr: np.ndarray) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok, encoded = cv2.imencode(".png", arr, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    if not ok:
        raise RuntimeError(f"Failed to encode PNG: {path}")
    data = encoded.tobytes()
    path.write_bytes(data)
    return sha256_bytes(data)


def _read_mask_bytes_index(records: list[SampleInputRecord]) -> dict[tuple[str, str], bytes]:
    """Preload compressed mask archive entries once per cohort archive cleanly."""
    zips_needed: dict[Path, list[tuple[tuple[str, str], str]]] = {}
    for rec in records:
        if rec.localization_eligible and rec.mask_zip_path is not None:
            zips_needed.setdefault(rec.mask_zip_path, []).append(
                ((rec.dataset_id, rec.image_id), rec.mask_archive_member)
            )
    loaded: dict[tuple[str, str], bytes] = {}
    for zpath, items in sorted(zips_needed.items()):
        with zipfile.ZipFile(zpath, "r") as zf:
            for key, member in items:
                loaded[key] = zf.read(member)
    return loaded


def _materialize_one_worker(
    task: tuple[SampleInputRecord, PreprocessConfig, TrainFitState, str, Path, bytes | None],
) -> tuple[list[str], str]:
    rec, cfg, fit_state, release_id, release_dir, raw_mask_bytes = task
    loaded = load_raw_image(rec.raw_path)
    orig_h, orig_w = loaded.array.shape[:2]

    orig_mask: np.ndarray | None = None
    orig_mask_px = 0
    post_crop_px = 0
    if rec.localization_eligible:
        assert raw_mask_bytes is not None
        orig_mask = load_verified_mask_from_bytes(
            raw_mask_bytes,
            rec.mask_expected_sha256,
            (orig_h, orig_w),
        )
        orig_mask_px = int(orig_mask.sum())

        # Recompute crop explicitly to record post-crop mask pixel invariant alongside transform.
        img_std = standardize_intensity_and_polarity(
            loaded.array,
            photometric_interpretation=loaded.photometric_interpretation,
            bits_stored=loaded.bits_stored,
            rescale_slope=loaded.rescale_slope,
            rescale_intercept=loaded.rescale_intercept,
            monochrome1_invert=cfg.monochrome1_invert,
            apply_dicom_rescale=cfg.apply_dicom_rescale,
        )
        if cfg.crop_enabled:
            cx0, cy0, cx1, cy1 = compute_safe_foreground_crop(
                img_std,
                roi_mask=orig_mask,
                air_threshold=cfg.air_threshold,
                min_component_area_frac=cfg.min_component_area_frac,
                safety_margin_px=cfg.safety_margin_px,
                safety_margin_frac=cfg.safety_margin_frac,
                skip_if_area_coverage_ge=cfg.skip_if_area_coverage_ge,
                enforce_zero_roi_clipping=cfg.enforce_zero_roi_clipping,
            )
            post_crop_px = int(orig_mask[cy0:cy1, cx0:cx1].sum())
        else:
            post_crop_px = orig_mask_px
        if post_crop_px != orig_mask_px:
            raise ValueError(
                f"ROI lesion clipping detected on {rec.dataset_id}/{rec.image_id}: "
                f"orig={orig_mask_px}, post_crop={post_crop_px}"
            )

    out: PreprocessOutput = preprocess_sample_pair(
        loaded.array,
        cfg,
        photometric_interpretation=loaded.photometric_interpretation,
        bits_stored=loaded.bits_stored,
        rescale_slope=loaded.rescale_slope,
        rescale_intercept=loaded.rescale_intercept,
        roi_mask=orig_mask,
        fit_state=fit_state,
    )
    img01 = np.clip(out.image_01, 0.0, 1.0)
    if not np.isfinite(img01).all():
        raise ValueError(f"Non-finite output image on {rec.dataset_id}/{rec.image_id}")
    img_max = float(img01.max())
    img_min = float(img01.min())
    img_mean = float(img01.mean())
    img_std_val = float(img01.std())
    if img_max <= 0.0 or img_std_val <= 0.0:
        raise ValueError(f"All-black/degenerate preprocessed image: {rec.dataset_id}/{rec.image_id}")

    u16_img = np.round(img01 * 65535.0).astype(np.uint16)
    img_rel = f"images/{rec.dataset_id}/{rec.image_id}.png"
    img_sha = _write_png_lossless(release_dir / img_rel, u16_img)

    mask_rel = ""
    mask_sha = ""
    proc_mask_px = 0
    if out.roi_mask is not None:
        mask_u8 = out.roi_mask.astype(np.uint8, copy=False)
        proc_mask_px = int(mask_u8.sum())
        if proc_mask_px <= 0:
            raise ValueError(
                f"Localized lesion mask vanished after {cfg.target_size}x{cfg.target_size} resize on "
                f"{rec.dataset_id}/{rec.image_id}"
            )
        mask_rel = f"masks/{rec.dataset_id}/{rec.image_id}.png"
        mask_sha = _write_png_lossless(release_dir / mask_rel, mask_u8)

    meta = out.spatial_meta
    fg_pct = round(100.0 * float((img01 > 0.0).mean()), 4)
    bits_key = f"{loaded.bits_stored or (16 if loaded.array.dtype == np.uint16 else 8)}-bit/{loaded.photometric_interpretation}"

    row = [
        release_id,
        cfg.preprocessing_id,
        rec.split_id,
        rec.dataset_id,
        rec.label_release_id,
        rec.image_id,
        rec.patient_group_id,
        rec.component_id,
        rec.primary_partition,
        rec.dev_fold_5,
        rec.binary_target,
        rec.label_class,
        rec.label_provenance_tier,
        rec.subtrack_a,
        rec.subtrack_b,
        rec.lesion_track,
        str(rec.localization_eligible),
        loaded.photometric_interpretation,
        str(loaded.bits_stored if loaded.bits_stored is not None else ""),
        str(meta.orig_h),
        str(meta.orig_w),
        str(meta.crop_x0),
        str(meta.crop_y0),
        str(meta.crop_x1),
        str(meta.crop_y1),
        str(meta.resized_h),
        str(meta.resized_w),
        str(meta.pad_top),
        str(meta.pad_bottom),
        str(meta.pad_left),
        str(meta.pad_right),
        str(meta.target_size),
        f"{meta.scale_x:.8f}",
        f"{meta.scale_y:.8f}",
        f"{fg_pct:.4f}",
        f"{img_min:.6f}",
        f"{img_max:.6f}",
        f"{img_mean:.6f}",
        f"{img_std_val:.6f}",
        str(orig_mask_px),
        str(post_crop_px),
        str(proc_mask_px),
        img_rel,
        img_sha,
        mask_rel,
        mask_sha,
    ]
    return row, bits_key


def _to_u8_preview(arr_01: np.ndarray, size: tuple[int, int]) -> Image.Image:
    u8 = np.round(np.clip(arr_01, 0.0, 1.0) * 255.0).astype(np.uint8)
    im = Image.fromarray(u8, mode="L").convert("RGB")
    return im.resize(size, resample=Image.Resampling.BILINEAR)


def _overlay_mask_contour(rgb_im: Image.Image, mask: np.ndarray | None) -> Image.Image:
    if mask is None or int(mask.sum()) == 0:
        return rgb_im
    arr = np.asarray(rgb_im).copy()
    mask_u8 = (mask > 0).astype(np.uint8)
    if mask_u8.shape != arr.shape[:2]:
        mask_u8 = cv2.resize(mask_u8, (arr.shape[1], arr.shape[0]), interpolation=cv2.INTER_NEAREST)
    kernel = np.ones((3, 3), dtype=np.uint8)
    edge = cv2.dilate(mask_u8, kernel, iterations=2) - cv2.erode(mask_u8, kernel, iterations=1)
    edge = (edge > 0) | (mask_u8 > 0)
    # Bright green tint for interior and vivid lime/yellow border for high visibility.
    arr[mask_u8 > 0, 1] = np.clip(arr[mask_u8 > 0, 1].astype(np.int32) + 70, 0, 255).astype(np.uint8)
    border = cv2.dilate(mask_u8, kernel, iterations=2) > mask_u8
    arr[border] = [0, 255, 128]
    return Image.fromarray(arr, mode="RGB")


def generate_qc_plates(
    records: list[SampleInputRecord],
    manifest_rows: list[list[str]],
    cfg: PreprocessConfig,
    release_id: str,
    release_dir: Path,
) -> list[Path]:
    """Generate stratified raw vs preprocessed + co-transformed mask contact sheets."""
    rec_map = {(r.dataset_id, r.image_id): r for r in records}
    col_idx = {name: i for i, name in enumerate(RELEASE_MANIFEST_COLUMNS)}

    # Group rows deterministically by dataset_id so every cohort gets inspected.
    by_ds: dict[str, list[list[str]]] = {}
    for row in manifest_rows:
        by_ds.setdefault(row[col_idx["DatasetID"]], []).append(row)

    selected: list[list[str]] = []
    for ds_id in sorted(by_ds):
        ds_rows = by_ds[ds_id]
        # Prefer diverse classes: localized malignant, localized benign, and normal control.
        picks: list[list[str]] = []
        for pred in (
            lambda r: r[col_idx["LocalizationEligible"]] == "True" and r[col_idx["BinaryTarget"]] == "1",
            lambda r: r[col_idx["LocalizationEligible"]] == "True" and r[col_idx["BinaryTarget"]] == "0",
            lambda r: r[col_idx["LabelClass"]] == "Normal",
            lambda r: r[col_idx["BinaryTarget"]] == "1",
        ):
            match = next((r for r in ds_rows if pred(r) and r not in picks), None)
            if match is not None:
                picks.append(match)
            if len(picks) == 3:
                break
        for r in ds_rows:
            if len(picks) >= 3:
                break
            if r not in picks:
                picks.append(r)
        selected.extend(picks)

    qc_dir = release_dir / "qc_overlays"
    qc_dir.mkdir(parents=True, exist_ok=True)
    plate_paths: list[Path] = []
    rows_per_plate = 5
    tile_w, tile_h = 256, 256
    pad = 12
    header_h = 34
    label_h = 22

    for plate_idx in range(0, len(selected), rows_per_plate):
        chunk = selected[plate_idx : plate_idx + rows_per_plate]
        canvas_w = pad * 4 + tile_w * 3
        canvas_h = header_h + len(chunk) * (tile_h + label_h + pad) + pad
        canvas = Image.new("RGB", (canvas_w, canvas_h), (24, 24, 28))
        draw = ImageDraw.Draw(canvas)
        draw.text(
            (pad, 10),
            f"{release_id} ({cfg.preprocessing_id}: {cfg.name}) — Col1: Raw Standardized | Col2: Processed 512x512 | Col3: Co-Transformed Mask",
            fill=(235, 240, 245),
        )

        for r_i, row in enumerate(chunk):
            ds_id = row[col_idx["DatasetID"]]
            img_id = row[col_idx["ImageID"]]
            rec = rec_map[(ds_id, img_id)]
            loaded = load_raw_image(rec.raw_path)
            raw_std = standardize_intensity_and_polarity(
                loaded.array,
                photometric_interpretation=loaded.photometric_interpretation,
                bits_stored=loaded.bits_stored,
                rescale_slope=loaded.rescale_slope,
                rescale_intercept=loaded.rescale_intercept,
                monochrome1_invert=cfg.monochrome1_invert,
                apply_dicom_rescale=cfg.apply_dicom_rescale,
            )

            proc_path = release_dir / row[col_idx["ImageRelPath"]]
            proc_u16 = cv2.imread(str(proc_path), cv2.IMREAD_UNCHANGED)
            proc_01 = proc_u16.astype(np.float32) / 65535.0

            proc_mask: np.ndarray | None = None
            mask_rel = row[col_idx["MaskRelPath"]]
            if mask_rel:
                proc_mask = cv2.imread(str(release_dir / mask_rel), cv2.IMREAD_UNCHANGED)

            # Fit aspect ratio inside tile box cleanly for raw thumbnail, exact square for 512x512.
            raw_thumb = _to_u8_preview(raw_std, (tile_w, tile_h))
            proc_thumb = _to_u8_preview(proc_01, (tile_w, tile_h))
            overlay_thumb = _overlay_mask_contour(proc_thumb.copy(), proc_mask)

            y0 = header_h + r_i * (tile_h + label_h + pad)
            caption = (
                f"{ds_id} | {img_id} | {row[col_idx['primary_partition']]} | "
                f"{row[col_idx['LabelClass']]} | orig={row[col_idx['orig_h']]}x{row[col_idx['orig_w']]} | "
                f"crop=({row[col_idx['crop_x0']]},{row[col_idx['crop_y0']]}..{row[col_idx['crop_x1']]},{row[col_idx['crop_y1']]}) | "
                f"mask_px={row[col_idx['ProcessedMaskPixels']]}"
            )
            draw.text((pad, y0), caption, fill=(210, 225, 240))
            y_img = y0 + label_h
            canvas.paste(raw_thumb, (pad, y_img))
            canvas.paste(proc_thumb, (pad * 2 + tile_w, y_img))
            canvas.paste(overlay_thumb, (pad * 3 + tile_w * 2, y_img))

        plate_path = qc_dir / f"qc_plate_{plate_idx // rows_per_plate + 1:02d}.png"
        canvas.save(plate_path, format="PNG")
        plate_paths.append(plate_path)

    return plate_paths


def _current_git_revision(repo_root: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short=12", "HEAD"],
            cwd=str(repo_root),
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out or "unknown"
    except Exception:
        return "unknown"


def materialize_release(
    config_path: Path,
    release_id: str,
    split_manifest: Path = Path("03_Datasets/splits/SPLIT0001/manifest.csv"),
    datasets_csv: Path = Path("03_Datasets/datasets.csv"),
    label_exports_dir: Path = Path("04_Labels_XAI_Governance/exports"),
    masks_dir: Path = Path("04_Labels_XAI_Governance/restricted_masks"),
    manifests_dir: Path = Path("03_Datasets/manifests"),
    output_root: Path = Path("05_Preprocessing/processed"),
    fitted_states_dir: Path = Path("05_Preprocessing/fitted_states"),
    verify_raw_integrity: bool = True,
    workers: int = 6,
    generate_qc: bool = True,
) -> MaterializeSummary:
    """Fit train-only state and materialize immutable REL#### dataset & manifest."""
    cfg = load_preprocess_config(config_path)
    config_hash = sha256_file(config_path)
    records = load_eligible_samples(split_manifest, datasets_csv, label_exports_dir, masks_dir)
    if not records:
        raise ValueError(f"Zero modeling-eligible records loaded from {split_manifest}")

    dataset_ids = sorted({rec.dataset_id for rec in records})
    raw_hashes_before = _snapshot_dataset_manifest_hashes(manifests_dir, dataset_ids)
    if verify_raw_integrity:
        _verify_all_raw_integrity(datasets_csv, manifests_dir, dataset_ids)

    release_dir = output_root / release_id
    release_dir.mkdir(parents=True, exist_ok=True)
    fit_summary = fit_training_state(
        records=records,
        cfg=cfg,
        fit_state_npz_path=fitted_states_dir / f"{cfg.preprocessing_id}_train_state.npz",
        fit_state_json_path=release_dir / "train_fit_state.json",
        workers=workers,
    )

    mask_bytes_map = _read_mask_bytes_index(records)
    manifest_rows: list[list[str]] = []
    bit_depth_counts: dict[str, int] = {}

    mat_tasks = [
        (
            rec,
            cfg,
            fit_summary.state,
            release_id,
            release_dir,
            mask_bytes_map.get((rec.dataset_id, rec.image_id)),
        )
        for rec in records
    ]
    if workers > 1 and len(mat_tasks) > 4:
        with ProcessPoolExecutor(max_workers=workers, initializer=_init_worker) as pool:
            for idx, (row, b_key) in enumerate(pool.map(_materialize_one_worker, mat_tasks, chunksize=16), start=1):
                manifest_rows.append(row)
                bit_depth_counts[b_key] = bit_depth_counts.get(b_key, 0) + 1
                if idx % 1000 == 0 or idx == len(mat_tasks):
                    print(f"[{release_id}] materialized {idx}/{len(mat_tasks)}", flush=True)
    else:
        for t in mat_tasks:
            row, b_key = _materialize_one_worker(t)
            manifest_rows.append(row)
            bit_depth_counts[b_key] = bit_depth_counts.get(b_key, 0) + 1

    # Records were sorted deterministically by (dataset_id, image_id), preserve exact order.
    col_idx = {name: i for i, name in enumerate(RELEASE_MANIFEST_COLUMNS)}
    manifest_rows.sort(key=lambda r: (r[col_idx["DatasetID"]], r[col_idx["ImageID"]]))

    manifest_path = release_dir / "manifest.csv"
    with manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(RELEASE_MANIFEST_COLUMNS)
        writer.writerows(manifest_rows)
    manifest_hash = sha256_file(manifest_path)

    qc_plates: list[Path] = []
    if generate_qc:
        qc_plates = generate_qc_plates(
            records=records,
            manifest_rows=manifest_rows,
            cfg=cfg,
            release_id=release_id,
            release_dir=release_dir,
        )

    raw_hashes_after = _snapshot_dataset_manifest_hashes(manifests_dir, dataset_ids)
    if raw_hashes_before != raw_hashes_after:
        raise RuntimeError(
            f"Raw dataset manifest hash mutated during materialization: "
            f"before={raw_hashes_before} after={raw_hashes_after}"
        )
    if verify_raw_integrity:
        _verify_all_raw_integrity(datasets_csv, manifests_dir, dataset_ids)

    partition_counts: dict[str, int] = {}
    cohort_counts: dict[str, int] = {}
    unique_components: set[str] = set()
    roi_mask_count = 0
    for row in manifest_rows:
        p_name = row[col_idx["primary_partition"]]
        c_name = row[col_idx["DatasetID"]]
        partition_counts[p_name] = partition_counts.get(p_name, 0) + 1
        cohort_counts[c_name] = cohort_counts.get(c_name, 0) + 1
        unique_components.add(row[col_idx["ComponentID"]])
        if row[col_idx["MaskRelPath"]]:
            roi_mask_count += 1

    code_rev = _current_git_revision(Path.cwd())
    summary_payload = {
        "release_id": release_id,
        "preprocessing_id": cfg.preprocessing_id,
        "preprocessing_name": cfg.name,
        "role": cfg.role,
        "split_id": records[0].split_id,
        "config_path": config_path.as_posix(),
        "config_hash": config_hash,
        "code_revision": code_rev,
        "total_images": len(manifest_rows),
        "total_components": len(unique_components),
        "roi_mask_count": roi_mask_count,
        "partition_counts": dict(sorted(partition_counts.items())),
        "cohort_counts": dict(sorted(cohort_counts.items())),
        "bit_depth_counts": dict(sorted(bit_depth_counts.items())),
        "fit_partition": fit_summary.state.fit_partition,
        "fit_sample_count": fit_summary.state.sample_count,
        "fit_state_npz_path": fit_summary.fit_state_npz_path.as_posix(),
        "fit_state_npz_hash": fit_summary.fit_state_npz_hash,
        "fit_state_json_path": fit_summary.fit_state_json_path.as_posix(),
        "fit_state_json_hash": fit_summary.fit_state_json_hash,
        "train_intensity_stats": fit_summary.stats_payload,
        "manifest_path": manifest_path.as_posix(),
        "manifest_hash": manifest_hash,
        "raw_integrity_verified": verify_raw_integrity,
        "raw_manifest_hashes_before": raw_hashes_before,
        "raw_manifest_hashes_after": raw_hashes_after,
        "qc_plates": [p.as_posix() for p in qc_plates],
        "config": asdict(cfg),
    }
    summary_json_path = release_dir / "summary.json"
    summary_json_path.write_text(json.dumps(summary_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return MaterializeSummary(
        release_id=release_id,
        preprocessing_id=cfg.preprocessing_id,
        split_id=records[0].split_id,
        config_hash=config_hash,
        code_revision=code_rev,
        total_images=len(manifest_rows),
        total_patients_or_components=len(unique_components),
        roi_mask_count=roi_mask_count,
        partition_counts=partition_counts,
        cohort_counts=cohort_counts,
        bit_depth_counts=bit_depth_counts,
        fit_summary=fit_summary,
        manifest_path=manifest_path,
        manifest_hash=manifest_hash,
        summary_json_path=summary_json_path,
        qc_plate_paths=qc_plates,
        raw_integrity_verified=verify_raw_integrity,
        raw_manifest_hashes_before=raw_hashes_before,
        raw_manifest_hashes_after=raw_hashes_after,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for STEP-021 release materialization."""
    parser = argparse.ArgumentParser(description="STEP-021 train-only preprocessing fit & REL#### materialization")
    parser.add_argument("--config", type=Path, required=True, help="Path to PP#### YAML config")
    parser.add_argument("--release-id", required=True, help="Target REL#### identifier (e.g. REL0001)")
    parser.add_argument("--split-manifest", type=Path, default=Path("03_Datasets/splits/SPLIT0001/manifest.csv"))
    parser.add_argument("--datasets-csv", type=Path, default=Path("03_Datasets/datasets.csv"))
    parser.add_argument("--label-exports-dir", type=Path, default=Path("04_Labels_XAI_Governance/exports"))
    parser.add_argument("--masks-dir", type=Path, default=Path("04_Labels_XAI_Governance/restricted_masks"))
    parser.add_argument("--manifests-dir", type=Path, default=Path("03_Datasets/manifests"))
    parser.add_argument("--output-root", type=Path, default=Path("05_Preprocessing/processed"))
    parser.add_argument("--fitted-states-dir", type=Path, default=Path("05_Preprocessing/fitted_states"))
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--skip-raw-integrity", action="store_true")
    parser.add_argument("--skip-qc", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint reporting release materialization and cryptographic hashes."""
    args = parse_args(argv)
    try:
        summary = materialize_release(
            config_path=args.config,
            release_id=args.release_id,
            split_manifest=args.split_manifest,
            datasets_csv=args.datasets_csv,
            label_exports_dir=args.label_exports_dir,
            masks_dir=args.masks_dir,
            manifests_dir=args.manifests_dir,
            output_root=args.output_root,
            fitted_states_dir=args.fitted_states_dir,
            verify_raw_integrity=not args.skip_raw_integrity,
            workers=args.workers,
            generate_qc=not args.skip_qc,
        )
    except Exception as exc:
        print(f"MATERIALIZE FAILED: {exc}", file=sys.stderr)
        return 1

    print(
        f"MATERIALIZE PASSED ({summary.release_id} / {summary.preprocessing_id}): "
        f"images={summary.total_images}, components={summary.total_patients_or_components}, "
        f"masks={summary.roi_mask_count}, fit_partition={summary.fit_summary.state.fit_partition}, "
        f"fit_n={summary.fit_summary.state.sample_count}, fit_npz_sha256={summary.fit_summary.fit_state_npz_hash}, "
        f"manifest_sha256={summary.manifest_hash}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

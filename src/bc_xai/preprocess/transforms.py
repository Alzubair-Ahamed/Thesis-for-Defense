"""Deterministic STEP-019 Mammography Preprocessing & Post-Hoc ROI Co-Transform Engine.

Implements `05_Preprocessing/specs/pipeline.md` (`UD12` / `PP0001` baseline vs `PP0002` CLAHE):
- Dynamic DICOM/raster bit-depth normalization (`8-bit`, `12-bit`, `16-bit`) without `/255` hardcoding
- `MONOCHROME1` -> `MONOCHROME2` polarity alignment
- Lesion-safe foreground bounding guaranteeing zero clipped pixels on verified ROI masks
- Aspect-ratio-preserving resize (`INTER_AREA` / `INTER_LINEAR`) + symmetric zero-pad paired
  `1:1` with `INTER_NEAREST` binary `{0, 1}` ROI-mask co-transform & exact inverse spatial mapping
- Controlled `PP0002` CLAHE ablation toggle (`uint16` dynamic precision)
- Strict `FitPartition == "train"` guard preventing any validation/test statistics leakage.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import yaml


@dataclass(frozen=True)
class PreprocessConfig:
    """Validated configuration matching `pp_baseline.yaml` or `pp_clahe_ablation.yaml`."""

    preprocessing_id: str
    name: str
    role: str
    monochrome1_invert: bool = True
    apply_dicom_rescale: bool = True
    air_threshold: float = 0.02
    min_component_area_frac: float = 0.005
    safety_margin_px: int = 16
    safety_margin_frac: float = 0.02
    skip_if_area_coverage_ge: float = 0.92
    crop_enabled: bool = True
    enforce_zero_roi_clipping: bool = True
    clahe_enabled: bool = False
    clahe_clip_limit: float = 2.0
    clahe_tile_grid_size: tuple[int, int] = (8, 8)
    target_size: int = 512
    preserve_aspect_ratio: bool = True
    pad_value: float = 0.0
    normalization_policy: str = "imagenet_rgb"
    norm_mean: tuple[float, float, float] = (0.485, 0.456, 0.406)
    norm_std: tuple[float, float, float] = (0.229, 0.224, 0.225)
    fit_partition_required: str = "train"
    horizontal_flip_prob: float = 0.5
    vertical_flip_prob: float = 0.0
    apply_during_rel_materialization: bool = False


@dataclass(frozen=True)
class TrainFitState:
    """Training-only fitted normalization parameters (created strictly post-G07)."""

    fit_partition: str
    mean: float
    std: float
    sample_count: int
    split_id: str = ""


@dataclass(frozen=True)
class SpatialTransformMeta:
    """Exact invertible mapping between native `(orig_h, orig_w)` and `(target_size, target_size)`."""

    orig_h: int
    orig_w: int
    crop_x0: int
    crop_y0: int
    crop_x1: int
    crop_y1: int
    resized_h: int
    resized_w: int
    pad_top: int
    pad_bottom: int
    pad_left: int
    pad_right: int
    target_size: int
    scale_x: float
    scale_y: float

    def project_point_to_canvas(self, x_orig: float, y_orig: float) -> tuple[float, float]:
        """Map a native-image `(x, y)` coordinate into `(target_size, target_size)` canvas space."""
        xc = (x_orig - self.crop_x0) * self.scale_x + self.pad_left
        yc = (y_orig - self.crop_y0) * self.scale_y + self.pad_top
        return xc, yc


@dataclass
class PreprocessOutput:
    """Outputs of deterministic single-sample mammography preprocessing."""

    image_01: np.ndarray            # float32 `(H_t, W_t)` in `[0.0, 1.0]`
    model_tensor: np.ndarray        # float32 `(3, H_t, W_t)` normalized for CNN input
    roi_mask: np.ndarray | None     # uint8 `(H_t, W_t)` strictly `{0, 1}` if supplied
    spatial_meta: SpatialTransformMeta


def validate_config_safety(cfg: PreprocessConfig) -> None:
    """Fail loudly if configuration violates radiographic or anti-leakage constraints."""
    if cfg.target_size <= 0:
        raise ValueError(f"target_size must be positive, got {cfg.target_size}")
    if cfg.vertical_flip_prob != 0.0:
        raise ValueError(
            f"Vertical flip violates mammographic anatomical orientation policy (got {cfg.vertical_flip_prob})"
        )
    if cfg.apply_during_rel_materialization:
        raise ValueError("Stochastic augmentation must NEVER be materialized into immutable REL#### releases.")
    if cfg.normalization_policy not in {"imagenet_rgb", "train_zscore"}:
        raise ValueError(f"Unsupported normalization policy: {cfg.normalization_policy}")


def load_preprocess_config(yaml_path: Path) -> PreprocessConfig:
    """Parse and validate `pp_baseline.yaml` / `pp_clahe_ablation.yaml`."""
    raw: dict[str, Any] = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    fg = raw.get("foreground_crop", {})
    inten = raw.get("intensity", {})
    clahe = raw.get("clahe", {})
    geom = raw.get("geometry", {})
    norm = raw.get("normalization", {})
    aug = raw.get("training_only_augmentations", {})

    grid = tuple(int(v) for v in clahe.get("tile_grid_size", [8, 8]))
    mean = tuple(float(v) for v in norm.get("mean", [0.485, 0.456, 0.406]))
    std = tuple(float(v) for v in norm.get("std", [0.229, 0.224, 0.225]))

    cfg = PreprocessConfig(
        preprocessing_id=str(raw["preprocessing_id"]),
        name=str(raw["name"]),
        role=str(raw["role"]),
        monochrome1_invert=bool(inten.get("monochrome1_invert", True)),
        apply_dicom_rescale=bool(inten.get("apply_dicom_rescale", True)),
        air_threshold=float(fg.get("air_threshold", 0.02)),
        min_component_area_frac=float(fg.get("min_component_area_frac", 0.005)),
        safety_margin_px=int(fg.get("safety_margin_px", 16)),
        safety_margin_frac=float(fg.get("safety_margin_frac", 0.02)),
        skip_if_area_coverage_ge=float(fg.get("skip_if_area_coverage_ge", 0.92)),
        crop_enabled=bool(fg.get("enabled", True)),
        enforce_zero_roi_clipping=bool(fg.get("enforce_zero_roi_clipping", True)),
        clahe_enabled=bool(clahe.get("enabled", False)),
        clahe_clip_limit=float(clahe.get("clip_limit", 2.0)),
        clahe_tile_grid_size=(grid[0], grid[1]),
        target_size=int(geom.get("target_size", 512)),
        preserve_aspect_ratio=bool(geom.get("preserve_aspect_ratio", True)),
        pad_value=float(geom.get("pad_value", 0.0)),
        normalization_policy=str(norm.get("policy", "imagenet_rgb")),
        norm_mean=(mean[0], mean[1], mean[2]),
        norm_std=(std[0], std[1], std[2]),
        fit_partition_required=str(norm.get("fit_partition_required", "train")),
        horizontal_flip_prob=float(aug.get("horizontal_flip_prob", 0.5)),
        vertical_flip_prob=float(aug.get("vertical_flip_prob", 0.0)),
        apply_during_rel_materialization=bool(aug.get("apply_during_rel_materialization", False)),
    )
    validate_config_safety(cfg)
    return cfg


def _collapse_to_luminance(arr: np.ndarray) -> np.ndarray:
    """Convert `(H, W)` or identical-channel `(H, W, 3)` raster into 2D array."""
    if arr.ndim == 2:
        return arr
    if arr.ndim == 3 and arr.shape[2] >= 3:
        c0 = arr[..., 0]
        if np.array_equal(c0, arr[..., 1]) and np.array_equal(c0, arr[..., 2]):
            return c0
        # Weighted luminance fallback if minor JPEG subsampling differences exist
        return (
            0.2989 * arr[..., 0].astype(np.float32)
            + 0.5870 * arr[..., 1].astype(np.float32)
            + 0.1140 * arr[..., 2].astype(np.float32)
        )
    raise ValueError(f"Unsupported mammogram array shape: {arr.shape}")


def _resolve_bit_max(arr: np.ndarray, bits_stored: int | None) -> float:
    """Resolve dynamic pixel ceiling cleanly from DICOM `BitsStored` or native dtype."""
    if bits_stored is not None and bits_stored > 0:
        return float((1 << int(bits_stored)) - 1)
    if arr.dtype == np.uint8:
        return 255.0
    if arr.dtype == np.uint16:
        max_px = int(arr.max()) if arr.size else 0
        return 4095.0 if max_px <= 4095 else 65535.0
    max_val = float(arr.max()) if arr.size else 1.0
    return max(max_val, 1.0)


def standardize_intensity_and_polarity(
    raw_arr: np.ndarray,
    photometric_interpretation: str = "MONOCHROME2",
    bits_stored: int | None = None,
    rescale_slope: float = 1.0,
    rescale_intercept: float = 0.0,
    monochrome1_invert: bool = True,
    apply_dicom_rescale: bool = True,
) -> np.ndarray:
    """Normalize `8/12/16-bit` mammogram array to `MONOCHROME2` `float32` in `[0.0, 1.0]`."""
    gray = _collapse_to_luminance(raw_arr)
    max_val = _resolve_bit_max(raw_arr if raw_arr.ndim == 2 else gray, bits_stored)

    arr_f = gray.astype(np.float32)
    if apply_dicom_rescale and (rescale_slope != 1.0 or rescale_intercept != 0.0):
        arr_f = arr_f * float(rescale_slope) + float(rescale_intercept)
        denom = abs(float(rescale_slope)) * max_val
        low = float(rescale_intercept)
        arr_f = (arr_f - low) / max(denom, 1e-6)
    else:
        arr_f = arr_f / max(max_val, 1e-6)

    arr_f = np.clip(arr_f, 0.0, 1.0)
    if monochrome1_invert and photometric_interpretation.strip().upper() == "MONOCHROME1":
        arr_f = 1.0 - arr_f
    if not np.isfinite(arr_f).all():
        raise ValueError("Non-finite NaN/Inf values detected after intensity standardization.")
    return arr_f.astype(np.float32)


def compute_safe_foreground_crop(
    img_f32: np.ndarray,
    roi_mask: np.ndarray | None = None,
    air_threshold: float = 0.02,
    min_component_area_frac: float = 0.005,
    safety_margin_px: int = 16,
    safety_margin_frac: float = 0.02,
    skip_if_area_coverage_ge: float = 0.92,
    enforce_zero_roi_clipping: bool = True,
) -> tuple[int, int, int, int]:
    """Compute `(x0, y0, x1, y1)` breast bbox guaranteeing zero ROI lesion clipping."""
    h, w = int(img_f32.shape[0]), int(img_f32.shape[1])
    fg_u8 = (img_f32 > air_threshold).astype(np.uint8)
    fg_area = int(fg_u8.sum())
    total_area = max(h * w, 1)

    if fg_area == 0 or (fg_area / total_area) >= skip_if_area_coverage_ge:
        return 0, 0, w, h

    n_labels, _, stats, _ = cv2.connectedComponentsWithStats(fg_u8, connectivity=8)
    min_px = max(1, int(round(min_component_area_frac * total_area)))
    kept = [i for i in range(1, n_labels) if int(stats[i, cv2.CC_STAT_AREA]) >= min_px]
    if not kept and n_labels > 1:
        kept = [max(range(1, n_labels), key=lambda i: int(stats[i, cv2.CC_STAT_AREA]))]
    if not kept:
        return 0, 0, w, h

    x0 = min(int(stats[i, cv2.CC_STAT_LEFT]) for i in kept)
    y0 = min(int(stats[i, cv2.CC_STAT_TOP]) for i in kept)
    x1 = max(int(stats[i, cv2.CC_STAT_LEFT] + stats[i, cv2.CC_STAT_WIDTH]) for i in kept)
    y1 = max(int(stats[i, cv2.CC_STAT_TOP] + stats[i, cv2.CC_STAT_HEIGHT]) for i in kept)

    pad_x = max(int(safety_margin_px), int(round(w * safety_margin_frac)))
    pad_y = max(int(safety_margin_px), int(round(h * safety_margin_frac)))
    x0 = max(0, x0 - pad_x)
    y0 = max(0, y0 - pad_y)
    x1 = min(w, x1 + pad_x)
    y1 = min(h, y1 + pad_y)

    # Mandatory ROI lesion safety expansion: never discard verified lesion pixels!
    if roi_mask is not None and np.any(roi_mask > 0):
        ys, xs = np.where(roi_mask > 0)
        rx0, rx1 = int(xs.min()), int(xs.max()) + 1
        ry0, ry1 = int(ys.min()), int(ys.max()) + 1
        if rx0 < x0 or ry0 < y0 or rx1 > x1 or ry1 > y1:
            if not enforce_zero_roi_clipping:
                raise ValueError("Foreground crop clips verified ROI lesion pixels while enforcement disabled.")
            x0 = max(0, min(x0, rx0 - pad_x))
            y0 = max(0, min(y0, ry0 - pad_y))
            x1 = min(w, max(x1, rx1 + pad_x))
            y1 = min(h, max(y1, ry1 + pad_y))

    return x0, y0, x1, y1


def apply_clahe_u16(
    img_f32: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: tuple[int, int] = (8, 8),
) -> np.ndarray:
    """Apply deterministic `uint16`-precision CLAHE for controlled ablation (`PP0002`)."""
    u16 = np.round(np.clip(img_f32, 0.0, 1.0) * 65535.0).astype(np.uint16)
    clahe = cv2.createCLAHE(clipLimit=float(clip_limit), tileGridSize=tile_grid_size)
    eq = clahe.apply(u16)
    return (eq.astype(np.float32) / 65535.0).clip(0.0, 1.0)


def resize_and_pad_pair(
    img_f32: np.ndarray,
    target_size: int = 512,
    crop_box: tuple[int, int, int, int] | None = None,
    roi_mask: np.ndarray | None = None,
    preserve_aspect_ratio: bool = True,
    pad_value: float = 0.0,
) -> tuple[np.ndarray, np.ndarray | None, SpatialTransformMeta]:
    """Co-transform image (`AREA/LINEAR`) and optional binary ROI mask (`AREA>0 downsample / NEAREST upsample`) 1:1."""
    orig_h, orig_w = int(img_f32.shape[0]), int(img_f32.shape[1])
    x0, y0, x1, y1 = crop_box if crop_box is not None else (0, 0, orig_w, orig_h)
    cropped = img_f32[y0:y1, x0:x1]
    ch, cw = int(cropped.shape[0]), int(cropped.shape[1])
    if ch <= 0 or cw <= 0:
        raise ValueError(f"Empty crop box {(x0, y0, x1, y1)} on image {(orig_h, orig_w)}")

    if preserve_aspect_ratio:
        scale = float(target_size) / max(ch, cw)
        new_h = max(1, min(target_size, int(round(ch * scale))))
        new_w = max(1, min(target_size, int(round(cw * scale))))
    else:
        new_h, new_w = target_size, target_size

    interp = cv2.INTER_AREA if (new_h < ch or new_w < cw) else cv2.INTER_LINEAR
    resized = cv2.resize(cropped, (new_w, new_h), interpolation=interp).astype(np.float32)

    pad_h = target_size - new_h
    pad_w = target_size - new_w
    pad_top = pad_h // 2
    pad_bottom = pad_h - pad_top
    pad_left = pad_w // 2
    pad_right = pad_w - pad_left

    canvas = cv2.copyMakeBorder(
        resized,
        pad_top,
        pad_bottom,
        pad_left,
        pad_right,
        borderType=cv2.BORDER_CONSTANT,
        value=float(pad_value),
    ).astype(np.float32)

    out_mask: np.ndarray | None = None
    if roi_mask is not None:
        if roi_mask.shape[:2] != (orig_h, orig_w):
            raise ValueError(f"ROI mask shape {roi_mask.shape[:2]} != image {(orig_h, orig_w)}")
        orig_pos = int((roi_mask > 0).sum())
        m_crop = (roi_mask[y0:y1, x0:x1] > 0).astype(np.uint8)
        cropped_pos = int(m_crop.sum())
        if cropped_pos != orig_pos:
            raise ValueError(
                f"ROI mask pixels clipped by crop {(x0, y0, x1, y1)}: orig={orig_pos}, after_crop={cropped_pos}"
            )
        if new_h < ch or new_w < cw:
            # Area-fraction downsample (> 0) preserves small micro-calcifications and point markers under >=8:1 shrink.
            m_area = cv2.resize(m_crop.astype(np.float32), (new_w, new_h), interpolation=cv2.INTER_AREA)
            m_res = (m_area > 0.0).astype(np.uint8)
        else:
            m_res = cv2.resize(m_crop, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
        m_pad = cv2.copyMakeBorder(
            m_res,
            pad_top,
            pad_bottom,
            pad_left,
            pad_right,
            borderType=cv2.BORDER_CONSTANT,
            value=0,
        )
        out_mask = (m_pad > 0).astype(np.uint8)
        if orig_pos > 0 and int(out_mask.sum()) == 0:
            raise ValueError("Non-empty ROI lesion collapsed to 0 pixels after resizing.")

    meta = SpatialTransformMeta(
        orig_h=orig_h,
        orig_w=orig_w,
        crop_x0=x0,
        crop_y0=y0,
        crop_x1=x1,
        crop_y1=y1,
        resized_h=new_h,
        resized_w=new_w,
        pad_top=pad_top,
        pad_bottom=pad_bottom,
        pad_left=pad_left,
        pad_right=pad_right,
        target_size=target_size,
        scale_x=float(new_w) / cw,
        scale_y=float(new_h) / ch,
    )
    return canvas, out_mask, meta


def inverse_map_canvas_to_orig(
    canvas_arr: np.ndarray,
    meta: SpatialTransformMeta,
    is_binary_mask: bool = False,
) -> np.ndarray:
    """Project a `(target_size, target_size)` mask or heatmap back onto native `(orig_h, orig_w)`."""
    unpadded = canvas_arr[
        meta.pad_top : meta.pad_top + meta.resized_h,
        meta.pad_left : meta.pad_left + meta.resized_w,
    ]
    ch = meta.crop_y1 - meta.crop_y0
    cw = meta.crop_x1 - meta.crop_x0
    interp = cv2.INTER_NEAREST if is_binary_mask else cv2.INTER_LINEAR
    restored_crop = cv2.resize(unpadded.astype(np.float32), (cw, ch), interpolation=interp)

    full = np.zeros((meta.orig_h, meta.orig_w), dtype=np.uint8 if is_binary_mask else np.float32)
    if is_binary_mask:
        full[meta.crop_y0 : meta.crop_y1, meta.crop_x0 : meta.crop_x1] = (restored_crop > 0.5).astype(np.uint8)
    else:
        full[meta.crop_y0 : meta.crop_y1, meta.crop_x0 : meta.crop_x1] = restored_crop.astype(np.float32)
    return full


def normalize_for_model(
    img_01: np.ndarray,
    cfg: PreprocessConfig,
    fit_state: TrainFitState | None = None,
) -> np.ndarray:
    """Convert `[0.0, 1.0]` `(H, W)` image into `(3, H, W)` float32 tensor cleanly."""
    rgb3 = np.stack([img_01, img_01, img_01], axis=0).astype(np.float32)
    if cfg.normalization_policy == "imagenet_rgb":
        mean = np.asarray(cfg.norm_mean, dtype=np.float32)[:, None, None]
        std = np.asarray(cfg.norm_std, dtype=np.float32)[:, None, None]
        return ((rgb3 - mean) / std).astype(np.float32)
    if cfg.normalization_policy == "train_zscore":
        if fit_state is None or fit_state.fit_partition != "train":
            raise RuntimeError(
                "Leakage guard triggered: `train_zscore` requires a TrainFitState with fit_partition == 'train'."
            )
        return ((rgb3 - float(fit_state.mean)) / max(float(fit_state.std), 1e-6)).astype(np.float32)
    raise ValueError(f"Unsupported normalization policy: {cfg.normalization_policy}")


def preprocess_sample_pair(
    raw_arr: np.ndarray,
    cfg: PreprocessConfig,
    photometric_interpretation: str = "MONOCHROME2",
    bits_stored: int | None = None,
    rescale_slope: float = 1.0,
    rescale_intercept: float = 0.0,
    roi_mask: np.ndarray | None = None,
    fit_state: TrainFitState | None = None,
) -> PreprocessOutput:
    """Run complete deterministic `STEP-019` preprocessing + optional ROI co-transform."""
    validate_config_safety(cfg)
    img_01 = standardize_intensity_and_polarity(
        raw_arr=raw_arr,
        photometric_interpretation=photometric_interpretation,
        bits_stored=bits_stored,
        rescale_slope=rescale_slope,
        rescale_intercept=rescale_intercept,
        monochrome1_invert=cfg.monochrome1_invert,
        apply_dicom_rescale=cfg.apply_dicom_rescale,
    )
    if cfg.crop_enabled:
        crop_box = compute_safe_foreground_crop(
            img_01,
            roi_mask=roi_mask,
            air_threshold=cfg.air_threshold,
            min_component_area_frac=cfg.min_component_area_frac,
            safety_margin_px=cfg.safety_margin_px,
            safety_margin_frac=cfg.safety_margin_frac,
            skip_if_area_coverage_ge=cfg.skip_if_area_coverage_ge,
            enforce_zero_roi_clipping=cfg.enforce_zero_roi_clipping,
        )
    else:
        crop_box = (0, 0, int(img_01.shape[1]), int(img_01.shape[0]))

    # Slice before CLAHE so air margins do not skew local histogram tiles
    x0, y0, x1, y1 = crop_box
    if cfg.clahe_enabled:
        cropped_eq = apply_clahe_u16(
            img_01[y0:y1, x0:x1],
            clip_limit=cfg.clahe_clip_limit,
            tile_grid_size=cfg.clahe_tile_grid_size,
        )
        img_for_resize = img_01.copy()
        img_for_resize[y0:y1, x0:x1] = cropped_eq
    else:
        img_for_resize = img_01

    canvas_01, out_mask, meta = resize_and_pad_pair(
        img_for_resize,
        target_size=cfg.target_size,
        crop_box=crop_box,
        roi_mask=roi_mask,
        preserve_aspect_ratio=cfg.preserve_aspect_ratio,
        pad_value=cfg.pad_value,
    )
    tensor = normalize_for_model(canvas_01, cfg=cfg, fit_state=fit_state)
    return PreprocessOutput(
        image_01=canvas_01,
        model_tensor=tensor,
        roi_mask=out_mask,
        spatial_meta=meta,
    )

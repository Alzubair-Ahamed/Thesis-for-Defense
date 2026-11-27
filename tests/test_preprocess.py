"""Synthetic unit tests for STEP-019 mammography preprocessing & ROI co-transforms."""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from bc_xai.preprocess.transforms import (  # noqa: E402
    TrainFitState,
    inverse_map_canvas_to_orig,
    load_preprocess_config,
    preprocess_sample_pair,
    standardize_intensity_and_polarity,
    validate_config_safety,
)


def test_yaml_configs_isolate_clahe_sole_ablation_factor() -> None:
    """Baseline PP0001 and CLAHE PP0002 YAML configs must differ solely on CLAHE role."""
    base = load_preprocess_config(ROOT / "05_Preprocessing" / "configs" / "pp_baseline.yaml")
    clahe = load_preprocess_config(ROOT / "05_Preprocessing" / "configs" / "pp_clahe_ablation.yaml")

    assert base.preprocessing_id == "PP0001" and base.clahe_enabled is False
    assert clahe.preprocessing_id == "PP0002" and clahe.clahe_enabled is True
    assert base.target_size == 512 and clahe.target_size == 512
    assert base.vertical_flip_prob == 0.0 and clahe.vertical_flip_prob == 0.0

    # Reject prohibited vertical flip or pre-materialized augmentation configs
    bad_vflip = dataclasses.replace(base, vertical_flip_prob=0.5)
    with pytest.raises(ValueError, match="Vertical flip"):
        validate_config_safety(bad_vflip)
    bad_mat_aug = dataclasses.replace(base, apply_during_rel_materialization=True)
    with pytest.raises(ValueError, match="never|NEVER"):
        validate_config_safety(bad_mat_aug)


def test_dynamic_bit_depth_polarity_and_rgb_collapse() -> None:
    """Must normalize 12-bit BMCD, 16-bit CMMD, 8-bit RGB, and MONOCHROME1 accurately."""
    bmcd_12 = np.array([[0, 2047], [4095, 1024]], dtype=np.uint16)
    s12 = standardize_intensity_and_polarity(bmcd_12, bits_stored=12)
    assert np.isclose(s12[1, 0], 1.0, atol=1e-4)
    assert np.isclose(s12[0, 1], 2047.0 / 4095.0, atol=1e-4)

    # MONOCHROME1 polarity inversion on 12-bit
    m1 = standardize_intensity_and_polarity(bmcd_12, photometric_interpretation="MONOCHROME1", bits_stored=12)
    assert np.isclose(m1[0, 0], 1.0, atol=1e-4) and np.isclose(m1[1, 0], 0.0, atol=1e-4)

    # 16-bit CMMD max 65535
    cmmd_16 = np.array([[0, 32768], [65535, 16384]], dtype=np.uint16)
    s16 = standardize_intensity_and_polarity(cmmd_16, bits_stored=16)
    assert np.isclose(s16[1, 0], 1.0, atol=1e-4) and np.isclose(s16[0, 1], 32768.0 / 65535.0, atol=1e-3)

    # 8-bit identical RGB (CDD-CESM / DMID)
    rgb = np.stack([np.full((8, 8), 128, dtype=np.uint8)] * 3, axis=-1)
    srgb = standardize_intensity_and_polarity(rgb)
    assert srgb.shape == (8, 8) and np.isclose(srgb[0, 0], 128.0 / 255.0, atol=1e-4)


def test_safe_foreground_crop_zero_roi_clipping_and_inverse_mapping() -> None:
    """Aspect-preserving resize + crop must preserve 100% peripheral ROI lesions and inverse map 1:1."""
    cfg = load_preprocess_config(ROOT / "05_Preprocessing" / "configs" / "pp_baseline.yaml")

    # 12-bit synthetic mammogram (1024 tall x 800 wide) with wide black air margins
    img = np.zeros((1024, 800), dtype=np.uint16)
    # Main breast parenchyma block in center-left [150:900, 100:550]
    img[150:900, 100:550] = 2200
    # Dense bright lesion centered at (y=220, x=580) extending beyond parenchyma threshold border
    img[200:240, 560:600] = 3500
    roi = np.zeros((1024, 800), dtype=np.uint8)
    roi[200:240, 555:605] = 1
    # Simulate an extreme peripheral lesion focus inside low-contrast chest-wall skin edge
    roi[110:120, 75:85] = 1

    out = preprocess_sample_pair(img, cfg=cfg, bits_stored=12, roi_mask=roi)
    assert out.image_01.shape == (512, 512)
    assert out.model_tensor.shape == (3, 512, 512)
    assert out.roi_mask is not None and out.roi_mask.shape == (512, 512)
    assert set(np.unique(out.roi_mask).tolist()).issubset({0, 1})
    assert int(out.roi_mask.sum()) > 0

    # Verify both the main lesion center AND peripheral chest-wall focus map positively to canvas
    cx1, cy1 = out.spatial_meta.project_point_to_canvas(580.0, 220.0)
    cx2, cy2 = out.spatial_meta.project_point_to_canvas(80.0, 115.0)
    assert out.roi_mask[int(round(cy1)), int(round(cx1))] == 1
    assert out.roi_mask[int(round(cy2)), int(round(cx2))] == 1

    # Inverse mapping must recover lesion locations inside original native (1024, 800) coordinates
    restored = inverse_map_canvas_to_orig(out.roi_mask, out.spatial_meta, is_binary_mask=True)
    assert restored.shape == (1024, 800)
    assert restored[220, 580] == 1 and restored[115, 80] == 1


def test_clahe_ablation_and_train_only_zscore_guard() -> None:
    """CLAHE must alter contrast deterministically and train_zscore must block val/unfitted states."""
    base = load_preprocess_config(ROOT / "05_Preprocessing" / "configs" / "pp_baseline.yaml")
    clahe = load_preprocess_config(ROOT / "05_Preprocessing" / "configs" / "pp_clahe_ablation.yaml")

    rng = np.random.default_rng(seed=20261128)
    syn = np.zeros((256, 256), dtype=np.uint16)
    syn[40:216, 40:216] = rng.integers(800, 1800, size=(176, 176), dtype=np.uint16)

    out_b = preprocess_sample_pair(syn, cfg=base, bits_stored=12)
    out_c1 = preprocess_sample_pair(syn, cfg=clahe, bits_stored=12)
    out_c2 = preprocess_sample_pair(syn, cfg=clahe, bits_stored=12)
    assert np.array_equal(out_c1.image_01, out_c2.image_01)
    assert float(np.abs(out_b.image_01 - out_c1.image_01).mean()) > 0.01

    z_cfg = dataclasses.replace(base, normalization_policy="train_zscore")
    with pytest.raises(RuntimeError, match="Leakage guard"):
        preprocess_sample_pair(syn, cfg=z_cfg, bits_stored=12, fit_state=None)
    with pytest.raises(RuntimeError, match="Leakage guard"):
        preprocess_sample_pair(
            syn,
            cfg=z_cfg,
            bits_stored=12,
            fit_state=TrainFitState(fit_partition="val", mean=0.3, std=0.2, sample_count=10),
        )
    ok_z = preprocess_sample_pair(
        syn,
        cfg=z_cfg,
        bits_stored=12,
        fit_state=TrainFitState(fit_partition="train", mean=0.3, std=0.2, sample_count=10, split_id="SPLIT0001"),
    )
    assert ok_z.model_tensor.shape == (3, 512, 512) and np.isfinite(ok_z.model_tensor).all()

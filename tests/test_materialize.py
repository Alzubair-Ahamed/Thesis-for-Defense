"""Unit and integration tests for STEP-021 release materialization and non-leakage."""

from __future__ import annotations

import csv
import io
from pathlib import Path
import zipfile

import cv2
import numpy as np
from PIL import Image
import pytest

from bc_xai.labels.freeze import sha256_bytes, sha256_file
from bc_xai.preprocess.materialize import fit_training_state, load_eligible_samples, materialize_release
from bc_xai.preprocess.transforms import load_preprocess_config


def _write_png_gray(path: Path, arr: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok, buf = cv2.imencode(".png", arr)
    assert ok
    path.write_bytes(buf.tobytes())


def _mask_png_bytes(mask: np.ndarray) -> bytes:
    buf = io.BytesIO()
    Image.fromarray(mask.astype(np.uint8), mode="L").save(buf, format="PNG")
    return buf.getvalue()


def _build_synthetic_workspace(tmp_path: Path, break_val_file: bool = False) -> dict[str, Path]:
    raw_ds3 = tmp_path / "raw" / "DS0003_CMMD"
    raw_ds5 = tmp_path / "raw" / "DS0005_BMCD"
    datasets_csv = tmp_path / "datasets.csv"
    with datasets_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["DS", "RestrictedLocation"])
        w.writerow(["DS0003", raw_ds3.as_posix()])
        w.writerow(["DS0005", raw_ds5.as_posix()])

    # Build 2 train scans (DS0003, 8-bit) + 1 val scan (DS0003, dark/poison option) + 1 external BMCD 12-bit scan w/ ROI mask.
    tr1 = np.zeros((128, 96), dtype=np.uint8)
    tr1[16:112, 8:80] = 120
    tr2 = np.zeros((128, 96), dtype=np.uint8)
    tr2[20:108, 12:84] = 180
    val1 = np.zeros((128, 96), dtype=np.uint8)
    val1[10:110, 10:80] = 250

    ext1 = np.zeros((160, 120), dtype=np.uint16)
    ext1[20:140, 10:100] = 2800  # 12-bit signal
    ext_mask = np.zeros((160, 120), dtype=np.uint8)
    ext_mask[60:80, 40:60] = 1

    _write_png_gray(raw_ds3 / "tr1.png", tr1)
    _write_png_gray(raw_ds3 / "tr2.png", tr2)
    if not break_val_file:
        _write_png_gray(raw_ds3 / "val1.png", val1)
    _write_png_gray(raw_ds5 / "ext1.png", ext1)

    mask_bytes = _mask_png_bytes(ext_mask)
    mask_sha = sha256_bytes(mask_bytes)
    masks_dir = tmp_path / "masks"
    masks_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(masks_dir / "LBL0004_masks.zip", "w") as zf:
        zf.writestr("masks/IMG00000001.png", mask_bytes)

    exports_dir = tmp_path / "exports"
    (exports_dir / "LBL0003").mkdir(parents=True, exist_ok=True)
    (exports_dir / "LBL0004").mkdir(parents=True, exist_ok=True)
    lbl_cols = [
        "LabelReleaseID",
        "DatasetID",
        "ImageID",
        "DispositionQC",
        "LocalizationEligible",
        "MaskStatus",
        "RawRelativePath",
        "MaskArchiveMember",
        "MaskSHA256",
    ]
    with (exports_dir / "LBL0003" / "LBL0003_manifest.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(lbl_cols)
        w.writerow(["LBL0003", "DS0003", "IMG00000001", "Retained", "False", "not_applicable", "tr1.png", "", ""])
        w.writerow(["LBL0003", "DS0003", "IMG00000002", "Retained", "False", "not_applicable", "tr2.png", "", ""])
        w.writerow(["LBL0003", "DS0003", "IMG00000003", "Retained", "False", "not_applicable", "val1.png", "", ""])
    with (exports_dir / "LBL0004" / "LBL0004_manifest.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(lbl_cols)
        w.writerow(["LBL0004", "DS0005", "IMG00000001", "Retained", "True", "ok_nonempty", "ext1.png", "masks/IMG00000001.png", mask_sha])
        w.writerow(["LBL0004", "DS0005", "IMG00000002", "Excluded_BorderRedBar", "False", "excluded_by_protocol", "ext1.png", "", ""])

    split_manifest = tmp_path / "split_manifest.csv"
    split_cols = [
        "SplitID",
        "ImageID",
        "DatasetID",
        "LabelReleaseID",
        "PatientGroupID",
        "ComponentID",
        "primary_partition",
        "dev_fold_5",
        "eligible_for_modeling",
        "BinaryTarget",
        "LabelClass",
        "LabelProvenanceTier",
        "SubTrackA_BiopsyEligible",
        "SubTrackB_ScreeningEligible",
        "LesionTrack_BenignVsMalignant",
        "LocalizationEligible",
    ]
    with split_manifest.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(split_cols)
        w.writerow(["SPLIT0001", "IMG00000001", "DS0003", "LBL0003", "P1", "C1", "train", "0", "True", "0", "Benign_Biopsy", "TierA_Biopsy", "True", "False", "False", "False"])
        w.writerow(["SPLIT0001", "IMG00000002", "DS0003", "LBL0003", "P2", "C2", "train", "1", "True", "1", "Malignant_Biopsy", "TierA_Biopsy", "True", "False", "False", "False"])
        w.writerow(["SPLIT0001", "IMG00000003", "DS0003", "LBL0003", "P3", "C3", "val", "2", "True", "0", "Benign_Biopsy", "TierA_Biopsy", "True", "False", "False", "False"])
        w.writerow(["SPLIT0001", "IMG00000001", "DS0005", "LBL0004", "P4", "C4", "external_test_bmcd", "-1", "True", "1", "Malignant_Screening", "TierA_Biopsy", "False", "True", "True", "True"])
        w.writerow(["SPLIT0001", "IMG00000002", "DS0005", "LBL0004", "P5", "C5", "excluded", "-1", "False", "0", "Excluded", "None", "False", "False", "False", "False"])

    cfg_path = tmp_path / "pp_test.yaml"
    cfg_path.write_text(
        Path("05_Preprocessing/configs/pp_baseline.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    return {
        "split_manifest": split_manifest,
        "datasets_csv": datasets_csv,
        "exports_dir": exports_dir,
        "masks_dir": masks_dir,
        "cfg_path": cfg_path,
    }


def test_fit_training_state_never_touches_non_train_files(tmp_path: Path) -> None:
    # Make val file physically missing, while bypassing raw check for val only inside fit_training_state.
    paths = _build_synthetic_workspace(tmp_path, break_val_file=True)
    # Create a val image so load_eligible_samples sees it, then delete it before fit_training_state.
    val_file = tmp_path / "raw" / "DS0003_CMMD" / "val1.png"
    _write_png_gray(val_file, np.ones((128, 96), dtype=np.uint8) * 200)
    records = load_eligible_samples(
        paths["split_manifest"], paths["datasets_csv"], paths["exports_dir"], paths["masks_dir"]
    )
    val_file.unlink()
    cfg = load_preprocess_config(paths["cfg_path"])
    fit = fit_training_state(
        records=records,
        cfg=cfg,
        fit_state_npz_path=tmp_path / "fitted" / "PP0001_train_state.npz",
        fit_state_json_path=tmp_path / "processed" / "train_fit_state.json",
        workers=2,
    )
    assert fit.state.fit_partition == "train"
    assert fit.state.sample_count == 2
    assert fit.stats_payload["excluded_partitions_from_fit"] == ["external_test_bmcd", "val"]


def test_materialize_release_deterministic_and_zero_clipping(tmp_path: Path) -> None:
    paths = _build_synthetic_workspace(tmp_path)
    out1 = materialize_release(
        config_path=paths["cfg_path"],
        release_id="REL9001",
        split_manifest=paths["split_manifest"],
        datasets_csv=paths["datasets_csv"],
        label_exports_dir=paths["exports_dir"],
        masks_dir=paths["masks_dir"],
        manifests_dir=tmp_path / "manifests",
        output_root=tmp_path / "processed_a",
        fitted_states_dir=tmp_path / "fitted_a",
        verify_raw_integrity=False,
        workers=2,
        generate_qc=True,
    )
    out2 = materialize_release(
        config_path=paths["cfg_path"],
        release_id="REL9001",
        split_manifest=paths["split_manifest"],
        datasets_csv=paths["datasets_csv"],
        label_exports_dir=paths["exports_dir"],
        masks_dir=paths["masks_dir"],
        manifests_dir=tmp_path / "manifests",
        output_root=tmp_path / "processed_b",
        fitted_states_dir=tmp_path / "fitted_b",
        verify_raw_integrity=False,
        workers=2,
        generate_qc=False,
    )
    assert out1.total_images == 4  # excludes Excluded row
    assert out1.roi_mask_count == 1
    assert out1.manifest_hash == out2.manifest_hash
    assert out1.fit_summary.fit_state_npz_hash == out2.fit_summary.fit_state_npz_hash
    assert len(out1.qc_plate_paths) == 1
    assert out1.qc_plate_paths[0].is_file()

    # Check output bit-depth & binary mask preservation.
    img_arr = cv2.imread(str(tmp_path / "processed_a" / "REL9001" / "images" / "DS0005" / "IMG00000001.png"), cv2.IMREAD_UNCHANGED)
    mask_arr = cv2.imread(str(tmp_path / "processed_a" / "REL9001" / "masks" / "DS0005" / "IMG00000001.png"), cv2.IMREAD_UNCHANGED)
    assert img_arr.shape == (512, 512)
    assert img_arr.dtype == np.uint16
    assert mask_arr.shape == (512, 512)
    assert set(np.unique(mask_arr).tolist()) == {0, 1}


def test_tampered_mask_zip_hash_fails_loudly(tmp_path: Path) -> None:
    paths = _build_synthetic_workspace(tmp_path)
    # Tamper mask bytes inside zip while leaving LBL0004_manifest.csv expected SHA-256 unchanged.
    tampered_mask = np.zeros((160, 120), dtype=np.uint8)
    tampered_mask[10:20, 10:20] = 1
    with zipfile.ZipFile(paths["masks_dir"] / "LBL0004_masks.zip", "w") as zf:
        zf.writestr("masks/IMG00000001.png", _mask_png_bytes(tampered_mask))

    with pytest.raises(ValueError, match="Mask archive member SHA-256 mismatch"):
        materialize_release(
            config_path=paths["cfg_path"],
            release_id="REL9002",
            split_manifest=paths["split_manifest"],
            datasets_csv=paths["datasets_csv"],
            label_exports_dir=paths["exports_dir"],
            masks_dir=paths["masks_dir"],
            manifests_dir=tmp_path / "manifests",
            output_root=tmp_path / "processed",
            fitted_states_dir=tmp_path / "fitted",
            verify_raw_integrity=False,
            workers=1,
            generate_qc=False,
        )


def test_tiny_5x5_mask_in_highres_scan_survives_512_downscale(tmp_path: Path) -> None:
    """Regression test: 5x5 point/calcification markers inside >=4096px scans must survive 8:1 resize."""
    from bc_xai.preprocess.transforms import preprocess_sample_pair

    raw = np.zeros((4096, 3328), dtype=np.uint16)
    raw[200:3800, 150:3100] = 2400
    tiny_mask = np.zeros((4096, 3328), dtype=np.uint8)
    # Odd coordinate where nearest-neighbor grid sampling can miss the 5x5 patch completely.
    tiny_mask[1001:1006, 1001:1006] = 1
    cfg = load_preprocess_config(Path("05_Preprocessing/configs/pp_baseline.yaml"))
    out = preprocess_sample_pair(raw, cfg, bits_stored=12, roi_mask=tiny_mask)
    assert out.roi_mask is not None
    assert int(out.roi_mask.sum()) >= 1
    assert set(np.unique(out.roi_mask).tolist()).issubset({0, 1})

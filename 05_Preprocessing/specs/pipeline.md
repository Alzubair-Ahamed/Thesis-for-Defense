# Mammography Preprocessing & Post-Hoc ROI Co-Transform Specification (`STEP-019` — `PP0001` Baseline vs `PP0002` CLAHE Ablation)

| Header Field | Value |
|---|---|
| `SpecID` | `PP_SPEC_v1.0.0` (`PP0001` Baseline + `PP0002` CLAHE Ablation) |
| `owner` | Alzubair Ahamed (`232-15-591`, Implementer) & Md Riyadul Hasan (`232-15-486`, Data Lead) |
| `date` | `2026-11-28` |
| `status` | `Drafted at STEP-019 (2026-11-28) — Pending UD12 (DEC0012) Approval; Zero Fitting or Disk Materialization Prior to G07` |
| `governing_section` | [OS §4.4, §4.6](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-019](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-019); [DEC0012](../../01_Project_Management/decision_log/DEC0012.md) |
| `parent_gates` | `G04 PASS` ([DS0001–0006 QC](../../03_Datasets/datasets.csv)), `G05 PASS` ([T09 v1.0.1](../../04_Labels_XAI_Governance/protocols/label_mask_protocol_v1.0.1.md) & [XAIP0001](../../04_Labels_XAI_Governance/xai_protocols/XAIP0001.md)), `G06 PASS` ([LBL0001–0005](../../04_Labels_XAI_Governance/label_registry.csv)) |

---

## 1. Empirical Grounding Across Frozen `LBL0001–LBL0005` Cohorts

Measured pixel formats from `STEP-013` quality audits (`DS0001–0006_quality.md`) require dynamic bit-depth & format normalization rather than naive `uint8 / 255.0` or arbitrary center-cropping:

| `LBL` / `DS` | Modality & Format | Bit Depth & Polarity (`Observed`) | Native Dimensions (`W x H`) | Key Preprocessing / Artifact Guardrail |
|---|---|---|---|---|
| **`LBL0003` (`DS0003 CMMD`)** | `FFDM` DICOM (`5,196` ret.) | `5,194` `8-bit uint8` + `2` `16-bit uint16` (`IMG00003519–3520`); `MONOCHROME2` (`slope=1, intercept=0`) | `1914x2294` | Must branch divisor on DICOM `BitsStored` (`255` vs `65535`); never hardcode `/255`. |
| **`LBL0005` (`DS0006 CDD-CESM LE`)** | `FFDM` Low-Energy JPEG (`1,003` ret.) | `100%` `8-bit uint8` `RGB` (`R == G == B`) | `1,002` distinct tightly-cropped aspect ratios (`~664x1816` to `2394x3062`) | `9` VIA masks touch border (`MaskCoordsClippedAtBorder`); aspect-preserving resize + symmetric zero-pad preserves breast shape without clipping skin/lesion borders. |
| **`LBL0004` (`DS0005 BMCD`)** | `FFDM` DICOM (`392` ret.) | `100%` `12-bit uint16` (`MONOCHROME2`, `BitsStored=12`, max `4095`) | `3328x4096` (`368`), `2560x3328` (`28`), `3328x4084` (`4`) | Normalize `uint16` using `4095.0` (`BitsStored=12`), **not** `65535.0` (`which would compress intensities 16x!`). Corner digital `RCC/LCC` stamps preserved for `RISK0004` audit. |
| **`LBL0002` (`DS0002 DMID`)** | `FFDM` DICOM (`507` ret.) | `8-bit uint8` (`488` `R==G==B` RGB + `22` `MONOCHROME2`) | `~3521x4784` to `4754x6000` | Reduce identical `RGB` channels to single luminance array `[0.0, 1.0]` prior to spatial transforms; preserve `1` BB skin marker for `RISK0004`. |
| **`LBL0001` (`DS0001 MIAS`)** | Digitized `SFM` PGM (`322` ret.) | `100%` `8-bit uint8` grayscale (`mode L`) | `4320x2600` (`149`), `4320x2048` (`101`), `4320x1600` (`48`), `5200x4000` (`24`) | Large horizontal scanner air margins trimmed via non-zero foreground bbox w/ safety padding; visible film tags (`R ML`) kept explicitly for `RISK0004` shortcut evaluation. |

---

## 2. Ordered Deterministic Operations (`src/bc_xai/preprocess/transforms.py`)

Both `PP0001` (`pp_baseline.yaml`) and `PP0002` (`pp_clahe_ablation.yaml`) execute **100% deterministic per-image operations** before model batching (with **zero stochastic augmentation** materialized into `REL####` disk caches):

1. **Header-Aware Decode & Polarity Standardization (`MONOCHROME1 -> MONOCHROME2`):**
   - For DICOMs: apply `RescaleSlope` & `RescaleIntercept` only when present and non-identity (`slope != 1 or intercept != 0`), determine `max_val = float((1 << BitsStored) - 1)` when `BitsStored` is set (`255` for `8-bit`, `4095` for `12-bit BMCD`, `65535` for `16-bit CMMD`), or infer conservatively (`255.0` for `uint8`, `4095.0` if `uint16 max <= 4095` else `65535.0`).
   - If `PhotometricInterpretation == "MONOCHROME1"`: invert via `max_val - arr` so dense breast parenchyma/lesions always map high and air maps near `0`.
   - Reduce identical-channel `RGB` (`max |R-G|, |R-B| == 0`) to a single `float32` array scaled strictly to `[0.0, 1.0]`.
2. **Lesion-Safe Foreground Bounding (`crop_safety_margin = 16 px / 2%`):**
   - Compute connected foreground thresholded above air floor (`arr > air_threshold`, default `0.02`), selecting main tissue region(s) covering `>= 0.5%` area (`suppressing isolated single-pixel scanner specks while preserving breast border`).
   - Expand bbox outward by `max(16 px, 2% of dimension)`. Skip cropping entirely if foreground already spans `>= 92%` of image area (e.g., pre-cropped `CDD-CESM`).
   - **Mandatory Post-Hoc ROI Safety Assertion:** When an optional binary `{0, 1}` ROI mask accompanies the sample (`during STEP-021 REL#### build and tests`), verify `clipped_roi_pixels == 0`; if any ROI pixel lies outside the candidate crop box, expand `crop_box` to encompass `100%` of the ROI mask (`+ margin`) so **zero target lesions are ever clipped**.
3. **Optional Controlled CLAHE Stage (`PP0002` Only — Isolated Ablation):**
   - **Disabled (`clahe.enabled = false`) in `PP0001` baseline.**
   - **Enabled (`clahe.enabled = true`, `clip_limit = 2.0`, `tile_grid_size = [8, 8]`) only in `PP0002`:** converts `[0.0, 1.0]` cropped luminance to `uint16` (`0..65535`) for high-precision histogram equalization inside `cv2.createCLAHE`, then scales back to `float32 [0.0, 1.0]`. Zero val/test statistics used (`purely per-image adaptive contrast`).
4. **Aspect-Ratio-Preserving Resize + Symmetric Zero-Pad (`512 x 512`):**
   - Rescale cropped image so `max(new_h, new_w) == target_size` (`512`, keeping `new_h / orig_crop_h == new_w / orig_crop_w`): uses `cv2.INTER_AREA` when shrinking high-res mammograms (`~2000–6000 px -> 512 px`) and `cv2.INTER_LINEAR` if upsampling.
   - Pad symmetrically with `0.0` (black background) to exact `(512, 512)` canvas (`pad_top, pad_bottom, pad_left, pad_right`).
   - **Exact 1:1 ROI-Mask Co-Transform:** Apply identical `crop_box` slice, `cv2.INTER_NEAREST` resize to `(new_h, new_w)`, and identical `(pad_top, pad_bottom, pad_left, pad_right)` `0`-padding to binary `{0, 1}` ROI masks (`asserting post_transform_mask.sum() > 0` whenever input mask had foreground pixels!).
   - Persist `SpatialTransformMeta` (`orig_h, orig_w, crop_x0, crop_y0, crop_x1, crop_y1, scale, pad_left, pad_top, target_size`) so post-hoc XAI heatmaps (`512 x 512`) and evaluation masks stay mathematically invertible `1:1` back to native coordinates.
5. **Channel Expansion & Normalization Policy (`Strict FitPartition = train` Boundary):**
   - Expand single-channel `[0.0, 1.0]` `(512, 512)` to `3-channel` `(3, 512, 512)` for `ImageNet`-pretrained CNN transfer learning (`UD13`).
   - **Default (`PP0001` & `PP0002`):** Deterministic `imagenet` channel standardization (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`) at training/inference dataloader time (zero dataset fitting leakage).
   - **Optional `train_zscore` mode:** Supported strictly only when a `FitState` with `FitPartition == "train"` fitted *after* `G07` (`STEP-020`) is passed; code raises `RuntimeError` loudly otherwise.

---

## 3. Radiographically Valid Training-Only Augmentation Rules (`Zero Pre-Materialization`)

Storing augmented copies before splitting or materializing augmented `REL####` caches is **strictly forbidden**. On-the-fly stochastic augmentation runs **only** inside `train` partition loaders during `STEP-027–031`:

| Augmentation | Allowed Bound (`Training Partition Only`) | Radiographic Rationale & Prohibited Alternatives |
|---|---|---|
| Horizontal Flip | `p = 0.5` | Symmetric bilateral breast geometry; **Vertical flip (`p = 0.0`) strictly banned** (`pectoralis & inframammary fold anatomy is top-bottom asymmetric`). |
| Bounded Rotation | `[-10°, +10°]` (`border=0.0`) | Preserves realistic CC/MLO positioning tilt; `>= 30°` rotations forbidden. |
| Shift / Scale Affine | `shift <= ±5%`, `scale in [0.95, 1.05]` (`zero shear`) | Preserves spatial aspect of masses & microcalcification clusters; aggressive crop `< 0.85` area banned (`would crop peripheral chest-wall/retroareolar lesions`). |
| Intensity / Gamma Jitter | `brightness/contrast ±8%`, `gamma in [0.90, 1.10]` | Mild exposure variability tolerance without clipping dense masses or erasing subtle microcalcifications. |
| Cutout / Random Erasing / MixUp / Hue | **Prohibited (`disabled`)** | Erasing regions mimics scars or removes subtle calcification foci; MixUp corrupts per-image XAI localization faithfulness. |

---

## 4. Non-Leakage & Verification Gates Ahead of `STEP-020` / `STEP-021`

- **`STEP-019` Completion (`Now`):** Only specification, YAML configs, `src/bc_xai/preprocess/transforms.py`, synthetic `tests/test_preprocess.py`, and `DEC0012` (`UD12`) review package are produced — **zero val/test fitting, zero split assumption, and zero disk image materialization**.
- **Unlocked After `G07 PASS` (`STEP-020` -> `STEP-021`):** `src/bc_xai/preprocess/materialize.py` will run `PP0001` -> `REL0001` and `PP0002` (`CLAHE` ablation) -> `REL0002` cleanly, asserting `DS####` raw hashes unchanged and zero lesions clipped across `1,005` `LesionTrack` masks.

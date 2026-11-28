# Gate Audit (`T24`) — `G08` (Immutable Data Releases `REL0001` + `REL0002` & Preprocessing Lock)

> [!NOTE]
> **Status:** **`PASS`** (**Ratified by Owner `2026-11-28`** in [`gates.csv`](../gates.csv)). `PP0001–PP0002` (`Active`) and `REL0001–REL0002` (`Frozen`) locked at completion of `STEP-021` Option A, closing `S09` and clearing entry into `S10 / STEP-022`.

## 1. Gate Metadata & Outcome
- **Gate ID:** `GATE0008` (`G08`)
- **Operating System Standard:** [`BC_XAI_RESEARCH_OPERATING_SYSTEM.md`](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) `§13.2` (`G08 — Dataset & Preprocessing Lock`) & [`BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md`](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md) `STEP-021`
- **Assessment Outcome:** **`PASS`** (**Approved `2026-11-28`**)
- **Assessors / Owners:** `Md Riyadul Hasan; Alzubair Ahamed` (Ratified by User/Supervisor & Data/Model Leads)

## 2. Scope & Upstream Inputs Locked
- **Raw Cohorts Verified Unchanged:** `DS0001` (`MIAS`), `DS0002` (`DMID`), `DS0003` (`CMMD`), `DS0005` (`BMCD`), `DS0006` (`CDD-CESM`) — all `v1.2.0` (`verify_manifest_integrity` passed pre- and post-materialization with `0` errors).
- **Label Schema Anchor:** [`04_Labels_XAI_Governance/label_map.json`](../../04_Labels_XAI_Governance/label_map.json) (`SHA-256: a6409b1054423b488b18b359e40d4b58a036a9eb7ad6e5758de88782f75d9f98`) and `LBL0001–LBL0005`.
- **Frozen Split Lock:** [`03_Datasets/splits/SPLIT0001/manifest.csv`](../../03_Datasets/splits/SPLIT0001/manifest.csv) (`SHA-256: dc386a2c4d0c03affdca9f439933929677478696b92aecbca0d755e085faf9cb`; `5,709` modeling-eligible scans out of `7,437` retained; `0` excluded scans leaked).
- **Approved Preprocessing Design (`DEC0012`):** [`pp_baseline.yaml`](../../05_Preprocessing/configs/pp_baseline.yaml) (`PP0001`) and [`pp_clahe_ablation.yaml`](../../05_Preprocessing/configs/pp_clahe_ablation.yaml) (`PP0002`), executed via [`materialize.py`](../../src/bc_xai/preprocess/materialize.py).

## 3. Criterion-by-Criterion `G08` Verification Matrix

| # | `OS §13.2` / `STEP-021` Criterion | Verification Method & Observed Result | Status |
|---|---|---|---|
| 1 | `TrainFitState` fit strictly on `FitPartition = train` | Fitted strictly on `SPLIT0001 train` (`DS0003`, `n = 2,614`); `val`, `internal_test`, and all `4` external partitions excluded and verified unaccessed (`test_fit_training_state_never_touches_non_train_files` + serialized exclusion log in `train_fit_state.json`) | **PASS** |
| 2 | Dual release materialization (`Option A`) complete | Both `REL0001` (`PP0001` baseline, `845.03 MiB`) and `REL0002` (`PP0002` `uint16` `CLAHE` ablation, `856.49 MiB`) materialized across all `5,709` scans, `2,796` unique components, and `1,121` ROI masks | **PASS** |
| 3 | Zero ROI lesion clipping or mask collapse | `OrigMaskPixels == PostCropMaskPixels` and `ProcessedMaskPixels >= 1` for `1,121 / 1,121` (`100%`) localized masks across `DS0001`, `DS0002`, `DS0005`, `DS0006` (`0` clipped, `0` collapsed) | **PASS** |
| 4 | Zero NaN/Inf/all-black processed outputs | Every `512x512` `uint16` image verified finite, `ImageMax01 > 0`, `ImageStd01 > 0` (`bad_imgs = 0` in both `REL0001` & `REL0002`) | **PASS** |
| 5 | Deterministic hashing & reproducibility | Re-running `materialize_release` yields bit-identical `manifest.csv` and `.npz` `TrainFitState` SHA-256 digests (`test_materialize_release_deterministic_and_zero_clipping` passed) | **PASS** |
| 6 | Raw dataset SHA-256 invariance | `DS0001`, `DS0002`, `DS0003`, `DS0005`, `DS0006` raw manifest hashes identical before/after both releases (`verify_manifest_integrity`: `0` errors) | **PASS** |
| 7 | Stratified visual QC overlay inspection | Visual inspection of `qc_plate_01..03.png` across all `5` cohorts in both `REL0001` and `REL0002` verified breast crop framing, contrast fidelity, and `1:1` ROI contour alignment | **PASS** |
| 8 | Canonical registries, `T12` reports, & `.gitignore` | `preprocessing_registry.csv` (`PP0001–0002`), `releases.csv` (`REL0001–0002`), [`PP0001.md`](../../05_Preprocessing/reports/PP0001.md), [`PP0002.md`](../../05_Preprocessing/reports/PP0002.md), and `validate_registries.py` updated; processed PNGs/states gitignored | **PASS** |

## 4. Cryptographic Lineage & Evidence Registry

| Artifact ID | Type / Scope | Path | SHA-256 |
|---|---|---|---|
| `PP0001` | Config YAML (`baseline`) | [`05_Preprocessing/configs/pp_baseline.yaml`](../../05_Preprocessing/configs/pp_baseline.yaml) | `2142653c2656bda90e36c11735a9b4281d73a3c9ae40d947804cbedd338aad92` |
| `PP0001_STATE` | Fitted train `.npz` (`Tier-2`) | `05_Preprocessing/fitted_states/PP0001_train_state.npz` | `972ca024327e11cb3dc3354276191affa6fabab786a80158989e4fbc981a9ede` |
| `REL0001` | Baseline release manifest (`5,709` imgs / `1,121` masks, `Tier-2`) | `05_Preprocessing/processed/REL0001/manifest.csv` | `11a439a22654b70c73933348cbcb98ed5f5bf8dca6cd7b104e4f40faed0bbe65` |
| `PP0002` | Config YAML (`uint16 CLAHE`) | [`05_Preprocessing/configs/pp_clahe_ablation.yaml`](../../05_Preprocessing/configs/pp_clahe_ablation.yaml) | `e76881257f91538d2727e643ca9a4d694877ec994bee45a8fac03724044ebc95` |
| `PP0002_STATE` | Fitted train `.npz` (`Tier-2`) | `05_Preprocessing/fitted_states/PP0002_train_state.npz` | `14cabd0eb650b1b2bf6fa8c3c9754a0096a51f80a89c65609c506690f6b28eb4` |
| `REL0002` | CLAHE release manifest (`5,709` imgs / `1,121` masks, `Tier-2`) | `05_Preprocessing/processed/REL0002/manifest.csv` | `75f6e84723412d48ba8c5588d72e665ca761a5fb0ae9277f284ace8ba08d6ffd` |

## 5. Deviations & Mitigations
- **Binary ROI Mask Downscale Precision Fix ([`transforms.py`](../../src/bc_xai/preprocess/transforms.py)):** During initial `REL0001` execution, `10` tiny (`21–150` px, `5x5–10x6`) `DS0005` `Normal_Control` reference dot masks collapsed to `0` pixels under `cv2.INTER_NEAREST` at `8:1` shrink (`4096x3328 -> 512x512`). Replaced downscale interpolation in `resize_and_pad_pair` with exact spatial area-coverage thresholding (`cv2.INTER_AREA > 0.0` on downscale, retaining `cv2.INTER_NEAREST` on upsample) and added regression test `test_tiny_5x5_mask_in_highres_scan_survives_512_downscale` (`tests/test_materialize.py`), reducing vanished masks to `0 / 1,121`.
- **Patient Count Accounting:** `PatientCount = 2,796` in [`03_Datasets/releases.csv`](../../03_Datasets/releases.csv) records unique connected patient/L-R components across modeling-eligible scans (`DS0001` groups left/right views from `322` per-breast IDs into `161` components).

## 6. Ratification Decision
- **Outcome:** **`GATE0008 = PASS`** ratified on `2026-11-28` (`Approved by User/Supervisor & Data/Model Leads`). `PP0001–PP0002` locked as `Active` in [`preprocessing_registry.csv`](../../05_Preprocessing/preprocessing_registry.csv) and `REL0001–REL0002` locked as `Frozen` in [`releases.csv`](../../03_Datasets/releases.csv), closing **`S09`** and authorizing **`S10 / STEP-022`** (`G09`).

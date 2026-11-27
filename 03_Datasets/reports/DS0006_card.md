# DS0006 Dataset Card — CDD-CESM Low-Energy Track (`CAND0013`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T08` (`T08_dataset_card.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DS0006` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Data Steward) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-27` |
| `status` | `QC_Audited_Pending_G04` |
| `source_inputs` | [DS0006_intake_receipt.md](./DS0006_intake_receipt.md); [DS0006_quality.md](./DS0006_quality.md); `03_Datasets/cache/qc/DS0006_qc_details.csv` |
| `governing_section` | [OS §1.2 (`RF15`), §4](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [STEP-013](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-013) |
| `sensitivity` | Tier-1 Governance Card (`raw bytes & private linkage segregated in Tier-2`) |
| `reviewer` | Alzubair Ahamed (`232-15-591`); Md Riyadul Hasan (`232-15-486`); Israt Jahan (Supervisor — pending G04 sign-off) |

---

## 1. Identity, Provenance & Citation
- **Dataset ID / Candidate:** `DS0006` (`CAND0013`)
- **Collection Name:** Categorized Digital Database for Low Energy and Subtracted Contrast Enhanced Spectral Mammography Images (`CDD-CESM`, Cairo, Egypt)
- **Custodian & Persistent Identifier:** The Cancer Imaging Archive (`TCIA`, `DOI: 10.7937/29kw-ae92`; Khaled et al. `2022`, *Scientific Data*, `DOI: 10.1038/s41597-022-01238-0`).

## 2. License, DUA & Ethics Governance
- **License Record:** [LICENSE_CDD_CESM_TCIA.md](../licenses/LICENSE_CDD_CESM_TCIA.md) (`CC BY 4.0`).
- **DIU Secondary-Data Ethics Waiver:** Approved under `DEC0006` (`2026-11-27`).
- **Scope Rule (`RF15`):** Only **Low-Energy (`DM`) 2D mammography images** are permitted; contrast-subtracted (`CESM / CM`) images are hard-excluded from model training/evaluation.

## 3. Storage Tier & Checksum Custody
- **Restricted Raw Location (Tier-2 Gitignored):** `03_Datasets/raw/DS0006_CDD_CESM`
- **Immutable Intake Manifest Hash:** `e1732776952a7562a811b16800924563a33cc645f72fd33aa056a38a0919ecd4`
- **Post-QC SHA-256 Integrity Check:** `0` / `0` mismatches (`verify_manifest_integrity` verified `2026-11-27`).

## 4. Cohort Scale & `STEP-013` Accounting Reconciliation
- **Total Raw Files Inventoried:** `2,337` (`1,003` Low-Energy `DM` `.jpg` + `1,003` Subtracted `CESM` `.jpg` + `1` `desktop.ini` + `1` `~$P54.docx` + `326` `P*.docx` reports + `Radiology-manual-annotations.xlsx` + `Radiology_hand_drawn_segmentations_v2.csv` + `CDD-CESM.sums`).
- **Primary LE Track Accounting (`Acquired = Retained + Excluded + Quarantined`):** **`1,003` = `1,003` Retained + `0` Excluded + `0` Quarantined**.
- **Full Image Pool Accounting (`LE + CESM`):** `2,006` JPEGs = `1,003` Retained Low-Energy `DM` + **`1,003` Excluded Subtracted `CESM` (`Excluded_SubtractedCESM_RF15`)** + `0` Quarantined; plus `2` excluded non-medical filesystem artifacts (`desktop.ini`, Word lock `~$P54.docx`).
- **Patient Count:** `326` distinct patients (`P1–P326`).

## 5. Modality, Pixel Format, Bit Depth & Polarity
- **Imaging Modality:** `2D` Low-Energy Full-Field Digital Mammography (`equivalent to standard 2D DM`, acquired on GE Senographe Pristina / Hologic systems).
- **File Format & Channels:** `1,003/1,003` `8-bit uint8 RGB` JPEGs verified **`100%` channel-identical (`identical_R_eq_G_eq_B=1003`, `nonzero_diff=0`)** -> clean grayscale luminance, `MONOCHROME2`-equivalent polarity.
- **Dimension Heterogeneity (`CONFIRMED`):** **`1,002` unique `W x H` resolutions across `1,003` images** (`e.g. 2394x3062, 1308x2316, 664x1816, 714x1970`) because ~30% of scans were manually cropped tightly to breast region upstream (`P1498`). Preprocessing (`STEP-021`) must resize with aspect-ratio-preserving padding (`zero distortion of polygonal coordinates`)!

## 6. Privacy & Duplicate Screening (`STEP-013`)
- **DICOM / Image Privacy:** Raster JPEGs contain zero DICOM metadata; visual contact sheet shows zero patient names or hospital identifiers burned into sampled frames. (`Note: `~$P54.docx` temp Word lock quarantined cleanly in QC ledger`).
- **Exact & Pixel-Clone Audit:** Exhaustive uncompressed pixel SHA-256 across all `1,003` LE images confirmed **`0` exact duplicates and `0` pixel clones** (`42` non-trivial `dHash <= 4` pairs verified distinct, max `64x64 r = 0.8586`).
- **Cross-Cohort Overlap:** `0` overlaps against `DS0001`, `DS0002`, `DS0003`, `DS0005`.

## 7. Diagnostic Labels & Provenance (`Preview for S07 / G05`)
- **Upstream Labels (`Radiology-manual-annotations.xlsx`):** `Pathology Classification/ Follow up` (`Benign`, `Malignant`, `Normal`), `BIRADS` (`1–6`), `Findings`.
- **Header Anomalies Queued for `S07 / STEP-014–015`:** Initial workbook inspection revealed special sub-sheets (`postoperative`, `postneoajuvant chemotherapy`) and anomalous rows (`e.g. P156_L_DM_CC` tagged `BIRADS=6` yet `Pathology='Normal'`). Strict clinical inclusion/exclusion rules must be ratified at `G05`!

## 8. ROI Localization & Spatial Annotations
- **Available Spatial Ground Truth:** Radiologist hand-drawn polygonal segmentations (`Radiology_hand_drawn_segmentations_v2.csv`) keyed by `Image_name` (`using Low-Energy DM rows only`, with exact polygon vertex coordinates aligned to each JPEG's native `W x H`).

## 9. Split Grouping & Leakage Controls (`Preview for S09 / G07`)
- **Grouping Key:** Strict `Patient_ID` (`P1–P326`, keeping `L/R` and `CC/MLO` up to 4 LE views per woman together). Zero cross-cohort overlap.

## 10. Subgroup Metadata & Covariates
- **Available Covariates:** `Age`, `ACR` breast density (`A–D`), `BI-RADS`, `Machine` (`1/2`), `Side`, `View`, morphological findings (`mass`, `calcifications`, `distortion`, `asymmetry`).

## 11. Observed Artifacts & Quality Risks (`Visual QC`)
- **Visual Contact Sheet (`DS0006_qc_grid.png`):** Clean breast tissue with zero radiopaque lead tags, varying aspect ratios (`narrow cropped views like 714x1970 alongside full 2394x3062 frames`), requiring careful aspect-ratio-safe padding & polygon coordinate rescaling (`not naive stretch`).

## 12. Authorized Research Role (`UD05`)
- **Permitted Role:** **Primary FFDM Polygonal XAI Localization (`Pointing Game, EBPG, IoU/Dice`) & Independent Biopsy-Verified External Evaluation / Nested FFDM Benchmark (`RQ2, RQ3, RQ4`)** — strictly on the **`1,003` Low-Energy `DM` subset (`zero CESM subtraction`)**.

## 13. Open Actions & Next Gate
- Audit `postoperative` / `postneoajuvant chemotherapy` cases and `BIRADS=6 / Normal` rows plus verify polygon rasterization (`mask vs native JPEG WxH`) at `S07 / STEP-014–015` (`G05`).

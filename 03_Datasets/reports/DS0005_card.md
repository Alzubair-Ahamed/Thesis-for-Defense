# DS0005 Dataset Card — BMCD (`CAND0012`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T08` (`T08_dataset_card.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DS0005` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Data Steward) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-28` (QC `2026-11-27`; Ratified `G04 PASS` `2026-11-28`) |
| `status` | `Approved_G04_PASS` |
| `source_inputs` | [DS0005_intake_receipt.md](./DS0005_intake_receipt.md); [DS0005_quality.md](./DS0005_quality.md); `03_Datasets/cache/qc/DS0005_qc_details.csv` |
| `governing_section` | [OS §4](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [STEP-013](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-013) |
| `sensitivity` | Tier-1 Governance Card (`raw bytes & private linkage segregated in Tier-2`) |
| `reviewer` | Alzubair Ahamed (`232-15-591`); Md Riyadul Hasan (`232-15-486`); Israt Jahan (Supervisor — Approved `G04 PASS` `2026-11-28`) |

---

## 1. Identity, Provenance & Citation
- **Dataset ID / Candidate:** `DS0005` (`CAND0012`)
- **Collection Name:** Breast Micro-Calcification Dataset (`BMCD`, Cyprus temporal screening pairs)
- **Custodian & Persistent Identifier:** Zenodo (`DOI: 10.5281/zenodo.5036062`, Loizidou et al. `2021`, *Insights into Imaging*, `DOI: 10.1186/s41747-021-00238-w`).

## 2. License, DUA & Ethics Governance
- **License Record:** [LICENSE_BMCD_Zenodo.md](../licenses/LICENSE_BMCD_Zenodo.md) (`CC BY 4.0`).
- **DIU Secondary-Data Ethics Waiver:** Approved under `DEC0006` (`2026-11-27`).

## 3. Storage Tier & Checksum Custody
- **Restricted Raw Location (Tier-2 Gitignored):** `03_Datasets/raw/DS0005_BMCD`
- **Immutable Intake Manifest Hash:** `4a1faa4ceeb921b6694c0458e4a7ce6702b5471deda259d9784121a08e989efe`
- **Post-QC SHA-256 Integrity Check:** `0` / `0` mismatches (`verify_manifest_integrity` verified `2026-11-27`).

## 4. Cohort Scale & `STEP-013` Accounting Reconciliation
- **Total Raw Files Inventoried:** `802` (`400` FFDM DICOMs + `400` `*_GT.jpg` color overlay JPEGs + `Description.xlsx` + `README.txt`).
- **Primary Track (`DICOM`) Reconciliation (`Acquired = Retained + Excluded + Quarantined`):** **`400` = `392` Retained + `0` Excluded + `8` Quarantined**.
  - *Quarantined Cross-Label Pixel Clones (`8`):* **`Dataset/Normal_cases/40`** (`PAT00000035`, uppercase `.DCM`, `Description.xlsx` = `BI-RADS 2`, density `c`, Age `53`, Right, `2017-2015`, Biopsy `NOT AVAILABLE`) and **`Dataset/Suspicious_cases/16`** (`PAT00000058`, lowercase `.dcm`, `Description.xlsx` = `BI-RADS 4a`, density `b`, Age `53`, Right, `2017-2015`, Biopsy `NOT AVAILABLE`) share **`100%` bit-exact raw DICOM pixels (`r = 1.0`, `PixelContentSHA256` match)** across ALL `4` views (`CC_prior, CC_recent, MLO_prior, MLO_recent`), while their `*_GT.jpg` files differ! All **`8` DICOMs (`2` folders)** quarantined under `Quarantined_CrossLabelPixelCloneConflict` leaving **`98` clean patient folders (`392` scans)**!
- **Auxiliary Overlay Track:** `400` `*_GT.jpg` images isolated cleanly (`Excluded_OverlayGT_NotRawInput`) for post-hoc XAI localization reference only (`varying preview resolutions e.g. 645x794 [219], 1059x1303 [46], 3328x4096 [18]`).

## 5. Modality, Pixel Format, Bit Depth & Polarity
- **Imaging Modality:** `2D` Full-Field Digital Mammography (`FFDM`, sequential `prior` + `recent` `CC` & `MLO` unilateral exams).
- **File Format & Bit Depth (`VERIFIED`):** `100%` (`400/400`) `Explicit VR Little Endian` **`12-bit uint16`** (`BitsAllocated=16`, `BitsStored=12`), `MONOCHROME2`, `RescaleSlope=1`, `RescaleIntercept=0`, `WindowCenter=2047` (`Note: upstream P1497/README summary had referred to 8-bit in prose; empirical DICOM headers prove true 12-bit unsigned 16-bit allocation`).
- **Image Dimensions (`W x H`):** `3328x4096` (`368`), `2560x3328` (`28`), `3328x4084` (`4`).

## 6. Privacy & Duplicate Screening (`STEP-013`)
- **DICOM Header PHI:** `None populated` across sensitive PHI fields (`PatientID`, `PatientName`, `InstitutionName` empty); `StudyDate/SeriesDate/AcquisitionDate` set to `1970` (`400/400` Unix epoch de-identification); `BurnedInAnnotation = NO`.
- **Within-Cohort & Cross-Cohort Clones:** Exhaustive raw pixel SHA-256 across all `400` DICOMs found `1` clone cluster (`Normal_cases/40 == Suspicious_cases/16`, `4` views quarantined cleanly); `0` cross-cohort duplicates against `DS0001/2/3/6`.

## 7. Diagnostic Labels & Provenance (`Preview for S07 / G05`)
- **Upstream Labels (`Description.xlsx`):** `50` `Normal_cases` folders (`BI-RADS 1` or benign `BI-RADS 2`, follow-up `NOT AVAILABLE`) and `50` `Suspicious_cases` folders (`BI-RADS 4a–5`, with **histopathology biopsy results for `32/50` suspicious cases** and `18/50` `NOT AVAILABLE`).
- **Temporal Prior vs Recent Note (`S07 / STEP-014`):** `prior` views come from an earlier normal screening round (1–4 yrs prior) whereas microcalcifications are present in `recent` views — `STEP-014–015` must specify whether only `recent` views or temporally labeled pairs enter classification/localization!

## 8. ROI Localization & Spatial Annotations
- **Available Spatial Ground Truth:** Radiologist microcalcification annotations in `*_GT.jpg` (`400` color JPEG overlays at variable resolutions, NOT lossless PNGs as stated in `README.txt`). `S07 / STEP-014` must extract red/yellow marked pixels and rescale `*_GT.jpg` to `3328x4096` / `2560x3328` native aspect ratio when computing `Pointing Game` / `EBPG` (`never used as model input`).

## 9. Split Grouping & Leakage Controls (`Preview for S09 / G07`)
- **Grouping Key:** `Normal_cases/<1..50>` & `Suspicious_cases/<1..50>` (`98` clean patient folders after `Normal_40/Suspicious_16` quarantine); keep `prior + recent + CC + MLO` (`4` views per folder) atomic in external evaluation / nested folds.

## 10. Subgroup Metadata & Covariates
- **Available Covariates:** `Breast (Right/Left)`, `Age (38–83)`, `BI-RADS breast density (a–d)`, `BI-RADS classification (1, 2, 4a, 4b, 4c, 5)`, screening interval years, biopsy pathology (`32` suspicious cases).

## 11. Observed Artifacts & Quality Risks (`Visual QC`)
- **Visual Contact Sheet (`DS0005_qc_grid.png`):** Clean `12-bit` digital mammograms with **small digital radiopaque view/laterality corner stamps (`RCC, LCC, RMLO, LMLO`)** in upper corners (`edge=177` on narrow-breast scans where center is air).

## 12. Authorized Research Role (`UD05`)
- **Permitted Role:** **Zero-Shot External FFDM Evaluation Cohort (`12-bit`, `BI-RADS` density `a–d`, microcalcification localization `RQ2, RQ3, RQ4`)** — strictly excluding the `8` quarantined `Normal_40 / Suspicious_16` conflicting DICOMs!

## 13. Open Actions & Next Gate
- Specify `recent`-vs-`prior` labeling policy, `Biopsy-only (32)` vs `BI-RADS` triage sensitivity, and `*_GT.jpg` mask extraction tolerance at `S07 / STEP-014–015` (`G05`).

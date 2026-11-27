# DS0003 Dataset Card — CMMD (`CAND0002`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T08` (`T08_dataset_card.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DS0003` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Data Steward) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-28` (QC `2026-11-27`; Ratified `G04 PASS` `2026-11-28`) |
| `status` | `Approved_G04_PASS` |
| `source_inputs` | [DS0003_intake_receipt.md](./DS0003_intake_receipt.md); [DS0003_quality.md](./DS0003_quality.md); `03_Datasets/cache/qc/DS0003_qc_details.csv` |
| `governing_section` | [OS §4](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [STEP-013](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-013) |
| `sensitivity` | Tier-1 Governance Card (`raw bytes & private linkage segregated in Tier-2`) |
| `reviewer` | Alzubair Ahamed (`232-15-591`); Md Riyadul Hasan (`232-15-486`); Israt Jahan (Supervisor — Approved `G04 PASS` `2026-11-28`) |

---

## 1. Identity, Provenance & Citation
- **Dataset ID / Candidate:** `DS0003` (`CAND0002`)
- **Collection Name:** The Chinese Mammography Database (`CMMD`)
- **Custodian & Persistent Identifier:** The Cancer Imaging Archive (`TCIA`, `DOI: 10.7937/tcia.eqde-4b16`).

## 2. License, DUA & Ethics Governance
- **License Record:** [LICENSE_TCIA_CBIS_DDSM_and_CMMD.md](../licenses/LICENSE_TCIA_CBIS_DDSM_and_CMMD.md) (`CC BY 4.0`).
- **DIU Secondary-Data Ethics Waiver:** Approved under `DEC0006` (`2026-11-27`).

## 3. Storage Tier & Checksum Custody
- **Restricted Raw Location (Tier-2 Gitignored):** `03_Datasets/raw/DS0003_CMMD`
- **Immutable Intake Manifest Hash:** `b933e5f7efb3767ea92143a0bc652d5c81fdc33f024df6f5fefee98537c4f6ed`
- **Post-QC SHA-256 Integrity Check:** `0` / `0` mismatches (`verify_manifest_integrity` verified `2026-11-27`).

## 4. Cohort Scale & `STEP-013` Accounting Reconciliation
- **Total Raw Files Inventoried:** `8,757` (`5,202` DICOMs + `3,555` supporting metadata/TCIA assets: `CMMD_clinicaldata_revision.xlsx`, `The-Chinese-Mammography-Database-nbia-digest.xlsx`, `.json`, `.log`, `.tcia`, `1,775` `.extracted_ok`, `1,775` `LICENSE`).
- **Primary Track Reconciliation (`Acquired = Retained + Excluded + Quarantined`):** **`5,202` = `5,196` Retained + `0` Excluded + `6` Quarantined**.
  - *Quarantined Bit-Exact Cross-Patient Clones (`6`):*
    1. `D1-0202` (`PAT00000122`, Age 38) vs `D2-0284` (`PAT00001310`, Age 38) share `100%` bit-exact raw pixels across all `4` views (`IMG00000507–510` == `IMG00005967–5970`, `r=1.0, MAE=0.0`) -> `4` duplicate copies `IMG00005967–5970` quarantined under `Quarantined_PixelCloneAcrossPatients`.
    2. `D1-0808` (`PAT00000476`, Age 45, `R mass`, `Benign`) vs `D1-1292` (`PAT00000815`, Age 45, `R mass`, `Malignant`) share `100%` bit-exact pixels (`IMG00001999` == `IMG00003418`, `r=1.0, MAE=0.0`) with **contradictory biopsy labels**, while their companion views (`IMG00002000` vs `IMG00003417`) correlate at `r=0.9933` -> both `IMG00001999` and `IMG00003418` quarantined under `Quarantined_CrossLabelPixelCloneConflict`, and both patients (`PAT00000476`, `PAT00000815`) flagged for atomic quarantine/linkage in `S07–S09`.
- **Patient Count:** `1,775` upstream `PatientID`s & `StudyInstanceUID`s (`1,773` distinct physical patients after merging/quarantining exact clone pairs).

## 5. Modality, Pixel Format, Bit Depth & Polarity
- **Imaging Modality:** `2D` Full-Field Digital Mammography (`FFDM`, `GE Senographe DS`).
- **Codec & Dimensions:** `100%` (`5,202/5,202`) `Explicit VR Little Endian`, `MONOCHROME2`, `1914x2294`, `RescaleSlope=1`, `RescaleIntercept=0`.
- **Mixed Bit-Depth Discovery (`CRITICAL`):** `5,200` DICOMs are **`8-bit uint8`** (`WindowCenter=128`), while **`2` DICOMs (`IMG00003519`, `IMG00003520` of `PAT00000840`) are `16-bit uint16`** (`WindowCenter=32768`, `PixelMin=0`, `PixelMax=65535`). Preprocessing (`STEP-021`) MUST normalize dynamically by header `BitsStored`/dtype rather than hardcoding `/255`.

## 6. Privacy & Duplicate Screening (`STEP-013`)
- **DICOM Header PHI:** `NonPseudonymPHITags = None populated` (`0/5,202`); `PatientName == PatientID` pseudonym echo (`5,202/5,202`); demographic/date fields present (`PatientAge`, `PatientSex`, `StudyDate/SeriesDate/AcquisitionDate` years `2008–2012`); `BurnedInAnnotation = NO` (`5,202/5,202`).
- **Duplicate Check:** Exhaustive uncompressed pixel SHA-256 across all `5,202` DICOMs confirmed **exactly `2` cross-patient clone clusters** (`5` bit-exact pixel clones resolved cleanly above via `6` quarantines).
- **Cross-Cohort Overlap:** `0` exact or pixel-clone overlaps against `DS0001`, `DS0002`, `DS0005`, `DS0006`.

## 7. Diagnostic Labels & Provenance (`Preview for S07 / G05`)
- **Upstream Labels (`CMMD_clinicaldata_revision.xlsx`):** 100% biopsy-confirmed pathology (`Benign` vs `Malignant`) on biopsied breast sides (`D1/D2`), alongside contralateral views (`total 5,202 DICOMs vs ~3,728 labeled breast-side views`). Explicit contralateral vs biopsied-side policy and `D1-0202/D2-0284`, `D1-0808/D1-1292` arbitration required in `STEP-014–015` (`G05`).

## 8. ROI Localization & Spatial Annotations
- **Available Spatial Ground Truth:** `NONE` inside `DS0003_CMMD` (`0` bounding boxes or pixel contours natively; note optional external `TOMPEI-CMMD` companion segmentations if desired later). Primary role focuses on **classification, probability calibration (`ECE/Brier`), XAI faithfulness (`Deletion/Insertion/ROAD`), and `Adebayo` sanity checks (`RQ1`)**.

## 9. Split Grouping & Leakage Controls (`Preview for S09 / G07`)
- **Mandatory Connected-Component Edges (`STEP-020`):** Group strictly on **`PatientID`** AND enforce clone-pair graph edges merging `PAT00000122 <-> PAT00001310` (`D1-0202 <-> D2-0284`) and `PAT00000476 <-> PAT00000815` (`D1-0808 <-> D1-1292`). Evaluate both **patient-level** and **breast-side (`ID+L/R`)** metrics per `P0385` / `CLAIM0007`.

## 10. Subgroup Metadata & Covariates
- **Available Covariates:** `LeftRight`, `Age`, `abnormality` (`mass`, `calcification`, `both`), `subtype` (molecular subtypes on `D2`), **NO breast density attribute natively in `CMMD_clinicaldata_revision.xlsx`** (`0` density tags).

## 11. Observed Artifacts & Quality Risks (`Visual QC`)
- **Visual Contact Sheet (`DS0003_qc_grid.png`):** Ultra-clean FFDM frames (`zero visible lead markers or scanner borders`), balanced left/right views, `0` failed decodes, `0` blank/saturated frames. Residual quality risks: mixed `8-bit`/`16-bit` files (`IMG00003519–3520`), contralateral unlabeled-side policy, and `96%` patient-level abnormality skew.

## 12. Authorized Research Role (`UD05`)
- **Permitted Role:** **Primary Biopsy-Confirmed FFDM Training, Internal Cross-Validation & Patient/Side Calibration Benchmark (`RQ1`)**.

## 13. Open Actions & Next Gate
- Define contralateral healthy breast labeling rules, resolve `D1-0808/D1-1292` (`4` views total) & `D1-0202/D2-0284` (`Luminal A` merge), and verify `IMG00003519–3520` intensity histogram at `S07 / STEP-014–015` (`G05`).

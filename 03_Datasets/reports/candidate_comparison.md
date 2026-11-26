# Candidate 2D Mammography Dataset Audit & Provenance Comparison (`STEP-010` / `UD05`)

- **Document:** `03_Datasets/reports/candidate_comparison.md`
- **Date:** `2026-11-27` (Executed immediately after Supervisor `G03 PASS` ratification)
- **Owner:** Md Riyadul Hasan (`232-15-486`, Data Lead) & Alzubair Ahamed (`232-15-591`, Verifier)
- **Governing Rules:** [OS §4.1](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04), [Blueprint STEP-010](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-010), ratified **Option 1** & **`RQ1–RQ4`** ([research_questions.md](../../02_Literature/research_questions.md)), `RF05`, `RF15`, `RF19`, and `GAP0002–GAP0004`
- **Access Guardrail:** **Zero restricted medical image bytes have been downloaded in `STEP-010`.** Formal DUA/license verification and DIU ethics waiver audit follow next in **`STEP-011` (`UD06`)** before any `STEP-012` raw acquisition.

---

## 1. Inclusion Requirements Derived From Ratified Option 1 & `RQ1–RQ4`

Per ratified **Option 1** (`G03 PASS`, `2026-11-27`), our dataset architecture must satisfy five non-negotiable scientific constraints:
1. **Strict 2D Mammography Scope (`RF15`):** Include only 2D `FFDM` or digitized `SFM` whole-image cohorts (`zero` ultrasound, MRI, histopathology, DBT slices, or tabular benchmarks).
2. **Primary-Source Traceability & Mirror Deduplication (`OS §4.1`):** Trace every candidate to its official custodian portal/DOI (PhysioNet, TCIA, INESC TEC, Figshare, PEIPA, AWS Open Data) and formally link derivatives via `DuplicateOf` so shared-patient collections (`DDSM` ↔ `CBIS-DDSM` ↔ `Mini-DDSM`) are **never** paired as independent external tests.
3. **Biopsy Pathology vs Radiological Triage Segregation (`GAP0002`, `CLAIM0008`):** Never pool biopsy-proven datasets (`CMMD`, `CBIS-DDSM`, `INbreast`) invisibly with unbiopsied radiologist `BI-RADS` triage datasets (`VinDr-Mammo`).
4. **Quantitative XAI Localization Coverage (`RQ3`):** At least one `FFDM` (`VinDr-Mammo`, `INbreast`, `DMID`, `EMBED`) and one `SFM` (`CBIS-DDSM`) track must carry expert lesion bounding boxes or segmentation polygons/masks for `Pointing Game`, `Delta-PG`, `EBPG`, and `IoU/Dice` audits (keeping masks strictly post-hoc, never leaked into classification inputs).
5. **Density & Multi-Vendor Covariates (`RQ2`, `RQ4`):** Preserve explicit `ACR BI-RADS A–D` breast density, `mass vs calcification`, and scanner-vendor metadata across `>=5` geographically and sensor-distinct public cohorts.

---

## 2. Primary-Source Candidate Matrix (`CAND0001–CAND0011`)

| `CAND` | Dataset & Custodian Portal / DOI | Modality & Format | Scale (`Primary Docs`) | Diagnostic Label Provenance | Lesion Localization Ground Truth | Patient / View Grouping Keys | Subgroup Metadata | Duplicate Lineage | `STEP-010` Disposition (`Pending STEP-011 DUA`) |
|---|---|---|---|---|---|---|---|---|---|
| **`CAND0001`** | **`VinDr-Mammo`**<br>PhysioNet (`10.13026/br2v-7517`) | `2D FFDM` DICOM (`SIEMENS`, `IMS`, `Planmed`; *DICOM warning in P0039 p. 7*) | `5,000` 4-view exams / `20,000` imgs (`4k train / 1k test`) | **Radiologist double-read + arbitration BI-RADS `1–5` ONLY** (`zero biopsy / zero BI-RADS 6` -> **Triage Track**) | `2,449` bounding boxes on `BI-RADS 3–5` findings (`BI-RADS 2` unboxed; no CC–MLO links) | `study_id`, `series_id`, official `4,000/1,000` split (*repeat-pt across studies unknown*) | **`89.96%` dense (`C+D`)**, 10 finding types, 3 vendors | `none` | **Shortlisted (Primary FFDM Triage + Multi-Vendor + Localization)** |
| **`CAND0002`** | **`CMMD`**<br>TCIA (`10.7937/tcia.eqde-4b16`) | `2D FFDM` DICOM (`GE Senographe DS`, China) | `1,775` pts (`3,728` labeled / `5,202` total DICOMs; `706` 4-view pts in `P0385`) | **100% biopsy pathology** (`affected benign/malignant`, contralateral `BI-RADS 0`; **`96.2%` pt positive caveat**) | **`NONE`** (`0` boxes/masks -> *classification + calibration + faithfulness only*) | Complete `PatientID` + `L/R` + `CC/MLO` | Mass/calc, age, `749` molecular subtypes (**`0` density tags**) | `none` | **Shortlisted (Primary/Ext Biopsy FFDM + Side-vs-Patient + Cal)** |
| **`CAND0003`** | **`INbreast`**<br>INESC TEC Porto (`10.1016/j.acra.2011.09.014`) | `2D FFDM` DICOM (`Siemens`, Portugal) | `115` cases / `410` images | **100% biopsy pathology** + `BI-RADS 1–6` | **Exact XML lesion contours** (mass, calc, asym, distortion) | `case_id` + `CC/MLO` views | `ACR` density `1–4`, lesion types | `none` | **Shortlisted (External FFDM Biopsy + Exact Contour XAI)** |
| **`CAND0004`** | **`DDSM`**<br>USF Legacy (`marathon.csee.usf.edu`) | `2D SFM` digitized film (obsolete `.LJPEG`) | `~2,620` studies / `~10,480` imgs | Mixed histology + clinical `BWC`; legacy overlay bugs | Freeman chain-code overlays | Patient/study/volume IDs | `ACR` density `1–4`, mass/calc | Root (`none`) | **Excluded (Superseded by `CAND0005` `CBIS-DDSM`)** |
| **`CAND0005`** | **`CBIS-DDSM`**<br>TCIA (`10.7937/K9/TCIA.2016.7O02S9CY`) | `2D SFM` digitized `16-bit` DICOM (USA) | `1,644` studies (`891` mass + `753` calc; `~3,103` full imgs / `~1,566` pts) | **Biopsy-confirmed** (`BENIGN`, `BENIGN_WITHOUT_CALLBACK`, `MALIGNANT`; `0` normals) | **Refined binary ROI masks (DICOM)** for all annotated lesions | `patient_id` complete (*audit `71` dup views & official split overlaps in `STEP-013/020`*) | Pre-5th-ed `density 1–4`, mass/calc, margin/shape | `CAND0004` | **Shortlisted (Primary SFM Biopsy + Density XAI Fairness Track)** |
| **`CAND0006`** | **`Mini-DDSM`**<br>BTH / Kaggle (`arXiv:2010.00494`) | `2D SFM` downsampled `PNG/JPEG` | Repackaged `DDSM` subset | Derived from `DDSM` | Chain-code derived masks | `DDSM` folders | Age, density | **`CAND0004;CAND0005`** | **Rejected (`DuplicateOf CBIS-DDSM / DDSM`)** |
| **`CAND0007`** | **`DMID`**<br>Figshare (`10.6084/m9.figshare.24522883`) | `2D FFDM` mixed (`DICOM` + `TIFF`, India) | `510` digital imgs (`abnormal + normal`) | Radiology reports + clinical/pathology notes (*verify biopsy subset at `STEP-012`*) | **Pixel-level masks + bboxes** on abnormalities | *Must audit DICOM/CSV patient links at `STEP-012–013`* | `ACR BI-RADS` density, lesion types | `none` | **Shortlisted (External Indian Digital Cohort + Masks)** |
| **`CAND0008`** | **`MIAS / Mini-MIAS`**<br>PEIPA Essex | `2D SFM` `8-bit` `PGM` (UK, `MLO` only) | `322` `MLO` imgs / `161` pt pairs | Historical radiologic/biopsy `B/M/Normal` (mixed `P0040`) | Coarse circle `(x, y, radius)` (*non-polygon*) | Paired L/R `161` patient IDs | `F/G/D` 3-class tissue, 6 lesion types | `none` | **Shortlisted (Optional Lightweight External SFM Check)** |
| **`CAND0009`** | **`RSNA Breast Cancer Detection`**<br>Kaggle / RSNA | `2D FFDM` multi-vendor DICOM | `54,706` train imgs / `~11,913` pts (`~2%` pos) | Biopsy `cancer` + clinical follow-up | **`NONE`** (`0` lesion boxes) | `patient_id`, `prediction_id`, `laterality`, `view` | Age, implant, partial density (absent on AUS site) | `none` | **Deferred Backup (Massive storage + zero ROI masks)** |
| **`CAND0010`** | **`EMBED` (AWS Open `20%` Subset)**<br>AWS Open Data (`Jeong et al. 2023`) | `2D FFDM` (*strictly exclude `DBT` per `RF15`*) | `20%` of `3.4M` imgs / `110k` pts (USA) | Biopsy pathology severity + `BI-RADS` | Lesion ROI bounding boxes | `empi_anon`, `acc_anon`, view | **Black/White race equity**, `A–D` density, vendor, margins | `none` | **Shortlisted Contingent on Emory DUA & Storage (`STEP-011`)** |
| **`CAND0011`** | **`BCDR` (`BCDR-F` & `BCDR-D`)**<br>INESC / FMUP (`bcdr.eu`) | `2D SFM` (`8-bit TIFF`) & `2D FFDM` (`16-bit TIFF`) | `BCDR-F: 3,703` imgs; `BCDR-D: 3,612` imgs | Mixed biopsy (`276/1,493`) + clinical impression (`P0040`) | Segmentation outlines on subsets | `patient_id`, `study_id` | `ACR` density, lesion subtype | `none` | **Deferred Backup (2-month gated DUA + mixed provenance)** |

---

## 3. Recommended Option 1 Experimental Track Partitioning (Zero Overlap, Zero Task Conflation)

To prevent every cross-dataset trap documented in `GAP0002–GAP0004`, shortlisted candidates fall into **strictly isolated evaluation tracks** (subject to `STEP-011` DUA & `STEP-013` integrity verification):

1. **Track A — Screening BI-RADS Triage + Localization + Dense Asian Baseline (`FFDM`):**
   - **`VinDr-Mammo` (`CAND0001`):** Official `4,000 / 1,000` exam split (`BI-RADS 1–2` non-recall vs `BI-RADS 3–5` recall, explicitly disclosed as radiologist consensus triage), `3` FFDM vendors (`SIEMENS/IMS/Planmed`), `89.96%` dense (`C+D`), and `BI-RADS 3–5` bounding-box XAI localization (`RQ1, RQ3, RQ4`).
2. **Track B — Biopsy-Confirmed FFDM Diagnosis, Side-vs-Patient Granularity & Zero-Shot Shift (`FFDM`):**
   - **Internal Biopsy FFDM (`CMMD`, `CAND0002`):** Strict `PatientID` split reporting **both patient-level & side-level** metrics (`RQ1`, per `P0385`), `ECE/Brier`, `Deletion/Insertion/ROAD`, and `Adebayo` checks.
   - **Zero-Shot External Biopsy Targets (`FFDM -> FFDM`):** **`INbreast` (`CAND0003`)** (Portugal FFDM + exact XML contour localization + `A–D` density), **`DMID` (`CAND0007`)** (India digital + masks + `A–D` density), and conditionally **`EMBED` 2D open subset (`CAND0010`)** (USA multi-ethnic + ROIs) (`RQ2, RQ3, RQ4`).
3. **Track C — Digitized Film (`SFM`) Biopsy, Dense-Tissue Saliency Fairness & `SFM <-> FFDM` Cross-Sensor Transfer:**
   - **`CBIS-DDSM` (`CAND0005`):** Strict connected-component patient split (audited for `71` duplicate views per `P0810` and official-split overlaps) evaluating **`BENIGN` vs `MALIGNANT`** (`RQ1`), **`BI-RADS 1–4` dense-breast fairness (`Delta-PG`, `ROAD`, `Adebayo`, `ECE`) (`RQ3, RQ4`)**, and bidirectional **`SFM <-> FFDM` domain/calibration collapse (`CBIS-DDSM <-> CMMD / INbreast / DMID / MIAS`) (`RQ2`)**.
   - **Strictly Excluded Mirror Pairs:** `DDSM` (`CAND0004`) and `Mini-DDSM` (`CAND0006`) share upstream patients with `CBIS-DDSM` (`CAND0005`) and are permanently blocked from acting as external comparators.

---

## 4. Concrete Questions Queued for `STEP-011` (`UD06` DUA, Ethics & Custody Verification)

Before downloading a single mammogram archive in `STEP-012`, `STEP-011` must resolve verbatim written terms for every shortlisted source:
1. **`VinDr-Mammo` (`CAND0001`):** Active PhysioNet CITI/credentialing status under team institutional accounts; PhysioNet 1.5.0 clause on cloud GPU training (`Kaggle/Colab/institutional server`) and thesis/Q1 illustrative heatmap figure publication.
2. **`INbreast` (`CAND0003`):** Current responsiveness of `medicalresearch.inescporto.pt` DUA form (or official custodian email at INESC TEC / Porto); explicitly confirm non-use of unauthorized third-party Kaggle copies.
3. **`CBIS-DDSM` (`CAND0005`) & `CMMD` (`CAND0002`):** Verify exact TCIA `CC BY 3.0 / 4.0` usage banner terms and citation requirements for figure disclosure and derived weight release (`UD24`).
4. **`DMID` (`CAND0007`) & `MIAS` (`CAND0008`):** Confirm `CC BY 4.0` Figshare metadata (`DMID`) and `PEIPA` `MIAS` research terms, plus inspect `DMID` clinical spreadsheet patient-grouping keys prior to `G04`.
5. **`EMBED` (`CAND0010`):** Evaluate whether Emory DUA processing lead time and `20%` AWS `2D`-only `S3` storage footprint fit DIU FYDP timeline and Tier-2 storage (`UD14`).
6. **Institutional Ethics (`UD06`):** Obtain formal DIU Ethics Committee / Supervisor determination or exemption waiver for secondary de-identified public medical imaging datasets.

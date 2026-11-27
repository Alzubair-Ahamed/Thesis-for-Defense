# DS0002 Dataset Card — DMID (`CAND0007`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T08` (`T08_dataset_card.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DS0002` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Data Steward) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-28` (QC `2026-11-27`; Ratified `G04 PASS` `2026-11-28`) |
| `status` | `Approved_G04_PASS` |
| `source_inputs` | [DS0002_intake_receipt.md](./DS0002_intake_receipt.md); [DS0002_quality.md](./DS0002_quality.md); `03_Datasets/cache/qc/DS0002_qc_details.csv` |
| `governing_section` | [OS §4](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [STEP-013](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-013) |
| `sensitivity` | Tier-1 Governance Card (`raw bytes & private linkage segregated in Tier-2`) |
| `reviewer` | Alzubair Ahamed (`232-15-591`); Md Riyadul Hasan (`232-15-486`); Israt Jahan (Supervisor — Approved `G04 PASS` `2026-11-28`) |

---

## 1. Identity, Provenance & Citation
- **Dataset ID / Candidate:** `DS0002` (`CAND0007`)
- **Collection Name:** Digital Mammography Dataset for Breast Cancer Diagnosis Research (`DMID`, India)
- **Custodian & Persistent Identifier:** Figshare (`DOI: 10.6084/m9.figshare.24522883`, Oza et al. `2023/2024`).

## 2. License, DUA & Ethics Governance
- **License Record:** [LICENSE_DMID_Figshare.md](../licenses/LICENSE_DMID_Figshare.md) (`CC BY 4.0`).
- **DIU Secondary-Data Ethics Waiver:** Approved under `DEC0006` (`2026-11-27`).

## 3. Storage Tier & Checksum Custody
- **Restricted Raw Location (Tier-2 Gitignored):** `03_Datasets/raw/DS0002_DMID`
- **Immutable Intake Manifest Hash:** `40882b4e5506f11675acccee1776e7469de1713bad0fabe9a33d0898892cf5da`
- **Post-QC SHA-256 Integrity Check:** `0` / `0` mismatches (`verify_manifest_integrity` verified `2026-11-27`).

## 4. Cohort Scale & `STEP-013` Accounting Reconciliation
- **Total Raw Files Inventoried:** `2,072` (`510` DICOMs + `511` mirror TIFFs + `538` ROI annotation TIFFs + `511` `Reports/*.txt` + `Metadata.xlsx` + `separate_benign_and_malignant_data.py`).
- **Primary Track (`DICOM Images/`) Reconciliation (`Acquired = Retained + Excluded + Quarantined`):** **`510` = `507` Retained + `0` Excluded + `3` Quarantined**.
  - *Quarantined Hidden Clones (`3`):* `IMG00000318` (`IMG318.dcm`, `r=0.999996` clone of `IMG019.dcm` with conflicting `B/3` vs `N/4a`), `IMG00000319` (`IMG319.dcm`, `r=1.0` clone of `IMG021.dcm`), `IMG00000172` (`IMG172.dcm`, `r=0.999998` clone of `IMG034.dcm` with `CIRC` vs `CIRC+SPIC`).
  - *Auxiliary Track Disposition:* `TIFF Images/IMG279 - Copy.tif` (`IMG00001838`) excluded as exact SHA-256 copy of `IMG279.tif`; remaining `510` mirror TIFFs held as `Supporting_MirrorTIFF_Secondary` (`DICOM` selected as canonical source track).
- **Patient Count Status:** **`0/510` DICOM headers populate `PatientID`** (`510` distinct `StudyInstanceUID`s; `507` unique non-clone scans). Cannot verify cross-view (`CC` vs `MLO`) patient identity links automatically without upstream patient IDs!

## 5. Modality, Pixel Format, Bit Depth & Polarity
- **Imaging Modality:** `2D` Full-Field Digital Mammography (`FFDM`, `CCLT`, `CCRT`, `MLOLT`, `MLORT`).
- **DICOM Codec & Decode:** `100%` (`510/510`) `JPEG Lossless, Process 14 [Selection Value 1]` (`pydicom + python-gdcm` decoded cleanly, `0` errors).
- **Bit Depth & Photometric Encoding:** `100%` `8-bit uint8`; **`488` encoded as `RGB` (`SamplesPerPixel=3` verified `identical_R_eq_G_eq_B=488`, `nonzero_diff=0` -> pure grayscale)** + **`22` encoded as `MONOCHROME2` (`RescaleSlope=1, Intercept=0`)** (`0` `MONOCHROME1`).
- **Image Dimensions (`W x H`):** Primarily `~4744–4754 x 6000` plus `3512–3521 x 4784` subsets (`paired TIFFs match 510/510 dimensions`).

## 6. Privacy & Duplicate Screening (`STEP-013`)
- **DICOM Header PHI:** `None populated` across sensitive patient/physician/institution tags (`PatientName`, `InstitutionName`, `PatientID` all blank); `StudyDate = 2022` (`510/510`); `BurnedInAnnotation` absent.
- **Hidden Clone Audit (`DS0002_dup_pairs.png`):** Visibly confirmed `IMG019/IMG318`, `IMG021/IMG319`, and `IMG034/IMG172` are pixel-clones under distinct `IMG###` names and divergent clinical table annotations -> **`3` redundant clone copies quarantined (`507` Retained)**; pairs `IMG223/263` and `IMG263/274` visually verified as distinct anatomies.
- **Cross-Cohort Overlap:** `0` exact or pixel-clone overlaps against `DS0001`, `DS0003`, `DS0005`, `DS0006`.

## 7. Diagnostic Labels & Provenance (`Preview for S07 / G05`)
- **Metadata & Clinical Text:** `Metadata.xlsx` (`510` `IMG###` rows with view, tissue `F/G/D`, subtype `CALC/CIRC/SPIC/MISC/ARCH/ASYM`, `N/B/M`, coordinates) + `511` radiologist `Reports/Img*.txt` reporting `ACR` density and `BI-RADS 1–5`.
- **Conflict Flag Queued for `STEP-014–015`:** Audit `IMG019` (`XLS='N'` yet `TXT='BIRADS 4a'`) and other potential `XLS`-vs-`TXT` mismatches across all `507` retained cases at `S07`.

## 8. ROI Localization & Spatial Annotations
- **Available Spatial Ground Truth:** `538` `Pixel-level annotation/*.tif` files plus `(x, y, radius)` coordinates in `Metadata.xlsx`.
- **Technical Caution:** Sampled `Pixel-level annotation/*.tif` (`RGBA uint8`) are full-resolution **colored overlay images (`RGBMaxChannelDiff > 0`)**, NOT binary `0/1` masks; `S07 / STEP-014` must build and audit explicit mask extraction rules (`and never leak annotation colors into image inputs`).

## 9. Split Grouping & Leakage Controls (`Preview for S09 / G07`)
- **Structural Constraint:** Because `DMID` releases no cross-view `PatientID` linking `CC` and `MLO` views (proven by `0/510` `PatientID` headers and sequential analysis of `IMG019 CCLT` & `IMG021 MLOLT`), using `DS0002` inside a random train/test split risks bilateral/multi-view leakage! Therefore **`UD05` designates `DS0002_DMID` strictly as an External Held-Out Test Cohort** (`so intra-cohort multi-view clustering never splits train vs test!`).

## 10. Subgroup Metadata & Covariates
- **Available Covariates:** `4` mammogram views (`CCRT, CCLT, MLORT, MLOLT`), `ACR` breast density (`F/G/D` in XLS, `ACR A–D` in reports), `BI-RADS`, lesion subtype (`CALC, CIRC, SPIC, MISC, ARCH, ASYM`).

## 11. Observed Artifacts & Quality Risks (`Visual QC`)
- **Visual Contact Sheet (`DS0002_qc_grid.png`):** High-clarity FFDM images; circular BB radiopaque skin marker visible on `IMG00000140` (`row 2 col 4`); paired TIFFs emit non-fatal `TIFFReadDirectory: Incorrect count for "SampleFormat"` libtiff warnings and include `IMG279 - Copy.tif`.

## 12. Authorized Research Role (`UD05`)
- **Permitted Role:** **Zero-Shot External Clinical Evaluation & ROI Localization Cohort (`RQ2, RQ3, RQ4`)** using canonical `507` Retained `DICOM Images/` (`not TIFF Images/`).
- **Restricted Role:** Blocked from internal train/val splitting unless explicit `CC–MLO` patient identity reconstruction is established and verified at `G07`.

## 13. Open Actions & Next Gate
- Audit `Metadata.xlsx` vs `Reports/*.txt` label consistency (`incl. IMG019/IMG318`) and `Pixel-level annotation/*.tif` binary mask extraction in `S07 / STEP-014–015` (`G05`).

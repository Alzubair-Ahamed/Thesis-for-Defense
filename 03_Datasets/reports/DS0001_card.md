# DS0001 Dataset Card — MIAS v1.21 (`CAND0008`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T08` (`T08_dataset_card.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DS0001` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Data Steward) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-27` |
| `status` | `QC_Audited_Pending_G04` |
| `source_inputs` | [DS0001_intake_receipt.md](./DS0001_intake_receipt.md); [DS0001_quality.md](./DS0001_quality.md); `03_Datasets/cache/qc/DS0001_qc_details.csv` |
| `governing_section` | [OS §4](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [STEP-013](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-013) |
| `sensitivity` | Tier-1 Governance Card (`raw bytes & private linkage segregated in Tier-2`) |
| `reviewer` | Alzubair Ahamed (`232-15-591`); Md Riyadul Hasan (`232-15-486`); Israt Jahan (Supervisor — pending G04 sign-off) |

---

## 1. Identity, Provenance & Citation
- **Dataset ID / Candidate:** `DS0001` (`CAND0008`)
- **Collection Name:** Mammographic Image Analysis Society (`MIAS` v1.21 `50 um` digitized film dataset)
- **Custodian & Persistent Identifier:** University of Cambridge Apollo (`DOI: 10.17863/CAM.105113`, handle `1810/250394`)
- **Primary Citation:** Suckling et al. (`1994`), *The Mammographic Image Analysis Society Digital Mammogram Database*, Excerpta Medica International Congress Series `1069`.

## 2. License, DUA & Ethics Governance
- **License Record:** [LICENSE_MIAS_Cambridge_Apollo_and_PEIPA.md](../licenses/LICENSE_MIAS_Cambridge_Apollo_and_PEIPA.md) (`CC BY 2.0 UK` per `license.txt` inside Apollo deposit; verified `DEC0006` Batch A clearance `2026-11-27`).
- **DIU Secondary-Data Ethics Waiver:** Covered by `DEC0006` Supervisor/Ethics determination (`2026-11-27`).

## 3. Storage Tier & Checksum Custody
- **Restricted Raw Location (Tier-2 Gitignored):** `03_Datasets/raw/DS0001_MIAS`
- **Immutable Intake Manifest Hash:** `2e3f8559ed425aee3d716174767558d2e8adf41c017915eecefb81da9ec9fdf1`
- **Post-QC SHA-256 Integrity Check:** `0` / `0` mismatches (`verify_manifest_integrity` verified `2026-11-27`).

## 4. Cohort Scale & `STEP-013` Accounting Reconciliation
- **Total Raw Files Inventoried:** `327` (`322` `.pgm` scans + `license.txt`, `miasdbv1.21.zip`, `.extracted_ok`, `00README.pdf`, `MIASDB Excerpta Medica 1994.pdf`).
- **Primary Track Reconciliation (`Acquired = Retained + Excluded + Quarantined`):** **`322` = `322` Retained + `0` Excluded + `0` Quarantined**.
- **Patient Count:** `161` paired left/right patients (`322` filename `MLO` views).

## 5. Modality, Pixel Format, Bit Depth & Polarity
- **Imaging Modality:** 2D Digitized Screen-Film Mammography (`SFM`, `MLO`-only view).
- **File Format & Bit Depth:** `322/322` `8-bit uint8` grayscale `.pgm` (`mode='L'`); `100%` decode success (`PIL`).
- **Photometric Polarity:** `MONOCHROME2` (`dark air background, bright breast parenchyma`).
- **Image Dimensions (`W x H`):** `4320x2600` (`149`), `4320x2048` (`101`), `4320x1600` (`48`), `5200x4000` (`24`).

## 6. Privacy & Duplicate Screening (`STEP-013`)
- **DICOM Header PHI:** N/A (headerless `.pgm` raster files; zero patient names in manifests).
- **Within-Cohort Duplicates & Pixel Clones:** `0` exact SHA-256 duplicates; `0` pixel clones (`3` non-trivial `dHash <= 4` pairs verified distinct, max `64x64 r = 0.9501`).
- **Cross-Cohort Overlap:** `0` exact or clone overlaps against `DS0002`, `DS0003`, `DS0005`, or `DS0006`.

## 7. Diagnostic Labels & Provenance (`Preview for S07 / G05`)
- **Upstream Labels:** Historical `B` (Benign) / `M` (Malignant) / `Normal` classes recorded in `00README.pdf` (mixed historical clinical/biopsy provenance per `P0040`, to be formally harmonized at `STEP-014–015` / `G05`).

## 8. ROI Localization & Spatial Annotations
- **Available Spatial Ground Truth:** Coarse abnormality circle approximations `(x, y, radius)` in `00README.pdf` (not pixel polygons; missing radius for diffuse/unbounded cases).

## 9. Split Grouping & Leakage Controls (`Preview for S09 / G07`)
- **Grouping Key:** `161` left/right breast patient pairs (`mdb001/002`, `mdb003/004`, etc.) must stay atomic in any evaluation grouping (`never split L vs R MLO`).

## 10. Subgroup Metadata & Covariates
- **Available Metadata:** `3`-class background tissue (`F` Fatty, `G` Fatty-glandular, `D` Dense-glandular) and `6` abnormality categories (`CALC`, `CIRC`, `SPIC`, `MISC`, `ARCH`, `ASYM`).

## 11. Observed Artifacts, Shortcut Risks & Limitations (`Visual QC`)
- **Visual Contact Sheet (`DS0001_qc_grid.png`):** Heavy top/bottom black horizontal film scanner bars, occasional bright white scanner edge strips (`IMG00000148`, `IMG00000138`, `IMG00000302`), and high-contrast white radiopaque corner film labels (`R ML`, `L ML`, `L MED-LAT OBL`, index numerals). Directly informs **`RISK0004`** shortcut-learning audits (`RQ2`, `RQ3`).
- **Limitations:** `SFM` digitized `50 um` film (`non-FFDM`), `MLO`-only view (`no CC`), small `161`-patient size (`zero role in primary FFDM training`).

## 12. Authorized Research Role (`UD05`)
- **Permitted Role:** Lightweight **External Zero-Shot Digitized-Film (`SFM`) Cross-Domain & Shortcut-Sensitivity Evaluation Cohort** (`RQ2`).
- **Prohibited Role:** Not pooled into primary FFDM training (`DS0003`).

## 13. Open Actions & Next Gate
- Proceed to `S07 / STEP-014–015` (`G05`) for `B/M/Normal` & circle-ROI normalization rules, and crop/border-shortcut policy (`S09 / STEP-019`).

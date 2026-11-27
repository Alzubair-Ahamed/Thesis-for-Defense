# Diagnostic Label Verification & ROI-Mask Standardization Protocol (`T09` — `v1.0.0`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T09` (`T09_label_mask_protocol.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `T09_LABEL_MASK_PROTOCOL_v1.0.0` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Label/Mask Lead) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-28` (Drafted `STEP-014`; Ratified `G05` `2026-11-28`) |
| `status` | `Approved at G05 (2026-11-28 — DEC0007–DEC0009 Ratified)` |
| `source_inputs` | [DEC0005.md](../../01_Project_Management/decision_log/DEC0005.md); [DS0001_card.md](../../03_Datasets/reports/DS0001_card.md); [DS0002_card.md](../../03_Datasets/reports/DS0002_card.md); [DS0003_card.md](../../03_Datasets/reports/DS0003_card.md); [DS0005_card.md](../../03_Datasets/reports/DS0005_card.md); [DS0006_card.md](../../03_Datasets/reports/DS0006_card.md); raw XLSX/CSV schema inspection (`2026-11-28`) |
| `governing_section` | [OS §4.3, §6.1, §14.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-014](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-014) |
| `sensitivity` | Tier-1 Ratified Protocol Specification (`raw patient metadata stays in Tier-2`) |
| `reviewer` | Israt Jahan (Supervisor); User/Research Owner; Md Riyadul Hasan (`232-15-486`); Alzubair Ahamed (`232-15-591`) — Ratified `G05` `2026-11-28` |

---

## 1. Classification Paradigm Rule (`UD07` — FFDM Whole-Breast vs ROI/Patch Isolation)

1. **Selected Paradigm (`Option A` — Strict Whole-Image 2D Classification):**
   - Models classify **whole-breast `2D` mammograms** (`CC` and `MLO` views) — **never** cropped lesion patches — matching `RF05`, clinical computer-aided triage framing, and meaningful full-image Grad-CAM spatial localization (`RQ3`).
2. **Absolute Track Segregation (`Zero Conflation`):**
   - **Primary Internal Biopsy `FFDM` Development Track:** **`DS0003 CMMD`** (`5,196` `G04`-retained DICOMs).
   - **Primary Quantitative `FFDM` Localization & Secondary `FFDM` Track:** **`DS0006 CDD-CESM LE`** (`1,003` Low-Energy `DM` scans; `1,003` subtracted `CESM CM` scans permanently excluded per `RF15`).
   - **Zero-Shot External `FFDM` Validation & Density/Localization Tracks:** **`DS0005 BMCD`** (`392` `12-bit` FFDM DICOMs) and **`DS0002 DMID`** (`507` Indian FFDM DICOMs — restricted to external evaluation because upstream DICOM headers lack cross-view `PatientID`).
   - **Zero-Shot External Digitized-Film (`SFM`) Cross-Domain & Marker-Shortcut Track:** **`DS0001 MIAS v1.21`** (`322` `MLO` PGMs). Never pooled with `FFDM` training data.
3. **Lesion Morphology Treatment (`mass` vs `calcification`):** Kept strictly as evaluation stratification attributes (`RQ4`), never split into disjoint single-type models unless declared as exploratory subgroup slices (`STEP-037`).

---

## 2. Binary Ground-Truth Label Mapping (`0 = Benign`, `1 = Malignant`) & Provenance (`UD08`)

Every image across `7,420` `G04`-retained scans receives a deterministic `BinaryTarget` (`0 = Benign / Non-Malignant`, `1 = Malignant`, or `Excluded`) AND an explicit **`LabelProvenanceTier`** distinguishing **histopathologic biopsy truth (`Tier-A`)** from **radiological BI-RADS / screening follow-up (`Tier-B`)**:

| Cohort (`Retained`) | Join Key & Scope Rule | Mapped `1 = Malignant` | Mapped `0 = Benign` (`Biopsy`) | Conditional `0` (`Non-Malignant + Normal` Track Only) | Explicit `Excluded_*` Buckets (`STEP-016–018`) |
|---|---|---|---|---|---|
| **`DS0003 CMMD`** (`5,196`) | `ID1 == DICOM PatientID` + `LeftRight == ImageLaterality` (`1,872` side rows = `3,744` annotated scans) | `classification == 'Malignant'` (`1,316` side rows) | `classification == 'Benign'` (`556` side rows) | *N/A (`0` annotated Normal rows)* | `~1,452` unannotated contralateral scans (`Excluded_UnlabeledContralateral`); `IMG00002000` & `IMG00003417` companion views of conflicted clone `D1-0808/D1-1292` (`Excluded_CrossLabelClonePatient`); `6` already `G04`-quarantined clones |
| **`DS0006 CDD-CESM LE`** (`1,003`) | `Image_name` (`Type == 'DM'`) in `Radiology-manual-annotations.xlsx` (`all` sheet) | `Pathology == 'Malignant'` (`304` non-op/non-NAC scans) | `Pathology == 'Benign'` (`277` non-op/non-NAC scans -> **`581` Pure Biopsy Track**) | `Pathology == 'Normal'` (`338` non-op/non-NAC scans -> **`919` Non-Malignant Track**) | `80` `postoperative` LE rows (`Excluded_PostOperative`); `4` `postneoajuvant chemotherapy` LE rows incl. all `4` `BIRADS=6` rows (`Excluded_PostNAC_BIRADS6`) |
| **`DS0005 BMCD`** (`392`) | Folder `Normal_cases/#` / `Suspicious_cases/#` + `recent` vs `prior` suffix (`98` clean folders = `196` `recent` + `196` `prior`) | `recent` scans in `Suspicious_cases` where `Biopsy Results in {'MALIGNANT', 'DCIS'}` (`11` pts / `22` scans) | `recent` scans in `Suspicious_cases` where `Biopsy Results == 'BENIGN'` (`21` pts / `42` scans) | `Normal_cases` `BI-RADS 1–2` (`49` folders / `98` `recent` + `98` `prior` normal scans -> disclosed `NonMalignant` control only) | `196` `prior` scans of `Suspicious_cases` (`Excluded_PriorScreeningRound`); `18` `Suspicious_cases` with `Biopsy == 'NOT AVAILABLE'` (`Excluded_UnconfirmedBiopsy` for biopsy truth; optional BI-RADS `4–5` triage sensitivity track); `8` `G04` clone conflict scans (`Normal_40 / Suspicious_16`) |
| **`DS0002 DMID`** (`507`) | `IMG###` stem -> `Metadata.xlsx` cross-checked against `Reports/Img*.txt` | `Metadata class == 'M'` (`118` rows; verify `TXT` concordance) | `Metadata class == 'B'` (`157` rows -> **`275` Lesion Benign vs Malignant Track**) | `Metadata class == 'NORM'` (`200` rows -> disclosed `NonMalignant` track) | **`36` rows with ambiguous token `'N'`** (`verified NOT Normal: 17 BIRADS 4a, 6 4b, 2 4c, 5 3, 2 3+4a, 1 BIRADS 0, 2 1, 1 lesion 4a` -> **`Excluded_AmbiguousClassToken_N`** pending clinical adjudication); `3` `G04` clones (`IMG172/318/319`); any `XLS`-vs-`TXT` severe discordance |
| **`DS0001 MIAS`** (`322`) | `mdb###` stem -> `00README.pdf` table (`MLO`-only SFM) | Historical class `'M'` (`Malignant`) | Historical class `'B'` (`Benign`) | `'NORM'` (`Normal`, disclosed `SFM_NonMalignant` track only) | Any corrupt/unparsed `00README` row (`if observed in STEP-016`) |

> **Provenance Guardrail:** Never pool `Tier-A` biopsy metrics silently with `Tier-B` (`BI-RADS` / `DMID` / `MIAS`) metrics (`RISK0003`). Every evaluation table (`G12`) reports cohort-level provenance explicitly.

---

## 3. Inclusion / Exclusion Rules for `Normal (BI-RADS 1)`, `BI-RADS 0`, Unlabeled & Post-Treatment Cases

1. **Zero Silent `Normal -> Benign` Merging:** `Normal` (`BI-RADS 1` or `DMID NORM` or `CDD-CESM Pathology='Normal'`) is **never** silently labeled as `Biopsy-Confirmed Benign`. Each benchmark reports:
   - **`Sub-Track A (Pure Abnormality Biopsy: Benign vs Malignant)`** on biopsy-verified abnormal lesions (`CMMD 3,744`, `CDD-CESM 581`, `BMCD 64 recent`, `DMID 275 B vs M`), AND
   - **`Sub-Track B (Full Screening-Style: Benign+Normal vs Malignant)`** transparently disclosing `Normal` control composition (`CDD-CESM 919`, `BMCD 392/recent`, `DMID 471`, `MIAS 322`).
2. **`CMMD` Unlabeled Contralateral Rule:** The `~1,452` unbiopsied contralateral DICOMs absent from `CMMD_clinicaldata_revision.xlsx` receive **`Excluded_UnlabeledContralateral`** (`0` clinical ground truth verified; optional patient-level all-views sensitivity logged strictly separately).
3. **`DMID` Token `'N'` Guardrail:** Because `36` `DMID` spreadsheet rows carry `'N'` alongside active abnormality codes (`CIRC/MISC/CALC`) and `Reports/Img*.txt` BI-RADS `3/4a/4b/4c/0/1`, all `'N'` records default strictly to `Excluded_AmbiguousClassToken_N` (`zero silent coercion`).
4. **`CDD-CESM` Treatment Artifacts & `$`-Delimited BI-RADS:** Exclude `postoperative` (`80`) and `postneoajuvant chemotherapy` (`4`, encompassing all `4` `BIRADS=6` rows incl. `P156` `Normal` + `BIRADS=6`). Multi-lesion `$`-delimited BI-RADS tags (`e.g. 3$2`, `4$2`, `5$2`) map to `max(int(tok))` for subgroup audits.
5. **`BI-RADS 0` / Missing Confirmation:** Any record whose primary clinical report resolves exclusively to incomplete `BI-RADS 0` or missing follow-up/biopsy in a biopsy-only track receives `Excluded_Incomplete_BIRADS0` / `Excluded_UnconfirmedBiopsy`.

---

## 4. Multi-Lesion Precedence Rule (`Malignant Dominance`)

1. **Breast-Side / Image Level:** When multiple abnormalities or ROI annotations appear on one mammogram/side (`e.g. CDD-CESM multiple VIA polygon rows or multi-finding text reports`), **Malignant dominates (`target = 1`)**: if *any* verified finding is Malignant (`1`), the image is `1 = Malignant`; only images where *all* verified findings are Benign (`0`) map to `0 = Benign`.
2. **Patient-Level Aggregation (`CMMD` `30` Bilateral-Discordant Patients):**
   - At **breast-side granularity (`P0385` / `CLAIM0007`)**, each side keeps its verified pathology label (`L = 0, R = 1` or vice versa, both residing in the *same* `STEP-020` split partition!).
   - At **patient-level aggregation**, patient label = `max(left_label, right_label)` (`Malignant dominance`).

---

## 5. Lesion ROI-Mask Coordinate Convention, Orientation & Multi-ROI Union (`UD09`)

Canonical XAI localization ground-truth masks are binary `uint8` arrays (`0 = background`, `1 = lesion ROI`) spatially matching each retained primary image's **exact native `(Height, Width)` pixel grid**:

| Cohort | Authorized Mask Source (`G04 Audited`) | Prohibited / Broken Asset | Extraction & Multi-ROI Union Formula | Verification Gate (`STEP-016–018`) |
|---|---|---|---|---|
| **`DS0006 CDD-CESM LE`** | `Radiology_hand_drawn_segmentations_v2.csv` (`1,797` `DM` polygons across `657` `LE` images) | Exclude `_CM_` subtracted polygons (`RF15`) | Parse `region_shape_attributes` JSON (`all_points_x`, `all_points_y`); rasterize every polygon `region_id` for that `#filename` via `cv2.fillPoly(..., 1)` and take logical **OR union** across all regions onto native `(Height, Width)` | Verify `0 <= x < Width`, `0 <= y < Height`, non-empty mask (`area > 0`) on 100% of `657` annotated `LE` scans |
| **`DS0005 BMCD`** | Paired `*_GT.jpg` color overlays (`392` retained pairs) | None | Extract chromatic radiologist ink (`max(R,G,B) - min(R,G,B) > 25`), fill interior contours/connected loops if hollow (`calibrated on STEP-016 pilot`), and map via `INTER_NEAREST` + aspect ratio check to native DICOM `(Height, Width)`; zero-mask for negative controls (`Normal_cases` blank overlay = empty mask verified) | Verify `*_GT.jpg` aspect ratio matches DICOM `W/H` within `< 1%` before resizing (`normal scans expected empty; suspicious recent scans expected >0`) |
| **`DS0002 DMID`** | **`Pixel-level annotation/*.tif`** (`269/269` valid `RGBA` overlays) cross-checked vs `Metadata.xlsx (x, y, radius)` | **Hard-Ban `ROI Masks/*.tif`** (`268/269` fail `libtiff` `decoder error -2` due to malformed `SampleFormat=(1,1,1)` tag!) | Extract colored outline/fill channels (`max(R,G,B) - min(R,G,B) > 25`, morphological hole fill) on matching native `(Height, Width)` grid; verify overlay centroid lies within documented `(x, y, radius)` circle | Assert exact `(Width, Height)` equality vs `.dcm` & positive foreground overlap with breast tissue (`zero background-only masks`) |
| **`DS0001 MIAS`** | `00README.pdf` circle coordinates `(x, y, radius)` | None | Rasterize binary circle `(col - x)^2 + (row - (Height - y_mias))^2 <= radius^2` (honoring MIAS bottom-left origin y-flip!) strictly for coarse circular SFM audit | Flag missing-radius diffuse lesions (`Excluded_NoRadiusForROI`) and visually verify top-vs-bottom y-origin orientation on pilot overlay |
| **`DS0003 CMMD`** | `None` (`0` native masks) | — | Marked `LocalizationEligible = False` (used for classification, calibration, faithfulness & Adebayo sanity) | Confirm zero synthetic masks generated or invented |

---

## 6. Strict Post-Hoc-Only XAI Localization Boundary (`Zero Mask Leakage`)

1. Binary ROI masks, VIA polygons, `*_GT.jpg`, `Pixel-level annotation/*.tif`, and `(x, y, r)` coordinates MUST reside solely inside Tier-2 mask archives indexed by `label_registry.csv`.
2. Training data loaders, image preprocessing crops (`STEP-019/021`), model weights, and inference inputs MUST have **zero runtime access** to mask directories (`enforced via isolated manifest config & unit assertions verifying identical classifier logits with mask files absent`).
3. Masks are consumed **exclusively post-hoc inside `src/bc_xai/xai/`** (`STEP-035`) to compute `Pointing Game`, `EBPG`, and `IoU/Dice` on test saliency maps.

---

## 7. Pilot Sample Stratification, Adjudication & Acceptance Criteria (`STEP-016`–`STEP-018`)

- **Deterministic Pilot Set (`STEP-016`, `N = 170` retained scans, fixed seed `20261128`):**
  - `DS0003 CMMD`: `60` scans (`20 Malignant`, `20 Benign`, `10 bilateral-discordant side pairs`, `10 UnlabeledContralateral`, `plus mandatory inclusion of 2x 16-bit IMG00003519–3520`).
  - `DS0006 CDD-CESM LE`: `40` scans (`15 Malignant + mask`, `15 Benign + mask`, `10 Normal` + `spot verification of postop/postNAC exclusions`).
  - `DS0005 BMCD`: `24` scans (`8 recent Biopsy-Malignant/DCIS + *_GT.jpg`, `8 recent Biopsy-Benign + *_GT.jpg`, `4 Normal_cases`, `4 prior baseline scans`).
  - `DS0002 DMID`: `30` scans (`10 M + RGBA mask`, `10 B + RGBA mask`, `5 NORM`, `5 ambiguous 'N' token checks`).
  - `DS0001 MIAS`: `16` scans (`6 M + circle`, `6 B + circle`, `4 NORM`; verifying MIAS y-origin flip alignment!).
- **Acceptance Thresholds for `G06` Freeze (`STEP-018`):**
  1. `100%` arithmetic closure per cohort: `Benign + Malignant + NormalControl + ProtocolExcluded == G04_Retained`.
  2. `0` unmapped label tokens, `0` unadjudicated `XLS`-vs-`TXT` severe contradictions, `0` corrupt masks inside `LocalizationEligible` subset.
  3. Pilot overlay inspection error rate `< 2%` on mask alignment/orientation (`and 100% of detected issues fixed/adjudicated cleanly in 04_Labels_XAI_Governance/adjudications/` before `LBL####` freeze).

---

## 8. Protocol Version, Checksum & Human Approval Status

- **Protocol Version:** `v1.0.0` (`Ratified at G05 PASS — 2026-11-28`)
- **SHA-256 Digest:** Verified and recorded in [G05_assessment_2026-11-28.md](../../01_Project_Management/reviews/G05_assessment_2026-11-28.md) alongside [XAIP0001.md](../xai_protocols/XAIP0001.md) upon `G05 PASS` ratification (`2026-11-28`).
- **Human Ratification (`G05 PASS`):** Approved (`2026-11-28`) by Research Owner/User alongside Supervisor **Israt Jahan**, **Md Riyadul Hasan** (`232-15-486`), and **Alzubair Ahamed** (`232-15-591`), preserving documented `UD18` advisor/fallback rules.

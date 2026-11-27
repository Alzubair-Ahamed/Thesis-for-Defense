# Diagnostic Label Verification & ROI-Mask Standardization Protocol (`T09` — `v1.0.1`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T09` (`T09_label_mask_protocol.md`) |
| `template_version` | `v1.0.1` *(Clarification & Operational Refinement Addendum to [v1.0.0](./label_mask_protocol_v1.0.0.md))* |
| `entity_id` | `T09_LABEL_MASK_PROTOCOL_v1.0.1` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Label/Mask Lead) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-28` (`v1.0.0` Ratified `G05`; `v1.0.1` Updated & Accepted upon `STEP-016` Pilot Pass `2026-11-28`) |
| `status` | `Approved Addendum (G05 Current + STEP-016 Pilot Accepted 2026-11-28)` |
| `source_inputs` | [label_mask_protocol_v1.0.0.md](./label_mask_protocol_v1.0.0.md); [pilot_label_mask_audit.md](../reviews/pilot_label_mask_audit.md); [STEP016_pilot_discrepancies.md](../adjudications/STEP016_pilot_discrepancies.md); [verify.py](../../src/bc_xai/labels/verify.py) |
| `governing_section` | [OS §4.3, §6.1, §14.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-016](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-016) |
| `sensitivity` | Tier-1 Ratified Protocol Specification (`raw patient metadata stays in Tier-2`) |
| `reviewer` | User/Research Owner; Israt Jahan (Supervisor); Md Riyadul Hasan (`232-15-486`); Alzubair Ahamed (`232-15-591`) — `STEP-016` Pilot & `v1.0.1` Clarifications Approved `2026-11-28` |

> **Version Change Note (`v1.0.0 -> v1.0.1`):** Preserves `100%` of `v1.0.0` classification paradigm (`UD07`), dual `Tier-A` Biopsy vs `Non-Malignant` tracks (`UD08`), and post-hoc mask non-leakage boundary (`UD09`), while encoding `7` empirical refinements discovered and visually proved on the `N = 170` `STEP-016` pilot ([STEP016_pilot_discrepancies.md](../adjudications/STEP016_pilot_discrepancies.md)). [label_mask_protocol_v1.0.0.md](./label_mask_protocol_v1.0.0.md) stays immutable on disk as the historical `G05` baseline reference.

---

## 1. Classification Paradigm Rule (`UD07` — FFDM Whole-Breast vs ROI/Patch Isolation)

1. **Selected Paradigm (`Option A` — Strict Whole-Image 2D Classification):**
   - Whole-breast `2D` mammograms (`CC` and `MLO` views) — **never** cropped lesion patches (`RF05`, `RQ3`).
2. **Absolute Track Segregation (`Zero Conflation`):**
   - **Primary Internal Biopsy `FFDM` Development Track:** **`DS0003 CMMD`** (`5,196` `G04`-retained DICOMs). Standard DICOM SNOMED `ViewCodeSequence` (`399162004 = CC`, `399368009 = MLO`) resolves view position deterministically where `ViewPosition` (`0018,5101`) is blank (`ADJ-016-07`).
   - **Primary Quantitative `FFDM` Localization & Secondary `FFDM` Track:** **`DS0006 CDD-CESM LE`** (`1,003` Low-Energy `DM` scans; `1,003` subtracted `CESM CM` scans excluded per `RF15`).
   - **Zero-Shot External `FFDM` Validation & Density/Localization Tracks:** **`DS0005 BMCD`** (`392` `12-bit` FFDM DICOMs) and **`DS0002 DMID`** (`507` Indian FFDM DICOMs — restricted to external evaluation because DICOM headers omit cross-view `PatientID`).
   - **Zero-Shot External Digitized-Film (`SFM`) Cross-Domain & Marker-Shortcut Track:** **`DS0001 MIAS v1.21`** (`322` `MLO` PGMs). Never pooled with `FFDM` training data.
3. **Lesion Morphology Treatment (`mass` vs `calcification`):** Evaluated strictly via `RQ4` subgroup attributes, never siloed models.

---

## 2. Binary Ground-Truth Label Mapping (`0 = Benign`, `1 = Malignant`) & Provenance (`UD08`)

Every image across `7,420` `G04`-retained scans receives a deterministic `BinaryTarget` (`0`, `1`, or `Excluded`), `LabelProvenanceTier` (`TierA_Biopsy`, `TierA_Biopsy_NormalControl`, `TierB_Radiology_BIRADS`, `TierB_Historical_SFM`, or `Excluded`), and explicit sub-track eligibility (`SubTrackA_BiopsyEligible`, `SubTrackB_ScreeningEligible`, `LesionTrack_BenignVsMalignant`):

| Cohort (`Retained`) | Join Key & Scope Rule | Mapped `1 = Malignant` | Mapped `0 = Benign` (`Biopsy / Lesion`) | Conditional `0` (`Non-Malignant + Normal`) | Explicit `Excluded_*` Buckets (`STEP-016–018`) |
|---|---|---|---|---|---|
| **`DS0003 CMMD`** (`5,196`) | `ID1 == DICOM PatientID` + `LeftRight == ImageLaterality` (`+ ViewCodeSequence CC/MLO`) | `classification == 'Malignant'` (`TierA_Biopsy`) | `classification == 'Benign'` (`TierA_Biopsy`) | *N/A (`0` annotated Normal rows)* | `~1,452` unannotated contralateral (`Excluded_UnlabeledContralateral`); `D1-0808` & `D1-1292` companion views (`Excluded_CrossLabelClonePatient`); `6` `G04` clones |
| **`DS0006 CDD-CESM LE`** (`1,003`) | `Image_name` (`Type == 'DM'`) in `Radiology-manual-annotations.xlsx` (`all`) | `Pathology == 'Malignant'` (`flag OccultOnDM_BIRADS_1_2 if DM BIRADS<=2`) | `Pathology == 'Benign'` (`581` pure biopsy alongside Malignant) | `Pathology == 'Normal'` (`flag DM_BIRADS_3_5_ClearedNormal if LE BIRADS>=3`; **fail loudly if non-NAC `BIRADS=6`**) | `80` `postoperative` LE (`Excluded_PostOperative`); `4` `postneoajuvant chemotherapy` LE (`Excluded_PostNAC_BIRADS6`) |
| **`DS0005 BMCD`** (`392`) | `Normal_cases/#` & `Suspicious_cases/#` + `prior/recent` (`tolerate Zenodo typos recemt/reent/.Jpg read-only + flag UpstreamFilenameTypo_*`) | `recent` `Suspicious_cases` with `Biopsy in {'MALIGNANT', 'DCIS'}` | `recent` `Suspicious_cases` with `Biopsy == 'BENIGN'` | `Normal_cases` `BI-RADS 1–2` (`recent` & `prior` tagged separately for optional `recent`-only sensitivity) | `prior` `Suspicious_cases` (`Excluded_PriorScreeningRound`); `18` suspicious `NOT AVAILABLE` (`Excluded_UnconfirmedBiopsy`); `8` `G04` clones |
| **`DS0002 DMID`** (`507`) | `IMG###` stem -> `Metadata.xlsx` (`strip whitespace, normalize CCLRT`) cross-checked vs `Reports/Img*.txt` | Any row `'M'` (incl. `20` `[B,M]` via malignant dominance; zero `'N'`) | `'B'` only (`LesionTrack` `TierB`, never pooled into `TierA_Biopsy`) | `'NORM'` (`disclosed NonMalignant`; flag any `XLS`-vs-`TXT` BI-RADS contradictions) | All `'N'` images incl. mixed `[B,N]` `IMG125` (`Excluded_AmbiguousClassToken_N`); `3` `G04` clones |
| **`DS0001 MIAS`** (`322`) | `mdb###` stem -> `00README.pdf` (`incl. *** see note 2 diffuse rows`) | Historical `'M'` (`TierB_Historical_SFM`) | Historical `'B'` (`TierB_Historical_SFM`) | `'NORM'` (`SFM_NonMalignant` track only) | Any corrupt/unparsed row |

---

## 3. Inclusion / Exclusion & Concordance Rules (`ADJ-016-05` Addendum)

1. **Zero Silent `Normal -> Benign` Merging:** Always isolate `SubTrackA` (`Tier-A` Biopsy Benign vs Malignant) from `SubTrackB` (`Benign + Normal` vs Malignant) and `Tier-B` (`DMID`, `MIAS`) metrics.
2. **`CDD-CESM` Cleared `DM` & Occult Cancers (`v1.0.1` Clarification):**
   - `Normal` pathology on LE scans carrying `DM BI-RADS 3–4` (`cleared by negative subtracted CESM`) is valid and flagged `DM_BIRADS_<k>_ClearedNormal`; only `Normal + BI-RADS 6` outside NAC aborts validation.
   - Biopsy-proven `Malignant` scans carrying `DM BI-RADS 1–2` (`occult on unenhanced 2D mammography`) remain `Target = 1` and are tagged `OccultOnDM_BIRADS_<k>` for `STEP-037` false-negative analysis.
3. **`DMID` Token `'N'` & `BMCD` Filename Typos:** Strictly exclude `'N'` (`zero coercion`); resolve `BMCD` upstream `CC_recemt.dcm`, `CC_reent_GT.jpg`, `MLO_reent_GT.jpg`, `.Jpg` read-only with explicit `UpstreamFilenameTypo_*` / `UpstreamGTTypo_*` flags.

---

## 4. Multi-Lesion Precedence Rule (`Malignant Dominance`)

- Unchanged from `v1.0.0`: Breast-side/image-level Malignant dominates (`any M -> 1`, mixed `[B, N] -> Excluded_AmbiguousClassToken_N`); CMMD keeps independent L/R breast-side pathology (`BilateralDiscordantPatient` flagged) alongside `max(L, R)` patient-level aggregation.

---

## 5. Lesion ROI-Mask Coordinate Convention, Color Filtering & Union Rules (`UD09`, `v1.0.1` Updated)

Canonical masks are binary `uint8` (`0/1`) arrays matching native image `(Height, Width)`:

| Cohort | Authorized Mask Source | Prohibited / Filtered Asset (`v1.0.1` Clarified) | Extraction & Multi-ROI Union Formula | Verification & Exclusion Gate (`STEP-016–018`) |
|---|---|---|---|---|
| **`DS0006 CDD-CESM LE`** | `Radiology_hand_drawn_segmentations_v2.csv` (`1,797` `DM` rows across `657` scans) | Exclude `_CM_` rows (`RF15`) | Rasterize OR-union across **all `5` VIA JSON primitives** (`ADJ-016-04`): `polygon` (`cv2.fillPoly`), `ellipse` (`cv2.ellipse` w/ `theta`), `circle` (`cv2.circle`), `polyline` (`cv2.fillPoly` if `>=3` pts else `polylines`), `point` (`r=5px` disk). | Assert non-empty (`area > 0`) and valid bounds on `100%` of segmented retained `LE` scans. |
| **`DS0005 BMCD`** | Paired `*_GT.*` (`case-insensitive`, incl. `recemt/reent`) | **Exclude `Green` calibration ruler/scale bar (`G > max(R,B)`)** present on `Normal` & `Suspicious` GTs (`ADJ-016-01`); **exclude bottom red margin bars (`ADJ-016-02`)** | Extract ONLY **`Red` benign microcalcifications** (`R - max(G,B) > 35`) OR **contour-filled `Blue` suspicious circles** (`B - max(R,G) > 35` -> `cv2.drawContours(..., -1)`), then `INTER_NEAREST` rescale to DICOM `(H, W)` (`aspect error < 1%`). **Hard Rule (`ADJ-016-02`):** If `>50%` of lesion-channel pixels (with `>50` red px) reside in the bottom `12%` air margin (`y > 0.88 * H`, e.g. `IMG00000627`), set `MaskStatus = flagged_border_red_bar` and **`LocalizationEligible = False`**. | Verify `aspect_rel_err < 0.01`, `0` ruler-bar contamination in `Normal` (`BI-RADS 1` empty), and `LocalizationEligible = False` on border-bar artifacts. |
| **`DS0002 DMID`** | **`Pixel-level annotation/*.tif`** (`269/269` `RGBA`) | **Hard-Ban `ROI Masks/*.tif`** (`268/269` corrupt `libtiff error -2`) | Threshold `max(R,G,B) - min(R,G,B) > 35` on RGB channels and fill hollow boundary rings via external contour interior fill (`cv2.drawContours(..., -1)`, `ADJ-016-06`). | Assert exact `(Width, Height) == DICOM (W, H)` & `filled_px >= outline_px > 0`. |
| **`DS0001 MIAS`** | `00README.pdf` `(x, y, radius)` | Exclude `*** see note 2` (`mdb216rl`, `mdb233lm`, `mdb245ls`, `ADJ-016-07`) | Rasterize `(col - x)^2 + (row - (Height - y_mias))^2 <= r^2` honoring verified bottom-left **Y-flip** (`ADJ-016-07` visual proof). | `100%` Y-flip alignment inside breast parenchyma (`Excluded_NoRadiusForROI` flagged cleanly). |
| **`DS0003 CMMD`** | `None` (`0` native masks) | — | `LocalizationEligible = False` (`0` invented boxes). | Confirm zero synthetic masks generated. |

---

## 6. Strict Post-Hoc-Only XAI Localization Boundary (`Zero Mask Leakage`)

- Unchanged from `v1.0.0`: ROI masks reside solely inside Tier-2 archives indexed by `label_registry.csv` and are consumed strictly post-hoc inside `src/bc_xai/xai/` (`STEP-035`).

---

## 7. `STEP-016` Pilot Acceptance & `STEP-017–018` Gate (`G06`) Criteria

- **`STEP-016` Pilot (`N = 170`, `seed = 20261128`):** Executed and visually verified `2026-11-28` across `DS0001 (16)`, `DS0002 (30)`, `DS0003 (60)`, `DS0005 (24)`, `DS0006 (40)` with `5/5` arithmetic closure (`True`), `24/24` passing tests, and `0%` post-fix alignment errors ([pilot_label_mask_audit.md](../reviews/pilot_label_mask_audit.md)) — **Pilot Accepted (`2026-11-28`)**.
- **`G06` Full Freeze Criteria (`STEP-017–018`):** `100%` cohort closure (`7,420` retained + `17` `G04` quarantined = `7,437` acquired), `0` unmapped tokens, `0` corrupt masks in `LocalizationEligible`, and stratified full-corpus spot-overlay verification ahead of `LBL####` freeze.

---

## 8. Version Lineage & Approval Record

- **Supersedes:** [label_mask_protocol_v1.0.0.md](./label_mask_protocol_v1.0.0.md) (`v1.0.0` preserved untouched for `G05 PASS` audit trail).
- **Approved By (`2026-11-28`):** User/Research Owner alongside `G05`-ratified governance rules, accepting `STEP-016` pilot, `BMCD` bottom red-bar `LocalizationEligible = False` isolation, and `v1.0.1` wording update to unlock `STEP-017` (`--mode full`).

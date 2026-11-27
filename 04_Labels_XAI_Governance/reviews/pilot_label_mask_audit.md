# Pilot Label Verification & ROI-Mask Alignment Audit (`STEP-016` — `N = 170`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T10` (`T10_label_audit_report.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `STEP016_PILOT_LABEL_MASK_AUDIT_v1.0.0` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Label/Mask Lead) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-28` (`Executed & Accepted 2026-11-28`) |
| `status` | **`PILOT_ACCEPTED_2026-11-28`** (`T09 v1.0.1 Adopted; STEP-017 Full Verification Unlocked`) |
| `source_inputs` | [label_mask_protocol_v1.0.1.md](../protocols/label_mask_protocol_v1.0.1.md); [label_mask_protocol_v1.0.0.md](../protocols/label_mask_protocol_v1.0.0.md); [verify.py](../../src/bc_xai/labels/verify.py); [test_label_verify.py](../../tests/test_label_verify.py); [datasets.csv](../../03_Datasets/datasets.csv); `04_Labels_XAI_Governance/native/pilot_verification_summary.json` (Tier-2) |
| `governing_section` | [OS §4.3, §6.1, §14.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [Blueprint STEP-016](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-016) |
| `sensitivity` | Tier-1 Aggregate Audit Report (`per-image paths & raw pixel overlays segregated in Tier-2`) |
| `reviewer` | User/Research Owner; Israt Jahan (Supervisor); Md Riyadul Hasan; Alzubair Ahamed — Pilot Accepted `2026-11-28` |

---

## 1. Parent DatasetID (`DS####`) & Immutable Manifest Hashes

| `DatasetID` | Cohort | Modality / Paradigm | Acquired Primary (`Retained` at `G04`) | Parent `ManifestHash` (`datasets.csv`) |
|---|---|---|---:|---|
| `DS0001` | `MIAS v1.21` | `SFM` (`MLO`-only) | `322` (`322`) | `2e3f8559ed425aee3d716174767558d2e8adf41c017915eecefb81da9ec9fdf1` |
| `DS0002` | `DMID` | `FFDM` (`8-bit DICOM`) | `510` (`507`) | `40882b4e5506f11675acccee1776e7469de1713bad0fabe9a33d0898892cf5da` |
| `DS0003` | `CMMD` | `FFDM` (`5,200 8b + 2 16b`) | `5,202` (`5,196`) | `b933e5f7efb3767ea92143a0bc652d5c81fdc33f024df6f5fefee98537c4f6ed` |
| `DS0005` | `BMCD` | `FFDM` (`12-bit uint16`) | `400` (`392`) | `4a1faa4ceeb921b6694c0458e4a7ce6702b5471deda259d9784121a08e989efe` |
| `DS0006` | `CDD-CESM (LE)` | `Low-Energy DM FFDM` | `1,003` (`1,003`) | `e1732776952a7562a811b16800924563a33cc645f72fd33aa056a38a0919ecd4` |

*(Partial `DS0004_CBIS_DDSM` local cropped/ROI directory remains untouched outside active scope per `G04 PASS`.)*

---

## 2. Pilot Scope, Sampling Seed (`20261128`), & Protocol (`T09 v1.0.0`)

- **Execution Scope:** Stratified deterministic pilot verification (`--mode pilot`, **`seed = 20261128`**) executed via [verify.py](../../src/bc_xai/labels/verify.py) across all `5` clean `G04` cohorts (`N = 170` total scans sampled prospectively across Benign, Malignant, Normal, bilateral-discordant, ambiguous-token, post-treatment, prior-round, and `16-bit` DICOM edge strata).
- **Automated Arithmetic Closure (`Target 0 + Target 1 + Excluded == PilotSample`):** **`100%` (`True` on all `5/5` cohorts; `0` unmapped label tokens)**.
- **Unit Test Verification:** `24 passed, 3 warnings in 4.99s` across `tests/` (`including 5 dedicated synthetic test suites in` [test_label_verify.py](../../tests/test_label_verify.py)).

---

## 3. Reconciled Pilot Target, Sub-Track & Pathology/BI-RADS Concordance Counts

| Cohort | Pilot `N` | Target `0` (`Benign / Normal`) | Target `1` (`Malignant`) | `Excluded` | `SubTrack A` (`Tier-A Biopsy`) | `SubTrack B` (`Screening`) | `LesionTrack` (`B vs M`) | `Closure OK` |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`DS0001 MIAS`** | `16` | `10` (`6 B + 4 Norm`) | `6` | `0` | `0` *(SFM Tier-B)* | `16` | `12` | `True` |
| **`DS0002 DMID`** | `30` | `15` (`10 B + 5 Norm`) | `10` | `5` (`'N' token`) | `0` *(Tier-B)* | `25` | `20` | `True` |
| **`DS0003 CMMD`** | `60` | `22` (`Benign`) | `25` | `13` (`Contralateral`) | `47` | `47` | `47` | `True` |
| **`DS0005 BMCD`** | `24` | `12` (`8 B + 4 Norm`) | `8` (`6 DCIS + 2 Mal`) | `4` (`Prior Round`) | `16` | `20` | `16` | `True` |
| **`DS0006 CDD-CESM LE`** | `40` | `20` (`15 B + 5 Norm`) | `15` | `5` (`PostOp`) | `30` | `35` | `30` | `True` |
| **Pilot Total** | **`170`** | **`79`** | **`64`** | **`27`** | **`93`** | **`143`** | **`125`** | **`5/5 True`** |

### Key Metadata & Concordance Findings (`STEP-016` Empirical Schema Audit)
1. **`DS0003 CMMD` View Tags (`ViewCodeSequence` Recovery):** `ds.ViewPosition` is blank across CMMD headers, but standard DICOM SNOMED `ViewCodeSequence` codes (`399162004 = CC`, `399368009 = MLO`) cleanly resolve `100%` of `CC` vs `MLO` views (`visually verified on 16/16 CMMD panels`). Both `16-bit uint16` scans (`IMG00003519`, `IMG00003520`) decoded cleanly, and `11` sampled scans belonged to `BilateralDiscordantPatient` cases (`sides preserve distinct L/R biopsy truth`).
2. **`DS0006 CDD-CESM LE` Occult Cancers & Cleared BI-RADS (`Critical Clinical Finding`):** Cross-tabulating the full `1,003`-row LE sheet against `CESM` rows revealed legitimate clinical imaging behavior that naive BI-RADS hard-filters would wrongly crash on or misclassify:
   - `9` LE `Normal` scans carry `DM BI-RADS 3–4` (`e.g. P147_R_DM_CC` distortion `BI-RADS 4`), yet subtracted `CESM CM` was negative (`BI-RADS 1`) and follow-up/pathology confirmed `Normal` -> tracked transparently via `DM_BIRADS_<k>_ClearedNormal` flag (`only BI-RADS 6 outside NAC fails loudly`).
   - `11` LE `Malignant` scans (`P29_L`, `P38_R`, `P111_R_CC`, `P137_L`, `P214_L`, `P221_L`, `P230_R`, `P299_R_MLO`) appear radiographically occult on 2D LE mammography (`DM BI-RADS 1–2`) -> tracked transparently via `OccultOnDM_BIRADS_<k>` for `STEP-037` false-negative analysis.
3. **`DS0002 DMID` Multi-Lesion & Report Concordance:** Pilot included `3` multi-lesion `['B', 'M']` scans (`IMG00000142`, `IMG00000445`, `IMG00000446`) cleanly resolved via Malignant Dominance (`T09 §4`), and `5` `'N'` exclusions verified against `Reports/Img*.txt` (`4 BI-RADS 4`, `1 BI-RADS 3`). Cross-checking all `510` DMID rows confirms `21` multi-class scans (`20 [B,M]` + `1 [B,N]` `IMG125`).
4. **`DS0001 MIAS` Diffuse Notes:** `3` diffuse malignant calcifications in `00README.pdf` (`mdb216rl`, `mdb233lm`, `mdb245ls`) omit numeric `(x, y, radius)` with `*** see note 2`; parser cleanly maps labels `M` (`CALC`) while marking `MaskStatus = excluded_by_protocol` (`Excluded_NoRadiusForROI`).

---

## 4. Automated ROI-Mask Geometry & Orientation Verification

| Cohort | Mask Extraction Rule (`verify.py`) | Pilot `LocalizationEligible` | `ok_nonempty` | `ok_expected_empty` | `Excluded / Non-Appl / Flagged` | Observed Alignment Notes |
|---|---|---:|---:|---:|---:|---|
| **`DS0001`** | `MIAS_Circle_YFlip` (`row = H - y`) | `12` | `12` | `4` | `0` | **Visual `YFlip` verified `12/12` vs `top-left` air misfire** |
| **`DS0002`** | `DMID_RGBA_ContourFill` (`diff > 35` + external contour fill; hard-ban `ROI Masks/`) | `20` | `20` | `5` | `5` `not_applicable` | Hollow outlines filled cleanly onto lesions (`0` read errors) |
| **`DS0003`** | `None` (`0` native masks per `T09 §5`) | `0` | `0` | `0` | `60` `not_applicable` | Zero invented boxes (`clean FFDM classification/faithfulness`) |
| **`DS0005`** | `BMCD_GT_Chromatic` (`Red + filled Blue ONLY`; **exclude Green ruler bar**; aspect check `< 1%`) | `18` | `18` | `1` | `4 excl + 1 flagged_border_red_bar` | Caught `Green` ruler bar across all panels + `IMG00000627` red margin bar |
| **`DS0006`** | `VIA_MultiPrimitive` (**all 5 shapes**: `polygon`, `ellipse`, `circle`, `polyline`, `point`) | `30` | `30` | `5` | `5` `excluded_by_protocol` | All `1,797` DM VIA rows span 5 shape primitives (`not polygon alone`) |

---

## 5. Stratified Visual Overlay Spot-Inspection Evidence (`Tier-2`)

Visual inspection of all `5` restricted Tier-2 overlay contact sheets (`04_Labels_XAI_Governance/restricted_masks/pilot_overlays/DS000*_pilot_overlays.png`, pseudonymous IDs only):
1. **`DS0001_pilot_overlays.png` (`16/16` shown):** `12/12` flipped cyan circles (`Height - y_mias`) center accurately on breast lesions (`top-to-bottom inversion confirmed — all non-flipped yellow reference circles fall into empty dark air beneath breast!`); `4/4` `Normal_Control` scans are mask-free. Observed `MIAS` film labels (`R ML`, `L ML`, `L MED-LAT OBL`) for `RISK0004`.
2. **`DS0002_pilot_overlays.png` (`16/30` shown):** `12/12` shown lesion overlays accurately fill circumscribed masses, spiculated lesions, and multifocal clusters; `4/4` shown `Excluded_AmbiguousClassToken_N` frames (`e.g. IMG00000028` visible calc cluster) visually validate rejecting `'N'`.
3. **`DS0003_pilot_overlays.png` (`16/60` shown):** SNOMED `CC` (`IMG00003519`) vs `MLO` (`IMG00003520` + pectoral wall) tags match `16/16` panels cleanly (`occasional small round BB nipple markers noted for RISK0004`).
4. **`DS0005_pilot_overlays.png` (`14/24` shown):** Visually confirmed **`Green` pixels in BMCD `*_GT.jpg` (`rendered yellow` on sheet) are calibration ruler scale bars**, NOT calcifications — proving green exclusion mandatory. Benign/suspicious red calc dots & blue circles hug true findings, **except `IMG00000627`**, which shows a large horizontal red margin bar at `y > 0.88h` alongside a small true calcification -> flagged (`BMCD_GT_BottomMarginRedBar`) & excluded from `LocalizationEligible`.
5. **`DS0006_pilot_overlays.png` (`16/40` shown):** Polygons, ellipses, circles, and multi-region skin-thickening contours (`e.g. IMG00000259` `Malignant` mass + skin ribbon) align accurately inside variable cropped breast frames (`0%` spatial offset).

---

## 6. Discrepancy Summary & `STEP-016` Adjudication Outcome

All `7` structural/protocol findings identified during `STEP-016` are closed and codified in [STEP016_pilot_discrepancies.md](../adjudications/STEP016_pilot_discrepancies.md) and [label_mask_protocol_v1.0.1.md](../protocols/label_mask_protocol_v1.0.1.md):
- **Operationalized cleanly in code + unit tests (`6/7`):** `DS0006` 5 VIA primitives, `DS0006` cleared BI-RADS `3–4` / occult BI-RADS `1–2` concordance flags, `DS0005` Green ruler bar exclusion & Zenodo filename typos (`recemt/reent/.Jpg`), `DS0002` hollow RGBA contour fill, `DS0003` SNOMED `ViewCodeSequence`, `DS0001` `*** see note 2` fallback.
- **Ratified Pilot Decision (`ADJ-016-02` + `T09 v1.0.1`, `2026-11-28`):** **`BMCD` `IMG00000627`-like bottom-margin red-bar masks (`BMCD_GT_BottomMarginRedBar`) are permanently marked `LocalizationEligible = False`**, and protocol addendum [label_mask_protocol_v1.0.1.md](../protocols/label_mask_protocol_v1.0.1.md) is approved for **`STEP-017` full execution**.

---

## 7. Tier-2 Artifact Inventory & Next Step

- **Tier-2 Pilot Outputs (Gitignored):**
  - `04_Labels_XAI_Governance/native/pilot_verification_summary.json`
  - `04_Labels_XAI_Governance/native/DS000{1,2,3,5,6}_pilot_labels.csv`
  - `04_Labels_XAI_Governance/restricted_masks/pilot_overlays/DS000{1,2,3,5,6}_pilot_overlays.png`
- **Next Step:** Execute full-corpus **`STEP-017`** (`--mode full` across `7,420` retained / `7,437` primary acquired scans) -> `STEP-018` `LBL####` freeze (`G06`).

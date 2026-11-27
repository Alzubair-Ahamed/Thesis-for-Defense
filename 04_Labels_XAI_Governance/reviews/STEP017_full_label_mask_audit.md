# Full-Corpus Label & ROI-Mask Audit Report (`STEP-017` — All `5` Clean `CC BY` Cohorts)

| Header Field | Value |
|---|---|
| `TemplateID` | `T10` (`T10_label_audit_report.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `STEP017_FULL_LABEL_MASK_AUDIT_2026-11-28` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Label & Mask Harmonization Lead) & Alzubair Ahamed (`232-15-591`, Cross-Check Verifier) |
| `date` | `2026-11-28` |
| `status` | `CLOSED AT STEP-017 (2026-11-28) — All Adjudications Settled (incl. ADJ-017-02 Option B), Ready for STEP-018 LBL#### Freeze & G06` |
| `source_inputs` | [label_mask_protocol_v1.0.1.md](../protocols/label_mask_protocol_v1.0.1.md) (`T09 v1.0.1`) + `ADJ-017-02` Option B; [verify.py](../../src/bc_xai/labels/verify.py); `04_Labels_XAI_Governance/native/full_verification_summary.json` (`Tier-2`); `04_Labels_XAI_Governance/native/DS000{1,2,3,5,6}_full_labels.csv` (`Tier-2`); `04_Labels_XAI_Governance/restricted_masks/pilot_overlays/DS000{1,2,3,5,6}_full_overlays.png` (`Tier-2`) |
| `governing_section` | [OS §4.3, §6.1, §13.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-017](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-017) |
| `sensitivity` | Tier-1 Public Audit Summary (`0` raw paths or PII; scan-level `RawRelativePath` and `MaskRelativePath` remain strictly gitignored in Tier-2) |
| `reviewer` | User/Research Owner (`ADJ-017-02` Option B Ratified `2026-11-28`); Israt Jahan (Supervisor) |

---

## 1. Execution Scope & `100%` Primary-Acquired / `G04`-Retained Reconciliation

After `STEP-016` pilot acceptance (`4584f6d`) and owner ratification of **`ADJ-017-02` Option B (`Excluded_ReportMetadataDiscordance`)**, deterministic full-corpus verification ran across **`100%` of primary acquired scans (`N = 7,437`, comprising `7,420` `G04`-retained images + `17` `G04`-quarantined pixel clones)** with `--mode full --seed 20261128` (`exit code = 0`).

| Cohort (`DatasetID`) | Primary Acquired | `G04` Quarantined Clones | `G04` Retained | Full Audited | Arithmetic Closure (`AC = Retained + Clones = Audited`) |
|---|---:|---:|---:|---:|---|
| **`DS0001` (`MIAS v1.21`)** | `322` | `0` | `322` | **`322`** | **`True`** (`322 / 322`) |
| **`DS0002` (`DMID`)** | `510` | `3` | `507` | **`510`** | **`True`** (`510 / 510`) |
| **`DS0003` (`CMMD`)** | `5,202` | `6` | `5,196` | **`5,202`** | **`True`** (`5,202 / 5,202`) |
| **`DS0005` (`BMCD`)** | `400` | `8` | `392` | **`400`** | **`True`** (`400 / 400`) |
| **`DS0006` (`CDD-CESM LE`)** | `1,003` | `0` | `1,003` | **`1,003`** | **`True`** (`1,003 / 1,003`) |
| **Total (`5` Clean `CC BY` Cohorts)** | **`7,437`** | **`17`** | **`7,420`** | **`7,437`** | **`5 / 5 True (0 Unmapped Tokens)`** |

---

## 2. Full-Corpus Binary Target, Class, Provenance & Modeling Track Breakdown

Per `T09 v1.0.1` (`UD08`) and `ADJ-017-02` Option B, every image receives a deterministic `BinaryTarget`, `LabelClass`, `LabelProvenanceTier`, and non-conflated modeling track flags:

| Cohort | Binary `0` (`Benign / Normal`) | Binary `1` (`Malignant`) | `Excluded` | `SubTrackA` (`Tier-A` Biopsy Only) | `SubTrackB` (`Screening w/ Normal`) | `LesionTrack` (`Benign vs Malignant`) | `LocalizationEligible` (`ok_nonempty`) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **`DS0001` (`MIAS v1.21`)** | `271` (`64 Benign_Lesion + 207 Normal_Control`) | `51` (`Malignant`) | `0` | `0` | `322` | `115` | `109` (`61 B + 48 M`) |
| **`DS0002` (`DMID`)** | `342` (`143 Benign_Lesion + 199 Normal_Control`) | `128` (`Malignant`) | `40` (`35 Token_N + 3 Clones + 2 ReportDiscordant`) | `0` | `470` | `271` | `264` (`141 B + 123 M`) |
| **`DS0003` (`CMMD`)** | `1,110` (`Benign_Biopsy`) | `2,628` (`Malignant`) | `1,464` (`1,456 Contralat + 6 Clones + 2 CrossClonePat`) | `3,738` | `3,738` | `3,738` | `0` (`N/A`) |
| **`DS0005` (`BMCD`)** | `238` (`42 Benign_Biopsy + 196 Normal_Control`) | `22` (`12 DCIS + 10 MALIGNANT`) | `140` (`98 Prior + 34 Unconf + 8 Clones`) | `64` | `260` | `64` | `175` (`42 B + 11 DCIS + 10 M + 112 Norm`) |
| **`DS0006` (`CDD-CESM LE`)** | `615` (`277 Benign_Biopsy + 338 Normal_Control`) | `304` (`Malignant`) | `84` (`80 PostOp + 4 PostNAC_B6`) | `581` | `919` | `581` | `573` (`270 B + 299 M + 4 Norm`) |
| **Full-Corpus Totals** | **`2,576`** | **`3,133`** | **`1,728`** | **`4,383`** | **`5,709`** | **`4,769`** | **`1,121`** |

### Provenance Tier & XAI Mask Breakdown (`Zero Silent Track Pooling`)
- **`TierA_Biopsy`:** `4,383` scans (`3,738 DS0003 + 64 DS0005 + 581 DS0006`).
- **`TierA_Biopsy_NormalControl`:** `534` scans (`196 DS0005 + 338 DS0006`) — cleanly tagged so `SubTrackA` (`4,383`) stays pure biopsy while `SubTrackB` (`5,709`) includes disclosed controls.
- **`TierB_Radiology_BIRADS`:** `470` `DS0002 DMID` scans (`never pooled into Tier-A training`; `2` discordant scans `IMG00000062` & `IMG00000302` excluded via `ADJ-017-02` Option B).
- **`TierB_Historical_SFM`:** `322` `DS0001 MIAS` digitized-film `MLO` scans (`cross-domain external/shortcut stress-test only`).
- **`LocalizationEligible = True` (`1,121` total):** Separable by `BinaryTarget` and `LabelClass`:
  - **`BinaryTarget = 1` (`Malignant`) localized lesions:** **`491`** scans (`48 MIAS + 123 DMID + 21 BMCD [11 DCIS, 10 MALIGNANT] + 299 CDD-CESM LE`).
  - **`BinaryTarget = 0` (`Benign_Biopsy / Benign_Lesion`) localized lesions:** **`514`** scans (`61 MIAS + 141 DMID + 42 BMCD + 270 CDD-CESM LE`). *(Total `LesionTrack` localized scans = **`1,005`**.)*
  - **`Normal_Control` non-empty annotations:** **`116`** scans (`112 DS0005 BMCD` `Red`-channel benign microcalcification dots across `Normal_Control` screening rounds + `4 DS0006` `Normal_Control` VIA polygons `IMG00000117, 118, 124, 125`). These stay filtered from lesion pointing/IoU denominators via `LabelClass != 'Normal_Control'`.

---

## 3. Full-Corpus Mask Integrity & Failure-Mode Telemetry

| Cohort | `ok_nonempty` (`Eligible`) | `ok_expected_empty` | `excluded_by_protocol` | `flagged_border_red_bar` | `dimension_mismatch` | `not_applicable` | Corrupt Masks marked `Eligible=True` |
|---|---:|---:|---:|---:|---:|---:|---:|
| **`DS0001` (`MIAS v1.21`)** | `109` | `207` | `6` | `0` | `0` | `0` | **`0`** |
| **`DS0002` (`DMID`)** | `264` | `206` | `5` | `0` | `0` | `35` | **`0`** |
| **`DS0003` (`CMMD`)** | `0` | `0` | `0` | `0` | `0` | `5,202` | **`0`** |
| **`DS0005` (`BMCD`)** | `175` | `84` | `139` | `1` (`IMG00000627`) | `1` (`IMG00000635`) | `0` | **`0`** |
| **`DS0006` (`CDD-CESM LE`)** | `573` | `346` | `84` | `0` | `0` | `0` | **`0`** |
| **Total** | **`1,121`** | **`843`** | **`234`** | **`1`** | **`1`** | **`5,237`** | **`0`** |

Key verification proofs across `7,437` masks/images:
1. **`DS0001 MIAS` Y-Flip & Diffuse Exclusions:** All `109` radiused lesions render inside parenchyma under `(H - y_mias)`; `6` non-circular diffuse/unradiused abnormal scans (`IMG00000063, 216, 218, 220, 237, 249`, `3 Benign + 3 Malignant`) cleanly trigger `Excluded_NoRadiusForROI` (`excluded_by_protocol`, `LocalizationEligible = False`).
2. **`DS0002 DMID` `RGBA` Contour Fill & Option B Exclusions:** `100%` of `264` localized lesions use `Pixel-level annotation/*.tif` (`ROI Masks/*.tif` blocked), match native DICOM `(W, H)`, and convert hollow outlines into solid interior binary masks; `IMG00000062` (which has `.tif`) cleanly flips to `MaskStatus = excluded_by_protocol`, `LocalizationEligible = False` under `Excluded_ReportMetadataDiscordance`; `7` concordant abnormal scans without `.tif` (`2 Benign + 5 Malignant`) record `AbnormalWithoutPixelAnnotationTIF` (`LocalizationEligible = False`).
3. **`DS0005 BMCD` Color Filtering & Hard Artifact Gates (`T09 v1.0.1`):**
   - `Green` calibration tick/ruler channels (`G_ignored`) are cleanly stripped (`0` normal `BI-RADS 1` empty controls polluted by rulers).
   - `IMG00000627` (`PAT00000079`, `Malignant_DCIS`) triggers `BMCD_GT_BottomMarginRedBar` (`botR = 14,450 / R = 15,343` px in bottom `12%` margin) -> **`MaskStatus = flagged_border_red_bar`, `LocalizationEligible = False`** (classification label retained as `BinaryTarget = 1`).
   - `IMG00000611` (`PAT00000077`, already `Excluded_UnconfirmedBiopsy`) also triggers `BMCD_GT_BottomMarginRedBar` (`botR = 14,450 / R = 15,286` px, alongside `UpstreamFilenameTypo_CC_recemt`) -> `excluded_by_protocol`, `LocalizationEligible = False`.
   - `IMG00000635` (`PAT00000080`, `Excluded_UnconfirmedBiopsy`) triggers `BMCD_GT_AspectMismatch` (`gt = 688x832`, `ar_err = 0.01775 > 0.01`) -> `dimension_mismatch`, `LocalizationEligible = False`.
4. **`DS0006 CDD-CESM LE` `5`-Primitive VIA Rasterizer:** All `573` retained localized LE scans (`270 Benign + 299 Malignant + 4 Normal`) rasterize across all `5` VIA JSON primitives with `0` unmapped shape types; `9` border-touching polygon coordinates cleanly trigger `MaskCoordsClippedAtBorder` (clamped safely to `(W, H)` bounds); `12` abnormal scans (`7 Benign + 5 Malignant`) without VIA segmentation rows remain classification-eligible (`LocalizationEligible = False`).

---

## 4. Visual Overlay Plate Inspection (`5` Full-Run Stratified Grids)

All `5` generated Tier-2 overlay grids (`04_Labels_XAI_Governance/restricted_masks/pilot_overlays/DS000*_full_overlays.png`, `16` stratified tiles per cohort) were visually inspected (with `DS0002_full_overlays.png` re-checked after the `ADJ-017-02` Option B run):
- **[`DS0001_full_overlays.png`](../../04_Labels_XAI_Governance/restricted_masks/pilot_overlays/DS0001_full_overlays.png) (`N = 322`):** Red Y-flipped circle + cyan fill lands directly over hyperdense masses (`IMG00000005, 0006, 0014, 0019, 0025, 0029`), whereas the yellow unflipped circle misses (`IMG00000017`). Normal controls show `cov = 0.0%`.
- **[`DS0002_full_overlays.png`](../../04_Labels_XAI_Governance/restricted_masks/pilot_overlays/DS0002_full_overlays.png) (`N = 510`):** Solid filled red-contour lesion interiors accurately delineate unifocal and multifocal lesions (`IMG00000001, 0011, 0012, 0024`), with empty `0.0%` overlays on `Normal_Control` (`IMG00000002–0005`).
- **[`DS0003_full_overlays.png`](../../04_Labels_XAI_Governance/restricted_masks/pilot_overlays/DS0003_full_overlays.png) (`N = 5,202`):** Confirms `100%` `cov = 0.0%` (`0` synthetic masks) with proper `CC/MLO` and `L/R` view metadata resolved across SNOMED `ViewCodeSequence`.
- **[`DS0005_full_overlays.png`](../../04_Labels_XAI_Governance/restricted_masks/pilot_overlays/DS0005_full_overlays.png) (`N = 400`):** Visually verifies green/yellow burned-in orientation rulers on `Normal_Control` scans are ignored while tiny red benign microcalcification dots (`IMG00000017–0047`, `cov < 0.01%`) are isolated cleanly, and `BI-RADS 1` normals (`IMG00000001–0007`) remain completely empty (`0.0%`).
- **[`DS0006_full_overlays.png`](../../04_Labels_XAI_Governance/restricted_masks/pilot_overlays/DS0006_full_overlays.png) (`N = 1,003`):** Visually confirms complex irregular VIA polygons (`IMG00000012, 0013, 0022, 0023, 0024, 0027`), circles (`IMG00000016, 0017`), skin-thickening + scar exclusions (`Excluded_PostOperative`: `IMG00000002, 0003, 0018`), and clean `0.0%` normal controls (`IMG00000004–0007`).

---

## 5. Multi-Lesion & Report/BI-RADS Concordance Summary

| Cohort | Multi-Lesion Conflicts | Concordance / Clinical Anomaly Highlights (`Full Corpus`) | Disposition |
|---|---:|---|---|
| **`DS0001` (`MIAS v1.21`)** | `0` | `ok_sfm_benign = 64`, `ok_sfm_malignant = 51`, `ok_sfm_normal = 207` (`100%` consistent with `00README.pdf`) | Pass (`TierB_Historical_SFM`) |
| **`DS0002` (`DMID`)** | `21` (`20 [B,M] -> 1`, `1 [B,N] -> Excluded`) | `2` Report-vs-Sheet Discordances (`IMG00000062` & `IMG00000302`) **excluded under `ADJ-017-02` Option B** (`Excluded_ReportMetadataDiscordance`); `35` `Excluded_AmbiguousClassToken_N`; `470` concordant `Tier-B` scans retained (`199 Norm + 143 Benign + 128 Malig`) | **Closed & Ratified (`Option B`)** |
| **`DS0003` (`CMMD`)** | `2` (`CrossLabelClonePatient`) | `3,738` `ok_biopsy_side_match`; `1,456` `unlabeled_contralateral`; `120` images across `30` patients with `BilateralDiscordantPatient` (`preserved at breast-side granularity`) | Pass (`SubTrackA`) |
| **`DS0005` (`BMCD`)** | `0` | `64` `ok_biopsy_recent`; `196` `Normal_Control` (`88 BI-RADS 1`, `108 BI-RADS 2` across `prior/recent`); `98` `excluded_prior_baseline`; `34` `unconfirmed_biopsy_birads_triage` | Pass (`SubTrackA` + `SubTrackB`) |
| **`DS0006` (`CDD-CESM LE`)** | `0` | `897` `ok_pathology_birads`; `13` `OccultOnDM_BIRADS_1/2` (`11 BIRADS-1`, `2 BIRADS-2` -> kept `T=1`); `9` `DM_BIRADS_3/4_ClearedNormal` (`8 BIRADS-3`, `1 BIRADS-4` -> kept `T=0`); `4` `FalsePositiveDM_BIRADS_5_BiopsyBenign` (`kept T=0`); `84` Post-Op / Post-NAC `Excluded` | Pass (`T09 v1.0.1`) |

All full-corpus discrepancy and exclusion rationales are closed in [STEP017_full_adjudications.md](../adjudications/STEP017_full_adjudications.md).

---

## 6. Readiness Verdict for `STEP-018` (`LBL####` Freeze & `G06`)

- **Technical & Governance Result:** `5 / 5` clean cohorts (`7,437` primary acquired / `7,420` `G04`-retained) passed `--mode full --seed 20261128` with `100%` arithmetic closure, `0` unmapped tokens, `0` corrupt masks marked `LocalizationEligible = True`, and **`100%` closed adjudications** (`ADJ-017-01` through `ADJ-017-06`, including **`ADJ-017-02` Option B**).
- **`STEP-017` Definition of Done Satisfied:** Ready for `STEP-018` (`04_Labels_XAI_Governance/label_registry.csv` `LBL####` freeze, canonical `label_map.json`, `T10 LBL####_audit.md`, `DEC0008–0009` closeout, and `GATE0006 = PASS`).

---

## 7. Sign-Off Record (`STEP-017`)

- **Prepared By:** Md Riyadul Hasan (`232-15-486`) & Alzubair Ahamed (`232-15-591`) — `2026-11-28`
- **Approved Adjudication (`ADJ-017-02` Option B):** User/Research Owner (`2026-11-28`)
- **Next Action:** Execute [STEP-018](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-018) (`LBL####` freeze & `GATE0006` assessment).

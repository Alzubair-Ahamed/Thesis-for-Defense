# STEP-016 Pilot Discrepancies & Adjudication Log (`T09` Protocol vs Observed Source Files)

| Header Field | Value |
|---|---|
| `TemplateID` | `T10-ADJ` (`STEP-016 Adjudication Log`) |
| `entity_id` | `STEP016_PILOT_DISCREPANCIES_v1.0.0` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Label/Mask Lead) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-28` (`Logged & Adjudicated 2026-11-28`) |
| `status` | **`ADJUDICATED_APPROVED_AT_STEP016 (2026-11-28 — T09 v1.0.1 Adopted)`** |
| `source_inputs` | [label_mask_protocol_v1.0.1.md](../protocols/label_mask_protocol_v1.0.1.md); [label_mask_protocol_v1.0.0.md](../protocols/label_mask_protocol_v1.0.0.md); [pilot_label_mask_audit.md](../reviews/pilot_label_mask_audit.md); [verify.py](../../src/bc_xai/labels/verify.py) |
| `governing_section` | [OS §4.3, §6.1](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [Blueprint STEP-016](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-016) |
| `sensitivity` | Tier-1 Adjudication Ledger (`strictly pseudonymous IDs / zero PHI`) |
| `reviewer` | User/Research Owner; Israt Jahan (Supervisor); Md Riyadul Hasan; Alzubair Ahamed — Approved `2026-11-28` |

---

## Summary of `7` Empirical Findings During `STEP-016` Pilot

| Adj ID | Cohort | Finding / Discrepancy vs Initial `T09 v1.0.0` Wording | Observed Evidence (`2026-11-28`) | Applied Code Resolution (`verify.py`) | Status / Action Needed |
|---|---|---|---|---|---|
| **`ADJ-016-01`** | `DS0005 BMCD` | **Green Calibration Ruler in `*_GT.jpg`:** `T09 §5` initially specified `max(RGB)-min(RGB) > 25`. Empirical pixel & visual plate check proves every `Normal_cases` and `Suspicious_cases` `*_GT.jpg` carries a **green calibration scale/ruler bar** (`1,100–5,800` `G > max(R,B)` pixels). | Verified across all `14` BMCD visual panels (`yellow trace` on `DS0005_pilot_overlays.png`) & `README.txt` (`Red = benign calc`, `Blue circle = suspicious`). | Restricted lesion extraction to `Red` + contour-filled `Blue` (`lesion_red_blue` mode), excluding `Green` scale bars cleanly. | **Ratified (`T09 v1.0.1`)** |
| **`ADJ-016-02`** | `DS0005 BMCD` | **Red Bottom-Margin Artifact (`IMG00000627`):** `PAT00000079` contains `15,343` red pixels, of which `14,450` (`94.2%`) form a solid red horizontal strip in bottom air (`y > 0.88 * Height`) with `blue_px = 0`. | Visually confirmed on `DS0005_pilot_overlays.png` row 3 col 2 (`IMG00000627`). | Flagged automatically via `BMCD_GT_BottomMarginRedBar` (`MaskStatus = flagged_border_red_bar`, **`LocalizationEligible = False`**) so zero margin-bar artifacts enter XAI `PG/IoU`. | **Approved (`LocalizationEligible = False` locked in `T09 v1.0.1`)** |
| **`ADJ-016-03`** | `DS0005 BMCD` | **Upstream Zenodo Filename Typos:** Real folders contain `CC_recemt.dcm`, `CC_reent_GT.jpg`, `MLO_reent_GT.jpg`, and `.Jpg` uppercase extension (`IMG00000743` caught in pilot). | Direct raw filesystem audit (`4` typo filenames confirmed). | Tolerated `recemt/reent` + case-insensitive matching read-only and emitted explicit `UpstreamFilenameTypo_*` / `UpstreamGTTypo_*` flags. | **Resolved Read-Only (`T09 v1.0.1`)** |
| **`ADJ-016-04`** | `DS0006 CDD-CESM` | **5 VIA Shape Primitives (`Not Polygon Only`):** `1,797` `DM` segmentations comprise `1,135` polygons, **`378` ellipses, `274` circles, `6` polylines, and `4` points**. | Full `Radiology_hand_drawn_segmentations_v2.csv` `DM` shape inventory (`37%` non-polygon!). | `rasterize_cdd_cesm_shapes` implements deterministic union across all `5` VIA primitives (`tested in test_label_verify.py`). | **Ratified (`T09 v1.0.1`)** |
| **`ADJ-016-05`** | `DS0006 CDD-CESM` | **Valid Radiographic Concordance Gaps (`DM` vs `CESM`):** Full sheet check revealed `9` LE `Normal` scans with `DM BI-RADS 3–4` cleared on `CESM`, plus `11` LE `Malignant` scans occult on `DM` (`BI-RADS 1–2`, enhancing on `CM`). | Cross-checked bilateral/type rows in `Radiology-manual-annotations.xlsx` (`e.g. P29_L`, `P38_R`, `P147_R`). | Replaced naive crash on `BI-RADS 3–4 Normal` with structured audit flags (`DM_BIRADS_<k>_ClearedNormal`, `OccultOnDM_BIRADS_<k>`); retained hard fail on `Normal + BI-RADS 6`. | **Resolved & Flagged** |
| **`ADJ-016-06`** | `DS0002 DMID` | **Hollow `RGBA` Lesion Outlines (`~3.7x` interior area):** `Pixel-level annotation/*.tif` draws colored boundary rings (`IMG00000001`: `65,523` raw outline px vs `240,616` filled interior px). | Visually confirmed on `20/20` DMID pilot overlays (`0%` offset). | Applied external contour interior fill (`cv2.drawContours(..., -1)`) inside `extract_dmid_rgba_mask` (`roi masks/ hard-banned`). | **Verified Clean** |
| **`ADJ-016-07`** | `DS0003 CMMD` & `DS0001 MIAS` | **CMMD SNOMED View Codes & MIAS `*** see note 2`:** `DS0003` populates `ViewCodeSequence` (`399162004=CC`, `399368009=MLO`) rather than `ViewPosition`; `DS0001` has `3` diffuse `M` `CALC` rows with `*** see note 2` instead of `(x, y, r)`. | `16/16` CMMD panels view-verified visually; `3/322` MIAS diffuse rows parsed cleanly (`mdb216rl/233lm/245ls`). | Implemented SNOMED `ViewCodeSequence` decoder in `_harmonize_cmmd` and `*** see note 2` regex fallback in `_parse_mias_lines` -> `Excluded_NoRadiusForROI`. | **Resolved & Tested** |

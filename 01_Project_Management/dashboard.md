# Research Project Management Dashboard

- **Document:** `01_Project_Management/dashboard.md`
- **Last Updated:** `2026-11-28` (**`STEP-017` Full Audit Complete**; `G01–G05 PASS`, `5` Clean `CC BY` Cohorts = `7,437` Acquired / `7,420` Retained Audited, Ready for `STEP-018` `LBL####` Freeze & `G06`)
- **Approved Title:** *Explainable Deep Learning-Based Early Breast Cancer Detection Using Mammogram Images* (`RF01`)
- **Researchers:** Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`)
- **Supervisors:** Israt Jahan (Supervisor) & Ms Faiza Feroz (Co-Supervisor)
- **GitHub Remote:** `https://github.com/Alzubair-Ahamed/Thesis-for-Defense.git` (`main`)

---

## 1. Live Stage & Gate Status Matrix (`S01–S16`, `G01–G17`)

| Stage | Steps | Description | Exit Gate(s) | Current Status |
|---|---|---|---|---|
| **S01** | `STEP-001` | Foundation, scope constitution & `UD01–UD28` assignment | `G01` | **COMPLETED (`G01 PASS`, `2026-11-23`)** |
| **S02** | `STEP-002–003` | Repository skeleton, `T01–T35` templates, 24 CSV registries & Phase-1 `environment/data/` | `G02` | **COMPLETED (`G02 PASS`, `2026-11-23`)** |
| **S03** | `STEP-004–007` | PRISMA literature search, screening, `49` `T05` extractions (`42` core + `6` OA + `P0063`) & `UD04` audit | Feeds `G03` | **COMPLETED (`2026-11-26`; residual `908` DB abstracts `Pending_FullText`)** |
| **S04** | `STEP-008–009` | Novelty/gap verification (`GAP0001–0005`), thematic synthesis & `RQ1–RQ4` dossier | `G03` | **COMPLETED (`G03 PASS`, `2026-11-27` — Option 1 & `RQ1–RQ4` Ratified)** |
| **S05** | `STEP-010–012` | 6-dataset public 2D mammography discovery (`UD05`), DUAs/ethics (`UD06`) & raw intake | Feeds `G04` | **COMPLETED (`G04 PASS`, `2026-11-28` — `DEC0005` & `DEC0006` Batch A Approved; `5` `CC BY` Cohorts Locked)** |
| **S06** | `STEP-013` | Mammogram decoding, 16-bit/polarity/PHI QC & dataset suitability approval | `G04` | **COMPLETED (`G04 PASS`, `2026-11-28` — `7,420` Retained / `17` Clones Quarantined / `0` Integrity Errors)** |
| **S07** | `STEP-014–015` | FFDM/ROI paradigm (`UD07`), label/ROI-mask rules (`UD08–09`) & prospective XAI (`XAIP0001`) | `G05` | **COMPLETED (`G05 PASS`, `2026-11-28` — `DEC0007–0009`, `DEC0016–0018`, `T09 v1.0.0` & `XAIP0001` Ratified)** |
| **S08** | `STEP-016–018` | Pilot & full-dataset label/ROI-mask verification and `LBL####` freeze | `G06` | **IN PROGRESS (`STEP-017` Full Audit `N=7,437` Closed `2026-11-28` w/ `ADJ-017-02` Option B — Ready for `STEP-018` `LBL####` Freeze & `G06`)** |
| **S09** | `STEP-019–021` | Preprocessing design, connected-component patient split & `REL####` release | `G07`, `G08` | `NOT STARTED` (`G07–G08 NOT ASSESSED`) |
| **S10** | `STEP-022–026` | Transfer learning CNN roster (`UD13`), Phase-2 `environment/model/`, `src/bc_xai/` & smoke/recovery | `G09` | `NOT STARTED` (`G09 NOT ASSESSED`) |
| **S11** | `STEP-027–031` | Multi-architecture CNN training, controlled ablations & multi-seed runs | `G10` (per EXP) | `NOT STARTED` (`G10 NOT ASSESSED`) |
| **S12** | `STEP-032–033` | Validation-only selection/threshold/calibration, `G11` freeze & locked test inference | `G11` | `NOT STARTED` (`G11 NOT ASSESSED`) |
| **S13** | `STEP-034–036` | Q1 metrics, calibration, DeLong/McNemar stats, quantitative XAI & external validation | `G12` | `NOT STARTED` (`G12 NOT ASSESSED`) |
| **S14** | `STEP-037–039` | Subgroups/errors/blinded clinical XAI review, local CAD prototype & CLAIM/TRIPOD+AI replay | `G13`, `G14` | `NOT STARTED` (`G13–G14 NOT ASSESSED`) |
| **S15** | `STEP-040–047` | Dual-track FYDP thesis + Q1 paper writing, submission, archival & project closure | `G15`, `G16` | `NOT STARTED` (`G15–G16 NOT ASSESSED`) |
| **S16** | `STEP-048–050` | Conditional hosted FYDP defense Grad-CAM web demonstration (`UD25`) | `G17` | `NOT STARTED` (`G17 NOT ASSESSED`) |

---

## 2. Canonical Registry Inventory (24 Master CSVs)

- **Populated Registries (`10`):**
  1. `01_Project_Management/decisions.csv` (`28` rows: `DEC0001`, `DEC0003–0005`, **`DEC0007–0009`**, **`DEC0016–0018`** Approved; `DEC0006` Batch A Approved; `DEC0014` Phase-1 Approved)
  2. `01_Project_Management/gates.csv` (`18` rows: **`G01–G05 PASS`**, `G06–G17` `NOT ASSESSED`)
  3. `01_Project_Management/risk_register.csv` (`10` risk themes `RISK0001–RISK0010`; `RISK0002–RISK0004` updated with live `STEP-013` clone & shortcut evidence)
  4. `02_Literature/papers.csv` (`1,501` rows: `42/42` curated local PDFs extracted to `T05` + `11` Stage-2 OA landmarks verified/extracted incl. `P1497–P1501` + `13` `UD04` `SEED` leads audited/quarantined + `908` Stage-1 candidates `Pending_FullText_*` + `527` Stage-1/GS exclusions)
  5. `02_Literature/screening.csv` (`2,226` rows: `62` GS FT + `34` GS dup + `13` SEED intake + `677` open-DB dup + `1,421` Stage-1 `title_abstract` + `6` Stage-2 OA `full_text` + `13` `seed_ud04_audit`)
  6. `02_Literature/gaps.csv` (`5` verified gaps `GAP0001–GAP0005` testing `RF16` & `UD04`, backed by `02_Literature/gap_notes/`)
  7. `02_Literature/claims.csv` (`10` primary-source empirical claims `CLAIM0001–CLAIM0010`, backed by `02_Literature/claim_notes/`)
  8. `03_Datasets/candidates.csv` (`13` audited primary/derived 2D mammography collections `CAND0001–CAND0013` backing `candidate_comparison.md`)
  9. `03_Datasets/datasets.csv` (`5` **`Approved_G04_PASS_Locked`** tracks totaling **`7,420` retained / `7,437` primary acquired + `17` clones quarantined**: `DS0001 MIAS` [`322/322`], `DS0002 DMID` [`507/510`], `DS0003 CMMD` [`5,196/5,202`], `DS0005 BMCD` [`392/400`], `DS0006 CDD-CESM LE` [`1,003/1,003` + `1,003` CESM excluded])
  10. `04_Labels_XAI_Governance/xai_protocol_registry.csv` (`1` row: `XAIP0001` **`Approved at G05 PASS`**)
- **Header-Only Scientific Registries Awaiting Downstream Steps (`14`):**
  - `03_Datasets/releases.csv`
  - `04_Labels_XAI_Governance/label_registry.csv`
  - `05_Preprocessing/preprocessing_registry.csv`
  - `06_Models/{candidates,model_registry}.csv`
  - `07_Experiments/experiment_registry.csv`
  - `08_Checkpoints/checkpoint_registry.csv`
  - `09_Evaluation/{evaluation_registry,xai_audit_registry,statistical_comparisons}.csv`
  - `10_Figures_Tables/assets.csv`
  - `11_Writing/writing_registry.csv`
  - `15_Archive/archive_manifest.csv`
  - `16_Web_Demo/deployment_registry.csv`

---

## 3. Immediate Next Action
- **Ready for `S08 / STEP-018` (`LBL####` Freeze & `G06`):** `STEP-017` full-corpus label & ROI-mask audit (`7,437` primary / `7,420` retained, `5/5` arithmetic closure `True`, `1,121` verified masks, `ADJ-017-02` Option B closed) is complete in [STEP017_full_label_mask_audit.md](../04_Labels_XAI_Governance/reviews/STEP017_full_label_mask_audit.md) and [STEP017_full_adjudications.md](../04_Labels_XAI_Governance/adjudications/STEP017_full_adjudications.md); next execute **`STEP-018` (`label_registry.csv` `LBL####` freeze + `GATE0006 = PASS`)**.
- **Optional Batch B Queue (Parallel Non-Blocking):** Continue PhysioNet CITI (`VinDr-Mammo`) & INESC TEC (`INbreast`) DUA requests; unused `23.41 GB` partial `DS0004_CBIS_DDSM` cropped/ROI folder stays untouched outside active modeling scope.

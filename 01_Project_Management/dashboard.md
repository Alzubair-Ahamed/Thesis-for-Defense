# Research Project Management Dashboard

- **Document:** `01_Project_Management/dashboard.md`
- **Last Updated:** `2026-11-27` (**`STEP-013` Technical QC, PHI Audit, Pixel-Clone Quarantine & `T08` Cards Complete across `5` Cohorts [`7,420` Retained Scans] — `G04` Assessment Package Ready for Sign-off**; unused `DS0004_CBIS_DDSM` `23.41 GB` partial folder left untouched outside scope)
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
| **S05** | `STEP-010–012` | 6-dataset public 2D mammography discovery (`UD05`), DUAs/ethics (`UD06`) & raw intake | Feeds `G04` | **COMPLETED FOR 5 OPEN COHORTS (`DEC0005` Proposed; `DEC0006` Batch A Approved; `DS0001/2/3/5/6` SHA-256 Inventoried)** |
| **S06** | `STEP-013` | Mammogram decoding, 16-bit/polarity/PHI QC & dataset suitability approval | `G04` | **TECHNICAL PREP READY (`G04_assessment_2026-11-27.md` Prepared — Awaiting Supervisor Sign-off; `G04 NOT ASSESSED`)** |
| **S07** | `STEP-014–015` | FFDM/ROI paradigm (`UD07`), label/ROI-mask rules (`UD08–09`) & prospective XAI (`XAIP0001`) | `G05` | `NOT STARTED` (`G05 NOT ASSESSED`) |
| **S08** | `STEP-016–018` | Pilot & full-dataset label/ROI-mask verification and `LBL####` freeze | `G06` | `NOT STARTED` (`G06 NOT ASSESSED`) |
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

- **Populated Registries (`9`):**
  1. `01_Project_Management/decisions.csv` (`28` rows: `DEC0001`, `DEC0003`, `DEC0004` Approved; **`DEC0005` Proposed for `G04`**; `DEC0006` Batch A Approved; `DEC0014` Phase-1 Approved)
  2. `01_Project_Management/gates.csv` (`18` rows: `G01 PASS`, `G02 PASS`, `G03 PASS` [`2026-11-27`], `G04–G17` `NOT ASSESSED`; **`G04` Assessment Ready**)
  3. `01_Project_Management/risk_register.csv` (`10` risk themes `RISK0001–RISK0010`; `RISK0002–RISK0004` updated with live `STEP-013` clone & shortcut evidence)
  4. `02_Literature/papers.csv` (`1,501` rows: `42/42` curated local PDFs extracted to `T05` + `11` Stage-2 OA landmarks verified/extracted incl. `P1497–P1501` + `13` `UD04` `SEED` leads audited/quarantined + `908` Stage-1 candidates `Pending_FullText_*` + `527` Stage-1/GS exclusions)
  5. `02_Literature/screening.csv` (`2,226` rows: `62` GS FT + `34` GS dup + `13` SEED intake + `677` open-DB dup + `1,421` Stage-1 `title_abstract` + `6` Stage-2 OA `full_text` + `13` `seed_ud04_audit`)
  6. `02_Literature/gaps.csv` (`5` verified gaps `GAP0001–GAP0005` testing `RF16` & `UD04`, backed by `02_Literature/gap_notes/`)
  7. `02_Literature/claims.csv` (`10` primary-source empirical claims `CLAIM0001–CLAIM0010`, backed by `02_Literature/claim_notes/`)
  8. `03_Datasets/candidates.csv` (`13` audited primary/derived 2D mammography collections `CAND0001–CAND0013` backing `candidate_comparison.md`)
  9. `03_Datasets/datasets.csv` (`5` `QC_Audited_STEP013_Pending_G04` tracks totaling **`7,420` retained / `7,437` primary acquired + `17` clones quarantined**: `DS0001 MIAS` [`322/322`], `DS0002 DMID` [`507/510`], `DS0003 CMMD` [`5,196/5,202`], `DS0005 BMCD` [`392/400`], `DS0006 CDD-CESM LE` [`1,003/1,003` + `1,003` CESM excluded])
- **Header-Only Scientific Registries Awaiting Downstream Steps (`15`):**
  - `03_Datasets/releases.csv`
  - `04_Labels_XAI_Governance/{label_registry,xai_protocol_registry}.csv`
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
- **Awaiting Human Ratification (`G04` Gate Review):** Supervisor **Israt Jahan** & Data Steward **Md Riyadul Hasan** review [G04_assessment_2026-11-27.md](./reviews/G04_assessment_2026-11-27.md) and [DEC0005.md](./decision_log/DEC0005.md) (`UD05`) to sign off `GATE0004 = PASS`.
- **Next Pipeline Stage Upon `G04 PASS` (`S07 / STEP-014–015`):** Establish unified clinical label, contralateral-breast, `BMCD/DMID/CDD-CESM` ROI mask extraction (`T09`), and prospective XAI evaluation protocol (`XAIP0001`) ahead of **`G05`**.
- **Optional Batch B Queue (Parallel Non-Blocking):** Continue PhysioNet CITI (`VinDr-Mammo`) & INESC TEC (`INbreast`) DUA requests; unused `23.41 GB` partial `DS0004_CBIS_DDSM` cropped/ROI folder stays untouched outside active modeling scope.

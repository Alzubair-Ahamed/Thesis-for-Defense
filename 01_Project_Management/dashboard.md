# Research Project Management Dashboard

- **Document:** `01_Project_Management/dashboard.md`
- **Last Updated:** `2026-11-23` (`STEP-003` / `G02 PASS`)
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
| **S03** | `STEP-004–007` | PRISMA literature search, screening, extraction & `UD04` bibliography audit | Feeds `G03` | **NEXT ACTIVE STAGE (`STEP-004` Ready)** |
| **S04** | `STEP-008–009` | Novelty/gap verification, Q1 contribution framing & RQ ratification | `G03` | `NOT STARTED` (`G03 NOT ASSESSED`) |
| **S05** | `STEP-010–012` | 6-dataset public 2D mammography discovery (`UD05`), DUAs/ethics (`UD06`) & raw intake | Feeds `G04` | `NOT STARTED` |
| **S06** | `STEP-013` | Mammogram decoding, 16-bit/polarity/PHI QC & dataset suitability approval | `G04` | `NOT STARTED` (`G04 NOT ASSESSED`) |
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

- **Populated Governance Registries (`3`):**
  1. `01_Project_Management/decisions.csv` (`28` rows: `DEC0001` Approved, `DEC0014` Phase-1 Approved, `DEC0002–0013` & `DEC0015–0028` awaiting their designated milestones)
  2. `01_Project_Management/gates.csv` (`18` rows: `G01 PASS`, `G02 PASS`, `G03–G17` `NOT ASSESSED`)
  3. `01_Project_Management/risk_register.csv` (`10` initial project risk themes `RISK0001–RISK0010`)
- **Header-Only Scientific Registries Ready for Execution Intake (`21`):**
  - `02_Literature/{papers,screening,gaps,claims}.csv`
  - `03_Datasets/{candidates,datasets,releases}.csv`
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
- Execute **[STEP-004](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-004)** (`Approve PRISMA-style systematic literature search and screening protocol` under `02_Literature/searches/protocol.md`).

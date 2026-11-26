# Explainable Deep Learning-Based Early Breast Cancer Detection Using Mammogram Images

[![Stage](https://img.shields.io/badge/Current_Stage-S04_G03_Review_Ready-blue)](./01_Project_Management/reviews/G03_assessment_2026-11-26.md)
[![STEP-001](https://img.shields.io/badge/STEP--001-DONE_(G01_PASS)-brightgreen)](./01_Project_Management/reviews/G01_assessment_2026-11-23.md)
[![STEP-002--003](https://img.shields.io/badge/STEP--002--003-DONE_(G02_PASS)-brightgreen)](./01_Project_Management/reviews/G02_assessment_2026-11-23.md)
[![STEP-004--008](https://img.shields.io/badge/STEP--004--008-DONE_(49_T05_+_UD04)-brightgreen)](./02_Literature/synthesis.md)
[![Gates G03-G17](https://img.shields.io/badge/Gates_G03--G17-NOT_ASSESSED-lightgrey)](./01_Project_Management/reviews/G03_assessment_2026-11-26.md)

## 1. Project Identity (`RF01–RF04`)

| Field | Authoritative Value |
|---|---|
| **Approved Title** | *Explainable Deep Learning-Based Early Breast Cancer Detection Using Mammogram Images* |
| **Institution** | Daffodil International University (DIU), Department of Computer Science and Engineering |
| **Program Context** | Final Year Design Project (FYDP — Title Phase Evaluation Report v2.0, Summer 2026) |
| **Researchers** | **Alzubair Ahamed** (ID: `232-15-591`) & **Md Riyadul Hasan** (ID: `232-15-486`) |
| **Supervisor** | **Israt Jahan**, Lecturer (Senior Scale) |
| **Co-Supervisor** | **Ms Faiza Feroz**, Lecturer |
| **Governing Constitution** | [BC_XAI_RESEARCH_OPERATING_SYSTEM.md](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md) (`v1.0.0`) |
| **Sequential Manual** | [BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md](./BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md) (`v1.0.0`) |
| **Approved Scope Charter** | [01_Project_Management/scope.md](./01_Project_Management/scope.md) (`G01 PASS`, `2026-11-23`) |

> **Research-Only Medical AI Disclaimer (`RF15`, OS §1.3):** This repository contains a retrospective academic research framework for binary classification (**Benign** vs **Malignant**) of publicly available 2D mammogram images using transfer learning and Explainable AI (**Grad-CAM** and approved comparators). It is **not** a certified medical device, is **not** approved for clinical diagnosis or screening, and explicitly excludes hospital/PACS integration, real-patient clinical trials, non-mammogram imaging modalities, and automated treatment recommendations.

---

## 2. Repository Architecture ([OS §2](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02))

```text
.
├── BC_XAI_RESEARCH_OPERATING_SYSTEM.md      # Canonical Q1 research governance handbook (v1.0.0)
├── BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md    # 16-stage, 50-step sequential execution manual (v1.0.0)
├── README.md                                # Root repository overview and status
├── CHANGELOG.md                             # Versioned repository and milestone history
├── CONTRIBUTING.md                          # Epistemic rules, commit conventions, Universal DoD
├── .gitignore                               # Tier-2/Tier-3 medical data, checkpoint, and secret guards
├── .gitattributes                           # Deterministic text/line-ending normalization
├── environment/
│   ├── data/                                # Phase 1 minimal data/QC/split dependency lock & verification
│   └── model/                               # Phase 2 DL/XAI/statistical runtime (locked at STEP-023)
├── src/bc_xai/                              # Reusable core Python package (thin entry points)
├── tests/                                   # Automated unit, geometry, grouping, and smoke tests
├── 01_Project_Management/                   # Scope, decisions.csv, decision_log/, gates, risks, diary/
├── 02_Literature/                           # PRISMA searches, papers.csv, screening, gaps, claims, BibTeX
├── 03_Datasets/                             # 6-dataset candidate audit, DUAs, raw (Tier-2), splits/
├── 04_Labels_XAI_Governance/                # Diagnostic label/ROI-mask verification & XAIP protocols
├── 05_Preprocessing/                        # Mammography preprocessing specs, configs, processed (Tier-2)
├── 06_Models/                               # Transfer learning CNN candidate roster & model cards
├── 07_Experiments/                          # Experiment plan, immutable EXP#### configs & training logs
├── 08_Checkpoints/                          # Checkpoint policy, SHA-256 manifests (binaries in Tier-3)
├── 09_Evaluation/                           # Protocol, G11 freeze, classification/calibration/stats/XAI audits
├── 10_Figures_Tables/                       # Reproducible asset specs, scripts, and disclosure-cleared plots
├── 11_Writing/                              # Dual-track DIU FYDP thesis and Q1 journal manuscript sources
├── 12_Documentation/                        # Installation, pipeline, reproducibility, CLAIM/TRIPOD+AI guides
├── 13_Automation/                           # Thin CLI wrappers for registry, training, and figure validation
├── 14_Templates_Prompts/                    # Blank canonical templates (T01-T35) installed at STEP-003
├── 15_Archive/                              # Immutable release manifests (ARCH####) and restoration proofs
├── web/                                     # Conditional thin defense Grad-CAM showcase app (Stage S16)
└── 16_Web_Demo/                             # Conditional deployment registry, parity checks, runbook (S16)
```

---

## 3. Execution Progress

| Stage / Step | Title | Status | Gate / Evidence |
|---|---|---|---|
| `S01` / `STEP-001` | Confirm the research mandate, team roles, and unresolved-decision register | **COMPLETED** (`2026-11-23`) | `G01 PASS` ([G01 Assessment](./01_Project_Management/reviews/G01_assessment_2026-11-23.md), [DEC0001](./01_Project_Management/decision_log/DEC0001.md)) |
| `S02` / `STEP-002` | Instantiate repository skeleton, storage-tier controls, and minimal data-tool environment | **COMPLETED** (`2026-11-23`) | Feeds `G02` ([Verification Report](./environment/data/verification.md), [DEC0014](./01_Project_Management/decision_log/DEC0014.md)) |
| `S02` / `STEP-003` | Install blank templates (`T01–T35`), canonical CSV registries, and validation checks | **COMPLETED** (`2026-11-23`) | `G02 PASS` ([G02 Assessment](./01_Project_Management/reviews/G02_assessment_2026-11-23.md), [Dashboard](./01_Project_Management/dashboard.md)) |
| `S03` / `STEP-004` | Approve PRISMA-style systematic literature search and screening protocol | **COMPLETED** (`2026-11-23`) | Feeds `G03` ([Search Protocol](./02_Literature/searches/protocol.md), [Provisional RQs](./02_Literature/research_questions.md), [DEC0003](./01_Project_Management/decision_log/DEC0003.md)) |
| `S03` / `STEP-005` | Execute database searches and register deduplicated candidate papers | **COMPLETED** (`2026-11-26`) | `2,207` intake records (`96` GS PDFs + `366` `DB01` PubMed + `1,594` `DB03` OpenAlex + `138` `DB05` arXiv + `13` `SEED`) → `711` `EX04` duplicates removed → `1,496` unique records (`T04` logs, [papers.csv](./02_Literature/papers.csv)); `DB02`/`DB04` institutional access blocks logged honestly |
| `S03` / `STEP-006` | Screen candidate records and document PRISMA eligibility | **COMPLETED** (`2026-11-26`) | `62` GS full-text + `1,421` Stage-1 `title_abstract` + `6` Stage-2 OA `full_text` + `13` `UD04` `SEED` audits (`2,226` rows, [screening.csv](./02_Literature/screening.csv)) |
| `S03` / `STEP-007` | Extract deep `T05` cards (`48` + `P0063`), `UD04` seed audit & `claims.csv` | **COMPLETED** (`2026-11-26`) | `42/42` curated local + `6` Stage-2 OA (`P0156, P0385, P0675, P0810, P1030, P1433`) + `P0063` ([summaries/](./02_Literature/summaries/), [UD04 Audit](./02_Literature/reports/report_bibliography_audit_UD04.md), [claims.csv](./02_Literature/claims.csv)) |
| `S04` / `STEP-008–009` | Test `RF16` hypotheses, write thematic synthesis & prepare `RQ1–RQ4` / `G03` dossier | **PREP COMPLETE** (`2026-11-26`; `G03 NOT ASSESSED`) | [gaps.csv](./02_Literature/gaps.csv) (`GAP0001–0005`), [synthesis.md](./02_Literature/synthesis.md), [research_questions.md](./02_Literature/research_questions.md), [G03 Dossier](./01_Project_Management/reviews/G03_assessment_2026-11-26.md) |
| `S05–S16` / `STEP-010–050` | Multi-dataset acquisition (`UD05`), labeling, modeling, stats, writing & defense demo | `NOT STARTED` (Blocked on `G03`) | `G04–G17` (`NOT ASSESSED`) |

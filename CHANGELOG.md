# Changelog

All notable governance, repository, and scientific execution milestones for **Explainable Deep Learning-Based Early Breast Cancer Detection Using Mammogram Images** are documented in this file.

## [v1.0.0-g03-pass-step010] — 2026-11-27 (`G03 PASS` & `STEP-010` Dataset Discovery)
### Added & Changed
- **Storage Firewall Hardened (`.gitignore`):** Expanded dataset and paper exclusions (`Dataset*/`, `dataset*/`, `Paper*/`, `Papers/`, `03_Datasets/{raw,downloads,external,cache,images,masks,processed,releases}/`, raw imaging/archive extensions, and `*.pdf` outside cleared output paths) and pushed literature + management baseline across 8 clean sequential commits.
- **Gate `G03 PASS` (`STEP-009` Ratified):** Recorded Supervisor Israt Jahan's approval (`2026-11-27`) of **Option 1** and `RQ1–RQ4` ([DEC0003](01_Project_Management/decision_log/DEC0003.md), [DEC0004](01_Project_Management/decision_log/DEC0004.md), [gates.csv](01_Project_Management/gates.csv), [research_questions.md](02_Literature/research_questions.md)), honestly preserving out-of-repo `[6]–[8]` transcription status as deferred non-blocking note.
- **Public 2D Mammography Discovery (`STEP-010` / `UD05`):** Audited 11 authoritative 2D mammogram sources (`CAND0001–CAND0011`) in `03_Datasets/candidates.csv` and `03_Datasets/reports/candidate_comparison.md` (zero restricted image downloads; segregated biopsy pathology tracks `CMMD/CBIS-DDSM/INbreast/DMID` from radiologist BI-RADS triage `VinDr-Mammo`; quarantined upstream overlap across `DDSM`/`CBIS-DDSM`/`Mini-DDSM` via `DuplicateOf`). Updated `13_Automation/validate_registries.py` for `03_Datasets/candidates.csv` + `DuplicateOf` FK enforcement.

## [v1.0.0-step007-008-009-prep] — 2026-11-26 (`STEP-007`–`008` Complete & `G03` Dossier Prepared)
### Added & Changed
- **Complete `T05` Literature Extractions (`02_Literature/summaries/`, `49` files):** Authored deep locator-backed `13`-section `T05` cards for all `42/42` curated local PDFs (`P0001–P0042`), `6` verified Stage-2 Open-Access landmarks retrieved cleanly via Europe PMC JATS XML / arXiv / PLOS ONE (`P0156, P0385, P0675, P0810, P1030, P1433`), plus `P0063` (`SEED [1]`, `PMC10572157`).
- **Mandatory `UD04` Primary-Source Seed Audit:** Authored `02_Literature/reports/report_bibliography_audit_UD04.md` and `01_Project_Management/decision_log/DEC0004.md` resolving `Table 1.1 SL 1–10` and `Refs [1]–[12]` (`P0063–P0075`), proving `P0063` (`Khalid 2023`) analyzed Kaggle `WDBC` tabular rows in `Sec. 4 Table 3` despite abstract mammography claims and retiring all `10/10` `SL` works to quarantined `B4_CTX` / `Excluded` status (keeping `[6]–[8]` p. 10 strings flagged for physical-PDF check at `G03`).
- **Literature Registries & Claim/Gap Synthesis (`STEP-007–008`):** Populated `02_Literature/claims.csv` (`CLAIM0001–CLAIM0010` + `claim_notes/`), `02_Literature/gaps.csv` (`GAP0001–GAP0005` + `gap_notes/`), and `02_Literature/synthesis.md`; updated `papers.csv`, `screening.csv` (`2,226` rows), `references.bib` (`965` entries), and `13_Automation/validate_registries.py` (`POPULATED_SCIENTIFIC_REGISTRIES` includes `gaps.csv` and `claims.csv`).
- **`STEP-009` Prep Without Self-Approval:** Upgraded `02_Literature/research_questions.md` (`v1.0.0-candidate_G03`) and authored `01_Project_Management/reviews/G03_assessment_2026-11-26.md` while keeping `gates.csv` `G03 = NOT ASSESSED` awaiting supervisor ratification.

## [v1.0.0-step005-006-complete] — 2026-11-26 (`STEP-005` & `STEP-006` Multi-Database Completion Prior to `STEP-007`)
### Added & Changed
- Executed full API bibliographic exports across all accessible protocol databases (`2016–2026`, English) in `02_Literature/searches/raw_exports/` with SHA-256 verification (`export_sha256_manifest.json`): **`DB01` PubMed** (`366` records), **`DB03` OpenAlex** (`1,594` records; open proxy for Scopus/WoS), and **`DB05` arXiv** (`138` filtered 2016–2026 records from `139` raw hits) — totaling `2,098` new database records.
- Authored `T04` search logs for all 5 database sources: `T04_DB01_pubmed.md`, `T04_DB03_openalex.md`, `T04_DB05_arxiv.md`, plus honest institutional-subscription / API-key limitation logs `T04_DB02_ieee_xplore.md` and `T04_DB04_sciencedirect_springerlink.md`.
- Completed deterministic cross-database/cross-query deduplication (`76` matches against baseline `P0001–P0062` + `601` internal/preprint merges = `677` open-DB `EX04` duplicates; combined total `711` duplicates removed across `2,207` intake records) and conservative Stage-1 `title_abstract` PRISMA screening across `1,421` net-new unique studies (`914` advancing to `STEP-007` full-text retrieval [`548` OA URLs + `366` `abstract_only`]; `507` excluded at Stage 1 across `EX01`/`EX02`/`EX03`/`EX05`/`EX06`/`EX07`/`EX09`).
- Expanded `02_Literature/papers.csv` (`1,496` unique rows `P0001–P1496`), `02_Literature/screening.csv` (`2,207` total rows `SCR0001–SCR2207`), `02_Literature/references.bib` (`956` entries), and `02_Literature/searches/screening_summary.md` (`G03` remains `NOT ASSESSED` pending `STEP-007` `T05` extraction, Stage-2 full-text eligibility, and `UD04` seed verification).

## [v1.0.0-step005-006-gs] — 2026-11-25 (`STEP-005` & `STEP-006` Google Scholar Batch)
### Added & Changed
- Protected local downloaded PDFs (`Paper/` and `02_Literature/full_texts/`) in `.gitignore` so zero copyrighted PDFs enter Git history.
- Logged 8 executed Google Scholar query batches (`02_Literature/searches/T04_GS-Q1a.md`–`T04_GS-Q4.md`), `gs_download_manifest.csv` (`96` downloaded records), and `T04_SEED_title_report.md` (`13` Title Report seed leads).
- Populated `02_Literature/papers.csv` (`75` rows: `P0001–P0042` curated local studies, `P0043–P0062` excluded unique studies, `P0063–P0075` unverified seed leads) and initial `02_Literature/references.bib`.
- Recorded full-text PRISMA screening and cross-query deduplication in `02_Literature/screening.csv` (`109` rows) and `02_Literature/searches/screening_summary.md` (`96` downloaded → `34` duplicates removed → `62` unique full-text screened → `42` included across `B1`/`B2`/`B3_METH`/`B4_CTX`, `20` excluded across `EX01`/`EX02`/`EX05`/`EX06`).
- Updated `13_Automation/validate_registries.py` and `tests/test_registries.py` to enforce foreign-key integrity on `02_Literature/{papers,screening}.csv` while keeping downstream scientific registries (`03_Datasets/`–`16_Web_Demo/`) header-only. (`DB01–DB05` systematic searches, `STEP-007` `T05`/`UD04` extraction, and `G03` remain open.)

## [v1.0.0-step004] — 2026-11-23 (`STEP-004`)
### Added
- Created and approved the PRISMA 2020 systematic literature search, screening, and quality appraisal protocol (`02_Literature/searches/protocol.md`) featuring four Boolean query families (`Q1–Q4`), inclusion codes `INC01–INC04`, exclusion codes `EX01–EX09`, taxonomic modality/task buckets `B1–B4_CTX`, and the forensic audit plan for Table 1.1 & References `[1]`–`[12]` (`UD04`).
- Authored provisional operational research questions `RQ1–RQ4` mapped to Objectives `O1–O6` (`02_Literature/research_questions.md`, `v0.9.0-provisional`).
- Recorded Phase-1 `UD03` search-protocol approval in `01_Project_Management/decision_log/DEC0003.md` and `01_Project_Management/decisions.csv` (keeping final Q1 novelty positioning & RQ ratification open for `STEP-009` / `G03`).

## [v1.0.0-step003] — 2026-11-23 (`STEP-003` / `G02 PASS`)
### Added
- Materialized all 35 blank canonical operational templates (`T01–T35`) in `14_Templates_Prompts/` (`T01_readme.md` through `T35_demo_runbook.md`, including `T15_config.yaml`).
- Initialized all 24 canonical CSV registries matching [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b) and [Appendix A.4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a) verbatim (`01_Project_Management/{decisions,risk_register,gates}.csv` populated with real governance records; all 21 scientific registries initialized strictly header-only with zero dummy rows).
- Created `01_Project_Management/dashboard.md` and `01_Project_Management/timeline.md`.
- Implemented `13_Automation/validate_registries.py` and `tests/test_registries.py` verifying all 24 CSV schemas, 35 templates, primary-key uniqueness, header-only scientific initialization, and foreign-key integrity (`7/7 pytest checks PASSED`).
- Completed and passed quality gate `G02` (`01_Project_Management/reviews/G02_assessment_2026-11-23.md`, `GATE0002 = PASS`).

## [v1.0.0-step002] — 2026-11-23 (`STEP-002`)
### Added
- Materialized the complete 20-folder canonical repository architecture defined in [OS §2](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02) with `T01`-compliant `README.md` contracts in every domain directory.
- Added root governance files: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `.gitignore`, and `.gitattributes` (deferring `LICENSE` until `UD24` approval per `STEP-002`).
- Established four-tier storage isolation rules ([OS §10.2](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10)) blocking restricted mammograms/DICOMs (`03_Datasets/raw/`), processed images (`05_Preprocessing/processed/`), checkpoints (`08_Checkpoints/*.pt|*.pth|*.h5|*.ckpt|*.onnx`), private patient linkage tables, secrets, and local structural reference files from Git.
- Pinned and smoke-tested the Phase-1 data-tool runtime (`environment/data/requirements.txt` and `environment/data/verification.md`) on Python 3.14.6 (`numpy==2.5.1`, `pandas==3.0.6`, `scipy==1.18.1`, `scikit-learn==1.9.1`, `pillow==12.3.0`, `opencv-python==5.0.0.93`, `networkx==3.7`, `PyYAML==6.0.3`, `jsonschema==4.26.0`, `pytest==9.1.1`) via `tests/test_step002_smoke.py`.
- Documented installation and storage-tier pipeline contracts in `12_Documentation/installation.md` and `12_Documentation/pipeline.md`.
- Recorded Phase-1 storage and runtime decision `01_Project_Management/decision_log/DEC0014.md` (`UD14` Phase 1; Phase-2 GPU/DL stack remains deferred to `STEP-023`).

## [v1.0.0-step001] — 2026-11-23 (`STEP-001` / `G01 PASS`)
### Added
- Created and ratified `01_Project_Management/scope.md` preserving verbatim title (`RF01`), team/supervisory roles (`RF02`), Objectives `O1–O6` (`RF12`), required metrics (`RF09`), and Section 8 exclusions (`RF15`).
- Initialized `01_Project_Management/decisions.csv` registering all 28 decisions (`DEC0001–DEC0028` / `UD01–UD28`) with named owners and blocking steps.
- Ratified `01_Project_Management/decision_log/DEC0001.md` (`UD01`) and passed quality gate `G01` (`01_Project_Management/reviews/G01_assessment_2026-11-23.md`).

## [v1.0.0] — 2026-11-23 (Initial Planning Baseline)
### Added
- Authored `BC_XAI_RESEARCH_OPERATING_SYSTEM.md` (`v1.0.0`) and `BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md` (`v1.0.0`) covering 16 stages (`S01–S16`), 50 20-field steps (`STEP-001`–`STEP-050`), 17 quality gates (`G01–G17`), 24 canonical CSV registry schemas, and 35 operational templates (`T01–T35`).

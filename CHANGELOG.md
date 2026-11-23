# Changelog

All notable governance, repository, and scientific execution milestones for **Explainable Deep Learning-Based Early Breast Cancer Detection Using Mammogram Images** are documented in this file.

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

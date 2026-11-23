# Mammography Preprocessing and Release Materialization (`05_Preprocessing/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `05_Preprocessing/` |
| `Owner` | Alzubair Ahamed (Implementer) & Md Riyadul Hasan (Data Lead) |
| `Governing Section` | [OS §4.4, §4.6](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [Blueprint STEP-019, 021](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-019) |
| `Sensitivity Tier` | Mixed: Specs, YAML configs, registry, and reports in Tier-1 Git; `processed/REL####/` images and binary fitted states in Tier-2 Restricted Storage |

## Purpose
Governs deterministic mammography preprocessing specifications (`specs/`), versioned configurations (`configs/`, isolating CLAHE contrast enhancement as a controlled ablation from baseline `PP####`), `preprocessing_registry.csv`, visual/geometry QA reports (`reports/`), training-only fitted normalization states, and immutable prepared releases (`processed/REL####/`).

# Public Mammogram Datasets and Leakage-Safe Splits (`03_Datasets/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `03_Datasets/` |
| `Owner` | Md Riyadul Hasan (Data Steward) & Alzubair Ahamed (Verifier) |
| `Governing Section` | [OS §4](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [Blueprint STEP-010–013, 020](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-010) |
| `Sensitivity Tier` | Mixed: Safe CSV registries/reports in Tier-1 Git; `raw/` mammograms and private linkage maps strictly in Tier-2 Restricted Storage |

## Purpose
Governs multi-dataset 2D mammography candidate discovery (`candidates.csv`, evaluating the team's 6-dataset pool under `UD05`), licenses/DUAs & ethics waivers (`licenses/`), immutable raw inventories (`datasets.csv`, restricted `raw/DS####/`), technical/PHI quality reports (`reports/`), connected-component patient-level splits (`splits/SPLIT####/`), and prepared release manifests (`releases.csv`).

## Forbidden Contents in Git
- Raw DICOM/PGM/PNG mammogram files (`03_Datasets/raw/`) and identifying patient linkage tables.

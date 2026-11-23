# Automated Test Suite (`tests/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `tests/` |
| `Owner` | Md Riyadul Hasan (Evaluation/Reproducibility Lead) & Alzubair Ahamed (Implementer) |
| `Governing Section` | [OS §2.2](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02) |
| `Sensitivity Tier` | Tier-1 Source Control (Synthetic or license-permitted fixtures only) |

## Purpose
Contains unit, integration, geometry, connected-component leakage, statistical (DeLong/McNemar/clustered bootstrap), XAI faithfulness/sanity, and parity tests.

## Allowed Contents
- `pytest` test modules (`test_*.py`) and synthetic in-memory fixtures.

## Forbidden Contents
- Unlicensed, unreviewed, or PHI-bearing clinical mammograms or model checkpoint binaries.

## Commands
```powershell
python -m pytest tests/ -v
```

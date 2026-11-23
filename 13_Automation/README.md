# Thin Automation and Validation Entry Points (`13_Automation/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `13_Automation/` |
| `Owner` | Alzubair Ahamed & Md Riyadul Hasan (Implementers) |
| `Governing Section` | [OS §2.2](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02) |
| `Sensitivity Tier` | Tier-1 Source Control |

## Purpose
Houses thin CLI wrapper scripts for registry/schema/link validation (`validate_registries.py` at `STEP-003`), experiment training/evaluation orchestration, figure rendering (`generate_figures.py`), and local CAD prototype execution (`run_cad_prototype.py`).

## Contract
- Reusable scientific logic belongs in `src/bc_xai/`; scripts in `13_Automation/` are strictly thin CLI callers and never auto-approve scientific gates.

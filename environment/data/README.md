# Phase-1 Minimal Data, QC & Governance Runtime (`environment/data/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `environment/data/` |
| `Owner` | Md Riyadul Hasan (Data Steward) & Alzubair Ahamed (Implementer) |
| `Governing Section` | [OS §10.3](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [Blueprint STEP-002](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-002) |
| `Sensitivity Tier` | Tier-1 Source Control |

## Purpose
Provides the pinned, smoke-tested Phase-1 Python runtime for:
1. Canonical CSV registry validation and foreign-key integrity checks (`STEP-003`).
2. Read-only mammogram image inventory, SHA-256 hashing, 16-bit/polarity (`MONOCHROME1/2`) QC, and ROI-mask coordinate co-transform verification (`STEP-012–019`).
3. Connected-component patient/laterality/view/duplicate graph grouping and leakage-safe splitting (`STEP-020`).

## Contents
- `requirements.txt` — Pinned Phase-1 package versions observed and tested on the workstation.
- `verification.md` — Observed runtime inventory, hardware record, `.gitignore` safety audit, and `pytest` smoke-test verification output.

## Workflow Commands
```powershell
python -m pytest tests/test_step002_smoke.py -v
```

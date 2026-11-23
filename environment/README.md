# Environment Locks and Hardware Inventories (`environment/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `environment/` |
| `Owner` | Alzubair Ahamed (Model/XAI Lead) & Md Riyadul Hasan (Data/Reproducibility Lead) |
| `Governing Section` | [OS §2.2](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §10.3](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10) |
| `Sensitivity Tier` | Tier-1 Source Control (Zero credentials or tokens allowed) |

## Purpose and Two-Phase Architecture
Per [OS §10.3](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10), environment readiness is separated into two immutable phases so early data/QC/splitting provenance is never overwritten by later GPU/deep-learning upgrades:
- `environment/data/` — **Phase 1 Minimal Data, QC, Graph-Splitting & Registry Runtime** (`STEP-002`, verified at `G02`).
- `environment/model/` — **Phase 2 Deep Learning, Transfer Learning, XAI & Statistical Runtime** (`STEP-023`, verified at `G09` after `UD13` architecture selection).

## Allowed Contents
- Pinned dependency lockfiles (`requirements.txt` / environment manifests), observed hardware & OS inventories, and smoke-test verification reports (`verification.md`).

## Forbidden Contents
- Virtual environment binaries (`.venv/`), API keys/tokens, or unverified speculative package pins claimed as tested.

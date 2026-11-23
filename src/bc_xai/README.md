# Core Reusable Mammography XAI Package (`src/bc_xai/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `src/bc_xai/` |
| `Owner` | Alzubair Ahamed (Model/XAI Lead) & Md Riyadul Hasan (Data/Evaluation Lead) |
| `Governing Section` | [OS §2.2–2.3](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02) |
| `Sensitivity Tier` | Tier-1 Source Control |

## Purpose
Centralizes all reusable Python modules for dataset inventory/QC, diagnostic label & ROI-mask verification, connected-component patient splitting, deterministic preprocessing, multi-architecture transfer learning, quantitative XAI faithfulness/sanity/localization evaluation, calibration, paired statistical tests, and the local research CAD prototype.

## Allowed Contents
- Pure modular Python source code (`data/`, `labels/`, `preprocess/`, `models/`, `train/`, `xai/`, `eval/`, `infer.py`).
- All scientific parameters must be passed via validated YAML configurations (`T15`).

## Forbidden Contents
- Raw or processed mammogram images, model weight binaries, hardcoded local paths, or hidden hyperparameter defaults.

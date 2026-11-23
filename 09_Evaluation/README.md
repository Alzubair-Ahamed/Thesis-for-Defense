# Q1 Classification, Calibration, Statistical, and Quantitative XAI Evaluation (`09_Evaluation/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `09_Evaluation/` |
| `Owner` | Md Riyadul Hasan (Evaluation Lead) & Alzubair Ahamed (XAI Lead) |
| `Governing Section` | [OS §6.3–6.4](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [Blueprint STEP-024, 032–037](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-032) |
| `Sensitivity Tier` | Mixed: Protocols, `freeze.md`, registries, aggregate CSVs, and reports in Tier-1 Git; raw per-image predictions, raw 2D saliency arrays, and private visual plates in Tier-3 Storage |

## Purpose
Houses `protocol.md`, `freeze.md` (`G11`), `evaluation_registry.csv` (`EVAL####`), `xai_audit_registry.csv` (`XAIA####`), `statistical_comparisons.csv` (`STAT####`), and per-evaluation bundles (`EVAL####/` covering all 6 report metrics + Specificity/PR-AUC/MCC/clinical operating points, ECE/Brier calibration, patient-clustered bootstrap 95% CIs, DeLong/McNemar/Holm-Bonferroni tests, Deletion/Insertion/ROAD faithfulness, Adebayo sanity checks, ROI Pointing Game/EBPG/IoU, density/view/subtype subgroups, FN/FP taxonomy, and blinded clinical-advisor review).

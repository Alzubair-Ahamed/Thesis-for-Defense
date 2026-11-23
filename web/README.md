# Conditional Thin Defense Web Showcase Application (`web/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `web/` |
| `Owner` | Alzubair Ahamed (Deployment Owner) |
| `Governing Section` | [OS §8.3](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-08-3); [Blueprint STEP-048–050](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-048) |
| `Sensitivity Tier` | Tier-1 Source Control (Zero model weights, patient uploads, or secrets in Git) |

## Purpose
Houses the conditional FYDP defense web frontend, API, `Dockerfile`, dependency lock, and web tests (`S16`, gated by `UD25`). Must import the frozen `STEP-038` `src/bc_xai/infer.py` CAD + Grad-CAM entry point unchanged without duplicating preprocessing, calibration, thresholds, or Grad-CAM logic.

# Immutable Checkpoint Registry and Recovery Manifests (`08_Checkpoints/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `08_Checkpoints/` |
| `Owner` | Alzubair Ahamed (Experiment Lead) |
| `Governing Section` | [OS §5.4](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [Blueprint STEP-026, 028–029](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-026) |
| `Sensitivity Tier` | Mixed: `checkpoint_registry.csv`, `checkpoint_policy.md`, and `manifests/CKPT####.md` in Tier-1 Git; binary `.pt`/`.pth`/`.onnx` weights strictly in Tier-3 Artifact Storage |

## Purpose
Tracks immutable `CKPT####` provenance, saved training-state components, SHA-256 digests, Tier-3 backup pointers, and interruption/restoration verification evidence.

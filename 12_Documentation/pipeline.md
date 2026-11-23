# Research Pipeline, Storage Tiers, and Lineage Contract

- **Document:** `12_Documentation/pipeline.md`
- **Version / Date:** `v1.0.0` / `2026-11-23`
- **Governing Section:** [OS §2](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §10](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [Blueprint STEP-002](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-002)

---

## 1. Four-Tier Storage and Privacy Firewall ([OS §10.2](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10))

| Storage Tier | Allowed Artifact Types | Canonical Locations | Git Policy & Access Control |
|---|---|---|---|
| **Tier 1: Source Control** | Modular Python code (`src/bc_xai/`), unit tests (`tests/`), YAML configs, non-sensitive CSV registries, markdown reports, aggregate metrics, SHA-256 pointers | Git repository synced to `https://github.com/Alzubair-Ahamed/Thesis-for-Defense.git` (`main`) | Tracked in Git; inspect `git status` and `git diff --cached` before every commit |
| **Tier 2: Restricted Medical Data** | Immutable raw mammogram archives/DICOMs (`DS####`), native/verified lesion ROI masks (`LBL####`), private `PatientID` linkage tables, processed image releases (`REL####`), serialized training-only fitted states | `03_Datasets/raw/`, `04_Labels_XAI_Governance/restricted_masks/`, `05_Preprocessing/processed/` (local encrypted/access-controlled disk + off-disk backup) | **Strictly blocked by `.gitignore`**; governed by dataset DUAs (`UD06`) |
| **Tier 3: Research Artifacts** | Trained model checkpoints (`CKPT####`), exported weights (`MODEL####`), full per-image test predictions, raw 2D XAI attribution arrays, bootstrap replicates, private clinical-review plates | `06_Models/weights/`, `08_Checkpoints/*.pt|*.pth|*.onnx`, `09_Evaluation/EVAL*/xai/raw_arrays/` + durable cloud/institutional artifact backup | **Strictly blocked by `.gitignore`**; addressed in Tier-1 registries by immutable path + SHA-256 |
| **Tier 4: Release & Archive** | Immutable release snapshots (`ARCH####`), compiled FYDP thesis & Q1 journal submission PDFs, official portal receipts, lawful public release bundle (`UD24`) | `15_Archive/` (manifests in Git; large bundles in write-once Tier-4 storage) | Public subset released only after license, DUA, and PHI disclosure sign-off (`STEP-046`) |

---

## 2. Cryptographic Data & Artifact Lineage Chain ([OS §2.3](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02))

```text
Source Portal Archive
  └──> DS#### (03_Datasets/datasets.csv; immutable raw SHA-256 inventory)
         ├──> LBL#### (04_Labels_XAI_Governance/label_registry.csv; verified Benign/Malignant labels & ROI masks)
         ├──> XAIP#### (04_Labels_XAI_Governance/xai_protocol_registry.csv; prospective Grad-CAM & XAI metric contract)
         └──> SPLIT#### (03_Datasets/splits/SPLIT####/manifest.csv; connected-component patient/view/duplicate split)
                └──> PP#### (05_Preprocessing/preprocessing_registry.csv; training-only fitted preprocessing state)
                       └──> REL#### (03_Datasets/releases.csv; immutable prepared dataset release)
                              └──> EXP#### / RUN#### (07_Experiments/experiment_registry.csv)
                                     └──> CKPT#### (08_Checkpoints/checkpoint_registry.csv)
                                            └──> MODEL#### (06_Models/model_registry.csv)
                                                   ├──> EVAL#### (09_Evaluation/evaluation_registry.csv)
                                                   ├──> XAIA#### (09_Evaluation/xai_audit_registry.csv)
                                                   └──> STAT#### (09_Evaluation/statistical_comparisons.csv)
                                                          ├──> FIG#### / TAB#### (10_Figures_Tables/assets.csv)
                                                          ├──> CLAIM#### / WR#### (11_Writing/writing_registry.csv)
                                                          ├──> DEPLOY#### (16_Web_Demo/deployment_registry.csv; conditional S16)
                                                          └──> ARCH#### (15_Archive/archive_manifest.csv)
```

---

## 3. Active Verification Commands

- **Phase-1 Smoke & `.gitignore` Safety Suite (`STEP-002`):**
  ```powershell
  python -m pytest tests/test_step002_smoke.py -v
  ```
- **Canonical Registry & Template Validator (to be added in `STEP-003`):**
  ```powershell
  python 13_Automation/validate_registries.py
  ```

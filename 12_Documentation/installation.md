# Environment Installation and Two-Phase Setup Guide

- **Document:** `12_Documentation/installation.md`
- **Version / Date:** `v1.0.0` / `2026-11-23`
- **Governing Section:** [OS §10.3](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [Blueprint STEP-002](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-002) & [STEP-023](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-023)

---

## 1. Two-Phase Environment Architecture ([OS §10.3](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10))

To prevent later deep-learning or CUDA library changes from altering early dataset QC, preprocessing, or patient-level splitting outputs, this repository separates runtime dependencies into two locked phases:

1. **Phase 1 — Minimal Data, QC, Graph-Splitting & Registry Runtime (`environment/data/`):**
   - Established and verified in `STEP-002` (audited at `G02`).
   - Supports CSV registry schema checks (`STEP-003`), read-only mammogram inventory & SHA-256 hashing (`STEP-012–013`), label/ROI-mask verification (`STEP-016–018`), connected-component patient splitting (`STEP-020`), and deterministic preprocessing (`STEP-021`).
2. **Phase 2 — Deep Learning, Transfer Learning, XAI & Statistical Runtime (`environment/model/`):**
   - Deferred until `STEP-023` (audited at `G09`) after the candidate CNN architecture roster (`UD13`) is ratified in `STEP-022`.

---

## 2. Phase-1 Setup and Verification Commands (`environment/data/`)

### 2.1Observed Workstation Baseline (`2026-11-23`)
- **OS:** Windows 11 (`Windows-11-10.0.26300-SP0`, 64-bit AMD64)
- **Python Runtime:** `Python 3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026) [MSC v.1944 64 bit (AMD64)]`
- **Lockfile:** [environment/data/requirements.txt](../environment/data/requirements.txt)

### 2.2 Install or Verify Phase-1 Packages
```powershell
python -m pip install -r environment/data/requirements.txt
```

### 2.3 Run Phase-1 Smoke Verification Suite
```powershell
python -m pytest tests/test_step002_smoke.py -v
```

See [environment/data/verification.md](../environment/data/verification.md) for the recorded verification log and SHA-256 digests.

---

## 3. Adding Format-Specific Readers (e.g., `pydicom`)
Before acquiring raw DICOM mammography datasets (such as VinDr-Mammo, INbreast, or CBIS-DDSM) in `STEP-012`, install, pin, and smoke-test any format-specific reader (e.g., `pydicom`, `pylibjpeg`) in `environment/data/requirements.txt` and append the verification record to `environment/data/verification.md`.

---

## 4. Phase-2 Model Runtime (`environment/model/` — Pending `STEP-023`)
- **Status:** `Deferred until STEP-023 (blocked by G08 and STEP-022 / UD13)`
- Do **not** install or pin unapproved deep-learning frameworks in `environment/data/`.

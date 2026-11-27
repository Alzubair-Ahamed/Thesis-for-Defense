# Phase-1 Minimal Data-Tool Runtime and Storage-Firewall Verification (`STEP-002`)

- **Document:** `environment/data/verification.md`
- **Date:** `2026-11-23`
- **Governing Step / Section:** [Blueprint STEP-002](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-002); [OS §10.3](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10)
- **Decision Reference:** [DEC0014](../../01_Project_Management/decision_log/DEC0014.md) (`UD14` Phase 1)
- **Status:** `VERIFIED (5/5 pytest smoke checks PASSED)`

---

## 1. Observed Runtime and Workstation Inventory (`2026-11-23`)

| Property | Observed Value |
|---|---|
| **Operating System** | `Windows-11-10.0.26300-SP0` (64-bit AMD64) |
| **Python Interpreter** | `Python 3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)]` |
| **Executable Path** | `C:\Users\ASUS\AppData\Local\Programs\Python\Python314\python.exe` |
| **Phase-1 Lockfile** | `environment/data/requirements.txt` |

### Pinned Phase-1 Dependencies Verified
- `numpy==2.5.1`
- `pandas==3.0.6`
- `scipy==1.18.1`
- `scikit-learn==1.9.1`
- `pillow==12.3.0`
- `opencv-python==5.0.0.93`
- `networkx==3.7`
- `PyYAML==6.0.3`
- `jsonschema==4.26.0`
- `pytest==9.1.1`
- `tabulate==0.10.0`
- `psutil==7.2.2`

*(Note: Deep-learning, GPU, and XAI package pins remain deferred to Phase-2 `environment/model/` at `STEP-023` per [OS §10.3](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10).)*

---

## 2. Executed Smoke-Test Output (`tests/test_step002_smoke.py`)

Command executed:
```powershell
python -m pytest tests/test_step002_smoke.py -v
```

Observed output (`2026-11-23`):
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\ASUS\AppData\Local\Programs\Python\Python314\python.exe
cachedir: .pytest_cache
rootdir: D:\Zubair Riyad Thesis
plugins: anyio-4.15.1
collecting ... collected 5 items

tests/test_step002_smoke.py::test_section2_directory_skeleton_and_readmes PASSED [ 20%]
tests/test_step002_smoke.py::test_decisions_registry_schema_and_g01_state PASSED [ 40%]
tests/test_step002_smoke.py::test_synthetic_16bit_mammogram_polarity_and_roi_cotransform PASSED [ 60%]
tests/test_step002_smoke.py::test_connected_component_patient_view_duplicate_grouping PASSED [ 80%]
tests/test_step002_smoke.py::test_gitignore_blocks_restricted_medical_and_reference_paths PASSED [100%]

============================== 5 passed in 5.17s ==============================
```

---

## 3. Verified Capabilities
1. **Repository Skeleton (`test_section2_directory_skeleton_and_readmes`):** All 21 Section 2 directories (`environment`, `environment/data`, `src/bc_xai`, `tests`, `01_Project_Management` through `16_Web_Demo`, `web`) exist and contain `T01`-compliant `README.md` contracts.
2. **Registry Parsing (`test_decisions_registry_schema_and_g01_state`):** `01_Project_Management/decisions.csv` parses cleanly with 16 canonical columns, 28 `UD` rows, and `UD01 = Approved`.
3. **Mammogram 16-Bit Polarity & ROI Co-Transform (`test_synthetic_16bit_mammogram_polarity_and_roi_cotransform`):** Verified `MONOCHROME1` → `MONOCHROME2` 12/16-bit inversion and 1:1 lesion ROI-mask spatial preservation during resizing.
4. **Connected-Component Patient Grouping (`test_connected_component_patient_view_duplicate_grouping`):** Verified `networkx` equivalence graph keeps multi-view (LCC/RCC/LMLO/RMLO), longitudinal studies, and perceptual near-duplicates grouped atomically.
5. **Storage-Tier Firewall (`test_gitignore_blocks_restricted_medical_and_reference_paths`):** Confirmed via `git check-ignore` that raw DICOMs (`03_Datasets/raw/`), private linkage CSVs, processed images (`05_Preprocessing/processed/`), checkpoints (`08_Checkpoints/*.pth|*.onnx`), `.env` secrets, and workspace reference files (`Title_defence_evaluation_report.pdf`, `OPG_*`) are strictly blocked from Git tracking.

---

## Phase-1B Extension — DICOM Codecs & Local Workstation Verification (`2026-11-27`)

- **Verification Timestamp:** `2026-11-27T22:51+06:00`
- **Verified Workstation Environment:** `Python 3.14.10 (tags/v3.14.10:b703b2c, Oct 25 2026, 17:36:52) [MSC v.1944 64 bit (AMD64)]` (Windows 11, virtual environment `.venv/`)
- **Updated Lockfile ([requirements.txt](./requirements.txt)) SHA-256:** `2db0a7097d6495d4405d0e16822d0629a6338002e68bf4c1b151b0b0f528f338`
- **Format-Specific Readers Pinned Prior to `STEP-013`:**
  - `pydicom==3.0.2`
  - `pylibjpeg==2.1.0`
  - `pylibjpeg-libjpeg==2.5.0` *(verified decoding `DS0002_DMID` `JPEG Lossless, Non-Hierarchical, First-Order Prediction (Process 14 [Selection Value 1])`)*
  - `pylibjpeg-openjpeg==2.6.0`
  - `python-gdcm==3.2.6` *(C++ GDCM DICOM pixel codec — accelerated `DS0002_DMID` JPEG Lossless decode by ~5.5x alongside multiprocessing)*
  - `openpyxl==3.1.5` *(xlsx cohort metadata inspection)*
- **Verification Outputs Observed:**
  - `.venv/Scripts/python.exe -m pytest tests/ -v`: **`16 passed in 5.90s`** (`0` errors, `0` skipped)
  - `.venv/Scripts/python.exe 13_Automation/validate_registries.py`: **`VALIDATION PASSED`** (`24/24` canonical CSV registries, `35/35` templates, foreign keys clean)
  - Live sample pixel decode verified across `DS0002_DMID` (`IMG001.dcm`, JPEG Lossless Process 14 SV1, `(6000, 4751, 3)` `uint8`), `DS0003_CMMD` (`00000001.dcm`, Explicit VR Little Endian, `(2294, 1914)` `uint8`), and `DS0005_BMCD` (`CC_prior.dcm`, Explicit VR Little Endian, `(4096, 3328)` `uint16`).

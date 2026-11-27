# G04 Gate Assessment Package — Dataset Intake, Technical QC, PHI Audit & `UD05` Cohort Approval (`T24`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T24` (`T24_gate_audit.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `GATE0004` (`G04`) |
| `owner` | Md Riyadul Hasan (`232-15-486`, Data Steward) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-28` (Prep `2026-11-27`; Ratified **`PASS`** `2026-11-28`) |
| `status` | **`PASS` (`GATE0004` Ratified `2026-11-28` — `5` Clean `CC BY` Cohorts = `7,420` Retained Scans & `17` Clone Quarantines Approved)** |
| `source_inputs` | [DEC0005.md](../decision_log/DEC0005.md); [DEC0006.md](../decision_log/DEC0006.md); [datasets.csv](../../03_Datasets/datasets.csv); [DS0001_quality.md](../../03_Datasets/reports/DS0001_quality.md); [DS0002_quality.md](../../03_Datasets/reports/DS0002_quality.md); [DS0003_quality.md](../../03_Datasets/reports/DS0003_quality.md); [DS0005_quality.md](../../03_Datasets/reports/DS0005_quality.md); [DS0006_quality.md](../../03_Datasets/reports/DS0006_quality.md); `DS0001–0006` `T08` Cards |
| `governing_section` | [OS §1.5, §4, §13 (`G04`)](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [Blueprint STEP-010–013](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-013) |
| `sensitivity` | Tier-1 Ratified Gate Assessment Record |
| `reviewer` | Israt Jahan (Supervisor); Ms Faiza Feroz (Co-Supervisor); Md Riyadul Hasan (`232-15-486`); Alzubair Ahamed (`232-15-591`) — Ratified `2026-11-28` |

---

## 1. AssessmentID, GateID, and Current Status
- **`AssessmentID`:** `GATE0004`
- **`GateID`:** `G04` (`Feeds S07 / STEP-014` Label & ROI Mask Protocol)
- **`Gate Status in gates.csv`:** **`PASS`** (`Ratified 2026-11-28`, `v1.2.0`).

---

## 2. Bound EntityVersions and Exact SHA-256 Digests

| Artifact (`Tier-1 Repository`) | Role / Version | Verified SHA-256 Digest |
|---|---|---|
| [requirements.txt](../../environment/data/requirements.txt) | Phase-1 + DICOM codecs (`pydicom`, `pylibjpeg`, `python-gdcm`, `openpyxl`) | `2db0a7097d6495d4405d0e16822d0629a6338002e68bf4c1b151b0b0f528f338` |
| [verification.md](../../environment/data/verification.md) | `Python 3.14.10` & codec verification record | `16642097b8504b1c9bf65f1649e84df33b05c9fa7344ffcfa26f74f37fcdc556` |
| [inventory.py](../../src/bc_xai/data/inventory.py) | `STEP-012` immutable SHA-256 inventory engine | `44210434589b5c6f67fdab4b75e6ecda719b6336980c3c48c6950c29f7d03d72` |
| [qc.py](../../src/bc_xai/data/qc.py) | `STEP-013` read-only QC, PHI & clone detector | `06e51f9c071aeba9bfba05670d3f4f74294c411dd8c282ce2c17a46d43a8eda2` |
| [test_qc.py](../../tests/test_qc.py) | Unit tests (`MONOCHROME1`, blank, corrupt, CESM, pixel-clone) | `1c2e6ba8d07b542a85dc62b6f91460caebdd23faa7bccce2ba8f99e246ee1909` |
| [DEC0005.md](../decision_log/DEC0005.md) | `UD05` 5-cohort roster decision (`v1.2.0`, Approved `2026-11-28`) | `648aa0b2e9d188412ebbc0aca92e28c109dd43a5ab4b3b970ea183233fc40f30` |
| [DEC0006.md](../decision_log/DEC0006.md) | `UD06` DIU waiver + Batch A `CC BY` clearance | `88b0ba9ab59db88be3bb6abca5ebe72021fe8f4abdb02c50c2cd36fcbbb1b884` |
| [datasets.csv](../../03_Datasets/datasets.csv) | Registered cohort ledger (`v1.2.0`, `Approved_G04_PASS_Locked`) | `a4cfcb382ab109fe80b2706bdf330a596081904be31fa87cdacde03c5377e065` |
| [DS0001_quality.md](../../03_Datasets/reports/DS0001_quality.md) / [DS0001_card.md](../../03_Datasets/reports/DS0001_card.md) | `MIAS v1.21` (`322 / 322` retained; Manifest `2e3f8559...`) | `b01210513c322430a71cbba4f6d9111ec6dbc1c3a7cc8fca3d5e2760e0cee565` / `894920ffc9147c25849f81e9505acff904022e926204f02f4bfe15a7e6f6f319` |
| [DS0002_quality.md](../../03_Datasets/reports/DS0002_quality.md) / [DS0002_card.md](../../03_Datasets/reports/DS0002_card.md) | `DMID` (`507 / 510` retained, `3` clones quarantined; Manifest `40882b4e...`) | `66f1690d3a0c20e47a11d5322dae64ee88cbcc20b69a5c455c25b21e8296d1cc` / `20600e910c5cf44819dbb88de845bba62b2fa43620eb94e8ea26bdbc5d9ccd4a` |
| [DS0003_quality.md](../../03_Datasets/reports/DS0003_quality.md) / [DS0003_card.md](../../03_Datasets/reports/DS0003_card.md) | `CMMD` (`5,196 / 5,202` retained, `6` clones quarantined; Manifest `b933e5f7...`) | `e9d64b6b84d3558a22441dcd1ca2a0e13ffba443e87be36d2b0a23d0e1b079b3` / `1178e3345865718a85b6a910da3789a34fb5f90dd2cea72e0f606c64d186c024` |
| [DS0005_quality.md](../../03_Datasets/reports/DS0005_quality.md) / [DS0005_card.md](../../03_Datasets/reports/DS0005_card.md) | `BMCD` (`392 / 400` retained, `8` clones quarantined; Manifest `4a1faa4c...`) | `6b8290309dbbfa7058c50002b17704b972c2c06169ec741386593c336aa73b14` / `e7e90ccb8e33c27484e1b4dbaa88426904d6f97876a44139d80e3a63112d4107` |
| [DS0006_quality.md](../../03_Datasets/reports/DS0006_quality.md) / [DS0006_card.md](../../03_Datasets/reports/DS0006_card.md) | `CDD-CESM LE` (`1,003 / 1,003` retained + `1,003` CESM excluded; Manifest `e1732776...`) | `e05dc8338baaf94486ad9fbcfec21d189a6e2c2e89fc1e04dbd555db0c4244e3` / `a0473ee6767b43b58ec23dbf7ef4304c758c58a2466f1a4d33eaca50e03757f1` |

---

## 3. Itemized Mandatory `G04` Criteria Audit Table

| # | Mandatory `G04` Criterion ([OS §13](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13) & `STEP-010–013`) | Verified Evidence & Observed Figures | Gate Status | Required Action / Notes |
|---|---|---|---|---|
| 1 | **Primary-source `UD05` roster & `UD06` license/DIU waiver clearance** | `CAND0001–CAND0013` documented ([DEC0005](../decision_log/DEC0005.md)); DIU Batch A waiver + `CC BY` terms approved in [DEC0006](../decision_log/DEC0006.md) and ratified in `DEC0005` (`2026-11-28`) across all `5` cohorts (`CMMD, CDD-CESM LE, BMCD, DMID, MIAS`). | **PASS** | Batch B (`VinDr/INbreast`) remains optional & non-blocking. |
| 2 | **Immutable raw SHA-256 custody (`STEP-012`) & zero raw mutation post-QC** | `14,295` total raw files hashed cleanly; `verify_manifest_integrity` reported **`0 / 0` mismatches** pre- & post-QC across all `5` `DS####` raw directories. Unused `23.41 GB` partial `DS0004_CBIS_DDSM` left untouched outside scope. | **PASS** | Verified intact. |
| 3 | **`100%` mammogram decode, bit-depth, polarity (`MONOCHROME1/2`), Rescale & VOI audit** | **`7,437 / 7,437`** primary track scans (`+510` DMID TIFFs, `+400` BMCD overlays, `+1,003` CESM excluded) decoded `100%` cleanly (`0` corrupt/blank). Identified `5,200` `8b` + `2` `16b` in CMMD (`IMG00003519–3520`), `400` `12b uint16` in BMCD, `488 RGB (R=G=B) + 22 M2` in DMID, `0` `MONOCHROME1` traps. | **PASS** | `STEP-021` preprocessing will branch normalization on `BitsStored` / dtype rather than hardcoding `/255`. |
| 4 | **DICOM header PHI & `.gitignore` Tier-2 firewall** | `0` non-pseudonym PHI tags across `6,112` DICOMs (`CMMD` uses `PatientName == PatientID` pseudonym echo; `BMCD` epoch `1970`; `DMID` zero clinic identifiers); excluded `desktop.ini` & Word lock `~$P54.docx`; `git check-ignore` blocks `.venv/`, `raw/`, `cache/qc/`, `images/qc_contact_sheets/`. | **PASS** | Verified intact. |
| 5 | **Within- & cross-cohort exact + pixel-clone duplicate audit + `Acquired = Retained + Excluded + Quarantined` math** | `0` cross-cohort overlaps (`0` cross-cohort exact/pixel clones). Uncovered & quarantined **`17` intra-cohort clones**: **`3`** in `DMID` (`IMG172/318/319`), **`6`** in `CMMD` (`D1-0202=D2-0284`, `D1-0808=D1-1292`), **`8`** in `BMCD` (`Normal_40 == Suspicious_16`). All counts reconcile exactly (`7,437 = 7,420 Retained + 0 Primary Excluded + 17 Quarantined`, plus `1,003` `CESM` & `400` `BMCD _GT.jpg` auxiliary exclusions). | **PASS** | Merge `PAT00000122<->1310` & `PAT00000476<->0815` (`companion view r=0.9933`) cleanly at `STEP-015 / STEP-020`. |
| 6 | **Stratified visual QC inspection & completed `T08` dataset cards** | Inspected all `5` `DS0001/2/3/5/6_qc_grid.png` + `DS0002_dup_pairs.png`: documented `MIAS` lead tags/borders (`RISK0004`), `BMCD` corner `RCC/LCC` stamps, `DMID` BB marker (`IMG00000140`), and `CDD-CESM` crop heterogeneity (`1,002` sizes). Approved `5/5` `T08` cards + `datasets.csv` `v1.2.0`. | **PASS** | Approved `2026-11-28`. |

---

## 4. Overall Gate Outcome
- **Recorded Gate Outcome (`gates.csv`):** **`PASS`** (`Ratified 2026-11-28`; `6/6` mandatory `G04` criteria satisfied, `7,420` retained clean mammograms across `5` cohorts, `17` pixel clones quarantined, `19/19` tests passing).

---

## 5. Assessor, Date, and Required Human Reviewer Sign-off
- **Technical Assessors:** Alzubair Ahamed (`232-15-591`, Verifier) & Md Riyadul Hasan (`232-15-486`, Data Steward) — `2026-11-27` / `2026-11-28`
- **Human Ratification (`G04 PASS`):** **Approved (`2026-11-28`)** by Research Owner/User alongside Supervisor **Israt Jahan** & Data Steward **Md Riyadul Hasan** review (`gates.csv` `GATE0004 = PASS`; `decisions.csv` `DEC0005 = Approved`).

---

## 6. Invalidated Downstream Gates/Artifacts & Reassessment Log
- **Blocks:** `G04` (`GATE0004`) gates progression into **`S07` (`STEP-014–015`, Label & ROI Mask Protocol `T09` -> `G05`)** and `S09` (`STEP-020` split `G07`).
- **Scope Note:** Unused local `DS0004_CBIS_DDSM` partial directory (`23.41 GB` cropped/ROI files) stays untouched outside active scope.
- **Reassessment Trigger:** Adding optional Batch B cohorts (`VinDr-Mammo` / `INbreast`) if DUA clears later requires an additive `STEP-012–013` QC addendum and `G04` delta assessment.

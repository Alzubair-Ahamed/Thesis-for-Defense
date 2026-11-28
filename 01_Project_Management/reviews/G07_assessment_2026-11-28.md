# G07 Gate Assessment Package — Connected-Component Patient Split & Custody Seal (`SPLIT0001`, `T24`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T24` (`T24_gate_audit.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `GATE0007` (`G07`) |
| `owner` | Md Riyadul Hasan (`232-15-486`, Data Steward) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-28` (`Prepared & Ratified PASS 2026-11-28`) |
| `status` | **`PASS` (`GATE0007` Ratified `2026-11-28` — `SPLIT0001` & `DEC0010–0011` Approved)** |
| `source_inputs` | [split.py](../../src/bc_xai/data/split.py); [test_split.py](../../tests/test_split.py); [manifest.csv](../../03_Datasets/splits/SPLIT0001/manifest.csv); [config.yaml](../../03_Datasets/splits/SPLIT0001/config.yaml); [report.md](../../03_Datasets/splits/SPLIT0001/report.md); [DEC0010.md](../decision_log/DEC0010.md); [DEC0011.md](../decision_log/DEC0011.md); [decisions.csv](../decisions.csv) |
| `governing_section` | [OS §4.5, §13.1–13.2 (`G07`)](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [Blueprint STEP-020](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-020) |
| `sensitivity` | Tier-1 Ratified Gate Assessment Record (`0` raw filenames, DICOM UIDs, or PII in `SPLIT0001/manifest.csv`; `private_summary.json` stays `.gitignore`-blocked) |
| `reviewer` | User/Research Owner; Israt Jahan (Supervisor); Md Riyadul Hasan (`232-15-486`); Alzubair Ahamed (`232-15-591`) — Ratified **`PASS`** `2026-11-28` |

---

## 1. AssessmentID, GateID, and Current Status
- **`AssessmentID`:** `GATE0007`
- **`GateID`:** `G07` (`Unlocks STEP-021 train-only preprocessing fit & REL#### materialization -> G08`)
- **`Gate Status in gates.csv`:** **`PASS`** (`Ratified 2026-11-28`, `v1.0.0`).

---

## 2. Bound EntityVersions and Exact SHA-256 Digests

| Artifact | Role / Version | Verified SHA-256 Digest |
|---|---|---|
| [split.py](../../src/bc_xai/data/split.py) | `STEP-020` `NetworkX` equivalence graph & splitter | `96faac6ec5b9814f046a2756cb6129d938e79045eb602e347ab5b78e95e5e659` |
| [test_split.py](../../tests/test_split.py) | Connected-component & leak-injection crash tests | `e4a565e9249e9bb2b28b8f26959eae772e55da93bb3a911585294c91fc35b1ef` |
| [manifest.csv](../../03_Datasets/splits/SPLIT0001/manifest.csv) | Deterministic `7,437`-row pseudonymous `SPLIT0001` manifest | `dc386a2c4d0c03affdca9f439933929677478696b92aecbca0d755e085faf9cb` |
| [config.yaml](../../03_Datasets/splits/SPLIT0001/config.yaml) | Split parameters (`seed=20261128`, bound `LBL0001–0005` hashes) | `5ba26864ac2c2642a50c5b2fa6161b7fc245af8d919349ce74d3681e2c8b3d74` |
| [report.md](../../03_Datasets/splits/SPLIT0001/report.md) | `T13` split, custody & balance audit report | `0b527d38a74d3468a2088fb304431b2bc1af26f22d6fff91d69fe156a5398a83` |
| [DEC0010.md](../decision_log/DEC0010.md) | `UD10` connected-component keys & DMID fallback (`Proposed`) | `8e36d46d758876d7c64e8c37c3ff5c7f10a5e1640bb38458c37609f3d98ad2d0` |
| [DEC0011.md](../decision_log/DEC0011.md) | `UD11` split proportions & external isolation (`Proposed`) | `95f31262a9ea1d95af92d2750bbd08fe110e8fd15be5dff721c9717c2fcb47a9` |
| [decisions.csv](../decisions.csv) | Updated decision ledger (`DEC0010–0011` Pending) | `0bab584c286dcc4c35742c41a7d1926ade736a3b110b3552c4633bd58794abef` |

---

## 3. Itemized Mandatory `G07` Criteria Audit Table

| # | Mandatory `G07` Criterion ([OS §13.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13) & `STEP-020`) | Verified Evidence & observed Figures | Technical Verdict | Required Action / Notes |
|---|---|---|---|---|
| 1 | **Connected-component graph over PatientID, views, studies & clones (`UD10`)** | `build_equivalence_graph()` unites `PatientGroupID`, `DICOMPatientIDHash`, `DICOMStudyUIDHash`, `ExactDupCluster` (`CMMD` `PAT00000122<->1310`, `PAT00000476<->0815`; `BMCD` `PAT00000035<->0058`; `DMID` `3` clones), and `MIAS` `161` L/R film pairs (`2,866` atomic components; `0` cross-cohort edges). | **PASS** | Automated `LeakageError` crash verified in [test_split.py](../../tests/test_split.py). |
| 2 | **Deterministic reproducible `SPLIT0001` & zero cross-partition overlap** | Dual consecutive runs of [split.py](../../src/bc_xai/data/split.py) (`seed=20261128`) emitted exact identical `manifest.csv` SHA-256 (`dc386a2c...faf9cb`); `assert_zero_leakage()` verified **`0` overlapping `ComponentID`, `PatientGroupID`, or clone IDs** across `train`, `val`, `internal_test`, and `external_*`. | **PASS** | `0` sealed `internal_test` scans appear in `dev_fold_5`. |
| 3 | **Stratified class/view/morphology balance & `100%` external isolation (`UD11`)** | `DS0003 CMMD`: `train=2,614` (`1,241` comps, `70.31%` M), `val=560` (`266` comps, `70.36%` M), `internal_test=564` (`265` comps, `70.21%` M) + `5`-fold dev (`634–636` imgs/fold). External `DS0006` (`919` / `569` lesion masks), `DS0005` (`260` / `63` masks), `DS0002` (`470` / `264` masks), `DS0001` (`322` / `109` masks) remain **`100%` untouched by internal training**. | **PASS** | Secondary intra-cohort `DS0006` `cohort_subsplit` (`643/138/138`) also patient-grouped cleanly. |
| 4 | **Official-split audit & honest identity limitations** | [report.md](../../03_Datasets/splits/SPLIT0001/report.md) §3, §7 confirms none of the 5 cohorts supply an upstream canonical train/test manifest (`audit_external_split_overlap` tested) and documents `DS0002` missing `PatientID` (`100%` external isolation), `DS0001` odd/even pairing, and `DS0003` missing density. | **PASS** | Zero concealed caveats. |
| 5 | **Sealed test custody & named human sign-off (`Supervisor + Data Lead`)** | `internal_test` (`564`) & `external_*` (`1,971`) sealed (`custody_tier = sealed_until_G11` / `sealed_external_until_G11_G12`). **`DEC0010–0011` & `GATE0007 = PASS` ratified `2026-11-28` by User/Research Owner alongside Supervisor Israt Jahan.** | **PASS** | `gates.csv` `GATE0007 = PASS`; unlocks `STEP-021` upon owner trigger. |

---

## 4. Overall Gate Outcome
- **Recorded Gate Outcome (`gates.csv`):** **`PASS`** (`Ratified 2026-11-28`; `5/5` mandatory `G07` criteria verified, `DEC0010–0011` Approved, `32/32` pytest suite + `24/24` registry validation passed). Unlocks **`STEP-021` (`train`-only preprocessing fit & immutable `REL####` materialization -> `G08`)**.

---

## 5. Assessor, Date, and Required Human Reviewer Sign-off
- **Technical Assessors:** Md Riyadul Hasan (`232-15-486`, Data Lead) & Alzubair Ahamed (`232-15-591`, Verifier) — `2026-11-28`
- **Human Ratification (`DEC0010–0011` & `GATE0007`):** **Approved (`2026-11-28`)** by Research Owner/User alongside Supervisor **Israt Jahan** & Data/Verifier Leads (`gates.csv` `GATE0007 = PASS`; `decisions.csv` `DEC0010–0011 = Approved`).

---

## 6. Downstream Unlock & Reassessment Rule
- **Unlocks Upon `G07 PASS`:** **`STEP-021`** (`src/bc_xai/preprocess/materialize.py`, training-only fit on `SPLIT0001 train`, immutable `REL0001` baseline & `REL0002` CLAHE + co-transformed ROI masks, `preprocessing_registry.csv`, `03_Datasets/releases.csv`, `G08`).
- **Invalidation Trigger:** Any modification to `SPLIT0001/manifest.csv`, `DEC0010`, or `DEC0011` marks `G07` and all future `STEP-021+` derivatives **`STALE`**.

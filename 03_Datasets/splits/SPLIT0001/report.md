# Connected-Component Patient Split & Sealed Test Custody Report (`SPLIT0001`, `T13`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T13` (`T13_split.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `SPLIT0001` (`v1.0.0`) |
| `owner` | Md Riyadul Hasan (`232-15-486`, Data Lead) & Alzubair Ahamed (`232-15-591`, Verifier) |
| `date` | `2026-11-28` |
| `status` | **`Locked SPLIT0001 (seed=20261128, Zero-Leakage Verified, G07 PASS Approved 2026-11-28)`** |
| `source_inputs` | [datasets.csv](../../datasets.csv); [label_registry.csv](../../../04_Labels_XAI_Governance/label_registry.csv); [split.py](../../../src/bc_xai/data/split.py); [test_split.py](../../../tests/test_split.py); [config.yaml](./config.yaml); [manifest.csv](./manifest.csv); [DEC0010.md](../../../01_Project_Management/decision_log/DEC0010.md); [DEC0011.md](../../../01_Project_Management/decision_log/DEC0011.md) |
| `governing_section` | [OS §4.5, §13.2 (`G07`), §14.2](../../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-020](../../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-020) |
| `sensitivity` | Tier-1 Pseudonymous Split Specification (`0` raw filenames, DICOM UIDs, or PII in `manifest.csv`; `private_summary.json` stays gitignored) |
| `reviewer` | User/Research Owner; Israt Jahan (Supervisor); Md Riyadul Hasan (`232-15-486`); Alzubair Ahamed (`232-15-591`) — **`G07 PASS` Ratified `2026-11-28`** |

---

## 1. Input `DS####` and `LBL####` Manifest SHA-256 Hashes

`SPLIT0001` consumes 100% of the `G04`/`G06`-locked releases (`7,437` primary acquired records across `5` cohorts):

| Cohort (`DatasetID`) | Parent `DS####` `ManifestHash` | Frozen `LabelReleaseID` | Frozen `LBL####_manifest.csv` `SHA-256` |
|---|---|---|---|
| `DS0001` (`MIAS v1.21`) | `2e3f8559ed425aee3d716174767558d2e8adf41c017915eecefb81da9ec9fdf1` | **`LBL0001`** | `0af4cccefd98a347ebbf4da211659a69efde2c25015a9e4eb3bcc7e8c1d681c2` |
| `DS0002` (`DMID`) | `40882b4e5506f11675acccee1776e7469de1713bad0fabe9a33d0898892cf5da` | **`LBL0002`** | `4d6e7fde17bcb94dc758996f525422c3a3ad5623833317f8c1dac273f14f4665` |
| `DS0003` (`CMMD`) | `b933e5f7efb3767ea92143a0bc652d5c81fdc33f024df6f5fefee98537c4f6ed` | **`LBL0003`** | `3f4680d69013e133df59a010e44aa8ab1571f0e2a9a5857dc720fd57d2ae6c2e` |
| `DS0005` (`BMCD`) | `4a1faa4ceeb921b6694c0458e4a7ce6702b5471deda259d9784121a08e989efe` | **`LBL0004`** | `b0b2937c33ebda9aec144d46813404a3de9fab0ea89211ea6b197a7f593f75c9` |
| `DS0006` (`CDD-CESM LE`) | `e1732776952a7562a811b16800924563a33cc645f72fd33aa056a38a0919ecd4` | **`LBL0005`** | `0c5d380c0f49700ac88a9a6fd9a08215036216dfd0b82bf5ae34fa73db924f4e` |

- **Output `SPLIT0001` Determinism Proof:** Two consecutive fresh executions of [split.py](../../../src/bc_xai/data/split.py) (`seed = 20261128`) emitted bit-identical [manifest.csv](./manifest.csv) (`SHA-256 = dc386a2c4d0c03affdca9f439933929677478696b92aecbca0d755e085faf9cb`) and [config.yaml](./config.yaml) (`SHA-256 = 5ba26864ac2c2642a50c5b2fa6161b7fc245af8d919349ce74d3681e2c8b3d74`).

---

## 2. Connected-Component Equivalence Graph Keys (`UD10`)

Undirected `NetworkX` equivalence graph (`build_equivalence_graph`, **`2,866` atomic components across `7,437` images**) connects images sharing **any** of:
1. **Patient Identity (`PatientGroupID`):** All ipsilateral/contralateral, `CC/MLO`, and `prior/recent` views under the same pseudonym (`1,775` upstream IDs in `CMMD`, `326` in `CDD-CESM`, `100` folders in `BMCD`, `510` in `DMID`).
2. **DICOM Identity Hashes (`*_qc_details.csv`):** Non-empty `DICOMPatientIDHash` (`1,775` in `CMMD`) and `DICOMStudyUIDHash` (`1,775` in `CMMD`, `200` in `BMCD`, `510` in `DMID`).
3. **Pixel-Clone & Exact Duplicate Clusters (`ExactDupCluster` + Global `SHA256`):** Atomically merges cross-patient clone pairs discovered in `STEP-013` (`CMMD` `PAT00000122 <-> PAT00001310` and `PAT00000476 <-> PAT00000815`; `BMCD` `PAT00000035 <-> PAT00000058`; `DMID` `PAT00000019/318`, `021/319`, `034/172`), collapsing `CMMD`'s `1,775` raw IDs into `1,773` physical women (`1,772` active + `1` conflicting clone pair excluded).
4. **Bilateral Film Pairs (`MIAS` `DS0001`):** Pairs sequential odd/even film numbers (`mdb001/002` through `mdb321/322`) into **`161` atomic L/R women components** (`0` unpaired).

---

## 3. Official Benchmark Split Overlap Audit

- **Audit Result (`not_applicable_no_upstream_split`):** None of the `5` selected cohorts (`DS0001–0003, DS0005–0006`) distributes a fixed canonical train/test manifest requiring conflict reconciliation. `audit_external_split_overlap()` inside [split.py](../../../src/bc_xai/data/split.py) is verified via unit test to catch component bridging if any third-party split table is ever audited later.

---

## 4. Splitting Algorithm, Random Seed & Design (`UD11`)

- **Algorithm & Seed:** Deterministic greedy component-balanced stratified assignment (`seed = 20261128`) keeping every `ComponentID` atomic:
  - **Primary Internal Cohort (`DS0003 CMMD`, `1,772` clean physical patients / `3,738` biopsy FFDM scans):** Partitioned **`70% train` / `15% val` / `15% internal_test`**, stratified at component level by `(ComponentMaxTarget x HasBilateralDiscordance x DominantMorphology)`. Plus deterministic **`5-fold` `dev_fold_5`** (`0..4`) strictly across the `85%` **`train + val` pool** (`internal_test` & `Excluded` receive `dev_fold_5 = -1`).
  - **Independent Cross-Center & Quantitative Localization Cohorts (`0%` primary training overlap):**
    - `DS0006 CDD-CESM LE` (`312` patients / `919` non-excluded): Assigned `external_eval_loc` in `primary_partition` (`581 SubTrackA`, `569 LesionTrack` polygons), plus leak-free intra-cohort patient-grouped `cohort_subsplit` (`70/15/15`) for secondary nested `STEP-030` experiments.
    - `DS0005 BMCD` (`81` non-excluded patients / `260` scans): Assigned `external_test_bmcd`.
    - `DS0002 DMID` (`470` non-excluded scans): Assigned `external_test_dmid` (`strictly blocked from internal splitting due to absent DICOM PatientID`).
    - `DS0001 MIAS` (`161` L/R patient pairs / `322` scans): Assigned `external_test_mias_sfm` (`SFM` domain & `RISK0004` shortcut stress test).

---

## 5. Target vs Actual Partition, Class, ROI-Mask & Subgroup Distribution (`SPLIT0001`)

| Partition (`Role / Dataset`) | Components | Total Images | Target `0` (`Benign/Norm`) | Target `1` (`Malignant`) | `SubTrackA` | `LesionTrack` Masks | Views (`CC` / `MLO`) | Morphology (`mass` / `calc` / `both` / `none`) |
|---|---:|---:|---:|---:|---:|---:|---|---|
| **`train`** (`DS0003`, `69.93%` imgs / `70.03%` comps) | `1,241` | **`2,614`** | `776` (`29.69%`) | `1,838` (`70.31%`) | `2,614` | `0` | `1,307 / 1,307` | `1,600 / 370 / 644 / 0` |
| **`val`** (`DS0003`, `14.98%` imgs / `15.01%` comps) | `266` | **`560`** | `166` (`29.64%`) | `394` (`70.36%`) | `560` | `0` | `280 / 280` | `344 / 78 / 138 / 0` |
| **`internal_test`** (`DS0003`, `15.09%` imgs / `14.96%` comps) | `265` | **`564`** | `168` (`29.79%`) | `396` (`70.21%`) | `564` | `0` | `282 / 282` | `350 / 76 / 138 / 0` |
| **`external_eval_loc`** (`DS0006 CDD-CESM`) | `312` | **`919`** | `615` | `304` | `581` | **`569`** | `457 / 462` | `188+171 other / 154 / 68 / 338` |
| **`external_test_bmcd`** (`DS0005 BMCD`) | `81` | **`260`** | `238` | `22` | `64` | **`63`** | `130 / 130` | `0 / 172 / 0 / 88` |
| **`external_test_dmid`** (`DS0002 DMID`) | `470` | **`470`** | `342` | `128` | `0` | **`264`** | `232 / 238` | `190 / 56 / 25 / 199` |
| **`external_test_mias_sfm`** (`DS0001 MIAS`) | `161` | **`322`** | `271` | `51` | `0` | **`109`** | `0 / 322` | `90 / 25 / 0 / 207` |
| **`excluded`** (`Quarantined & Protocol-Excl.`) | `866` *(incl. shared comps)* | **`1,728`** | `0` | `0` | `0` | `0` | `862 / 866` | `Excluded from modeling` |

- **`DS0003` 5-Fold Dev CV (`train + val`, `3,174` images / `1,507` components):** Folds `0–4` contain `636, 636, 634, 634, 634` images across `302, 302, 301, 301, 301` components (`Malignant`: `446, 448, 446, 446, 446`), zero overlap with `internal_test`.
- **`DS0006` Intra-Cohort `cohort_subsplit` (`919` scans / `312` comps):** `train = 643` (`221` comps, `427/216`, `395` lesion masks), `val = 138` (`45` comps, `94/44`, `90` masks), `internal_test = 138` (`46` comps, `94/44`, `84` masks).

---

## 6. Automated Zero Cross-Partition & Cross-Cohort Overlap Assertions

- `assert_zero_leakage()` executed on `SPLIT0001`: **PASSED (`zero_leakage_verified = True`)**:
  - `0` `ComponentID`, `PatientGroupID`, `ImageID`, `ExactDupCluster`, or file `SHA256` overlaps across `{train, val, internal_test, external_*}`.
  - `0` sealed `internal_test` rows appear in `dev_fold_5`.
  - Synthetic leak-injection unit tests in [test_split.py](../../../tests/test_split.py) verified `LeakageError` fires loudly when a patient component or fold boundary is violated.

---

## 7. Residual Identity Metadata Limitations (`Honest Disclosure`)

1. **`DS0002 DMID` Missing Cross-View `PatientID`:** `0/510` DICOMs populate `PatientID`, so distinct views of the same patient cannot be linked automatically (`470` solo scan components after clone quarantine). Mitigated conservatively by placing `DS0002` strictly in `external_test_dmid` (`0%` internal training/tuning use) rather than risking train/test patient leakage.
2. **`DS0001 MIAS` Headerless PGMs:** Paired strictly by `mdb` odd/even sequence (`161` `(L, R)` women verified `100%` L/R balanced); any unrecorded repeat screening across distinct ID pairs is unknown upstream (`DS0001` stays `100%` in external SFM evaluation).
3. **`DS0003 CMMD` Missing ACR Breast Density:** `not_reported` (`3,738/3,738`), so internal density subgroup balance (`ACR A–D`) is evaluated on external cohorts (`DS0006`, `DS0005`, `DS0002`) during `STEP-037`.

---

## 8. Sealed Internal & External Test Custody Rules (`G07`)

- **`internal_test` (`DS0003`, `564` scans) & `external_*` (`1,971` retained non-excluded scans):** Sealed under `sealed_until_G11` / `sealed_external_until_G11_G12`. Zero threshold fitting, calibration tuning, architecture selection, or XAI target-layer tuning may inspect test images or labels prior to `G11`.
- **Sign-Off Status:** **Approved (`2026-11-28`)** — User/Research Owner & Supervisor `Israt Jahan` ratified `DEC0010–0011` and `GATE0007 = PASS`.

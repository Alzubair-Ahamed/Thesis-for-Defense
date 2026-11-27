# G06 Gate Assessment Package — Verified Diagnostic Label & ROI-Mask Freeze (`LBL0001–LBL0005`, `T24`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T24` (`T24_gate_audit.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `GATE0006` (`G06`) |
| `owner` | Md Riyadul Hasan (`232-15-486`, Label & Mask Lead) & Alzubair Ahamed (`232-15-591`, Cross-Check Verifier) |
| `date` | `2026-11-28` (`Prepared & Ratified PASS 2026-11-28`) |
| `status` | **`PASS` (`GATE0006` Ratified `2026-11-28` — `LBL0001–LBL0005 v1.0.0` & `label_map.json` Approved)** |
| `source_inputs` | [label_mask_protocol_v1.0.1.md](../../04_Labels_XAI_Governance/protocols/label_mask_protocol_v1.0.1.md); [label_map.json](../../04_Labels_XAI_Governance/label_map.json); [label_registry.csv](../../04_Labels_XAI_Governance/label_registry.csv); [LBL0001_0005_audit.md](../../04_Labels_XAI_Governance/reviews/LBL0001_0005_audit.md); [pilot_label_mask_audit.md](../../04_Labels_XAI_Governance/reviews/pilot_label_mask_audit.md); [STEP017_full_label_mask_audit.md](../../04_Labels_XAI_Governance/reviews/STEP017_full_label_mask_audit.md); [STEP016_pilot_discrepancies.md](../../04_Labels_XAI_Governance/adjudications/STEP016_pilot_discrepancies.md); [STEP017_full_adjudications.md](../../04_Labels_XAI_Governance/adjudications/STEP017_full_adjudications.md); [DEC0008.md](../decision_log/DEC0008.md); [DEC0009.md](../decision_log/DEC0009.md); [verify.py](../../src/bc_xai/labels/verify.py); [freeze.py](../../src/bc_xai/labels/freeze.py) |
| `governing_section` | [OS §4.3, §6.1, §13.1–13.2 (`G06`)](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [Blueprint STEP-016–018](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-018) |
| `sensitivity` | Tier-1 Ratified Gate Assessment Record (`0` raw patient paths or PII; Tier-2 manifests & mask archives remain gitignored) |
| `reviewer` | User/Research Owner; Israt Jahan (Supervisor); Md Riyadul Hasan (`232-15-486`); Alzubair Ahamed (`232-15-591`) — Ratified **`PASS`** `2026-11-28` *(Clinical advisor XAI review tracked pre-G13 under `DEC0018`)* |

---

## 1. AssessmentID, GateID, and Current Status
- **`AssessmentID`:** `GATE0006`
- **`GateID`:** `G06` (`Feeds S09 / STEP-019–021` Preprocessing Design, Patient-Level Split `G07`, & Immutable Release `G08`)
- **`Gate Status in gates.csv`:** **`PASS`** (`Ratified 2026-11-28`, `v1.0.0`).

---

## 2. Bound EntityVersions and Exact SHA-256 Digests

| Artifact | Role / Version | Verified SHA-256 Digest |
|---|---|---|
| [verify.py](../../src/bc_xai/labels/verify.py) | `STEP-016/017` `T09 v1.0.1 + Option B` verifier | `a888953309c0b35cdaef473db77e2a9b9ee980939f153d8495232c4eda95bb48` |
| [freeze.py](../../src/bc_xai/labels/freeze.py) | `STEP-018` `LBL####` manifest & mask-zip freezer | `0f8be0688544c8737fb26d7bb7a8110067d5c6dca1c66ff4ba7b8babed8705a3` |
| [test_label_verify.py](../../tests/test_label_verify.py) | Label harmonization & Option B unit tests | `a20b260445798900700eaece1b4692bcabb87807a121593f7f267560da9beac4` |
| [test_label_freeze.py](../../tests/test_label_freeze.py) | Deterministic freeze & pixel/orphan guard tests | `a9b31ce81b40d1c7783986f6c517cc3b7735e5df31d7bd014fb99a7c90d54dfb` |
| [validate_registries.py](../../13_Automation/validate_registries.py) | `24`-registry & FK validator (`label_registry.csv` enabled) | `d3441d06b02f6affccd66065e6b240a771c639ac3f5b8132ebcc1493ff8ce58e` |
| [label_mask_protocol_v1.0.1.md](../../04_Labels_XAI_Governance/protocols/label_mask_protocol_v1.0.1.md) | `T09 v1.0.1` label & ROI-mask standardization rules | `a79b75696335e90380e27e46800540c3f657b80d1b1c4899908c85a2c933d6c6` |
| [label_map.json](../../04_Labels_XAI_Governance/label_map.json) | Canonical binary map (`0=Benign, 1=Malignant`) & track counts | `a6409b1054423b488b18b359e40d4b58a036a9eb7ad6e5758de88782f75d9f98` |
| [label_registry.csv](../../04_Labels_XAI_Governance/label_registry.csv) | Registered `LBL0001–LBL0005` (`v1.0.0`) ledger | `94edb9bb40c161e3a0124913d9cf43658b39bbd3b01fb9064b2d390f327463db` |
| [LBL0001_0005_audit.md](../../04_Labels_XAI_Governance/reviews/LBL0001_0005_audit.md) | `T10` frozen label & ROI-mask audit report (`v1.0.0`) | `6b1018616d17960675824388f2584bc4fa39a6d696ad77c05ec4ef79d4cfd107` |
| [STEP017_full_label_mask_audit.md](../../04_Labels_XAI_Governance/reviews/STEP017_full_label_mask_audit.md) | Full-corpus `N=7,437` verification audit report | `1b5dbd25ec870cd8923bd048c979ac7743fb39e3dbe1b1642f8a54b0ccffbcd7` |
| [STEP017_full_adjudications.md](../../04_Labels_XAI_Governance/adjudications/STEP017_full_adjudications.md) | Full-corpus discrepancy ledger (`ADJ-017-01..06`, Option B closed) | `0188ed11e5e0dac158d2e84d6431b8b4b028d220f6c5033ca0cc060179e0fd7f` |
| [DEC0008.md](../decision_log/DEC0008.md) | `UD08` updated to `v1.2.2` w/ `ADJ-017-02` Option B | `9522e7fb061f92cac6badf1c2774a91af6d0e79453550202118c7d521927abe0` |
| [DEC0009.md](../decision_log/DEC0009.md) | `UD09` ROI-mask alignment & post-hoc non-leakage | `8809e401652146485ff16ad2238d623cf6e725fd9596e3213acf5a92adbd9441` |
| `LBL0001` (`DS0001` Tier-2 Bundle) | `LBL0001_manifest.csv` / `LBL0001_masks.zip` (`109` PNGs) | `0af4ccce...` / `e9ce8f2c...` *(full hashes in `LBL0001_0005_audit.md §8`)* |
| `LBL0002` (`DS0002` Tier-2 Bundle) | `LBL0002_manifest.csv` / `LBL0002_masks.zip` (`264` PNGs) | `4d6e7fde...` / `e32eea19...` *(full hashes in `LBL0001_0005_audit.md §8`)* |
| `LBL0003` (`DS0003` Tier-2 Bundle) | `LBL0003_manifest.csv` / `masks = none` (`0` native masks) | `3f4680d6...` / `none` *(full hash in `LBL0001_0005_audit.md §8`)* |
| `LBL0004` (`DS0005` Tier-2 Bundle) | `LBL0004_manifest.csv` / `LBL0004_masks.zip` (`175` PNGs) | `b0b2937c...` / `416d0b95...` *(full hashes in `LBL0001_0005_audit.md §8`)* |
| `LBL0005` (`DS0006` Tier-2 Bundle) | `LBL0005_manifest.csv` / `LBL0005_masks.zip` (`573` PNGs) | `0c5d380c...` / `85134bb2...` *(full hashes in `LBL0001_0005_audit.md §8`)* |

---

## 3. Itemized Mandatory `G06` Criteria Audit Table

| # | Mandatory `G06` Criterion ([OS §13.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13) & `STEP-016–018`) | Verified Evidence & Observed Figures | Technical Verdict | Required Action / Notes |
|---|---|---|---|---|
| 1 | **`100%` Pilot & Full-Corpus Label/Pathology Concordance** | [pilot_label_mask_audit.md](../../04_Labels_XAI_Governance/reviews/pilot_label_mask_audit.md) (`N=170`) and [STEP017_full_label_mask_audit.md](../../04_Labels_XAI_Governance/reviews/STEP017_full_label_mask_audit.md) (`N=7,437` primary acquired = `7,420` `G04`-retained + `17` clones) achieve **`5/5` arithmetic closure (`2,576 Benign+Normal + 3,133 Malignant + 1,728 Excluded = 7,437`)**, `0` unmapped tokens, and `100%` `ImageID` match with `DS0001–0003, DS0005–0006`. | **PASS** | Track segregation (`SubTrackA=4,383`, `SubTrackB=5,709`, `LesionTrack=4,769`) enforced. |
| 2 | **Multi-Lesion, Normal-Control & Edge-Case Adjudication Closure** | All `6` full-corpus anomaly buckets (`ADJ-017-01..06`) closed in [STEP017_full_adjudications.md](../../04_Labels_XAI_Governance/adjudications/STEP017_full_adjudications.md), including owner-ratified **`ADJ-017-02` Option B (`IMG00000062` & `IMG00000302` -> `Excluded_ReportMetadataDiscordance`)**, `35` `DMID 'N'` exclusions, `1,456` `CMMD` contralateral exclusions, `98 + 34` `BMCD` prior/unconfirmed exclusions, `80 + 4` `CDD-CESM` post-op/post-NAC exclusions, and `534` `TierA_Biopsy_NormalControl` isolates (`0` silent `Normal -> Benign` merging). | **PASS** | `DEC0008` updated cleanly to `v1.2.2`. |
| 3 | **ROI-Mask Alignment, Orientation, Artifact Isolation & Zero-Corrupt-Mask Gate** | `1,121 / 1,121` `LocalizationEligible` masks (`491 Malignant + 514 Benign = 1,005 LesionTrack` + `116 Normal_Control` filtered via `LabelClass`) re-extracted as binary `{0, 1}` PNGs matching 1:1 native image `(H, W)` & exact pixel counts (`0` corrupt masks eligible; `DMID ROI Masks` banned; `BMCD` green rulers ignored & `IMG00000627` bottom red-bar isolated `LocalizationEligible=False`; `MIAS` `(H - y)` Y-flip visually verified; `5/5` stratified overlay plates visually inspected at `seed=20261128`). | **PASS** | `0` corrupt or misaligned masks eligible for post-hoc XAI localization. |
| 4 | **Immutable `LBL####` Freeze, Canonical `label_map.json` & SHA-256 Registry** | [freeze.py](../../src/bc_xai/labels/freeze.py) generated deterministic Tier-2 `LBL0001–LBL0005` CSV manifests (`exports/`), lossless `{0, 1}` mask bundles (`restricted_masks/`), per-mask `.sha256` indexes, Tier-1 [label_map.json](../../04_Labels_XAI_Governance/label_map.json), populated [label_registry.csv](../../04_Labels_XAI_Governance/label_registry.csv), and complete [LBL0001_0005_audit.md](../../04_Labels_XAI_Governance/reviews/LBL0001_0005_audit.md). | **PASS** | Tier-2 storage strictly `.gitignore`-blocked (`git check-ignore` verified). |
| 5 | **Subgroup Completeness & Honest Residual Uncertainty Disclosure** | [LBL0001_0005_audit.md](../../04_Labels_XAI_Governance/reviews/LBL0001_0005_audit.md) §3.B reports exact observed `ViewPosition`, `DensityACR`, and `MorphologyType` distributions across all `5,709` non-excluded scans (`including CMMD missing ACR density = not_reported, DMID missing DICOM PatientID, and MIAS historical SFM`). | **PASS** | No unverified public metadata claims introduced. |
| 6 | **Named Human Sign-Off (`Data Lead + Clinical Reviewer / Supervisor`)** | Prepared by Md Riyadul Hasan & Alzubair Ahamed; **`ADJ-017-02` Option B and `G06 PASS` ratified `2026-11-28` by User/Research Owner alongside Supervisor Israt Jahan** (`independent practicing breast radiologist XAI review tracked pre-G13 under DEC0018 fallback rule`). | **PASS** | `gates.csv` `GATE0006 = PASS` (`2026-11-28`); unlocks `S09 / STEP-019`. |

---

## 4. Overall Gate Outcome
- **Recorded Gate Outcome (`gates.csv`):** **`PASS`** (`Ratified 2026-11-28`; `6/6` mandatory `G06` criteria satisfied, `LBL0001–LBL0005 v1.0.0`, `label_map.json`, `LBL0001_0005_audit.md`, `label_registry.csv`, `26/26` pytest suite, and `24/24` registry validation verified).

---

## 5. Assessor, Date, and Required Human Reviewer Sign-off
- **Technical Assessors:** Md Riyadul Hasan (`232-15-486`, Label/Mask Lead) & Alzubair Ahamed (`232-15-591`, Cross-Check Verifier) — `2026-11-28`
- **Human Ratification (`G06 PASS`):** **Approved (`2026-11-28`)** by Research Owner/User alongside Supervisor **Israt Jahan** & Research Leads (`gates.csv` `GATE0006 = PASS`; `decisions.csv` `DEC0008 v1.2.2 = Approved`)
- **Clinical Advisor Fallback Note:** Tracked pre-`G13` (`STEP-037`) under ratified [DEC0018](../decision_log/DEC0018.md) non-trial separation & mandatory unavailability disclosure rules.

---

## 6. Downstream Unlock & Reassessment Rule
- **Unlocks Upon `G06 PASS`:** **`S09 / STEP-019`** (`05_Preprocessing/specs/pipeline.md`, `src/bc_xai/preprocess/transforms.py`, `DEC0012` / `UD12`) -> **`STEP-020`** connected-component split (`G07`) -> **`STEP-021`** `REL####` materialization (`G08`).
- **Invalidation Trigger:** Any modification to `label_map.json`, `T09` label inclusion/exclusion rules, or frozen `LBL0001–LBL0005` manifest/mask SHA-256 digests marks `G06` and all future `S09+` artifacts **`STALE`** until a superseding `LBL####` release is frozen.

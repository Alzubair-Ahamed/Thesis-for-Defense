# G05 Gate Assessment Package — Label/ROI-Mask Protocol (`T09`) & Prospective XAI Governance (`XAIP0001` / `T11`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T24` (`T24_gate_audit.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `GATE0005` (`G05`) |
| `owner` | Md Riyadul Hasan (`232-15-486`, Label/Mask Lead) & Alzubair Ahamed (`232-15-591`, XAI Lead) |
| `date` | `2026-11-28` (Prepared & Ratified **`PASS`** `2026-11-28`) |
| `status` | **`PASS` (`GATE0005` Ratified `2026-11-28` — `DEC0007–0009`, `DEC0016–0018`, `T09 v1.0.0` & `XAIP0001` Approved)** |
| `source_inputs` | [label_mask_protocol_v1.0.0.md](../../04_Labels_XAI_Governance/protocols/label_mask_protocol_v1.0.0.md); [XAIP0001.md](../../04_Labels_XAI_Governance/xai_protocols/XAIP0001.md); [qualitative_review_rubric.md](../../04_Labels_XAI_Governance/xai_protocols/qualitative_review_rubric.md); [xai_protocol_registry.csv](../../04_Labels_XAI_Governance/xai_protocol_registry.csv); [DEC0007](../decision_log/DEC0007.md); [DEC0008](../decision_log/DEC0008.md); [DEC0009](../decision_log/DEC0009.md); [DEC0016](../decision_log/DEC0016.md); [DEC0017](../decision_log/DEC0017.md); [DEC0018](../decision_log/DEC0018.md) |
| `governing_section` | [OS §4.3, §6, §13 (`G05`)](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [Blueprint STEP-014–015](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-015) |
| `sensitivity` | Tier-1 Ratified Gate Assessment Record |
| `reviewer` | Israt Jahan (Supervisor); User/Research Owner; Alzubair Ahamed (`232-15-591`); Md Riyadul Hasan (`232-15-486`) — Ratified `2026-11-28` (`Clinical Advisor UD18 fallback retained pre-G13`) |

---

## 1. AssessmentID, GateID, and Current Status
- **`AssessmentID`:** `GATE0005`
- **`GateID`:** `G05` (`Feeds S08 / STEP-016–018` Label & ROI Verification -> `G06`)
- **`Gate Status in gates.csv`:** **`PASS`** (`Ratified 2026-11-28`, `v1.2.0`).

---

## 2. Bound EntityVersions and Exact SHA-256 Digests

| Artifact (`Tier-1 Repository`) | Role / Version | Verified SHA-256 Digest |
|---|---|---|
| [label_mask_protocol_v1.0.0.md](../../04_Labels_XAI_Governance/protocols/label_mask_protocol_v1.0.0.md) | `T09` Label & ROI-Mask Protocol (`v1.0.0`, Approved `2026-11-28`) | `8ed4cbeb3b65b83eacddd95dd7dccd26b79238e307d180c1941574c99ba40362` |
| [XAIP0001.md](../../04_Labels_XAI_Governance/xai_protocols/XAIP0001.md) | `T11` Prospective XAI Protocol (`XAIP0001 v1.0.0`, Approved `2026-11-28`) | `b98b3b9f2fc361f5b9b40996b000fcd62dfba6e3c6a7d483113f88bbe9196c1d` |
| [qualitative_review_rubric.md](../../04_Labels_XAI_Governance/xai_protocols/qualitative_review_rubric.md) | Blinded `N=40` Qualitative Review Rubric (`v1.0.0`) | `5038782dd3db0219d47b3825f6f5483fefd9d3a20e7c39bb6b7ec88ccf619528` |
| [DEC0007.md](../decision_log/DEC0007.md) | `UD07` Whole-Image Paradigm & Sensor Isolation (`Approved`) | `b938e3694e7deafcf38c6665ffaf599834cb78fce01884c7651db0b7d56e7590` |
| [DEC0008.md](../decision_log/DEC0008.md) | `UD08` Binary Mapping, Normal & Anomaly Rules (`Approved`) | `64e9ab1aa408c4b7f4a915b69a2b3244cfff00a38ab6b6a423eab33d14fdd3d2` |
| [DEC0009.md](../decision_log/DEC0009.md) | `UD09` ROI-Mask Geometry, Union & Post-Hoc Boundary (`Approved`) | `cfbfce149e146dab8b57172bd6458a1c658a47f6b493283ea06091fa9096b238` |
| [DEC0016.md](../decision_log/DEC0016.md) | `UD16` XAI Method Suite & Target-Layer Policy (`Approved`) | `5e2e0cbba9398b99177e1a8539f75b45526a9308700f1fbe9db75a19a8e61182` |
| [DEC0017.md](../decision_log/DEC0017.md) | `UD17` Quantitative Faithfulness/Sanity/Localization/Stability (`Approved`) | `19afb43b73bbf8410ae0d3b72344369ac5477302cc74e9b9c75b49aeea1996a5` |
| [DEC0018.md](../decision_log/DEC0018.md) | `UD18` Qualitative Advisor Rubric & Fallback Rule (`Approved`) | `ab5e6f64643d9f2b94d25e9dfbf2fda8a9548dbadb8885f3c88caabc5b0ec3d4` |

---

## 3. Itemized Mandatory `G05` Criteria Audit Table

| # | Mandatory `G05` Criterion ([OS §13](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13) & `STEP-014–015`) | Verified Evidence & Observed Details | Gate Status | Required Action / Notes |
|---|---|---|---|---|
| 1 | **FFDM vs ROI/SFM classification paradigm (`UD07`)** | [DEC0007](../decision_log/DEC0007.md) & `T09 §1` lock whole-image `2D FFDM` (`DS0003/0006/0005/0002`) strictly isolated from digitized `SFM` (`DS0001`) and zero lesion-crop training. | **PASS** | `UD07` ratified `2026-11-28`. |
| 2 | **Benign/Malignant & Normal/anomaly provenance rules (`UD08`)** | [DEC0008](../decision_log/DEC0008.md) & `T09 §2–§4` resolve `CMMD` `ID1+ImageLaterality` join (`~1,452` unlabeled contralateral excluded), `CDD-CESM` `80` postop + `4` post-NAC/`BIRADS=6` exclusions + dual biopsy/non-malignant tracks, `BMCD` `recent`-only + `18` unbiopsied exclusions, `DMID` `36` ambiguous `'N'` exclusions (`BI-RADS 0/1/3/4`), and malignant dominance. | **PASS** | `UD08` ratified `2026-11-28`; verified at `STEP-016–018`. |
| 3 | **ROI-mask geometry, multi-ROI union & post-hoc isolation (`UD09`)** | [DEC0009](../decision_log/DEC0009.md) & `T09 §5–§6` define `CDD-CESM` `1,797` VIA polygons (`cv2.fillPoly`), `BMCD` `*_GT.jpg` color extraction, **`DMID` `Pixel-level annotation/*.tif` (`269/269 ok`) with hard ban on corrupt `ROI Masks/*.tif` (`268/269 decoder error -2`)**, `MIAS` flipped `(x,y,r)`, and strict post-hoc non-leakage boundary. | **PASS** | `UD09` ratified `2026-11-28`; checked in `STEP-016` overlays. |
| 4 | **Prospective XAI suite, logit convention & collapsed-map rule (`UD16`)** | `XAIP0001 §1–§4` & [DEC0016](../decision_log/DEC0016.md) lock `Grad-CAM`, `Grad-CAM++`, `LayerCAM`, `Score-CAM`, `Integrated Gradients`, and negative sanity baseline `Guided Backpropagation` using raw pre-sigmoid Malignant logit $z_{\text{mal}}$ (`non-cherry-picking Collapsed_ZeroMap rule`). | **PASS** | `UD16` ratified; exact module strings bind at `STEP-022` (`G09`). |
| 5 | **Quantitative XAI faithfulness, Adebayo sanity, ROI localization & stability (`UD17`)** | `XAIP0001 §5–§8` & [DEC0017](../decision_log/DEC0017.md) freeze `Deletion/Insertion/ROAD` (`5%` steps, `sigma=15` blur + random baseline), Adebayo cascading & independent weight/label randomization, `PG / Delta-PG / EBPG / IoU / Dice`, and contrast/shift/multi-seed stability. | **PASS** | `UD17` ratified `2026-11-28`. |
| 6 | **Blinded clinical-advisor qualitative rubric & non-trial fallback (`UD18`)** | [qualitative_review_rubric.md](../../04_Labels_XAI_Governance/xai_protocols/qualitative_review_rubric.md) & [DEC0018](../decision_log/DEC0018.md) enforce `N=40` stratified `TP/FN/FP/TN` blinding (`RF15` non-trial separation) and honest `Unresolved_NotPerformed_AdvisorUnavailable` fallback; registered `XAIP0001` (`Approved`) in [xai_protocol_registry.csv](../../04_Labels_XAI_Governance/xai_protocol_registry.csv). | **PASS** | `UD18` ratified; `GATE0005 = PASS` unlocks `S08`. |

---

## 4. Overall Gate Outcome
- **Recorded Gate Outcome (`gates.csv`):** **`PASS`** (`Ratified 2026-11-28`; `6/6` mandatory `G05` criteria satisfied, `T09 v1.0.0`, `XAIP0001`, `qualitative_review_rubric.md`, and `DEC0007–0009, DEC0016–0018` Approved and registry-validated).

---

## 5. Assessor, Date, and Required Human Reviewer Sign-off
- **Technical Assessors:** Alzubair Ahamed (`232-15-591`, XAI Lead) & Md Riyadul Hasan (`232-15-486`, Label/Mask Lead) — `2026-11-28`
- **Human Ratification (`G05 PASS`):** **Approved (`2026-11-28`)** by Research Owner/User alongside Supervisor **Israt Jahan** & Research Leads (`gates.csv` `GATE0005 = PASS`; `decisions.csv` `DEC0007–0009, DEC0016–0018 = Approved`).
- **Radiologist / Clinical Advisor (`UD18`):** *Advisor outreach tracked ahead of `STEP-037` (`G13`), with mandatory `Unresolved_NotPerformed_AdvisorUnavailable` fallback bound if unavailable.*

---

## 6. Invalidated Downstream Gates/Artifacts & Reassessment Log
- **Unlocks:** `G05` (`GATE0005 = PASS`) unlocks **`S08` (`STEP-016–018`, `src/bc_xai/labels/verify.py` pilot, full verification, `LBL####` freeze -> `G06`)**.
- **Reassessment Trigger:** Adding `UD13` architecture-specific module strings in `STEP-022` (`G09`) updates target-layer mappings cleanly prior to `G11` lock without altering frozen `XAIP0001` rules.

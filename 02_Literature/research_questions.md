# Provisional Research Questions and Objective-to-Evaluation Mapping

| Header Field | Value |
|---|---|
| `Document` | `02_Literature/research_questions.md` |
| `Version / Date` | `v0.9.0-provisional` / `2026-11-23` (`STEP-004`) |
| `Owner` | Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`) |
| `Governing Section` | [OS §1.4](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3.3–3.4](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [Blueprint STEP-004 & STEP-009](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-004) |
| `Status` | **`PROVISIONAL — AWAITING STEP-008 GAP SYNTHESIS AND STEP-009 (G03) SUPERVISOR RATIFICATION`** |

---

## 1. Overarching Report Research Question (`RF11`)

Preserved verbatim from `Title_defence_evaluation_report.pdf` (p. 8, Section 5):

> **"Can an Explainable Deep Learning framework using transfer learning and mammogram images accurately detect early breast cancer while providing interpretable visual explanations that enhance clinicians' trust and diagnostic decision-making?"**

---

## 2. Candidate Operational Q1 Research Questions (`RQ1–RQ4` — Provisional)

To translate `RF11` and Objectives `O1–O6` (`RF12`) into falsifiable, Q1-journal-grade scientific questions without pre-assuming favorable outcomes or unproven clinical-trial claims (`RF15`), the following four subordinate research questions are formulated for testing against the `STEP-005–008` PRISMA literature evidence:

### `RQ1` — Controlled Multi-Architecture Diagnostic Discrimination, Calibration, and Efficiency (`O1`, `O3`, `O4`)
> **Provisional Question:** *Under strict connected-component patient-level leakage control, how do the approved pre-trained transfer learning CNN architectures (VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3, MobileNetV2, Xception, and any ratified Q1 modern baseline under `UD13`) compare in binary Benign vs Malignant 2D mammogram classification across mandatory report metrics (Accuracy, Precision, Recall/Sensitivity, F1-score, AUC-ROC, Confusion Matrix) and Q1 clinical metrics (Specificity, PR-AUC, Balanced Accuracy, MCC, sensitivity-anchored operating points, Expected Calibration Error, Brier score, and computational efficiency)?*

### `RQ2` — Multi-Center Cross-Dataset Generalization and Clinical Subgroup Robustness across 6 Public Mammogram Cohorts (`O2`, `O3`, `O4`)
> **Provisional Question:** *When trained and selected strictly on internal development cohorts under connected-component patient grouping, how well do the transfer learning architectures generalize zero-shot (and across multi-center splits) to independent external public 2D mammogram datasets within the 6-dataset benchmark pool (`UD05`: evaluating CBIS-DDSM, INbreast, VinDr-Mammo, CMMD, MIAS, and BCDR/DMID/RSNA), and how does performance vary across BI-RADS breast density (A–D), abnormality subtype (mass vs calcification), and view position (CC vs MLO)?*

### `RQ3` — Quantitative Explainable AI Faithfulness, Sanity Verification, Lesion ROI Localization, and Clinical Alignment (`O1`, `O5`, `O6`)
> **Provisional Question:** *Do Grad-CAM visual explanations (and prospectively adopted XAI comparators such as Grad-CAM++, Score-CAM, LayerCAM, Integrated Gradients, Guided Backpropagation, LIME, or SHAP under `UD16`) pass Adebayo model-parameter and data randomization sanity checks, achieve superior causal perturbation faithfulness (Deletion AUC, Insertion AUC, ROAD) and lesion ROI-mask localization (Pointing Game, Energy-Based Pointing Game, thresholded Heatmap-ROI IoU/Dice) across architectures, maintain stability across training seeds and input perturbations, and align with bounded blinded clinical-advisor visual review (`UD18`)?*

### `RQ4` — Controlled Single-Factor Methodological Ablation (`O2`, `O3`, `O5`)
> **Provisional Question:** *What is the isolated, statistically paired effect of prospectively registered methodological factors—specifically (a) CLAHE contrast enhancement vs minimal deterministic preprocessing (`UD12`), (b) two-stage unfrozen fine-tuning vs frozen-backbone feature extraction (`UD15`), and (c) imbalance-aware calibrated loss vs standard binary cross-entropy (`UD15`)—on validation/test discrimination, probability calibration, and quantitative XAI lesion localization?*

---

## 3. Provisional Traceability Matrix (`RQ1–RQ4` → `O1–O6` → Metrics & Gates)

| Candidate RQ | Addressed Report Objectives (`RF12`) | Required Dataset / Mask Properties | Primary Evaluation & Statistical Evidence | Claim Boundary (What Cannot Be Claimed) | Blocking Gate |
|---|---|---|---|---|---|
| **`RQ1`** | `O1`, `O3`, `O4` | Verified `0 = Benign`, `1 = Malignant` labels (`LBL####`); zero patient/view/duplicate leakage (`SPLIT####`) | Accuracy, Precision, Recall, Specificity, F1, AUC-ROC, PR-AUC, Confusion Matrix, ECE, Brier, Params/GFLOPs/Latency, patient-clustered 95% CIs, paired DeLong & McNemar (Holm-Bonferroni) | Cannot claim superiority where Holm-Bonferroni adjusted $p \ge 0.05$; cannot claim clinical diagnostic certainty from uncalibrated logits | `G03`, `G09`, `G11`, `G12` |
| **`RQ2`** | `O2`, `O3`, `O4` | Multi-center 6-dataset pool (`UD05`) with cross-cohort duplicate audit; density/view/subtype metadata where available | Zero-shot external test AUC-ROC, PR-AUC, Sensitivity/Specificity at frozen validation threshold, pre/post-calibration ECE, subgroup stratified tables (`subgroups.csv`) | Cannot treat overlapping DDSM derivatives (e.g., CBIS-DDSM & Mini-DDSM) as independent external cohorts; cannot over-interpret small-$n$ subgroups | `G03`, `G04`, `G07`, `G12`, `G13` |
| **`RQ3`** | `O1`, `O5`, `O6` | Verified co-transformed lesion ROI masks (`LBL####`, post-hoc only) on mask-equipped cohorts; prospective `XAIP####` layer map | Deletion AUC, Insertion AUC, ROAD vs random control; Adebayo cascading/independent sanity correlations; Pointing Game, EBPG, IoU/Dice; seed/perturbation stability; blinded rubric (`UD18`) | Attractive Grad-CAM overlays never prove causal reasoning if sanity or faithfulness checks fail; retrospective review is **not** a clinical trial (`RF15`) | `G03`, `G05`, `G06`, `G12`, `G13` |
| **`RQ4`** | `O2`, `O3`, `O5` | Matched `SPLIT####` across baseline `PP0001` and ablation `PP0002` (`REL####`) | Multi-seed mean $\pm$ SD validation & locked test $\Delta\text{AUC}$, $\Delta\text{ECE}$, and $\Delta\text{EBPG}$ under single-factor control | Cannot claim a single-factor gain if multiple hyperparameters changed simultaneously; negative/null ablations must be reported fully | `G03`, `G08`, `G10`, `G12` |

---

## 4. Path to Final Ratification (`STEP-009` / `G03`)
1. Execute PRISMA searches across `Q1–Q4` and register candidate papers (`STEP-005`).
2. Screen records into buckets `B1–B4_CTX` with explicit exclusion codes (`STEP-006`).
3. Extract included studies (`T05`) and complete the `UD04` primary-source audit of Table 1.1 & References `[1]`–`[12]` (`STEP-007`).
4. Test `RG1–RG4` (`RF16`) in `02_Literature/gaps.csv` and `synthesis.md` (`STEP-008`).
5. Refine and lock `RQ1–RQ4` with supervisor sign-off in `STEP-009` (`G03 PASS`).

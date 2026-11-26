# Research Questions and Objective Mapping (`STEP-009` Candidate for `G03` Ratification)

| Header Field | Value |
|---|---|
| `DocumentID` | `RESEARCH_QUESTIONS` |
| `Version / Date` | `v1.0.0` (Ratified at `G03`, `2026-11-27`) |
| `Owner` | Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`) |
| `Approver Required` | Israt Jahan (Supervisor, Approved `2026-11-27`) & Ms Faiza Feroz (Co-Supervisor) at **`G03`** (`DEC0003` Phase 2) |
| `Governing Inputs` | [scope.md](../01_Project_Management/scope.md) (`RF11–RF12`, `RF15`); [synthesis.md](./synthesis.md); [gaps.csv](./gaps.csv); [claims.csv](./claims.csv); [DEC0003](../01_Project_Management/decision_log/DEC0003.md); [DEC0004](../01_Project_Management/decision_log/DEC0004.md) |
| `Status` | `RATIFIED_G03_PASS` (`Option 1 + RQ1–RQ4 Approved by Supervisor Israt Jahan, 2026-11-27`) |

---

## 1. Overarching Research Question (`RF11`, `Title_defence_evaluation_report.pdf` p. 8, Sec. 5)

> *"Can an Explainable Deep Learning framework using transfer learning and mammogram images accurately detect early breast cancer while providing interpretable visual explanations that enhance clinicians' trust and diagnostic decision-making?"*

- **Post-`STEP-008` Epistemic Qualification (`RF15` & `GAP0001–GAP0004`):** Retrospective public 2D mammography modeling cannot prove real-time clinical workflow impact without prospective reader trials (outside `RF15` exclusions). Therefore, **"enhance clinicians' trust and diagnostic decision-making"** is operationalized conservatively as: (a) calibrated probabilities (`ECE`, `Brier`), (b) high-sensitivity operating-point triage (`Specificity@95%Sensitivity`), (c) verified XAI **causal faithfulness, `Adebayo` sanity invariance, chance-normalized localization, and seed stability**, and (d) **bounded blinded qualitative clinical-advisor alignment** (`UD18`).

---

## 2. Finalized Candidate Operational Research Questions (`RQ1–RQ4`)

| RQ ID | Finalized Falsifiable Research Question (Gated at `G03`) | Objectives (`O1–O6`) | Verified Gaps & Claims | Primary Endpoints & Statistical Protocol |
|---|---|---|---|---|
| **`RQ1`** *(Diagnostic Discrimination, Granularity & Calibration Under Zero Leakage)* | **Under strict connected-component patient-level leakage control (`zero augmented/diagnostic/side leakage`) and segregated ground-truth schemas (`biopsy pathology vs radiologist BI-RADS screening triage`), how do the approved pre-trained CNNs and aspect-preserving modern baselines compare in Benign-vs-Malignant discrimination, probability calibration (`ECE`, `Brier`), clinical sensitivity-anchored operating specificity (`Specificity@95%Sensitivity`), side-vs-patient reporting delta, and computational efficiency?** | `O1`, `O3`, `O4`, `O6` | `GAP0002`; `CLAIM0002`, `CLAIM0006`, `CLAIM0008`, `CLAIM0009` | **Metrics:** `AUROC`, `PR-AUC`, `Accuracy`, `Precision`, `Recall`, `Specificity`, `F1`, `Balanced Acc`, `MCC`, `Confusion Matrix`, `Spec@95%Sens`, `ECE`, `Brier score`, `Params / GFLOPs / Latency` reported at **both patient-level & side-level** (`P0385`).<br>**Stats:** Multi-seed mean ± SD; `>=5,000`-resample **patient-clustered bootstrap 95% CIs**; paired **`DeLong`** (`AUC`) & **`McNemar`** tests with **`Holm-Bonferroni` / `BH-FDR`** adjustment. |
| **`RQ2`** *(Cross-Vendor / Cross-Population Generalization & External Calibration-XAI Drift)* | **When evaluated strictly zero-shot across isolated multi-vendor `FFDM` (`VinDr-Mammo, CMMD, INbreast`) and digitized `SFM` (`CBIS-DDSM, MIAS/DMID`) cohorts, how severely do discrimination, calibration error (`ECE/Brier`), fixed internal thresholds, and XAI faithfulness/localization degrade across scanner vendors, screening-vs-enriched prevalence shifts, and geographic populations—and how much calibration mismatch can post-hoc validation temperature scaling recover?** | `O1`, `O4`, `O6` | `GAP0003`; `CLAIM0004`, `CLAIM0007`, `CLAIM0008` | **Metrics:** Zero-shot external `AUROC`, `PR-AUC`, `Spec@95%Sens` (`vs frozen internal threshold drift` per `P0675`), pre/post-temperature-scaling `ECE` & `Brier score`, plus external XAI **faithfulness & localization retention** (`Deletion/Insertion AUC`, `Delta-PG`, `Activation Precision`) across Castro's distribution shifts (`Acquisition, Prevalence, Population, Manifestation`). |
| **`RQ3`** *(Quantitative XAI Faithfulness, Sanity, Density-Aware Localization & Clinical Alignment)* | **Do `Grad-CAM` and comparator saliency/attribution methods (`Grad-CAM++, LayerCAM, Score-CAM, Integrated Gradients` per `UD16`) satisfy `Adebayo` model-parameter & data-randomization sanity checks, yield measurably higher perturbation faithfulness (`Deletion/Insertion/ROAD`) and ROI localization (`Pointing Game`, chance-normalized `Delta-PG`, `EBPG`, `IoU/Dice`) on correctly vs incorrectly classified `INbreast`/`VinDr-Mammo`/`CBIS-DDSM` cases, remain stable across random seeds, and align with blinded radiologist/advisor review?** | `O1`, `O5`, `O6` | `GAP0001`; `CLAIM0001`, `CLAIM0003`, `CLAIM0005` | **Metrics:** **`Deletion AUC`**, **`Insertion AUC`**, **`ROAD`**, **`Adebayo` cascading parameter & label randomization SSIM/Spearman rank correlation**, **`Pointing Game`**, chance-normalized **`Delta-PG` (`P0810`)**, **`EBPG / half-max IoU / Dice`**, seed/perturbation **`SSIM` stability**, plus bounded blinded clinical-advisor localization/usefulness rubric (`UD18`). |
| **`RQ4`** *(Breast Density `BI-RADS A–D` Fairness & Controlled Preprocessing / Resolution / Loss Ablations)* | **What are the controlled effects of mammography resolution (`224x224` vs aspect-preserving `>=512` / `1024x512`), contrast preprocessing (`raw 16-bit normalization` vs training-fitted `CLAHE`), class-imbalance loss (`unweighted` vs `weighted BCE / focal`), and backbone inductive bias (`CNN` vs `ConvNeXt / Swin / Hybrid`) on validation discrimination, calibration (`ECE`), BI-RADS `A–D` dense-breast fairness, and causal XAI faithfulness?** | `O2`, `O3`, `O4`, `O5` | `GAP0004`; `CLAIM0005`, `CLAIM0006` | **Subgroups & Factors:** Single-variable controlled ablations under identical patient splits & multi-seed seeds (`UD12–UD15`), stratified by **BI-RADS breast density (`A/B` vs `C/D`)**, **abnormality type (`mass` vs `calcification`)**, and **view (`CC` vs `MLO`)** (`paired DeLong / permutation + Holm-Bonferroni`). |

---

## 3. Binding Traceability Summary (`O1–O6` Coverage)

- **`O1` (Explainable Framework):** `RQ1 + RQ2 + RQ3` (`end-to-end hashed release -> trained calibrated model -> verified XAI + CAD prototype`).
- **`O2` (Preprocessing & Augmentation):** `RQ1 + RQ4` (`fit-free / train-only stats, bit-depth/polarity QC, aspect-preserving resolution vs 224x224, CLAHE ablation`).
- **`O3` (Multi-Architecture Transfer Learning):** `RQ1 + RQ4` (`UD13 resolution of Sec. 2/4/6 model discrepancy + controlled Q1 baselines`).
- **`O4` (Classification Evaluation + Q1 Rigor):** `RQ1 + RQ2 + RQ4` (all `6` required `RF09` metrics + calibration, clustered bootstrap CIs, DeLong/McNemar, external + subgroup fairness).
- **`O5` (XAI Visualization + Quantitative Audit):** `RQ2 + RQ3 + RQ4` (`Grad-CAM` + comparators verified with `Deletion/Insertion/ROAD`, `Adebayo`, `PG/Delta-PG/IoU`, stability, external retention, and clinical advisor rubric).
- **`O6` (Reliable Interpretable CAD Framework):** `RQ1–RQ3` (minimal local CAD inference + calibrated uncertainty + validated explanation overlays + explicit non-clinical disclaimers).

> **Ratified at `G03` (`2026-11-27`):** **Option 1** ([synthesis.md §4](./synthesis.md#4-three-bounded-q1-contribution-options-within-o1o6--rf15-for-g03-ratification)) and **`RQ1–RQ4`** were approved by Supervisor Israt Jahan ([DEC0003](../01_Project_Management/decision_log/DEC0003.md), [G03 Assessment](../01_Project_Management/reviews/G03_assessment_2026-11-26.md)), formally unblocking `STEP-010` (`UD05–UD06` public 2D mammography dataset audit). *(Note: exact printed `[6]–[8]` strings from out-of-repo physical `Title_defence_evaluation_report.pdf p. 10` remain honestly logged as un-transcribed while all `SL 1–10` rows remain retired per [DEC0004](../01_Project_Management/decision_log/DEC0004.md).)*

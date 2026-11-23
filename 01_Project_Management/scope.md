# Project Scope Constitution and Operational Role Charter

- **Document:** `01_Project_Management/scope.md`
- **Version / Date:** `v1.0.0` / `2026-11-23`
- **Governing Authority:** [BC_XAI_RESEARCH_OPERATING_SYSTEM.md](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) (§1, §11, §13) and `Title_defence_evaluation_report.pdf` (`RF01–RF20`)
- **Step / Gate:** [STEP-001](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-001) / `G01`
- **Approval Status:** `Approved / Ratified` (`2026-11-23`, via `DEC0001` / `UD01`; `G01 PASS`)

---

## 1. Verbatim Approved Project Identity (`RF01–RF04`)

| Field | Source-Grounded Value (`REPORT FACT`) | PDF Locator |
|---|---|---|
| **Approved Project Title** | *Explainable Deep Learning-Based Early Breast Cancer Detection Using Mammogram Images* | p. 1, Sec. I; p. 2, CO table; pp. 3, 5 (`RF01`) |
| **Institution & Department** | Daffodil International University (DIU), Department of Computer Science and Engineering | p. 1, Header (`RF02`) |
| **Evaluation Context** | FYDP (Title Phase) Evaluation Report [Version 2.0]; Reporting Period: Summer 2026; Submission Date: 15 August 2026 | p. 1, Header & Sec. V (`RF02`) |
| **Researcher 1** | **Alzubair Ahamed** (ID: `232-15-591`) | p. 1, Sec. II (`RF02`) |
| **Researcher 2** | **Md Riyadul Hasan** (ID: `232-15-486`) | p. 1, Sec. II (`RF02`) |
| **Supervisor** | **Israt Jahan**, Lecturer (Senior Scale) | p. 1, Sec. III (`RF02`) |
| **Co-Supervisor** | **Ms Faiza Feroz**, Lecturer | p. 1, Sec. IV (`RF02`) |
| **CO / PO Mapping** | `CO1 → PO1` (problem identification), `CO2 → PO2` (goal analysis), `CO3 → PO4` (literature review & FYDP goals) | p. 2, CO/PO Table (`RF04`) |
| **Title-Phase Certificate Boundary** | Signed certificate (`VII. Certificate:`, dated `15/8/26`, p. 1) and signed/dated feedback page (`15/8/26`, p. 11) certify title-defense phase record only | p. 1, Sec. VII (`RF03`); p. 11 (`RF20`) |

> **Epistemic Boundary (`RF03`):** The signed title-phase certificate on Page 1 does **not** constitute institutional ethics approval, dataset license/DUA authorization, clinical validation, or ratification of the Q1 planning recommendations in `BC_XAI_RESEARCH_OPERATING_SYSTEM.md`.

---

## 2. Binding Scope Inclusions and Exclusions (`RF05–RF15`)

### 2.1 Mandatory In-Scope Commitments (`RF05–RF10`, `RF12`, `RF14`)
1. **Primary Modality & Task (`RF05`, `RF14`):** Binary classification of publicly available 2D mammogram images into **Benign (`0`)** and **Malignant (`1`)** categories.
2. **Preprocessing Scope (`RF10`, `O2`):** Mammogram preprocessing covering resizing, normalization, and training-only data augmentation (with specific bit-depth, polarity, artifact-handling, and CLAHE-ablation parameters governed as `PLANNING RECOMMENDATIONS` under `UD12`).
3. **Transfer Learning Multi-Architecture Benchmark (`RF06–RF07`, `O3`):** Controlled comparison of multiple pre-trained CNN architectures using transfer learning (resolving the report's 5-model [Sec. 4: VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3] vs 6-model [Obj. 3: adding MobileNetV2] vs 7-model [Sec. 2: adding Xception] discrepancy explicitly under `UD13` at `STEP-022`).
4. **Required Classification Evaluation Metrics (`RF09`, `O4`):** **Accuracy, Precision, Recall (Sensitivity), F1-score, AUC-ROC, and Confusion Matrix** across all evaluated models (augmented by Q1 medical-AI metrics—Specificity, PR-AUC, Balanced Accuracy, MCC, clinical sensitivity-anchored operating points, ECE/Brier calibration, patient-clustered bootstrap 95% CIs, and paired DeLong/McNemar tests—under `UD19–UD20`).
5. **Explainable AI Integration (`RF08`, `O5`):** Mandatory **Grad-CAM** visual explanation heatmaps highlighting suspicious regions (plus prospectively ratified Q1 comparators such as Grad-CAM++, Score-CAM, LayerCAM, Integrated Gradients, Guided Backpropagation, LIME, or SHAP under `UD16`), evaluated via quantitative faithfulness (Deletion/Insertion/ROAD), Adebayo sanity checks, ROI-mask localization (Pointing Game/EBPG/IoU), stability (`UD17`), and bounded blinded clinical-advisor review (`UD18`).
6. **Research CAD Prototype & Deliverables (`O1`, `O6`):** Reproducible local research Computer-Aided Diagnosis (CAD) inference + Grad-CAM explanation prototype (`STEP-038`), FYDP thesis (`G15 / thesis`), Q1 journal manuscript pathway (`G15 / paper`), and conditional hosted defense web showcase (`S16`, `G17`, gated by `UD25`).

### 2.2 Hard Scope Exclusions (`RF15`, Section 8 — Non-Negotiable)
1. **No non-mammogram imaging modalities:** No detection/classification from MRI, CT Scan, Ultrasound, or Histopathology (e.g., BreakHis) images, nor tabular non-imaging datasets (e.g., Wisconsin).
2. **No post-diagnostic prognostic modeling:** No prediction of cancer stages, treatment planning, or survival analysis.
3. **No clinical/hospital deployment:** No real-time deployment in hospitals or integration with PACS systems.
4. **No mobile or hardware products:** No development of mobile applications or IoT-enabled healthcare devices.
5. **No clinical trials:** No prospective or interventional clinical trials involving real patients.
6. **No clinical prescribing:** No automated recommendation of medications or treatment procedures.

---

## 3. Approved Objectives (`O1–O6`, `RF12`) and Overarching Research Question (`RF11`)

**Overarching Report Research Question (`RF11`, p. 8, Sec. 5):**
> *"Can an Explainable Deep Learning framework using transfer learning and mammogram images accurately detect early breast cancer while providing interpretable visual explanations that enhance clinicians' trust and diagnostic decision-making?"*

*(Operational subordinate research questions `RQ1–RQ4` remain provisional until PRISMA literature verification and `G03` ratification at `STEP-009`.)*

| Objective ID | Verbatim Report Objective (`RF12`, p. 8, Sec. 6) | Governing Blueprint Stages | Exit Gate(s) |
|---|---|---|---|
| **O1** | To develop an explainable deep learning framework for early breast cancer detection using mammogram images. | `S01–S15` | `G01–G16` |
| **O2** | To preprocess mammogram images through resizing, normalization, and data augmentation to improve the performance and generalization capability of the deep learning models. | `S05–S09` (`STEP-010–021`) | `G04`, `G07`, `G08` |
| **O3** | To train and compare multiple pre-trained deep learning architectures such as VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3, and MobileNetV2 using transfer learning. | `S10–S11` (`STEP-022–031`) | `G09`, `G10` |
| **O4** | To evaluate the performance of each model using Accuracy, Precision, Recall, F1-score, AUC-ROC, and Confusion Matrix, and identify the best-performing architecture. | `S12–S13` (`STEP-032–036`) | `G11`, `G12` |
| **O5** | To integrate Explainable Artificial Intelligence (XAI) techniques such as Grad-CAM to generate visual heatmaps highlighting suspicious regions in mammogram images. | `S07–S08`, `S10`, `S13–S14` (`STEP-015`, `025`, `035–037`) | `G05`, `G06`, `G12`, `G13` |
| **O6** | To develop a reliable and interpretable computer-aided diagnosis (CAD) framework that supports radiologists in early breast cancer detection. | `S14–S16` (`STEP-037–050`) | `G13`, `G14`, `G15`, `G16` (+ `G17` if `UD25` adopted) |

---

## 4. Operational Role Assignments (`UD01` — Proposed for Team & Supervisor Ratification)

| Operational Role ([OS §11](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-11)) | Proposed Named Owner(s) | Primary Responsibilities & Decision Boundaries |
|---|---|---|
| **Research Lead & Project Coordinator** | **Alzubair Ahamed** (`232-15-591`) & **Md Riyadul Hasan** (`232-15-486`) (Co-Leads) | Overall schedule, registry integrity, decision logging (`decisions.csv`), gate preparation, weekly reviews |
| **Literature & Bibliographic Verification Lead** | **Alzubair Ahamed** (Lead) / **Md Riyadul Hasan** (Co-Reviewer) | PRISMA search execution, dual independent screening, `UD04` Table 1.1 & Ref `[1]`–`[12]` anomaly remediation (`STEP-004–009`) |
| **Data Steward & Label/Mask Audit Lead** | **Md Riyadul Hasan** (Lead) / **Alzubair Ahamed** (Verifier) | Public mammogram dataset discovery (including proposed 6-dataset multi-center evaluation under `UD05`), DUA/license tracking (`UD06`), DICOM/PHI QC, connected-component patient splitting (`STEP-010–021`) |
| **Model, Transfer Learning & XAI Lead** | **Alzubair Ahamed** (Lead) / **Md Riyadul Hasan** (Co-Implementer) | `src/bc_xai/` implementation, transfer learning benchmark (`UD13`), Grad-CAM & XAI comparators (`UD16`), faithfulness/sanity/localization harness (`STEP-022–031`, `035`) |
| **Evaluation, Calibration & Reproducibility Reviewer** | **Md Riyadul Hasan** (Lead) / **Alzubair Ahamed** (Auditor) | `G11` freeze audit, threshold/calibration verification (`UD19`), DeLong/McNemar/clustered bootstrap tests (`UD20`), clean-environment replay & CLAIM/TRIPOD+AI checklist (`STEP-032–039`) |
| **Writing, Release & Archival Owner** | **Alzubair Ahamed** & **Md Riyadul Hasan** (Joint Authors) | Evidence-first FYDP thesis & Q1 journal manuscript drafting, figure/citation verification, `ARCH####` packaging (`STEP-040–047`) |
| **Conditional Web Deployment Owner (`S16`)** | **Alzubair Ahamed** (Lead, if `UD25` ratified) | Thin containerized Grad-CAM web showcase, parity verification against `STEP-038`, offline fallback (`STEP-048–050`) |
| **Supervisory Scientific Authority** | **Israt Jahan** (Supervisor) & **Ms Faiza Feroz** (Co-Supervisor) | Non-delegable scientific ratification of scope, RQs (`G03`), dataset/label protocols (`G04–G05`), split (`G07`), test freeze (`G11`), limitations (`G13`), submissions (`G15`), web demo (`G17`), and closure (`G16`) |
| **Radiologist / Clinical Advisor (`UD18`)** | **To Be Assigned (`Unresolved / Human Decision Required`)** | Blinded qualitative XAI review rubric (`UD18`), FFDM/ROI & Normal-case clinical consultation (`UD07–UD08`); strictly non-trial advisory boundary |

---

## 5. Title-Defense Feedback Verification Record (`RF20`, `UD01`)

- **Physical PDF Inspection of Page 11 (`RF20`):**
  - Inside the `Supervisor's Feedback: Provide comments and suggestions for improvement` box, numbered lines `1.`, `2.`, and `3.` are **completely blank** (zero written comments).
  - Below the box, a handwritten signature (visually matching the Page 1 supervisor signature) appears on `Examiner's Signature:` and a handwritten date `15/8/26` appears on `Date:`.
- **Operational Rule:** Zero examiner feedback is invented or assumed from Page 11. Under `UD01` (`DEC0001`), the research team and supervisor confirm whether any separate verbal or external written title-defense feedback was given; if none exists, `UD01` closes with explicit confirmation that no unrecorded title-defense modifications are pending.

---

## 6. Queued Team Proposal Note: 6-Dataset Multi-Center Mammography Strategy (`UD05`)

The research team has expressed intent to evaluate **6 public 2D mammogram datasets** (e.g., candidate pool including CBIS-DDSM, INbreast, VinDr-Mammo, CMMD, MIAS, and BCDR/DMID/RSNA). In strict compliance with `STEP-001` discipline:
- No dataset is marked "acquired" or "pre-approved" at `G01`.
- This 6-dataset multi-center proposal is formally logged under `UD05` (`DEC0005`) to be systematically audited for 2D mammography eligibility (`RF15`), non-overlapping patient provenance (guarding against DDSM/CBIS-DDSM/Mini-DDSM overlap), licensing/DUAs (`UD06`), and internal-vs-external validation partitioning during `STEP-010`–`STEP-013` (`G04`).

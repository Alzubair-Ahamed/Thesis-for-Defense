# BC-XAI RESEARCH OPERATING SYSTEM

## Cover page

**Approved research title:** Explainable Deep Learning-Based Early Breast Cancer Detection Using Mammogram Images

| Field | Value |
|---|---|
| Document | BC_XAI_RESEARCH_OPERATING_SYSTEM.md |
| Type | Project-specific Q1-grade research governance and operational handbook |
| Version / date | v1.0.0 / 2026-11-23 |
| Status | Complete planning document; proposed operating policies awaiting human ratification; research execution NOT VERIFIED |
| Institution | Daffodil International University, Department of Computer Science and Engineering (report cover, p. 1) |
| Report context | FYDP (Title Phase) Evaluation Report [Version 2.0]; reporting period Summer 2026; submission date 15 August 2026 (p. 1) |
| Researchers | Alzubair Ahamed, ID 232-15-591; Md Riyadul Hasan, ID 232-15-486 (p. 1) |
| Supervisor | Israt Jahan, Lecturer (Senior Scale) (p. 1) |
| Co-supervisor | Ms Faiza Feroz, Lecturer (p. 1) |
| Operational owner | Research team; named task owners and qualified breast radiologist / clinical advisor remain to be assigned (UD01, UD18) |
| Scientific authority | `Title_defence_evaluation_report.pdf` (all 11 physical pages visually inspected and audited; see [source provenance](#source-status)) |
| Execution companion | [BC-XAI Project Execution Blueprint](./BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md) |
| Intended output | Reproducible, quantitatively evaluated Explainable Deep Learning Computer-Aided Diagnosis (CAD) research framework for 2D mammogram Benign vs Malignant classification with verified visual explanations (Grad-CAM baseline and approved XAI comparators), FYDP thesis, Q1 journal manuscript pathway, and conditional defense web showcase; research aid only, not validated clinical diagnosis or hospital deployment |

The cover's signed certificate (p. 1, dated 15/8/26) and the signature/date on the blank feedback form (p. 11, dated 15/8/26) are part of the supplied title-phase administrative record. They do **not** establish approval of this handbook's planning recommendations, institutional ethics clearance, dataset licensing, Q1 journal suitability, or clinical validation. No such approval is inferred here.

## Version history

| Version | Date | Change | Approval state |
|---|---|---|---|
| v1.0.0 | 2026-11-23 | Initial source-grounded mammography XAI research operating system aligned with a 16-stage, 50-step, 17-gate Q1 execution blueprint, incorporating quantitative XAI faithfulness/sanity/localization governance, Q1 calibration/statistical rigor, CLAIM/TRIPOD+AI compliance, dual-track thesis/Q1 journal submission, and conditional FYDP defense web demo | Proposed; human ratification pending; all execution gates NOT ASSESSED |

Record subsequent changes with author, date, rationale, affected `UD`/`DEC` records, affected steps and gates, and human approval evidence. Any change to the approved title, modality, binary classification scope, or explicit Section 8 exclusions requires formal supervisor review. Typographical corrections never silently alter scientific commitments.

## Table of contents

1. [Executive summary](#executive-summary)
2. [1. Project constitution and source authority](#os-01)
3. [2. Repository architecture and folder contracts](#os-02)
4. [3. Literature and Q1 research-question workflow](#os-03)
5. [4. Mammogram dataset, label/ROI-mask audit, preprocessing, and leakage-safe split operating system](#os-04)
6. [5. Transfer learning model benchmarking and experiment operating system](#os-05)
7. [6. Explainable AI (XAI) governance, quantitative faithfulness, sanity checks, and clinical alignment protocol](#os-06)
8. [7. Q1 classification, calibration, statistical testing, and error-analysis evaluation protocol](#os-07)
9. [8. Research CAD prototype, reproducibility audit, and conditional hosted web demonstration](#os-08)
10. [9. Evidence-first writing, Q1 journal manuscript, and FYDP thesis submission operating system](#os-09)
11. [10. Version control, artifact storage, and two-phase environment readiness](#os-10)
12. [11. Roles and human decisions](#os-11)
13. [12. Daily research operations, reviews, and risk register](#os-12)
14. [13. Quality gates and project completion criteria](#os-13)
15. [14. Template library](#os-14)
16. [Appendix A. Canonical definitions](#appendix-a)
17. [Appendix B. Registry catalog and schemas](#appendix-b)
18. [Appendix C. Stage map and dependency chain](#appendix-c)
19. [Appendix D. Glossary](#appendix-d)
20. [Appendix E. Acronyms](#appendix-e)
21. [Appendix F. Source coverage and self-review](#appendix-f)

<a id="executive-summary"></a>
## Executive summary

This handbook establishes a Q1-journal-grade research operating system for **Explainable Deep Learning-Based Early Breast Cancer Detection Using Mammogram Images**. Grounded strictly in the approved FYDP Title Phase Evaluation Report (`Title_defence_evaluation_report.pdf`, pp. 1–11), the project addresses binary classification of publicly available 2D mammogram images into **Benign** and **Malignant** categories using transfer learning across multiple pre-trained Convolutional Neural Network (CNN) architectures, integrated with Explainable Artificial Intelligence (XAI)—primarily **Grad-CAM**, with additional XAI techniques noted in the report as comparative candidates—to generate visual heatmaps supporting radiologists as a research Computer-Aided Diagnosis (CAD) aid.

The title report establishes six objectives (O1–O6), six required classification metrics (Accuracy, Precision, Recall, F1-score, AUC-ROC, and Confusion Matrix), candidate transfer learning architectures (with a documented discrepancy across report sections), high-level preprocessing concepts (resizing, normalization, and data augmentation), and six binding scope exclusions (no MRI/CT/Ultrasound/Histopathology; no staging/treatment/survival analysis; no hospital/PACS deployment; no mobile/IoT applications; no real-patient clinical trials; no automated medication or treatment recommendations). It does **not** select datasets, split ratios, FFDM-versus-ROI image paradigms, preprocessing parameters, hyperparameters, statistical tests, or quantitative XAI validation metrics. Those items remain explicitly governed as **Unresolved / Human Decision Required (`UD01–UD28`)**.

To elevate the approved FYDP scope to Q1 medical imaging journal standards (*Nature* family, *IEEE Transactions on Medical Imaging*, *Medical Image Analysis*, *Computers in Biology and Medicine*, *Radiology: Artificial Intelligence*), this operating system introduces structured **PLANNING RECOMMENDATIONS** gated by supervisor and domain-advisor ratification: (1) PRISMA-style systematic literature verification that rigorously tests—rather than assumes—the report's preliminary novelty claim and resolves Table 1.1 / reference anomalies; (2) strict connected-component patient/view/duplicate grouping before splitting plus an independent external-dataset validation track; (3) prospective diagnostic label provenance and lesion ROI-mask alignment audits; (4) quantitative XAI governance combining perturbation faithfulness (Deletion/Insertion/ROAD), Adebayo sanity checks, ROI-mask localization alignment, seed/perturbation stability, and bounded blinded clinical-advisor qualitative review; (5) Q1 classification rigor adding Specificity, PR-AUC, calibration (ECE, Brier score, reliability diagrams), validation-only operating-point selection, patient-clustered bootstrap 95% confidence intervals, DeLong and McNemar paired tests with multiple-comparison correction, and density/view/abnormality subgroup error analysis; (6) CLAIM and TRIPOD+AI reporting compliance and clean-environment reproducibility auditing; and (7) dual-track submission readiness separating `G15 / thesis` from `G15 / paper` alongside a conditional, research-only hosted web showcase for the FYDP defense (Stage S16, `G17`, gated by `UD25`).

This is a **planning specification**, not a record of completed research. No datasets have been acquired, no models have been trained, no literature citations have been independently verified, and no scientific claims have been proven. All execution steps (`STEP-001` through `STEP-050`) start **NOT STARTED**, and all quality gates (`G01–G17`) start **NOT ASSESSED**, blocking dependent execution until dated, hashed human-reviewed evidence exists.

<a id="os-01"></a>
# 1. Project constitution and source authority

## 1.1 Authority and evidence labels

Enforce the following three-tier epistemic labeling standard across all decisions, registries, protocols, code comments, drafts, and manuscripts:

- **REPORT FACT (`RF##`):** Content explicitly present in `Title_defence_evaluation_report.pdf`, accompanied by its exact physical PDF page (1–11) and section/table locator. A report statement summarizing an external paper is a fact about what the report states, **not** independent verification of that external paper.
- **PLANNING RECOMMENDATION:** A Q1-grade scientific, methodological, statistical, or engineering policy introduced by this operating system or its companion blueprint. A planning recommendation becomes an adopted project rule only when the responsible human records an approved decision (`DEC####`); it must **never** be attributed to the title evaluation report.
- **Unresolved / Human Decision Required (`UD##`):** Any missing, ambiguous, contradictory, unverified, or choice-dependent detail requiring named human ownership and concrete evidence before crossing its blocking milestone. Software library defaults never silently resolve a `UD` item.

**Authority hierarchy:** (1) `Title_defence_evaluation_report.pdf` and binding scope exclusions; (2) recorded supervisor-approved clarifications and decisions (`DEC####`) operating within that approved scope; (3) this handbook (`BC_XAI_RESEARCH_OPERATING_SYSTEM.md`); (4) the companion sequential manual ([BC-XAI Project Execution Blueprint](./BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md)); (5) validated executable experiment configurations. Two workspace governance reference files informed only structural architecture, registry mechanics, gate semantics, and step schema; zero external-domain concepts or implementation mandates were inherited (see [Appendix F](#appendix-f)). If an implementation or draft conflicts with a governing rule, halt dependent work, log the conflict, and either repair the implementation or formally ratify a policy revision—never retroactively reinterpret prior empirical results.

## 1.2 Source-grounded facts ledger

Physical PDF page numbers below run from page 1 (cover and project identification) through page 11 (feedback form), verified visually across all 11 rendered pages of `Title_defence_evaluation_report.pdf`.

| ID | REPORT FACT | Locator | Operational implication |
|---|---|---|---|
| RF01 | Exact approved title: *Explainable Deep Learning-Based Early Breast Cancer Detection Using Mammogram Images* | p. 1, Project Identification I; p. 2, CO table; pp. 3, 5, text | Preserve title verbatim across registries, thesis cover, and official records |
| RF02 | Institution and team: Daffodil International University, Dept. of CSE; FYDP (Title Phase) Evaluation Report [Version 2.0], Summer 2026; Submission Date 15 August 2026; Group Members: Alzubair Ahamed (ID: 232-15-591) & Md Riyadul Hasan (ID: 232-15-486); Supervisor: Israt Jahan, Lecturer (Senior Scale); Co-Supervisor: Ms Faiza Feroz, Lecturer | p. 1, Header & Project Identification II–V | Record exact institutional metadata and team/supervisory roles; assign operational leads in STEP-001 (UD01) |
| RF03 | Signed certificate (`VII. Certificate:`, skipping numeral `VI.` in the printed form) states title-defense work held on 15 August 2026 was found satisfactory; bears handwritten supervisor signature and date `15/8/26` | p. 1, Project Identification VII | Administrative title-phase record only; does not grant ethics clearance, data access, or clinical approval |
| RF04 | Title Defense Phase CO/PO alignment: CO1→PO1 (complex engineering problem identification), CO2→PO2 (engineering goal analysis), CO3→PO4 (literature review, issue delineation, FYDP goals) | p. 2, CO Description and Corresponding PO table | Preserve institutional outcome context; do not fabricate course assessment marks |
| RF05 | Core modality and task: binary classification of publicly available 2D mammogram images into **Benign** and **Malignant** categories | p. 3, Sec. 1; p. 5, Sec. 2; p. 7, Sec. 4; p. 9, Sec. 8 | Strictly 2D mammography binary classification; resolve FFDM vs ROI paradigm and Normal-case handling under UD07–UD08 |
| RF06 | Core modeling methodology: transfer learning using multiple pre-trained CNN architectures with comparative evaluation to identify the best-performing architecture | pp. 2–3, Sec. 1; p. 5, Sec. 2; p. 8, Sec. 4 & Sec. 6 Obj. 3–4; p. 9, Sec. 8 | Controlled multi-architecture transfer learning benchmark required under matched data/splits |
| RF07 | Candidate architecture discrepancy across sections: Sec. 1 (p. 2) lists VGG16, ResNet50, DenseNet121, EfficientNet, InceptionV3; Sec. 2 (p. 5) lists VGG16, ResNet50, DenseNet121, MobileNetV2, EfficientNet, InceptionV3, Xception; Sec. 4 (p. 8) lists 5 models (VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3); Sec. 6 Obj. 3 (p. 8) lists 6 models (adding MobileNetV2) | p. 2, Sec. 1; p. 5, Sec. 2; p. 8, Sec. 4 & Sec. 6 Obj. 3 | Preserve discrepancy verbatim; resolve exact architecture roster and optional Q1 baselines explicitly under UD13 |
| RF08 | Explainable AI (XAI) scope: **Grad-CAM** is specified as the primary method for visual heatmaps highlighting suspicious regions; narrative sections also reference LIME, SHAP (pp. 3, 5), Integrated Gradients, and Guided Backpropagation (p. 5) | p. 3, Sec. 1; p. 5, Sec. 2; pp. 7–8, Sec. 4 & Sec. 6 Obj. 5; p. 9, Sec. 8 | Grad-CAM is mandatory baseline; decide additional XAI comparators and quantitative XAI evaluation under UD16–UD17 |
| RF09 | Required classification evaluation metrics: **Accuracy, Precision, Recall, F1-score, AUC-ROC, and Confusion Matrix** (Sec. 2 p. 5 also notes ROC Curve/AUC in Rautela et al. summary) | p. 8, Sec. 6 Obj. 4; p. 5, Sec. 2 | Report all six metrics completely for every evaluated architecture; add Q1 clinical/statistical metrics under UD19–UD20 |
| RF10 | Preprocessing concepts mentioned: resizing, normalization, and data augmentation to improve performance and generalization | p. 8, Sec. 6 Obj. 2; p. 9, Sec. 8 | High-level categories only; no dimensions, bit-depth scaling, split ratios, or augmentation parameters are specified (UD11–UD12) |
| RF11 | Verbatim report Research Question: *"Can an Explainable Deep Learning framework using transfer learning and mammogram images accurately detect early breast cancer while providing interpretable visual explanations that enhance clinicians' trust and diagnostic decision-making?"* | p. 8, Sec. 5 | Retain as overarching guiding question; operationalize into testable, bounded subordinate RQs at STEP-009 (G03) |
| RF12 | Six numbered Objectives (O1–O6): (1) develop explainable DL framework for early breast cancer detection using mammograms; (2) preprocess mammograms via resizing, normalization, augmentation; (3) train and compare multiple pre-trained DL architectures using transfer learning; (4) evaluate using Accuracy, Precision, Recall, F1-score, AUC-ROC, Confusion Matrix and identify best model; (5) integrate XAI (Grad-CAM) to generate visual heatmaps of suspicious regions; (6) develop a reliable, interpretable CAD framework supporting radiologists | p. 8, Sec. 6, Objectives 1–6 | Map every experimental factor, evaluation artifact, and manuscript claim back to O1–O6 without claiming proven clinical utility |
| RF13 | Eight Expected Outcomes listed: high-performance explainable DL model; identification of best transfer learning architecture; improved accuracy over conventional ML; Grad-CAM visual explanations for transparency/trust; reduced false positives/negatives; extendable benchmark CAD framework; validated well-prepared dataset; foundation for future web-based or mobile clinical decision support application | pp. 8–9, Sec. 7 | Aspirational research targets, not pre-guaranteed outcomes; empirical claims must follow realized evidence |
| RF14 | Explicit Scope Inclusions (7 items): collection/preprocessing of public mammogram datasets; Benign vs Malignant binary classification; transfer learning with multiple pre-trained CNNs; model performance comparison; Grad-CAM visualization; standard classification evaluation; comparative analysis with SOTA methods | p. 9, Sec. 8, Included in this research | Defines mandatory minimum research deliverables |
| RF15 | Explicit Scope Exclusions (6 items): no MRI, CT Scan, Ultrasound, or Histopathology detection; no cancer staging, treatment planning, or survival analysis; no real-time hospital deployment or PACS integration; no mobile apps or IoT devices; no clinical trials with real patients; no automated medication or treatment recommendations | p. 9, Sec. 8, Not Included in this research | Hard negative boundaries; prohibit scope creep and keep any conditional defense web demo strictly research-only |
| RF16 | Preliminary problem/novelty claims: asserts existing studies emphasize accuracy over interpretability, operate as black-box systems, suffer from limited/imbalanced/low-diversity datasets, and states *"most previous research does not integrate Explainable Artificial Intelligence (XAI) techniques into the diagnostic process"* | p. 5, Sec. 2; pp. 7–8, Sec. 3–4 | Treat strictly as a **provisional hypothesis to test and potentially refine**—especially because CNN + vanilla Grad-CAM in mammography is already extensively published (UD03) |
| RF17 | Table 1.1 summarizes 10 prior works (SL 1–10) with a duplicated caption string (`1.1 Comparison between Existing WorksTable 1.1:...`); multiple rows involve non-mammogram data (BreakHis histopathology SL 2; Histopathology SL 5 & SL 10; Wisconsin tabular dataset SL 6–8) or review/survey articles (SL 3, SL 4, Ref [5]) | p. 6, Table 1.1 | Non-mammogram and survey entries cannot serve as direct numerical superiority benchmarks for mammography classification |
| RF18 | Table 1.1 and References `[1]`–`[12]` anomalies: printed citation numbers for SL 5–10 were omitted in printing and inserted by hand in ink (`[5]`–`[10]`, causing OCR corruption in text extractions); SL 10 cites "Hassan et al. [10]" (EfficientNet + CNN, Histopathology) whereas printed Ref [10] on p. 10 is D. Bazazeh & R. Shubair (2016) (ML comparison); SL 5 cites Nahid et al. [5] as CNN 97% whereas Ref [5] is a 2017 survey; Ref [9] omits publication venue; Refs [11] (WHO 2024) and [12] (ACS 2024) lack bracketed in-text citations | p. 6, Table 1.1; p. 10, Sec. 9 References | Treat `[1]`–`[12]` strictly as unverified seed leads; audit every original source and quarantine mismatches under UD04 |
| RF19 | Datasets named in Table 1.1 SL 4 (MIAS, DDSM, INbreast) appear only inside the summary of Rautela et al. [4] | p. 6, Table 1.1 SL 4 | Not selected, downloaded, or approved datasets; actual dataset choice, sample counts, and split ratios remain unresolved (UD05, UD11) |
| RF20 | Feedback form on Page 11: Supervisor's Feedback comment lines 1, 2, and 3 are completely blank (no written feedback comments); a handwritten signature (matching the p. 1 supervisor signature) appears on `Examiner's Signature:` and handwritten date `15/8/26` on `Date:` | p. 11, Supervisor's Feedback form | Zero substantive feedback is documented in the PDF; never invent examiner comments; confirm separately under UD01 whether verbal/written comments exist |

## 1.3 Binding scope and exclusions

**In scope:** Collection, licensing/ethics verification, and quality auditing of publicly available 2D mammogram image datasets (primary development/internal-test benchmark plus an optional independent external-validation dataset under UD05); diagnostic label provenance verification (Benign vs Malignant) and available lesion ROI-mask alignment auditing; patient-level connected-component leakage-safe splitting; mammography preprocessing and radiographically valid training-only augmentation; controlled transfer learning benchmarking across the approved pre-trained CNN roster (plus any supervisor-ratified Q1 architectural/loss/preprocessing comparison); mandatory Grad-CAM integration and approved Q1 XAI comparators with quantitative faithfulness, sanity, localization, and stability audits; Q1 classification, probability calibration, paired statistical testing, subgroup/error analysis, and bounded blinded qualitative clinical-advisor XAI review; CLAIM/TRIPOD+AI reproducibility auditing; a local research CAD prototype; FYDP thesis and Q1 journal manuscript preparation; and a **conditional** hosted web showcase of the frozen prototype for the FYDP defense (gated by UD25; governed by [Section 8.3](#os-08-3)).

**Outside the present approved study (binding exclusions from `RF15`):**
- Detection or classification using MRI, CT Scan, Ultrasound, Digital Breast Tomosynthesis (3D DBT) as primary task, or Histopathology/WSI images (such modalities may appear only as explicitly separated contextual literature).
- Prediction of cancer staging (TNM), molecular subtypes, treatment planning, chemotherapy response, or patient survival analysis.
- Real-time hospital deployment, clinical workstation integration, or PACS/HL7/DICOM-server integration.
- Development of mobile applications (Android/iOS) or IoT-enabled healthcare devices.
- Prospective or interventional clinical trials involving real patients.
- Automated recommendation of medications, biopsies, or treatment procedures.

**Epistemic and clinical boundaries:** Model output probabilities are statistical estimates conditional on retrospective public datasets, **not** definitive histopathologic diagnoses. A Benign prediction never certifies absence of cancer, and an attractive Grad-CAM heatmap never proves causal medical reasoning without quantitative faithfulness, sanity verification, and qualified radiologist review. Any conditional defense web showcase (Section 8.3) operates strictly as a non-clinical research demonstration with a persistent research-only disclaimer, honoring Section 8's exclusion of hospital deployment and clinical trials.

## 1.4 Objectives and candidate research questions

The six report objectives (`RF12`) are preserved as **O1–O6** and translated into Q1-auditable operational criteria (**PLANNING RECOMMENDATION**):

| Objective (`RF12`) | Operational Q1 interpretation (**PLANNING RECOMMENDATION**) | Required verification evidence |
|---|---|---|
| **O1:** Develop an explainable DL framework for early breast cancer detection using mammogram images | Construct an end-to-end, reproducible, leakage-controlled 2D mammogram classification + XAI pipeline linking immutable data releases to verified predictions and visual explanations | Versioned code (`src/bc_xai/`), locked environments, release manifests, model/XAI cards, CLAIM/TRIPOD+AI audit |
| **O2:** Preprocess mammogram images through resizing, normalization, and data augmentation | Implement deterministic, bit-depth-aware, artifact-checked mammogram preprocessing (fitted on training only where data-dependent) and radiographically valid training-only augmentation, testing enhancements (e.g., CLAHE) via controlled ablation rather than assuming benefit | `PP####` specs/configs, raw hash invariance, visual QC overlays, ablation records |
| **O3:** Train and compare multiple pre-trained DL architectures (VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3, MobileNetV2, etc.) using transfer learning | Resolve the candidate architecture discrepancy (UD13) and benchmark all approved CNN families (and optional Q1 modern baselines) under matched patient splits, transfer learning schedules, compute budgets, and multi-seed policy | `EXP####` configs, training logs, checkpoints (`CKPT####`), `MODEL####` cards, multi-seed tables, efficiency profiles |
| **O4:** Evaluate performance using Accuracy, Precision, Recall, F1-score, AUC-ROC, Confusion Matrix, and identify best architecture | Report all 6 required metrics plus Q1 medical-AI standards (Specificity, PR-AUC, Balanced Accuracy/MCC, sensitivity-anchored operating points, calibration, clustered bootstrap 95% CIs, DeLong/McNemar paired tests) on validation-selected frozen models across locked internal and external test cohorts | `EVAL####` prediction/coverage ledgers, `STAT####` paired tests, validation-only `freeze.md` |
| **O5:** Integrate XAI techniques (Grad-CAM and approved comparators) to generate visual heatmaps highlighting suspicious regions | Generate target-layer-documented Grad-CAM (and approved comparator) heatmaps and rigorously evaluate quantitative faithfulness (Deletion/Insertion/ROAD), Adebayo sanity checks, ROI-mask localization (Pointing Game/EBPG/IoU), stability, and bounded blinded radiologist alignment | `XAIP####` protocol, `XAIA####` quantitative/qualitative audit reports, disclosure-reviewed example plates |
| **O6:** Develop a reliable and interpretable CAD framework supporting radiologists | Package the frozen validation-selected inference + Grad-CAM pipeline into a documented local research CAD prototype (and conditional defense web showcase if UD25 passes) with explicit uncertainty, failure taxonomy, and non-clinical boundaries | Local CAD prototype guide, error/subgroup taxonomy (`G13`), reproducibility audit (`G14`), conditional `DEPLOY####` (`G17`) |

**Overarching report question (`RF11`):** *"Can an Explainable Deep Learning framework using transfer learning and mammogram images accurately detect early breast cancer while providing interpretable visual explanations that enhance clinicians' trust and diagnostic decision-making?"*

**Candidate operational Q1 research questions (PLANNING RECOMMENDATION; awaiting G03 ratification at STEP-009):**
- **RQ1 (Diagnostic discrimination & calibration):** Under strict patient-level leakage control, how do the approved transfer learning CNN architectures compare in Benign vs Malignant classification performance (Accuracy, Precision, Recall/Sensitivity, Specificity, F1-score, AUC-ROC, PR-AUC, Confusion Matrix), probability calibration (ECE, Brier score), and computational efficiency on the locked internal test cohort?
- **RQ2 (Cross-dataset generalization & subgroup robustness):** How well do the validation-selected architectures generalize zero-shot to an independent external public mammogram cohort (if adopted under UD05) and across clinically critical subgroups (breast density BI-RADS A–D, mass vs calcification, CC vs MLO views)?
- **RQ3 (Quantitative XAI faithfulness, sanity, localization & clinical alignment):** Do Grad-CAM (and any adopted XAI comparators) pass model/data randomization sanity checks, achieve higher perturbation faithfulness and lesion-ROI localization alignment across architectures, maintain explanation stability across seeds/perturbations, and align with blinded radiologist/clinical-advisor visual review?
- **RQ4 (Controlled methodological ablation):** What is the controlled effect of a prospectively defined preprocessing, imbalance-handling, fine-tuning, or architectural/attention factor on validation discrimination, calibration, and XAI faithfulness?

These candidate RQs are planning proposals, not report quotations. Final RQs receive stable IDs at G03 and must never presuppose favorable outcomes or unproven clinical-trust gains.

## 1.5 Research principles and medical AI ethics

1. **Protocol before compute:** Ratify data, label, split, training, XAI, and statistical protocols before touching held-out data or spending full compute.
2. **End-to-end lineage:** Every reported metric, p-value, curve, and Grad-CAM plate must trace via cryptographic hashes to raw dataset, verified labels, split manifest, preprocessing state, code commit, config, and model checkpoint.
3. **Zero selective omission:** Preserve all failed, diverged, OOM-aborted, negative-ablation, and low-faithfulness runs; negative or null findings are valid scientific evidence.
4. **Raw immutability:** Acquired mammogram archives and original DICOM/image files are read-only; all corrections or crops emit versioned derivatives.
5. **Strict test custody:** Validation drives architecture/hyperparameter/threshold/calibration selection; internal held-out test and external validation cohorts remain sealed until `G11` freeze.
6. **Patient privacy across every artifact:** Public mammogram datasets still require auditing for burned-in pixel PHI, DICOM header identifiers, institution watermarks, and identifying filenames before sharing figures or web samples.
7. **Independent rights verification:** Verify dataset licenses, institutional ethics/waiver determinations, third-party code licenses, and pretrained-weight terms independently—public downloadability never implies unrestricted redistribution or clinical use.
8. **Epistemic honesty:** Never fabricate dataset counts, hyperparameters, citation verifications, radiologist scores, p-values, or gate PASS states. Record `not reported`, `unknown`, or `Unresolved / Human Decision Required`.
9. **Validity vs performance:** A leakage-free, sanity-checked experiment with modest AUC or imperfect XAI localization is scientifically complete and publishable when honestly analyzed; a leaky high-AUC experiment is scientifically invalid.
10. **Human clinical and supervisory authority:** Automated tools and AI assistants never replace qualified breast radiology judgment, institutional ethics decisions, or supervisor sign-off.

Confirm DIU institutional ethics/waiver requirements for secondary research on de-identified public medical datasets before downloading restricted/controlled-access repositories (such as INbreast, VinDr-Mammo, or TCIA-hosted CBIS-DDSM/CMMD). Keep any patient-level source linkage keys segregated from shareable repository metadata; analytical manifests use pseudonymous `PatientGroupID` tokens.

## 1.6 Unresolved decision register at initialization

Every entry below is **Unresolved / Human Decision Required**. The canonical future ledger is `01_Project_Management/decisions.csv`, backed by detailed rationales in `01_Project_Management/decision_log/DEC####.md`. Decisions remain open until their blocking milestone; STEP-001 assigns owners and deadlines rather than guessing scientific values prematurely.

| ID | Decision / missing evidence | Owner role | Resolve before | Required resolution evidence |
|---|---|---|---|---|
| UD01 | Confirm scope interpretation, named operational leads, and whether any separate verbal/written title-defense feedback exists beyond blank lines on p. 11 | Researchers + Supervisor | G01 / STEP-001 | Signed/dated scope memo; actual feedback or explicit confirmation none exists |
| UD02 | Target Q1 journal shortlist, FYDP thesis format/deadlines, authorship order, and dual-track submission obligations | Researchers + Supervisor | Preliminary G01/G03; finalized STEP-040 & G15 | Institutional thesis guide, candidate Q1 journal Aims & Scope, author agreement |
| UD03 | PRISMA literature search databases, date cutoff, eligibility rules, and Q1 novelty positioning strategy if the broad "lack of XAI" hypothesis (`RF16`) is refuted or saturated | Literature Lead + Supervisor | G03 / STEP-004 & STEP-009 | Approved search protocol and supervisor-ratified Q1 contribution framing |
| UD04 | Verification and remediation of Table 1.1 & Ref `[1]`–`[12]` anomalies (handwritten brackets `[5]`–`[10]`, SL 10 Hassan vs Bazazeh/Shubair mismatch, SL 5 survey mismatch, Ref [9] missing venue, uncited Refs [11]–[12], non-mammogram comparator quarantine) | Literature Lead | G03 / STEP-007 & STEP-009 | Original publisher metadata checks; verified bibliography and quarantined mismatches |
| UD05 | Selection of primary public 2D mammogram dataset(s) (evaluating candidates such as CBIS-DDSM, INbreast, VinDr-Mammo, CMMD, MIAS, Mini-DDSM, RSNA) and independent external cross-dataset validation cohort (Q1 standard) | Data Lead + Supervisor | G04 / STEP-010 & STEP-013 | Evidence-backed candidate matrix, original provenance, measured counts |
| UD06 | Dataset licenses, DUA/access approvals (e.g., TCIA/PhysioNet/institutional portals), ethics/waiver determination, figure-disclosure permissions, and storage custody | Ethics Authority + Data Steward | Before acquisition (STEP-011); G04 | Written license/DUA terms and institutional ethics/waiver record |
| UD07 | Image-classification paradigm: Full-Field Digital Mammogram (FFDM) / whole-breast image vs lesion-level ROI/patch classification (or explicit dual-track design), plus mass vs calcification treatment | Researchers + Radiologist Advisor + Supervisor | G05 / STEP-014 | Written paradigm decision with clinical/methodological rationale; zero silent mixing |
| UD08 | Binary ground-truth provenance policy: biopsy/pathology-confirmed Benign vs Malignant vs BI-RADS-derived labels, and explicit inclusion/exclusion policy for Normal/Negative (BI-RADS 1) and unconfirmed findings | Radiologist Advisor + Supervisor | G05 / STEP-014 & STEP-015 | Approved `label_mask_protocol` defining label mapping and exclusions |
| UD09 | Lesion/ROI ground-truth mask availability, alignment verification rules, and acceptance criteria for quantitative XAI localization evaluation | Data Lead + Radiologist Advisor | G05 / STEP-015; G06 / STEP-018 | Verified mask inventory, overlay audit sample, acceptance thresholds |
| UD10 | Connected-component grouping keys (`PatientID`, laterality, LCC/RCC/LMLO/RMLO views, repeat exams, same-patient ROIs, exact/near duplicates) and conservative fallback if patient IDs are incomplete | Data Steward + Supervisor | G07 / STEP-020 | Audited grouping graph, duplicate check, explicit residual-leakage statement |
| UD11 | Leakage-safe split design: stratified group train/val/test ratios vs nested/repeated group K-fold CV, seed, stratification factors (class, density, view, abnormality), and external-set isolation (no split ratio exists in report) | Researchers + Supervisor | G07 / STEP-020 | Deterministic `SPLIT####` manifest, actual patient/image counts, supervisor sign-off |
| UD12 | Mammography preprocessing & augmentation policy: DICOM/16-bit scaling, background/pectoral-muscle/text-marker handling, aspect-ratio & resolution(s), CLAHE as testable ablation vs baseline, normalization stats, and radiographically valid training-only augmentations | Implementer + Radiologist Advisor + Supervisor | G08 / STEP-019 & STEP-021 | `PP####` spec, training-only fit proof, radiologist visual QC |
| UD13 | Final transfer learning architecture roster resolving `RF07` discrepancy (5 vs 6 vs 7 CNNs across report sections), library/implementation pins, pretrained weight licenses, and optional Q1 modern baseline(s) (e.g., ConvNeXt/Swin/ViT) or justified architectural/attention contribution | Model Lead + Supervisor | G09 / STEP-022 | Candidate comparison (`06_Models/candidates.csv`), baseline plan, `DEC####` |
| UD14 | Compute platform, GPU/CPU hardware, DL/XAI framework (PyTorch/timm vs TensorFlow/Keras), two-phase environment locks (`environment/data/`, `environment/model/`), storage tiers, backups, and Git remote controls | Researchers + Institution | G02 (storage & data env); G09 (model env) | Feasibility/access decision and smoke-tested dependency locks |
| UD15 | Training protocol: two-stage fine-tuning schedule (frozen vs unfrozen), class-imbalance handling (class weights/focal loss/training-only sampling), optimizer, LR schedule, batch size, epochs, early stopping, multi-seed count, and validation selection metric | Model Lead + Supervisor | G09 / STEP-024 & STEP-026 | Approved `experiment_plan.md` and validated executable YAML schema |
| UD16 | XAI method suite and architecture-specific target convolutional layer map: mandatory Grad-CAM baseline plus adoption/non-adoption of Grad-CAM++, Score-CAM, LayerCAM, Integrated Gradients, Guided Backprop, LIME, or SHAP | XAI Lead + Supervisor | G05 / STEP-015; frozen at G09 & G11 | Approved `XAIP####` protocol with layer map and implementation pins |
| UD17 | Quantitative XAI evaluation metrics: faithfulness (Deletion AUC, Insertion AUC, ROAD), Adebayo model/data randomization sanity checks, ROI-mask localization (Pointing Game, EBPG, thresholded IoU/Dice), and seed/perturbation stability | XAI Lead + Evaluation Lead + Supervisor | G05 / STEP-015; frozen at G11 / STEP-032 | Prospective XAI metric specification, perturbation baseline rules, unit tests |
| UD18 | Bounded qualitative radiologist/clinical-advisor XAI review protocol: stratified blinded sample (TP/TN/FP/FN), de-identification verification, scoring rubric, and strict separation from excluded clinical trials | Radiologist Advisor + Supervisor | G05 / STEP-015; executed STEP-037 / G13 | Approved blinded rubric, named reviewer credentials, non-trial scope statement |
| UD19 | Classification, threshold, and calibration protocol: 6 required report metrics plus Q1 metrics (Specificity, PR-AUC, Balanced Accuracy, MCC, Specificity at 90%/95% Sensitivity), validation-only threshold rule (e.g., Youden's J or clinical sensitivity target), and calibration (ECE, Brier, reliability diagrams, validation-only temperature/Platt scaling) | Evaluation Lead + Supervisor | G09 / STEP-024; frozen at G11 / STEP-032 | Frozen `09_Evaluation/protocol.md` and tested evaluator code |
| UD20 | Statistical inference & subgroup plan: patient-clustered bootstrap 95% CIs, DeLong paired AUC test, McNemar paired decision test, Holm-Bonferroni correction, efficiency profiling (params/FLOPs/latency), and stratified subgroups (BI-RADS density A–D, mass vs calcification, CC vs MLO, external cohort) | Evaluation Lead + Supervisor | G09 / STEP-024; frozen at G11 / STEP-032 | Prospective statistical analysis plan in `09_Evaluation/protocol.md` |
| UD21 | Optional numeric scientific success criteria (if explicitly required by supervisor), separated cleanly from methodological gate PASS/FAIL | Supervisor + Researchers | G09 / STEP-024 | Written supervisor rationale grounded in dataset difficulty |
| UD22 | Local research CAD inference + Grad-CAM prototype interface (CLI/script/minimal local UI), output schema, and disclosure-reviewed sample inputs | Implementer + Radiologist Advisor | STEP-038 | Interface decision, error contract, sample disclosure review |
| UD23 | Reproducibility audit level (inference + XAI replay vs full retraining), agreement tolerances, CLAIM & TRIPOD+AI checklists, and data/code/weight availability statements | Reproduction Reviewer + Supervisor | G14 / STEP-039 | Approved reproducibility scope, tolerance table, completed checklists |
| UD24 | Post-project code license, archival tiers (public vs restricted), artifact host, retention policy, and post-project ownership | Researchers + Data Steward + Supervisor | STEP-046; permissions before upload | Tiered release agreement and tested restoration evidence |
| UD25 | Conditional FYDP Defense Hosted Web Demonstration: confirm whether a live Grad-CAM CAD web showcase is requested for the defense, defense date/window, and live vs offline-fallback expectations (research showcase only, honoring Section 8 exclusions) | Researchers + Supervisor | STEP-001 (request) & STEP-048 (confirm/dispose) | Written supervisor confirmation and defense date, or approved non-adoption disposition |
| UD26 | Conditional Web Demo hosting platform, CPU/GPU tier (for CNN + Grad-CAM latency), web framework, budget, team-owned account, region, HTTPS URL, and containerization | Deployment Owner + Supervisor | STEP-048 (if UD25 adopted); G17 | Platform comparison against model/Grad-CAM memory & latency + optional spike |
| UD27 | Conditional Web Demo access control, input policy (curated disclosure-reviewed mammogram samples only vs in-memory non-stored uploads), format/size limits, scrubbed logs, retention, and mandatory research-only disclaimer | Deployment Owner + Data Steward + Radiologist Advisor | STEP-049 (if UD25 adopted); G17 | Approved `16_Web_Demo/web_policy.md` and disclosure review of every bundled sample |
| UD28 | Conditional Web Demo post-defense lifecycle (keep, freeze, or take down), ongoing cost/ownership, weight hosting license compliance, and DEPLOY archive handover | Deployment Owner + Supervisor + Data Steward | STEP-050 (if UD25 adopted); aligned with UD24 at STEP-046 | Recorded post-defense disposition and weight-hosting license check |

New uncertainties discovered during execution receive sequential IDs (`UD29`, etc.) in `decisions.csv`. The companion blueprint references this register exclusively.

<a id="os-02"></a>
# 2. Repository architecture and folder contracts

## 2.1 Proposed repository layout

Only `BC_XAI_RESEARCH_OPERATING_SYSTEM.md` and `BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md` are created during this planning phase. The directory tree below is a **future operational contract** to be instantiated in STEP-002 and STEP-003. Listed paths do **not** assert that files or folders currently exist.

```text
workspace/
  BC_XAI_RESEARCH_OPERATING_SYSTEM.md
  BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md
  README.md
  CHANGELOG.md
  CONTRIBUTING.md
  LICENSE                                    # only after UD24 license approval
  .gitignore
  .gitattributes
  environment/
    data/                                    # Phase 1 minimal data/DICOM/QC/split lock (STEP-002)
    model/                                   # Phase 2 DL/CNN/XAI/statistics lock (STEP-023)
  src/bc_xai/                                # reusable core modules; thin entry points
  tests/                                     # unit/integration tests on synthetic or permitted fixtures
  01_Project_Management/
  02_Literature/
  03_Datasets/
  04_Labels_XAI_Governance/
  05_Preprocessing/
  06_Models/
  07_Experiments/
  08_Checkpoints/
  09_Evaluation/
  10_Figures_Tables/
  11_Writing/
  12_Documentation/
  13_Automation/
  14_Templates_Prompts/
  15_Archive/
  web/                                       # conditional thin Grad-CAM web app + container (S16)
  16_Web_Demo/                               # conditional DEPLOY registry, policies, parity, runbook (S16)
```

## 2.2 Folder contracts

Every materialized domain folder includes a `README.md` (`T01`) defining purpose, owner, inputs, allowed contents, outputs, sensitivity tier, workflow commands, and links to this handbook. Never scaffold unused libraries merely to populate folders.

| Home | Writes / reads | Allowed contents and contract | Forbidden / validation |
|---|---|---|---|
| `environment/` | Implementer / all executors | `data/` (Phase 1 minimal QC/DICOM/split lock + `verification.md`) and `model/` (Phase 2 DL/XAI/stat lock + `versions.md` + hardware record) | No speculative untested pins; no credentials or tokens |
| `src/bc_xai/` | Implementer / pipeline users | Modular DICOM/image QC, label/mask verifiers, connected-component splitters, preprocessing, transfer learning trainers, XAI generators/metrics, calibration/statistical evaluators, local CAD inference | No raw mammograms, model weights, hardcoded private paths, or hidden hyperparameters |
| `tests/` | Implementer / reviewers | Schema, DICOM/bit-depth, patient-grouping, preprocessing leakage, metric, DeLong/McNemar, XAI faithfulness/sanity, checkpoint, and inference parity tests on synthetic/permitted fixtures | No unlicensed, unreviewed, or PHI-bearing patient fixtures |
| `01_Project_Management/` | Researchers / all roles | `decisions.csv`, `decision_log/`, `risk_register.csv`, `gates.csv`, `reviews/`, `diary/`, `meetings/`, `scope.md`, `dashboard.md`, `timeline.md` | No fabricated approvals or raw patient linkage tables |
| `02_Literature/` | Literature lead / modeling & writing | `searches/`, `papers.csv`, `screening.csv`, `gaps.csv`, `gap_notes/`, `claims.csv`, `claim_notes/`, `summaries/`, `references.bib`, `synthesis.md`, `research_questions.md`, permitted `papers/` | No redistribution of copyrighted PDFs; no unread summaries |
| `03_Datasets/` | Data steward / preprocessing & modeling | `candidates.csv`, `datasets.csv`, `releases.csv`, `licenses/`, restricted `raw/`, `manifests/`, `reports/`, `splits/` | Raw bytes immutable & excluded from Git; patient-ID linkage segregated from shareable metadata |
| `04_Labels_XAI_Governance/` | Data & XAI leads / modeling & evaluation | `label_registry.csv`, `xai_protocol_registry.csv`, `protocols/`, `xai_protocols/`, `reviews/`, `adjudications/`, restricted verified label/ROI-mask manifests | No silent BI-RADS/pathology relabeling; no post-hoc XAI target-layer tuning |
| `05_Preprocessing/` | Implementer / training & inference | `preprocessing_registry.csv`, `specs/`, versioned `configs/`, `reports/`; restricted `processed/` and serialized training-only fitted states | Reusable logic belongs in `src/bc_xai/`; no raw overwrites or val/test-fitted statistics |
| `06_Models/` | Model lead / evaluation & inference | `candidates.csv`, `model_registry.csv`, `baseline_plan.md`, `cards/`; pointers/hashes to approved pretrained & trained weights | No anonymous checkpoints or unverified pretrained weight provenance |
| `07_Experiments/` | Experiment lead / evaluation & writing | `experiment_registry.csv`, `experiment_plan.md`, `EXP####/config.yaml`, `run_manifest.json`, logs, curves, observations, failure reports | Never edit a launched config or merge distinct runs/seeds into one undocumented record |
| `08_Checkpoints/` | Experiment lead / recovery & inference | `checkpoint_registry.csv`, `checkpoint_policy.md`, `manifests/`, SHA-256 checksums, restricted artifact-tier pointers | Weight binaries belong in approved artifact storage, never ordinary Git |
| `09_Evaluation/` | Evaluation & XAI leads / writing | `evaluation_registry.csv`, `xai_audit_registry.csv`, `statistical_comparisons.csv`, `protocol.md`, `freeze.md`, `EVAL####/` predictions, calibration, stats, XAI audits, subgroup/error reviews | Sensitive outputs/heatmaps remain restricted; zero test-driven tuning |
| `10_Figures_Tables/` | Analysts / writing | `assets.csv`, `specs/`, `data/`, `rendered/`, captions; exact generation script commands and hashes | No hand-edited plot values, unlabeled axes, or disclosure-unreviewed mammogram plates |
| `11_Writing/` | Authors / reviewers | `writing_registry.csv`, `writing_plan.md`, `thesis/`, `paper/`, `reviews/`, submission receipts/dispositions; bibliography linked to canonical `02_Literature/references.bib` | No unsupported novelty/clinical claims; no competing citation databases |
| `12_Documentation/` | Implementer & researchers / auditors | `installation.md`, `pipeline.md`, `prototype_guide.md`, `web_demo_guide.md`, `reproduce.md`, `reproducibility_audit.md`, `claim_tripod_checklist.md`, data-access instructions | No duplicated scientific policy or unverified reproducibility claims |
| `13_Automation/` | Implementer / all roles | Thin CLI scripts for registry/hash verification, experiment orchestration, figure rendering, and export checks | No hidden scientific logic or automated gate approval |
| `14_Templates_Prompts/` | Researchers / all roles | Blank versioned templates (`T01–T35`), planning/implementation/review prompts, template changelog | Filled instances live in owning domain folders; zero patient data or secrets |
| `15_Archive/` | Release owner / authorized readers | Immutable release snapshots, `archive_manifest.csv`, `ARCH####.md`, submission receipts, retention & restoration proofs | No active drafts or overwritten archived snapshots |
| `web/` | Deployment owner / demo users | Conditional thin web UI/API calling frozen `src/bc_xai/` CAD+Grad-CAM inference entry point, container config (`Dockerfile`), lockfile, web tests (S16) | No reimplemented preprocessing, thresholds, calibration, or Grad-CAM logic; no weights/images/secrets in Git |
| `16_Web_Demo/` | Deployment owner / supervisor & examiners | Conditional `deployment_registry.csv`, `DEPLOY####.md`, `platform_decision.md`, `web_policy.md`, `hosted_model.md`, `samples_manifest.csv`, `parity_checks/`, `smoke_checks/`, `demo_runbook.md` (S16) | No stored uploads unless UD27 explicitly permits; no demo output presented as held-out evaluation evidence |

## 2.3 Artifact placement and integration contracts

All reusable scientific code lives in `src/bc_xai/`. Domain folders hold specifications, resolved configurations, audit reports, and registries. Notebooks are permitted only as thin, non-authoritative callers inside `07_Experiments/` or `09_Evaluation/`—never as the primary source of preprocessing, training, XAI computation, or metric logic. The conditional hosted web demo (`web/`) imports the exact frozen `src/bc_xai/` inference + Grad-CAM entry point from STEP-038 without forking code.

Maintain this unbroken cryptographic lineage chain:

```text
Source Archive → DS#### (immutable raw) → LBL#### (verified labels & ROI masks) + XAIP#### (XAI protocol)
→ SPLIT#### (patient-level connected-component split) → PP#### (training-only fitted preprocessing)
→ REL#### (immutable prepared release) → EXP#### / RUN#### → CKPT#### → MODEL####
→ EVAL#### + XAIA#### + STAT#### → FIG#### / TAB#### → CLAIM#### → WR#### → ARCH####
                                  └─(conditional S16)→ DEPLOY#### (parity-checked thin web layer)
```

Each pipeline stage consumes explicit input manifests and emits an output manifest binding parent IDs, SHA-256 hashes, image/mask dimensions, class/label maps, code commit, and environment lock hash. Downstream consumers must fail loudly on any hash, label-map, or split mismatch. Artifact pointers record immutable storage locations and SHA-256 digests—never expiring pre-signed URLs as sole locators.

<a id="os-03"></a>
# 3. Literature and Q1 research-question workflow

## 3.1 PRISMA-style systematic search design

**PLANNING RECOMMENDATION:** Conduct a reproducible, PRISMA-aligned systematic literature search spanning both biomedical/radiology and computer-vision/engineering databases. Candidate databases (subject to institutional availability recorded under `UD03`) include **PubMed/MEDLINE**, **IEEE Xplore**, **Scopus**, **Web of Science**, **ScienceDirect**, **SpringerLink**, and **arXiv/medRxiv** (with preprints explicitly flagged as non-peer-reviewed). Document exact database access limits rather than implying exhaustive coverage. Never use arbitrary paper quotas or raw citation counts as quality filters.

Seed search syntax (adapt and log verbatim per database):

```text
(mammogram OR mammography OR FFDM OR "breast cancer screening" OR "breast lesion")
AND ("deep learning" OR "convolutional neural network" OR CNN OR "transfer learning"
     OR ResNet OR DenseNet OR EfficientNet OR VGG OR Inception OR MobileNet
     OR "vision transformer" OR ConvNeXt)
AND ("explainable AI" OR XAI OR "Grad-CAM" OR "Grad-CAM++" OR "Score-CAM"
     OR "Integrated Gradients" OR SHAP OR LIME OR saliency OR interpretability
     OR faithfulness OR "pointing game")
```

Run complementary searches specifically targeting: (a) **existing XAI + mammography benchmarks and faithfulness/localization evaluations** (to actively challenge `RF16`); (b) **cross-dataset / external validation and patient-level leakage in mammography DL** (CBIS-DDSM, INbreast, VinDr-Mammo, CMMD, RSNA, MIAS); and (c) **probability calibration and clinical operating-point reporting in screening mammography AI**. Log database name, exact Boolean string, execution date, time window, filters, retrieved record count, export file hash, deduplication rule, and full-text exclusion reasons.

## 3.2 Intake, screening, extraction, and report anomaly remediation

1. **Pre-summary registration & deduplication:** Assign `P####` in `02_Literature/papers.csv` before summarizing. Deduplicate by DOI, normalized title, and preprint-to-journal links; link duplicate versions (`DuplicateOf`) so one study is never counted twice.
2. **Two-stage PRISMA screening:** Apply prospectively approved eligibility criteria at title/abstract and full-text stages in `02_Literature/screening.csv`. Record one explicit exclusion code per full-text exclusion. Strictly separate **direct 2D mammogram classification + XAI studies** from contextual work (non-XAI mammography DL, non-mammogram breast imaging such as histopathology/BreakHis/ultrasound/MRI, tabular Wisconsin benchmarks, and review/survey articles).
3. **Mandatory audit of report seed references (`RF17–RF18`, `UD04`):** Register report references `[1]`–`[12]` (p. 10) as unverified seed leads (`ReportRef`) and independently retrieve publisher records and full text to resolve every documented anomaly:
   - Verify handwritten Table 1.1 citations `[5]`–`[10]` against printed Reference entries `[5]`–`[10]` on p. 10.
   - Quarantine **SL 10 ("Hassan et al. [10]", EfficientNet + CNN, Histopathology)** vs printed **Reference [10] (D. Bazazeh & R. Shubair, 2016)**; do not conflate them or cite an unverified hybrid entry.
   - Correct **SL 5 (Nahid et al. [5])** where Ref [5] is a 2017 survey rather than a standalone 97% CNN experiment.
   - Locate and verify complete publication metadata for **Ref [9] (Tiwari et al., 2020)**, which omits venue information in the report.
   - Verify exact primary sources for **Ref [11] (WHO 2024)** and **Ref [12] (American Cancer Society 2024)** and reconcile their missing bracketed in-text citations.
   - Quarantine non-mammogram rows (BreakHis histopathology SL 2; Histopathology SL 5, SL 10; Wisconsin tabular dataset SL 6–8) and review rows (SL 3, SL 4) from any direct mammography numerical comparison table.
4. **Structured methodological extraction (`T05`):** Read full methods, tables, figures, and supplements (never abstracts alone). Extract: dataset(s) and version; FFDM vs ROI/patch paradigm; label source (biopsy vs BI-RADS) and Normal-case handling; reported patient/exam/image counts; split level (patient vs image vs unknown) and leakage risk; external validation presence; model architectures & pretraining; preprocessing & augmentation; XAI method(s), target layers, and whether XAI was evaluated quantitatively (faithfulness, sanity checks, ROI-mask localization) or only via qualitative visual vignettes; classification & calibration metrics; statistical testing; code/weight availability; and limitations. Record `not reported` for omitted details—never infer from familiarity.
5. **Locator discipline & human reconciliation:** Every extracted numerical value carries an exact page/table/figure locator. Reconcile ambiguous extractions through human review and retain edit history.

## 3.3 Testing the report's novelty claim and framing a Q1 contribution

The title report (`RF16`) proposes that most prior breast cancer DL work focuses on accuracy without XAI, lacks interpretability, and suffers from limited/imbalanced mammogram datasets. For a Q1 journal, **training standard pre-trained CNNs + vanilla Grad-CAM on a single public mammogram dataset is already well-studied and generally insufficient as a standalone novelty claim**. Therefore, STEP-008 MUST explicitly test the report's gap hypotheses against counterevidence using `GAP####` records:

| Provisional report theme (`RF16`) | What systematic review must test | Q1-grade honest disposition & refinement pathway |
|---|---|---|
| **RG1:** Lack of XAI integration in breast cancer mammography DL | Prevalence of existing mammography + Grad-CAM / Grad-CAM++ / Score-CAM / SHAP / ViT-attention studies | Likely **narrowed or refuted** as an absolute absence; test whether existing studies lack *quantitative XAI faithfulness, sanity verification, and ROI-localization benchmarking* |
| **RG2:** Black-box trust & unverified visual heatmaps | Whether prior mammography XAI papers stop at cherry-picked qualitative overlays without Adebayo sanity checks, deletion/insertion faithfulness, or blinded clinical alignment | Testable Q1 gap: rigorous multi-architecture quantitative XAI validation + clinical alignment |
| **RG3:** Limited, imbalanced, single-center mammogram datasets & poor generalization | Prevalence of image-level splitting (patient leakage), FFDM/ROI conflation, and absence of external cross-dataset testing and probability calibration | Testable Q1 gap: strict connected-component patient-level evaluation + zero-shot external cohort + calibration & density/view subgroup analysis |
| **RG4:** Comparative transfer learning evaluation across CNN families | Whether prior architecture comparisons match patient splits, budgets, multi-seed variance, paired statistical tests (DeLong/McNemar), and efficiency/faithfulness trade-offs | Testable Q1 gap: controlled multi-seed, statistically paired accuracy–calibration–efficiency–XAI-faithfulness trade-off benchmark |

Classify every `GAP####` as `proposed`, `supported-within-search`, `narrowed`, `refuted`, or `unresolved` with explicit supporting and contradicting `P####` IDs. **If the broad novelty claim is refuted or saturated**, retain the approved title and scope (`RF01`, `RF14–RF15`) and ratify a **defensible Q1 scientific contribution** with the supervisor at G03—such as:
- A rigorous, leakage-controlled, multi-center (internal + external) benchmark quantifying the **diagnostic-accuracy vs calibration vs XAI-faithfulness/sanity/ROI-localization trade-off** across pre-trained CNN families (and an optional modern baseline), paired with blinded clinical-advisor visual alignment; and/or
- A well-justified, controlled methodological ablation (e.g., domain-specific preprocessing/artifact removal, imbalance-aware calibrated loss, multi-XAI ensemble/faithfulness comparison, or lightweight attention/fine-tuning refinement) within the approved transfer learning mammography scope.

## 3.4 Question approval and living review

At STEP-009, map each approved `RQ#` to O1–O6, verified `GAP####` records, dataset/mask requirements, experiment factors, quantitative classification/XAI/statistical metrics, and claim boundaries. G03 certifies methodological honesty, search reproducibility, anomaly remediation (`UD04`), and a defensible Q1 contribution—it does **not** require confirming every preliminary proposal gap. Re-run targeted literature updates prior to model selection (STEP-022) and prior to Q1 manuscript submission (STEP-045), logging exact search cutoff dates.

**Failure handling:** Quarantine unsupported novelty statements or unverified citations immediately, retrieve original publisher metadata lawfully, revise `synthesis.md`, preserve refuted hypotheses transparently, and reassess G03.

<a id="os-04"></a>
# 4. Mammogram dataset, label/ROI-mask audit, preprocessing, and leakage-safe split operating system

## 4.1 Dataset lifecycle, candidate discovery, and permissions

Follow this strict lifecycle:
`Candidate discovery (internal & external) → license/DUA & ethics determination → controlled raw intake → DICOM/image integrity & PHI/artifact QC → G04 dataset approval → label/ROI-mask provenance audit → G05–G06 verified label freeze → preprocessing specification → connected-component patient split (G07) → training-only preprocessing fit & immutable release (G08)`.

**Public mammogram datasets are candidates to discover and audit under `UD05`—never pre-selected or pre-claimed.** Candidate public collections that may be investigated during STEP-010 include (illustrative discovery leads only, with actual availability, license terms, and counts unverified until STEP-010–013): CBIS-DDSM (TCIA), INbreast, VinDr-Mammo (PhysioNet), CMMD (TCIA), MIAS / Mini-DDSM, and RSNA Screening Mammography Breast Cancer Detection dataset. Audit every candidate against:
1. True 2D mammography modality (FFDM vs digitized screen-film mammogram [SFM]); strictly exclude histopathology, ultrasound, MRI, and tabular datasets (`RF15`).
2. Original authoritative provenance vs third-party Kaggle/GitHub mirrors (never treat a repackaged mirror of DDSM/CBIS-DDSM as an independent external dataset!).
3. Exact license, Data Use Agreement (DUA), non-redistribution rules, and whether de-identified example figures may legally be published in a Q1 journal or bundled in a defense web demo (`UD06`, `UD27`).
4. Diagnostic ground-truth provenance (biopsy/histopathology confirmation vs BI-RADS radiological assessment), availability of Benign vs Malignant vs Normal/Negative labels, and availability of lesion ROI masks or bounding annotations for quantitative XAI localization (`UD07–UD09`).
5. Patient, exam, laterality (L/R), and view (CC/MLO) metadata completeness required for connected-component grouping (`UD10`), plus breast density (BI-RADS A–D) and abnormality subtype (mass vs calcification) metadata for Q1 subgroup analysis (`UD20`).

**External / Cross-Dataset Validation Track (PLANNING RECOMMENDATION — Q1 Standard):** Because single-center/single-device evaluation is a primary rejection trigger at Q1 medical imaging journals, STEP-010–013 must explicitly evaluate selecting an **independent secondary public mammogram dataset** (different acquisition center/vendor/modality family where feasible, zero patient/archive overlap with the primary cohort) reserved strictly for **zero-shot external validation** after `G11` freeze (`UD05`, `UD11`). If no lawful compatible external cohort is feasible, document the exact screening evidence and record single-cohort generalization as a prominent limitation.

## 4.2 Controlled intake, raw integrity, and mammography QC

1. Verify source URLs, portal DUA/license receipts, and original archive checksums; extract into read-only restricted storage `03_Datasets/raw/DS####/`. Never modify original DICOM, PGM, PNG, or CSV bytes.
2. Inventory every single file (including unreadable, corrupted, or excluded items) into `03_Datasets/manifests/DS####_images.csv` with pseudonymous `ImageID`, `PatientGroupID`, source-relative path (restricted if identifying), SHA-256 hash, modality/format, bit depth, pixel dimensions, photometric interpretation (`MONOCHROME1` vs `MONOCHROME2` for DICOM), laterality, view position (LCC, RCC, LMLO, RMLO), duplicate cluster ID, inclusion status, and exclusion code.
3. **Mammography-specific integrity & privacy QC (STEP-013):**
   - Check DICOM decoding, window/level tags, RescaleSlope/Intercept, inverted LUTs (`MONOCHROME1` black-background polarity inversions), 12-bit/16-bit vs 8-bit truncation, and empty/all-zero frames.
   - Inspect for **burned-in pixel PHI**, institution stamps, radiopaque view-marker tags (`LMLO`, `RCC`, `M`, lead markers), bright film borders, digitization scanners' black/white framing, pectoral muscle prominence, breast implants, biopsy clips, and motion blur.
   - Screen for exact byte duplicates and perceptual near-duplicates (e.g., identical scans re-exported across subfolders or paired full-image + crop exports).
   - Conduct both deterministic QC scripts and a stratified human/clinical-advisor visual sample. Never invent exclusion thresholds after observing model errors.
4. **Count reconciliation:** `Acquired = Retained + Excluded + Quarantined` at both image and patient levels. If patient IDs are missing or partially ambiguous in a candidate dataset, report patient counts honestly as `unknown` or `bounded`—never guess.

## 4.3 Diagnostic paradigm, ground-truth provenance, and ROI-mask verification

Before preprocessing or splitting, resolve two foundational mammography traps explicitly under `UD07–UD09` (governed further in [Section 6](#os-06) and Stages S07–S08):
- **FFDM / Whole-Breast vs ROI/Patch Paradigm (`UD07`):** Whole-breast mammogram classification preserves global breast parenchymal context and clinical realism but demands careful resolution/artifact handling; pre-cropped lesion ROI classification simplifies background noise but assumes an upstream lesion detector/localizer already exists and cannot be claimed as full-mammogram screening detection. Choose one primary paradigm (or an explicitly separated dual-track design) and never pool full mammograms and ROI crops into one unlabeled dataset.
- **Ground-Truth Label Provenance & Normal-Case Policy (`UD08`):** Distinguish pathology/biopsy-confirmed Benign vs Malignant cases (gold standard) from BI-RADS-derived proxy labels (e.g., BI-RADS 2/3 vs 4/5/6). Because `RF05` defines binary classification (**Benign** vs **Malignant**), decide prospectively how **Normal / Negative (BI-RADS 1)** mammograms and unconfirmed BI-RADS 0/3 cases are handled (e.g., excluded from Benign vs Malignant binary task with exact counts disclosed, or explicitly documented under a clinical mapping ratified by the radiologist advisor and supervisor—never silently relabeled without provenance).
- **Lesion / ROI Ground-Truth Mask Audit (`UD09`):** Where the selected dataset provides pixel-level lesion masks or bounding regions (e.g., CBIS-DDSM ROI masks, INbreast XML contours, VinDr-Mammo lesion boxes), audit mask-to-image dimension alignment, orientation polarity, coordinate conventions, and multi-lesion handling during S07–S08 so quantitative XAI localization metrics (Pointing Game, EBPG, Heatmap-ROI IoU/Dice) rest on verified geometry.

## 4.4 Mammography preprocessing and augmentation contract

The report mentions resizing, normalization, and data augmentation (`RF10`) without parameters. Every preprocessing version `PP####` records rationale, ordered operations, library versions, exact parameters, output dimensions/channels, deterministic vs stochastic behavior, fitted partition, and visual/numeric QC evidence (`UD12`).

**PLANNING RECOMMENDATION — Mammography-safe preprocessing discipline:**
1. **Bit-depth and photometric standardization:** Convert `MONOCHROME1` to consistent dark-background polarity; preserve dynamic range during 12/16-bit scaling (e.g., documented percentile/min-max or DICOM VOI LUT windowing) before 3-channel adaptation for ImageNet pre-trained CNNs.
2. **Artifact and background handling:** Explicitly evaluate and document breast-region foreground cropping, border/marker removal, and optional pectoral-muscle masking. Verify on a clinical-advisor visual sample that peripheral/axillary lesions near the chest wall or breast boundary are **never** clipped away.
3. **Aspect-ratio and target resolution:** Document resizing policy (aspect-ratio-preserving pad-and-resize vs direct resize) and exact target dimensions per CNN architecture (e.g., respecting InceptionV3 native geometry if distinct from 224×224 or higher-resolution mammography settings under `UD12`/`UD13`). Verify that subtle microcalcifications remain perceptible at the selected resolution.
4. **Contrast enhancement as a testable ablation:** Do **not** assume CLAHE or histogram equalization improves mammography classification or XAI faithfulness. Establish a clean, minimal baseline `PP####` first; treat CLAHE or artifact-suppression variants as controlled, pre-registered ablation factors (`EXP####`) compared on validation.
5. **Strict leakage isolation for fitting & augmentation:** Any dataset-level normalization statistics (mean/std if dataset-fitted rather than fixed ImageNet constants) or intensity scalers MUST be fitted exclusively on the **training partition** after `G07` split lock, serialized with SHA-256 checksum, and applied unchanged to validation, internal test, and external test cohorts. All stochastic data augmentations (e.g., radiographically valid horizontal flip with laterality awareness, small rotations, mild brightness/contrast jitter—avoiding anatomically destructive extreme warps or harsh cutoffs that erase microcalcifications) are **training-only** and applied on-the-fly after splitting. Never augment images prior to splitting!

## 4.5 Connected-component patient-level leakage-safe splitting

The title evaluation report specifies **no split ratio** (`RF19`). Never assume 70/15/15 or any other ratio as a report fact; resolve the exact partitioning design under `UD10–UD11`:

1. **Connected-component grouping BEFORE partitioning (`UD10`):** Build an undirected equivalence graph linking images that share ANY of: same `PatientID`, same clinical exam/study accession, bilateral laterality pair (LCC/RCC/LMLO/RMLO from the same patient), longitudinal repeat scans, multiple ROI crops derived from the same patient or mammogram, or exact/near-duplicate perceptual hash match. Extract connected components (`PatientGroupID`) and assign **entire connected components** atomically to exactly one partition. Zero patient, view, or duplicate leakage may cross train/validation/test boundaries.
2. **Split design choice (`UD11`):** Choose prospectively between (a) stratified group train/validation/held-out-test split (with explicit proportions, seed, and stratification across Benign/Malignant class and, where feasible, breast density/abnormality subtype), or (b) nested/repeated stratified group K-fold cross-validation plus a locked held-out test set. Record target vs actual patient counts, image counts, class balance, and subgroup support; never split a patient component to hit exact percentage targets.
3. **Auditing supplied benchmark splits:** If a dataset provides an official train/test split (e.g., CBIS-DDSM official split), **audit it first** for hidden patient/bilateral/crop overlap before trusting it. Document any overlap discovered and either enforce a corrected connected-component split (noting literature comparability impact) or report both with explicit overlap disclosure.
4. **Missing-metadata rule:** If a candidate dataset lacks reliable patient IDs, prioritize datasets with verifiable patient-level identifiers for Q1 publication. Where partial uncertainty persists, document exact residual independence limits transparently; `G07` never certifies patient-safe splitting without audited evidence.
5. **Sealed test custody:** Lock both the internal held-out test set and any independent external validation cohort immediately upon `G07` PASS. No hyperparameter search, threshold optimization, calibration fitting, CLAHE choice, or error-driven relabeling may observe test outputs before `G11` freeze.

## 4.6 Versioned dataset release (`REL####`) and change control

An immutable prepared release `REL####` binds `DS####`, `LBL####`, `SPLIT####`, `PP####` (including serialized training-fitted state hash), exact image/label/ROI-mask manifests, code commit, and environment hash (`environment/data/`). Never overwrite an existing `REL####`.

| Upstream change | Mandatory governance action |
|---|---|
| Label or ROI-mask correction | Emit new `LBL####` with affected `ImageID` list and clinical rationale; regenerate `REL####`; mark downstream `G06–G12` STALE |
| Patient grouping or split modification | Emit new `SPLIT####` and `REL####`; reassess `G07` onward; disclose any prior test exposure |
| Preprocessing or augmentation change | Emit new `PP####`/`REL####`; verify raw hash invariance & visual QC; treat as controlled `EXP####` comparison |
| Discovery of burned-in PHI or unauthorized record | Halt use immediately; quarantine in restricted storage; notify supervisor/custodian; issue remediated `DS`/`REL` and invalidate affected assets |

<a id="os-05"></a>
# 5. Transfer learning model benchmarking and experiment operating system

## 5.1 Architecture roster resolution and fair benchmarking invariants

The title report contains a documented discrepancy in candidate CNN architectures (`RF07`):
- Sec. 1 (p. 2): VGG16, ResNet50, DenseNet121, EfficientNet, InceptionV3
- Sec. 2 (p. 5): VGG16, ResNet50, DenseNet121, MobileNetV2, EfficientNet, InceptionV3, Xception
- Sec. 4 (p. 8): 5 models — VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3
- Sec. 6 Obj. 3 (p. 8): 6 models — VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3, MobileNetV2

At STEP-022 (`UD13`), formally resolve the exact benchmark roster rather than silently dropping or adding models. **PLANNING RECOMMENDATION for Q1 competitiveness:** include at minimum the full 6-model set from Objective 3 (VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3, MobileNetV2—plus Xception if resources permit) AND evaluate under `UD13` whether to include 1–2 modern Q1 reference architectures (e.g., ConvNeXt-Tiny/Small or Swin Transformer / ViT) or a justified domain-specific refinement (e.g., calibrated focal/class-balanced loss, multi-scale/attention head, or multi-view fusion if multi-view metadata exists) so the benchmark addresses contemporary Q1 reviewer expectations while preserving full alignment with Objective 3.

Record every candidate in `06_Models/candidates.csv` with exact framework/library name and version (e.g., `torchvision` / `timm` / `keras.applications` commit or release), exact pretrained weight tag & SHA-256, pretraining source dataset (e.g., ImageNet-1K), software and weight licenses, native input resolution, parameter count, FLOPs, and Grad-CAM target-layer compatibility. Never claim architectural novelty merely from fine-tuning an off-the-shelf backbone on mammograms.

**Fair benchmarking invariants (mandatory across all compared models):**
- Identical `REL####`, `LBL####`, `SPLIT####` patient partitions, and locked internal/external test cohorts.
- Matched transfer learning regime (e.g., Stage 1 frozen-backbone classification head warm-up + Stage 2 controlled unfrozen fine-tuning, or explicitly documented per-architecture schedule justified under `UD15`).
- Explicit, training-only class-imbalance handling (e.g., inverse-frequency class weights, focal loss, or stratified batch sampling—never oversampling before splitting).
- Matched hyperparameter search/tuning budget and identical multi-seed policy (e.g., 3 or 5 fixed random seeds decided under `UD15`) so seed variance is reported alongside point estimates.
- Identical validation selection criterion (e.g., validation AUC-ROC or PR-AUC decided prospectively under `UD15`) and identical evaluation/calibration/XAI code.
- If an architecture requires a distinct native resolution (e.g., 299×299 for InceptionV3 vs 224×224 or uniform 384×384/512×512), declare that difference explicitly and test whether resolution confounds architecture ranking.

## 5.2 Configuration contract

Every launched experiment `EXP####` requires a validated `config.yaml` (`T15`) with **zero null/placeholder executable values**, capturing both requested settings and effective runtime library defaults:
- **Identity:** `experiment_id`, `research_question_id`, `purpose`, `parent_comparison_id`, `source_commit`, `timestamp`, `approval_record`.
- **Data:** `release_id`, `dataset_id`, `label_release_id`, `split_id`, `preprocessing_id`, exact manifest & label-map SHA-256 hashes, allowed partition paths (`train` and `val` only; `test` and `external` explicitly blocked in training configs).
- **Model:** `model_candidate_id`, library/version, exact architecture variant, pretrained weight tag/hash/license, classification head design (pooling, dropout, output logit), two-stage freeze/unfreeze layer policy.
- **Training:** random seed(s), determinism flags, epochs/budget, batch size & gradient accumulation, optimizer, initial/fine-tune learning rates, LR scheduler, weight decay, loss function & class-imbalance parameters, mixed-precision mode (`fp32`/`amp`), early-stopping patience & monitored validation metric, training-only augmentation spec.
- **XAI linkage:** `xai_protocol_id` (`XAIP####`), designated target convolutional layer(s) for Grad-CAM and adopted comparators.
- **Runtime:** OS, Python/framework/CUDA/cuDNN versions, exact GPU/CPU model, VRAM/RAM, `environment/model/` lock hash.
- **Outputs & checkpoints:** artifact tier destination, checkpoint retention policy, validation prediction output schema.

The configuration validator (`src/bc_xai/`) must reject unresolved nulls, mismatched release hashes, invalid partition references (e.g., accidental test-set path in training), or stale parent gates. Any change to a launched experiment's settings requires a **new `EXP####` ID**.

## 5.3 Training lifecycle and multi-seed discipline

`Register EXP → verify current gates & input hashes → validate effective config → load train/val only → Stage 1/2 transfer learning → persist logs & checkpoints → validate → register CKPT & MODEL → assess G10`.

1. **Diagnostic smoke test (STEP-026):** Run a labeled diagnostic smoke training on a tiny training/validation subset before full compute. Confirm image/label alignment, finite binary cross-entropy/focal loss, monotonic overfit capability on a tiny sanity batch, deterministic validation inference, Grad-CAM hook extraction without NaNs, and clean checkpoint reload/resume. Never touch test data during smoke testing.
2. **EXP vs RUN separation:** One `EXP####` binds one immutable scientific config (and one seed, or an explicitly grouped multi-seed family with per-seed configs—preferring one `EXP####` per seed for clean foreign-key linkage). Each execution attempt receives `RUN####` inside `run_manifest.json`.
3. **Complete failure preservation:** Log per-epoch training/validation loss, AUC-ROC, PR-AUC, F1, learning rate, GPU memory, epoch duration, warnings, OOM errors, NaN divergences, and preemption/interruptions. Preserve every failed or underperforming run (`T16`); never delete a low-AUC seed or retroactively label a failed full run as a smoke test.

## 5.4 Checkpoint, interruption, and efficiency governance

- Assign immutable `CKPT####` IDs embedding `EXP####`, `RUN####`, epoch, and role (`best_val_auc`, `last`, `recovery`). `best` and `last` are immutable hashed files or symlinks—never overwritten sole artifacts.
- Record full state components saved: model weights, optimizer state, LR scheduler, AMP GradScaler, epoch/step, RNG states (Python, NumPy, framework/CUDA). Verify exact-resume capability on an intentional interruption test during STEP-026; if framework nondeterminism prevents bitwise exact resume, document it honestly and classify non-exact continuations transparently.
- Persist checkpoints and logs off ephemeral compute (e.g., Colab/Kaggle/cluster scratch) to approved durable storage during training and hash-verify after transfer.
- **Computational efficiency profiling (`UD20`):** Record total trainable/non-trainable parameters, GFLOPs/MACs at target input resolution, checkpoint disk size (MB), training wall-clock time per epoch on recorded GPU, and single-image inference latency (classification-only AND classification + Grad-CAM end-to-end) so the Q1 benchmark explicitly quantifies clinical deployability trade-offs across heavy (VGG16, ResNet50) vs compact (MobileNetV2, EfficientNetB0) architectures.

## 5.5 Experiment matrix and G10 qualification

Structure Stage S11 into three disciplined layers:
1. **Single-run protocol verification (`STEP-027–029`):** Baseline model execution, checkpoint audit, `MODEL####` registration, and `G10` assessment.
2. **Multi-architecture transfer learning benchmark (`STEP-030`):** Controlled comparison across all `UD13`-approved CNN families (and optional Q1 modern baseline) on matched `REL####` and `SPLIT####`, repeating `STEP-027–029` (`G10` per qualifying `EXP####`).
3. **Controlled ablations & multi-seed stability (`STEP-031`):** Pre-registered single-factor ablations (e.g., CLAHE vs minimal baseline preprocessing, focal/class-weighted vs unweighted loss, two-stage fine-tuning vs frozen-feature extraction, or approved architectural refinement) plus all planned random-seed repeats under `UD15`.

Only `MODEL####` entries whose originating `EXP####` holds a current `G10 PASS` are eligible for validation selection at `STEP-032` (`G11`).

<a id="os-06"></a>
# 6. Explainable AI (XAI) governance, quantitative faithfulness, sanity checks, and clinical alignment protocol

*This section adapts repository governance to mammography's core scientific pillars: verified diagnostic labels/ROI masks (replacing manual bounding-box annotation workflows) and Q1-grade Explainable AI validation.*

## 6.1 Diagnostic label and lesion ROI-mask verification governance (Stages S07–S08)

Because public mammogram collections supply pre-existing diagnostic labels (and often lesion ROI masks/contours) rather than requiring de novo bounding-box annotation from scratch, Stages S07–S08 govern **prospective label/mask auditing and verification** before splitting or training:

1. **Label provenance contract (`T09`, `UD07–UD08`):** Document for every retained image how its binary label (`0 = Benign`, `1 = Malignant`) was derived: histopathologic biopsy confirmation, surgical excision, longitudinal follow-up stability, or BI-RADS radiological score. Explicitly document the disposition of Normal/Negative (BI-RADS 1), incomplete (BI-RADS 0), and conflicting multi-lesion exams (e.g., breast containing both a benign cyst and a malignant mass MUST be labeled Malignant at the breast/image level with explicit multi-finding provenance, never ambiguously duplicated into both classes!).
2. **ROI-mask geometry & integrity audit (`UD09`):** For datasets supplying lesion segmentation masks or bounding boxes (used strictly for post-hoc XAI localization benchmarking—never leaked as input features to the classifier!), verify:
   - Exact spatial dimensions and orientation alignment between mammogram and mask (catching flipped, transposed, or mis-cropped masks).
   - Non-empty mask coverage, valid binary pixel values, and union rules when multiple malignant or benign lesions exist on one image.
   - Pilot visual overlay verification (STEP-016) followed by full-release automated checks + clinical-advisor spot review (STEP-017) and immutable `LBL####` freeze with SHA-256 hashes at `G06` (STEP-018).

## 6.2 Prospective XAI protocol (`XAIP####`)

To meet Q1 medical imaging standards, XAI methodology MUST be specified **prospectively at G05 (STEP-015)** and **frozen before test evaluation at G11 (STEP-032)**—never cherry-picked after inspecting test heatmaps (`UD16`):

1. **Mandatory baseline method (`RF08`):** **Grad-CAM** (Selvaraju et al.) applied to every compared CNN architecture.
2. **Optional Q1 XAI comparators (`UD16`):** Evaluate and prospectively ratify adding 2–4 complementary methods referenced in the report (`RF08`) or Q1 literature—such as **Grad-CAM++**, **Score-CAM** (gradient-free), **LayerCAM** (higher spatial resolution for small microcalcifications), **Integrated Gradients** (axiomatic pixel attribution), **Guided Backpropagation** (specifically to test sanity behavior!), or **LIME / SHAP** (perturbation/game-theoretic baselines on a defined stratified subset if compute-bounded).
3. **Architecture-specific target layer map:** Explicitly document the exact final spatial convolutional feature layer (and any intermediate high-resolution layer if LayerCAM/multi-scale CAM is adopted) for every approved architecture (VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3, MobileNetV2, Xception, and any modern baseline such as ConvNeXt/Swin/ViT attention rollout). Verify spatial feature-map dimensions (e.g., 7×7 vs 14×14) and bilinear upsampling/normalization conventions (`[0, 1]` min-max vs energy-normalized maps, explicit handling of all-zero/ReLU-collapsed maps).
4. **Target class & logit convention:** Specify whether saliency maps are computed with respect to the raw pre-sigmoid/pre-softmax **Malignant logit** (recommended so Benign vs Malignant evidence is not distorted by sigmoid saturation) or predicted class logit, and document exact handling for True Positives, True Negatives, False Positives, and False Negatives.

## 6.3 Quantitative XAI evaluation (Non-negotiable Q1 standard)

Visual heatmap montages alone are unacceptable in Q1 medical AI journals because visually pleasing heatmaps can fail basic faithfulness or act as input edge detectors. Freeze the following four quantitative XAI pillars under `UD17` and execute them on the locked test cohort(s) in STEP-035:

| Quantitative XAI Pillar | Approved Metric Candidates (`UD17`) | What It Proves / Failure Trigger |
|---|---|---|
| **1. Faithfulness (Causal Perturbation)** | **Deletion AUC** (lower is better: masking top-attributed pixels rapidly drops Malignant confidence); **Insertion AUC** (higher is better: revealing top-attributed pixels rapidly restores confidence); **ROAD** (*Remove And Debias* using linear imputation to avoid out-of-distribution zero-masking artifacts); **Fidelity / Compr. & Sufficiency** | Tests whether highlighted pixels actually drive the model's prediction. Record perturbation baseline (blur, breast-background mean, linear imputation), step schedule (e.g., 0–100% in 5% increments), and random-mask baseline control |
| **2. Sanity Checks (Model & Data Sensitivity)** | **Adebayo et al. Cascading & Independent Model Parameter Randomization Test** (re-initializing weights layer-by-layer from top classifier backward and measuring Spearman rank correlation / SSIM / HOG similarity vs original heatmap); **Data / Label Randomization Sanity Check** | Proves XAI explanations depend on learned mammographic features rather than acting as model-independent breast-edge or text-marker detectors. Any XAI method failing sanity checks (e.g., Guided Backpropagation frequently exhibits edge-detector invariance) MUST be flagged honestly rather than presented as clinically faithful |
| **3. Lesion Localization Alignment** *(where verified ROI masks exist in `LBL####`)* | **Pointing Game Accuracy** (whether maximum saliency pixel falls inside dilated/exact lesion ROI mask); **Energy-Based Pointing Game (EBPG)** (proportion of total positive saliency energy inside ROI mask); **Thresholded Heatmap-to-ROI IoU and Dice** across prospectively fixed thresholds (e.g., top-10%/20% or 0.5 normalized map) | Quantifies whether the model attends to true radiologist-localized lesions vs shortcut confounders (pectoral muscle, view labels, film borders, background noise). Disclose mask granularity (tight contour vs bounding box) and exact image subset with masks |
| **4. Stability & Cross-Method Consistency** | **Input Perturbation Stability** (SSIM / Pearson / Spearman / top-k IoU of heatmaps under tiny radiographically benign intensity/shift perturbations that preserve prediction); **Multi-Seed Explanation Consistency** (heatmap agreement across independent training seeds of the same architecture); **Inter-XAI Agreement** (Grad-CAM vs Score-CAM vs Integrated Gradients concordance) | Tests whether explanations are reproducible across seeds and small acquisition variations rather than brittle noise |

All quantitative XAI runs receive `XAIA####` records in `09_Evaluation/xai_audit_registry.csv` linked to exact `MODEL####`, `EVAL####`, `XAIP####`, and `LBL####` hashes.

## 6.4 Bounded clinical-advisor qualitative review (Non-trial boundary)

To evaluate Objective 6 and RQ3 honestly while strictly obeying Section 8's exclusion of real-patient clinical trials (`RF15`), define a **bounded retrospective qualitative XAI review** (`UD18`, executed in STEP-037):
- **Sample construction:** Prospectively draw a stratified, de-identified subset from the locked test evaluation covering True Positives (Malignant correctly caught), False Negatives (missed cancers—highest clinical priority), False Positives (Benign flagged as Malignant), and True Negatives, stratified across breast density and mass/calcification subtypes. Never cherry-pick only visually neat successes!
- **Blinded review rubric:** A qualified breast radiologist / clinical advisor (credentials recorded without PHI) evaluates blinded mammogram + heatmap overlays using a pre-registered structured rubric (e.g., 1–5 Likert scale for: *Anatomical lesion localization accuracy*, *Absence of obvious shortcut/artifact focus*, *Clinical plausibility of highlighted region*, and *Perceived diagnostic interpretability support*), plus free-text notes on failure causes.
- **Honest scope boundary:** If a qualified radiologist cannot be secured before thesis submission, mark the qualitative clinical review explicitly as **Unresolved / Not Performed** in `UD18` and limitations—never fabricate clinician ratings or substitute student/AI opinion as expert radiological validation. Even when completed, frame findings strictly as a *retrospective qualitative reader assessment*, never as a prospective clinical trial or proof of reduced clinical workload.

<a id="os-07"></a>
# 7. Q1 classification, calibration, statistical testing, and error-analysis evaluation protocol

## 7.1 Protocol before training; freeze before testing

Draft `09_Evaluation/protocol.md` with the baseline experiment plan (STEP-024, `G09`) and freeze the winning validation-selected model(s), preprocessing state, operating threshold(s), post-hoc calibration parameters, XAI protocol (`XAIP####`), and statistical analysis code at **G11 (STEP-032)** prior to generating any internal held-out test or independent external-validation predictions.

Use one `EVAL####` per `(MODEL####, REL####/cohort, partition, protocol_hash)` execution. Emit an explicit **evaluated-image coverage ledger** accounting for 100% of scheduled test images (including decoding/inference failures if any—never silently drop hard cases from denominators). Store raw per-image Malignant probability logits, calibrated probabilities, binary predictions at frozen threshold(s), `PatientGroupID`, and subgroup metadata so all downstream metrics, ROC/PR curves, calibration plots, and paired statistical tests are reproducible from one immutable artifact.

## 7.2 Required report metrics and Q1 medical-AI evaluation suite

All six metrics mandated by Objective 4 (`RF09`) are **non-negotiable** for every evaluated architecture. Beyond those six, adopt the Q1 medical-AI evaluation suite prospectively under `UD19`:

| Category | Metric | Formula / Operational Definition | Required Accompaniments |
|---|---|---|---|
| **Required Report Metrics (`RF09`)** | **Accuracy** | `(TP + TN) / (TP + TN + FP + FN)` | Frozen threshold, class prevalence, patient/image counts |
| **Required Report Metrics (`RF09`)** | **Precision (PPV)** | `TP / (TP + FP)` (Malignant as positive class; also report macro/weighted if helpful) | Exact TP/FP counts, positive-class convention (`Malignant = 1`), N/A handling if `TP+FP=0` |
| **Required Report Metrics (`RF09`)** | **Recall (Sensitivity / TPR)** | `TP / (TP + FN)` | Exact TP/FN counts; critical screening metric reflecting missed cancers |
| **Required Report Metrics (`RF09`)** | **F1-score** | `2 × (Precision × Recall) / (Precision + Recall)` | Exact threshold and positive-class definition |
| **Required Report Metrics (`RF09`)** | **AUC-ROC** | Area under Receiver Operating Characteristic curve over continuous scores | Exact trapezoidal/scikit-learn version, patient-clustered 95% CI, full ROC curve |
| **Required Report Metrics (`RF09`)** | **Confusion Matrix** | Full 2×2 matrix (`TP, FP, FN, TN`) at frozen threshold | Both raw counts and row-normalized rates; patient-level and image-level if distinct |
| **Q1 Clinical Extensions (`UD19`)** | **Specificity (TNR)** | `TN / (TN + FP)` | Essential companion to Sensitivity to expose excessive false-positive biopsy referrals |
| **Q1 Clinical Extensions (`UD19`)** | **PR-AUC (AUPRC / AP)** | Area under Precision-Recall curve | Critical under class imbalance; report baseline prevalence alongside PR-AUC |
| **Q1 Clinical Extensions (`UD19`)** | **Balanced Accuracy & MCC** | `(Sensitivity + Specificity) / 2` and Matthews Correlation Coefficient | Thresholded imbalance-robust summary metrics |
| **Q1 Clinical Extensions (`UD19`)** | **Clinically Anchored Operating Points** | **Specificity at fixed high Sensitivity** (e.g., 90% and 95% Sensitivity, reflecting high clinical cost of missed malignancy) AND/OR **Sensitivity at fixed high Specificity** (e.g., 90% Specificity) | Operating threshold derived strictly on **validation set** (or explicitly labeled as fixed-target curve point) to prevent test leakage |

**Validation-only threshold selection (`UD19`):** Select the primary binary decision threshold strictly on the validation set using a prospectively chosen rule—such as **Youden's J** ($\max(\text{Sensitivity} + \text{Specificity} - 1)$), validation F1-maximization, or a pre-specified clinical sensitivity target (e.g., threshold achieving $\ge 90\%$ validation Sensitivity). Lock that scalar threshold at `G11` before touching test predictions. Never tune thresholds on the test set!

## 7.3 Probability calibration (Q1 standard)

Raw deep-learning softmax/sigmoid outputs are frequently overconfident, undermining clinical CAD risk interpretation. Under `UD19`:
- Compute **Expected Calibration Error (ECE)** (with prospectively fixed bin count, e.g., 10 or 15 equal-width/adaptive bins), **Brier Score** ($\frac{1}{N}\sum (\hat{p}_i - y_i)^2$), and **Reliability Diagrams** for raw model probabilities.
- If post-hoc probability calibration is adopted (e.g., **Temperature Scaling**, Platt Scaling, or Isotonic Regression), fit calibration parameters **exclusively on the validation set** prior to `G11`, freeze them alongside the model, and report both pre-calibration and post-calibration ECE/Brier scores on the locked internal and external test cohorts.

## 7.4 Statistical rigor and paired model comparisons (`STAT####`)

Point-estimate metric tables without uncertainty intervals or hypothesis tests rarely clear Q1 peer review. Under `UD20`:
1. **Patient-level clustered bootstrap 95% Confidence Intervals:** Resample **patients/connected components** (`PatientGroupID`) with replacement (e.g., $B = 2,000$ or $5,000$ replicates, fixed random seed) rather than individual images whenever patients contribute multiple views (CC/MLO) or bilateral scans, preserving within-patient correlation. Report 95% percentile or BCa CIs for AUC-ROC, PR-AUC, Sensitivity, Specificity, F1, Accuracy, ECE, and quantitative XAI metrics.
2. **Paired AUC-ROC comparison (DeLong's test):** Use two-sided **DeLong's test** (or patient-clustered DeLong / paired clustered bootstrap when multi-view clustering applies) to test statistically significant AUC-ROC differences between the selected winning model and every other benchmarked CNN architecture on the exact same test set.
3. **Paired binary decision comparison (McNemar's test):** Apply exact or continuity-corrected **McNemar's test** (or clustered Obuchowski/bootstrap equivalent where multi-view clustering is present) on paired binary predictions at frozen operating points.
4. **Multiple-comparison correction:** Control family-wise error rate across pairwise architecture comparisons using **Holm-Bonferroni** (or Benjamini-Hochberg FDR if pre-specified under `UD20`). Report raw p-values, adjusted p-values, exact effect sizes ($\Delta\text{AUC}$, $\Delta\text{Sensitivity}$), and 95% CIs of differences.
5. **Multi-seed variability:** Report mean ± SD across all planned training seeds (never the single highest seed alone), distinguishing optimization variance from finite-sample test uncertainty.
6. **External validation invariance:** Apply the **exact frozen model, threshold, and calibration parameters** zero-shot to the independent external dataset (if adopted under `UD05`) without re-tuning, reporting domain shift honestly.

Record every statistical comparison in `09_Evaluation/statistical_comparisons.csv` (`STAT####`, `T21`).

## 7.5 Stratified subgroup, failure taxonomy, and limitations analysis (`G13`)

Execute systematic stratified and qualitative error analysis in STEP-037:
- **Subgroup stratification (where verified metadata exists):** Report discrimination, sensitivity/specificity, calibration, and XAI localization stratified by (a) **BI-RADS breast density** (A: fatty, B: scattered fibroglandular, C: heterogeneously dense, D: extremely dense—directly testing the dense-breast challenge cited in `RF01`/pp. 2, 4, 6); (b) **Abnormality type** (mass vs calcification vs architectural distortion); (c) **Mammographic view** (CC vs MLO); and (d) **Image/dataset acquisition source** (internal vs external cohort). Report exact subgroup sample sizes; flag small-$n$ subgroups explicitly rather than over-interpreting noisy point estimates.
- **FN / FP + XAI failure taxonomy (`T22`):** Systematically categorize False Negatives (missed malignancies—highest patient-safety risk) and False Positives (unnecessary biopsy recalls), paired with their Grad-CAM/XAI heatmaps:
  - *Correct prediction + Correct lesion focus* (aligned success)
  - *Correct prediction + Shortcut/artifact focus* (Right for the Wrong Reasons — critical XAI discovery!)
  - *False Negative + Diffuse/missed focus* (subtle microcalcification, dense-tissue masking, boundary lesion)
  - *False Negative + Correct lesion focus but below threshold* (calibration/operating-point failure)
  - *False Positive + Benign calcifications/superimposed dense parenchyma/marker/pectoral artifact*
  - *Suspected reference-label ambiguity* (flagged via clinical advisor review without silently mutating frozen test labels)

## 7.6 Evaluation failure and test-exposure recovery

If evaluator bugs, coverage discrepancies, or hash mismatches are detected, mark the `EVAL####` record `INVALID`, preserve original artifacts untouched, repair verified code bugs under a new `EVAL####` with full disclosure, and reassess `G12`. If test results prompt architectural or hyperparameter retraining, the original test set is **permanently development-exposed**: either acquire a genuinely untouched external cohort or explicitly downgrade any post-test iteration to labeled exploratory analysis—never overwrite or conceal exposure history.

<a id="os-08"></a>
# 8. Research CAD prototype, reproducibility audit, and conditional hosted web demonstration

## 8.1 Minimal local research CAD prototype contract (STEP-038)

Package the frozen, validation-selected winning inference + XAI pipeline into a clean, documented local research CAD entry point (`src/bc_xai/infer.py` + thin CLI under `13_Automation/`, interface chosen under `UD22`):
1. Accepts an authorized 2D mammogram input (DICOM or approved image format), validates integrity/polarity/dimensions, applies the exact registered deterministic `PP####` pipeline (with frozen training-fitted state), loads the hash-verified `MODEL####` export, outputs calibrated Malignant probability, binary Benign/Malignant classification at the frozen validation threshold, and generates the registered `XAIP####` Grad-CAM (and optional comparator) visual heatmap overlay plus quantitative summary metadata.
2. Output payload binds `MODEL####`, `CKPT####`, `PP####`, `XAIP####`, threshold & calibration version, code commit hash, input identifier, inference latency, processing status, and an explicit **Research CAD Aid Only — Not for Clinical Diagnosis** disclaimer.
3. Explicit error contract covering corrupted/unreadable files, unsupported modalities/bit-depths, dimension/aspect anomalies, missing/hash-mismatched weights, and resource failures.
4. Any serialized export format (e.g., ONNX, TorchScript, FP16) must pass numerical prediction AND Grad-CAM heatmap parity checks against the source checkpoint within prospectively declared tolerances (`UD22`); otherwise it must be registered and evaluated as a distinct `MODEL####`/`EVAL####` artifact.

## 8.2 Reproducibility audit and CLAIM / TRIPOD+AI compliance (STEP-039, G14)

**PLANNING RECOMMENDATION — Q1 Mandatory Reporting Checklists:** Integrate both **CLAIM 2024 (Checklist for Artificial Intelligence in Medical Imaging)** and **TRIPOD+AI** directly into `G14` (and verify again at `G15`):
- Map every checklist item (study design, public dataset eligibility, de-identification, patient-level partitioning, ground-truth reference standard, preprocessing, model architecture/initialization, training hyperparameters, calibration, subgroup/external validation, XAI validation, failure analysis, code/data/model availability) to exact repository artifact paths and manuscript sections (`T26`, `12_Documentation/claim_tripod_checklist.md`).
- **Clean-environment reproduction audit (`T25`):** In a fresh authorized environment created solely from `environment/data/` and `environment/model/` lockfiles and `12_Documentation/installation.md` + `reproduce.md`, retrieve versioned artifacts by manifest, verify SHA-256 checksums, regenerate frozen internal/external predictions, classification metrics, calibration curves, paired statistical tests, quantitative XAI faithfulness/sanity scores, and representative figures, and verify agreement within prospectively chosen tolerances (`UD23`).
- Explicitly declare achieved reproducibility level: **(a) Inference, statistical & XAI replay** (mandatory for `G14`), **(b) Full single-seed retraining check** (recommended if compute permits), and **(c) Multi-seed conclusion reproducibility**. State lawfully what external readers can reproduce given dataset access agreements (e.g., credentialed PhysioNet/TCIA download instructions). `G14` fails on missing essential artifacts, hidden notebook state, or unexplained numeric discrepancies.

<a id="os-08-3"></a>
## 8.3 Conditional hosted web demonstration for the FYDP defense (Stage S16, G17)

**Status, authority, and conditionality:** The title report (`RF15`) explicitly excludes real-time hospital deployment, PACS integration, mobile/IoT applications, and clinical trials, while `RF13` notes a future foundation for web-based clinical decision support. Hosting a live web demonstration of the frozen CAD + Grad-CAM prototype specifically for the **FYDP defense** is a **conditional, optional presentation deliverable** gated strictly by **`UD25`** (research team & supervisor ratification). It is **not** a report requirement, does not alter O1–O6 or Q1 scientific claims, does not produce evaluation evidence, and is strictly **not** hospital/clinical deployment. If `UD25` declines a hosted demo, record an approved non-adoption disposition; S16 is skipped cleanly and `G16` verifies that disposition instead of `G17`.

**Hosted model selection (if `UD25` adopted):** Only the single validation-selected, `G11`-frozen, `G12`-evaluated, `G13`-audited winning `MODEL####` (with its frozen `PP####`, validation threshold, calibration state, and `XAIP####` Grad-CAM config) may be presented as the project's primary best model. Never pick a different model by test-set score or prettier Grad-CAM visuals! Display the hosted `MODEL####`, `EVAL####`, `XAIA####`, and locked test metrics (Accuracy, Sensitivity, Specificity, F1, AUC-ROC, PR-AUC, ECE) transparently on an *"About This Model"* page sourced directly from frozen `EVAL####` files. If hosting constraints require a lighter architecture (e.g., MobileNetV2 or EfficientNetB0 for CPU memory limits), it MUST already be a registered, `G12`-evaluated `MODEL####` labeled honestly by its own name and metrics.

**Thin architecture contract (PLANNING RECOMMENDATION):**

```text
Browser (examiner) ──HTTPS──> web/ UI & API ──> src/bc_xai/ frozen inference + Grad-CAM entry point (STEP-038)
                                                 │
                                                 └─> SHA-256-verified MODEL export + frozen PP + threshold/calibrator + XAIP
```

1. `web/` is strictly a thin presentation shell importing `src/bc_xai/` unchanged—never duplicating mammogram preprocessing, polarity handling, threshold/calibration logic, or Grad-CAM computation.
2. Startup enforces SHA-256 verification of model weights, preprocessing state, and config; mismatch aborts startup.
3. UI displays: curated sample selector (and/or in-memory upload per `UD27`), original de-identified mammogram alongside interactive Grad-CAM overlay (adjustable opacity), calibrated Benign/Malignant probability and frozen-threshold label, `MODEL`/`PP`/`XAIP`/commit provenance, **web response time** (explicitly distinguished from offline inference latency benchmark), *"About This Model"* panel with `EVAL`/`XAIA` metrics & limitations, and a **persistent non-dismissible research-only disclaimer** (*"Research CAD Prototype Only — Not Approved for Clinical Diagnosis, Screening, or Hospital/PACS Use"*).
4. **Hosting & Privacy (`UD26–UD27`):** Compare platforms (e.g., Hugging Face Spaces with Gradio/Streamlit, Render/Railway/Fly.io container host, university server, or VPS) on RAM/CPU latency for CNN + Grad-CAM, cold-start behavior, HTTPS, secret storage, and team-owned accounts. Default privacy policy: **curated, license-permitted, disclosure-reviewed de-identified sample mammograms only**, plus optional in-memory-only uploads that are **never written to disk or logged** (`UD27`). Strictly enforce MIME/file-size/dimension limits, timeouts, rate limiting, and scrubbed logs (no image bytes, no uploaded filenames).
5. **Parity, offline fallback, and lifecycle (`UD28`, `G17`):** Prove numerical probability and Grad-CAM heatmap parity between the containerized web API and STEP-038 CLI outputs within approved tolerance. Package the exact container (`Dockerfile`) as a tested **offline local fallback** on the presenter's machine alongside backup screenshots/screen recording for defense-day Wi-Fi resilience. Execute post-defense keep/freeze/takedown under `UD28` and archive `DEPLOY####` records at STEP-046.

<a id="os-09"></a>
# 9. Evidence-first writing, Q1 journal manuscript, and FYDP thesis submission operating system

## 9.1 Evidence-first writing discipline

Maintain one canonical claim ledger (`02_Literature/claims.csv`, `CLAIM####`) and one writing registry (`11_Writing/writing_registry.csv`, `WR####`). Every substantive scientific assertion must map to verified `P####`, `DS####`/`LBL####`/`SPLIT####`, `EXP####`, `EVAL####`, `XAIA####`, `STAT####`, or `FIG####`/`TAB####` IDs. Background and planned methodology may be drafted early while clearly tagged as *planned*; realized methods, dataset counts, metrics, p-values, and XAI results are written **only** after their governing gates pass. Never insert plausible dummy numbers—use `[Evidence pending — blocked by G##]` and resolve every marker before `G15`.

## 9.2 Dual-track architecture: FYDP Thesis vs Q1 Journal Manuscript

Both deliverables draw from the **exact same frozen evidence base**, differing only in narrative depth and formatting (`UD02`):

| Writing unit | Required verified inputs | Q1 & FYDP completion standard |
|---|---|---|
| **Title / Abstract** | Approved title (`RF01`), finalized `EVAL`/`XAIA`/`STAT` | Structured abstract (Background, Methods, Results with 95% CIs & external/XAI numbers, Conclusions); bounded research-aid scope |
| **Introduction & Related Work** | Verified `P####`, `GAP####`, remediated Table 1.1 (`UD04`), approved RQs (`G03`) | Honest Q1 novelty framing; clear separation of mammography vs non-mammogram contextual work; zero unverified citations |
| **Materials & Methods** | `DS`/`LBL`/`SPLIT`/`PP`/`REL` cards, `EXP`/`XAIP` configs, `09_Evaluation/protocol.md`, CLAIM/TRIPOD+AI mapping | Full reproducibility: dataset provenance, FFDM/ROI & Normal-case rules, connected-component patient splitting, preprocessing/augmentation, 2-stage transfer learning, XAI target layers & quantitative metrics, threshold/calibration/DeLong/McNemar rules |
| **Results** | `EVAL####`, `STAT####`, `XAIA####`, `FIG####`/`TAB####` | All 6 report metrics + Q1 suite with patient-clustered 95% CIs, paired DeLong/McNemar p-values (Holm-Bonferroni), calibration plots, internal vs external generalization, quantitative XAI faithfulness/sanity/localization/stability tables, multi-seed variance, efficiency profiles, and negative/ablation outcomes |
| **Error Analysis, Clinical Alignment & Prototype** | `G13` subgroup/error review, blinded clinical-advisor XAI rubric (`UD18`), STEP-038 CAD prototype, optional S16 showcase | Density/view/subtype breakdown, FN/FP + shortcut-focus taxonomy, honest limitations, explicit non-clinical boundary |
| **Discussion & Conclusion** | All verified evidence + literature comparison | Observations separated from causal hypotheses; contextualized comparison (no unfair cross-dataset/cross-modality ranking); exact objective O1–O6 fulfillment |
| **Declarations & Supplements** | `G14` reproducibility audit, `T26` CLAIM/TRIPOD+AI checklist, `UD06`/`UD24` statements | Ethics/waiver, data/code/weight availability, competing interests, author contributions (CRediT), funding, AI-use disclosure if required by venue |

## 9.3 Reproducible figures, tables, and verified citations

Every visual asset receives `FIG####` or `TAB####` in `10_Figures_Tables/assets.csv` (`T23`), binding source `EVAL`/`XAIA`/`STAT` hashes, exact Python plotting script + CLI command, code revision, units, aggregation/CI rules, caption, and disclosure clearance (mandatory for any mammogram + Grad-CAM visual plate!). Recommended Q1 visual suite (generated strictly from verified outputs):
- PRISMA literature screening flow diagram;
- Patient-level dataset flow & connected-component split consort diagram;
- Multi-architecture ROC curves, PR curves, and Reliability/Calibration diagrams (internal + external);
- Quantitative XAI Faithfulness (Deletion/Insertion/ROAD) curves + Adebayo sanity-check correlation decay plots + ROI localization box/bar charts;
- Stratified subgroup performance heatmap (BI-RADS density A–D, mass vs calcification, CC vs MLO);
- Disclosure-reviewed qualitative Grad-CAM + comparator plate showing TP, TN, FN, FP, and shortcut-focus cases side-by-side with ROI ground-truth contours.

Every citation must resolve against publisher-verified metadata in canonical `02_Literature/references.bib`. Preserve title-report numbering only as `ReportRef` audit metadata—never copy Table 1.1's unverified entries or anomalies (`RF18`) into the thesis or manuscript.

## 9.4 Document-scoped `G15` readiness, Q1 submission, and peer-review rebuttal workflow

`G15` is **strictly document-scoped** into two independent gate assessments recorded under separate `AssessmentID` rows in `01_Project_Management/gates.csv` (using `EntityVersions` to distinguish document and version):
1. **`G15 / thesis` (STEP-043):** Governs readiness of the DIU FYDP Thesis (`11_Writing/thesis/`) prior to institutional submission (`STEP-044`). Thesis readiness never waits for an undrafted Q1 journal manuscript.
2. **`G15 / paper` (STEP-045):** Governs readiness of the Q1 Journal Manuscript (`11_Writing/paper/`) prior to journal submission. Requires: verified target Q1 journal Aims & Scope and formatting compliance (`UD02`), complete CLAIM & TRIPOD+AI checklists (`T26`), cover letter & highlights (`T29`), ethics/data/code/CRediT statements, verified figures/tables/citations, and explicit co-author & supervisor sign-off.
   - If Q1 journal submission is explicitly deferred or not required at FYDP closure, record a supervisor-approved **disposition decision** (`DEC####`) instead of fabricating a `G15 / paper PASS` or claiming submission occurred.

**Structured Q1 Peer-Review & Rebuttal Workflow (STEP-045, `T29`):**
- Track every reviewer/editor comment with `CommentID`, reviewer number, verbatim text, classification (`editorial` vs `analytical` vs `new_experiment`), action taken, exact manuscript diff locator, supporting `EVAL`/`XAIA`/`STAT` evidence ID, polite point-by-point response, owner, and status.
- Any peer-review request requiring new experiments, new XAI metrics, or additional external datasets MUST re-enter the gated workflow (`STEP-027–036` with new `EXP`/`EVAL`/`XAIA` IDs)—never bypass validation/freeze rules during revision!
- Archive every submitted version (`v1_submitted`, `R1_revised`, `R2_revised`), marked-up tracked-changes PDF, rebuttal letter, and portal submission receipt immutably. Distinguish clearly between *drafted*, *ready (`G15 PASS`)*, *submitted (with receipt)*, *under revision*, and *accepted*—project closure (`G16`) never depends on uncertain external journal acceptance.

<a id="os-10"></a>
# 10. Version control, artifact storage, and two-phase environment readiness

## 10.1 Right-sized source control

**PLANNING RECOMMENDATION:** Use Git for source code (`src/bc_xai/`, `tests/`, `web/`), text configurations, non-sensitive CSV registries, documentation, aggregate metrics/statistics, figure/table specs, and hash-verified artifact pointers. Select the Git host and visibility (private recommended during active research) under `UD14`; no specific vendor is mandated. For a two-researcher FYDP team plus supervisors, a protected `main` branch with short-lived task branches and pull-request review provides adequate change control.

Use coherent semantic commit prefixes (`docs:`, `research:`, `data:`, `labels:`, `xai:`, `experiment:`, `evaluation:`, `writing:`, `web:`, `fix:`) referencing entity or step IDs. Record the Git commit hash separately from the configuration SHA-256 inside `run_manifest.json` so configs are never self-referential. Review `git diff` and `git status` before every push to ensure zero DICOM/mammogram bytes, raw Grad-CAM patient overlays, checkpoints, credentials, or identifying linkage tables enter source history.

## 10.2 Storage tiers

| Tier | Contents | Storage & Security Policy |
|---|---|---|
| **Tier 1: Source (Git)** | `src/bc_xai/`, `tests/`, `web/`, configs, non-sensitive CSV registries, docs, safe aggregate metrics/tables, specs, hash pointers | Git with `UD14`-approved private/controlled remote; diff inspection prior to push |
| **Tier 2: Restricted Data** | Immutable raw mammograms/DICOMs (`raw/DS####/`), verified ROI masks, patient linkage maps, derived `processed/REL####/`, serialized training-fitted states | Institutionally/team-approved encrypted or access-controlled storage complying with dataset DUAs (`UD06`); strictly excluded from ordinary Git |
| **Tier 3: Research Artifacts** | Model checkpoints (`CKPT####`), exported weights, full per-image predictions, raw XAI attribution arrays, private clinical-review plates, bootstrap samples | Versioned durable artifact tier with SHA-256 manifests and verified off-compute backups; never rely solely on ephemeral GPU notebooks |
| **Tier 4: Release & Archive** | Immutable `ARCH####` snapshots, final thesis/paper PDFs, submission receipts, CLAIM/TRIPOD+AI supplements, lawful public code/weight subset (`UD24`) | Write-once archival storage; public release subset cleared independently for dataset/weight licenses and zero PHI disclosure |

Configure `.gitignore` in STEP-002 to block `03_Datasets/raw/`, `05_Preprocessing/processed/`, `08_Checkpoints/*.pt|*.pth|*.h5|*.ckpt|*.onnx`, raw XAI array dumps, patient linkage CSVs, virtual environments, caches, notebook checkpoints, and `.env`/secret files—while keeping safe aggregate CSVs and manifests explicitly tracked.

## 10.3 Two-phase environment readiness (`environment/data/` vs `environment/model/`)

1. **Phase 1 — Minimal Data, DICOM & Governance Runtime (`environment/data/`, STEP-002, verified at G02):** Establish a lightweight, pinned environment supporting registry/link validation, read-only DICOM/image decoding and metadata auditing (e.g., `pydicom`, `Pillow`, `numpy`, `pandas`, `scikit-image`/perceptual hashing, `networkx`/graph connected-components for patient splitting, `pytest`). Record lockfile, OS/Python versions, and smoke-test output on synthetic/permitted fixtures in `environment/data/verification.md`. Do **not** prematurely pick the deep learning or GPU stack here.
2. **Phase 2 — Deep Learning, XAI & Statistical Runtime (`environment/model/`, STEP-023, verified at G09):** After architecture roster and framework approval (`UD13–UD14`), pin the full training, XAI, calibration, and statistical inference stack (e.g., PyTorch + `timm`/`torchvision` or TensorFlow/Keras, CUDA/cuDNN drivers, Grad-CAM/XAI libraries such as `pytorch-grad-cam`/`captum` or custom verified implementations, `scikit-learn`, `scipy`, `statsmodels`, plotting libraries). Preserve `environment/data/` untouched alongside its hash so early `PP####`/`REL####` provenance remains intact. If any shared package upgrade changes preprocessing outputs, verify hashes and regenerate versioned `PP`/`REL` with renewed `G08` before training.

## 10.4 Remote compute synchronization and disaster recovery

Before launching remote GPU compute (university cluster, cloud GPU, Colab/Kaggle if DUA-permitted under `UD06`): verify clean Git commit, DUA compliance for uploading/accessing dataset on that host, input `REL####` SHA-256 hashes, `environment/model/` lock, durable checkpoint destination, and disk quota. Persist logs and checkpoints off ephemeral local disks continuously during training; verify transfer checksums before terminating compute sessions. Test backup restoration explicitly at STEP-026 (checkpoint smoke), STEP-039 (reproducibility audit), and STEP-046 (archival). If sensitive data or credentials are exposed, halt distribution immediately, rotate credentials, notify the supervisor/custodian, and execute documented remediation without silently erasing scientific audit history.

<a id="os-11"></a>
# 11. Roles and human decisions

Roles define accountability boundaries; within a two-student FYDP team (Alzubair Ahamed & Md Riyadul Hasan, `RF02`) supervised by Israt Jahan and co-supervised by Ms Faiza Feroz, team members hold multiple operational roles assigned at STEP-001 (`UD01`), while clinical interpretation, ethics clearance, and supervisory ratification remain strict human boundaries.

| Role | Primary responsibilities | Non-delegable decision boundary |
|---|---|---|
| **Researchers (Team)** | Protocols, PRISMA screening, data/label QC, code (`src/bc_xai/`), experiments, XAI audits, statistical tests, writing, coordination | Propose decisions and produce verifiable evidence; record actual approvals faithfully |
| **Supervisor / Co-Supervisor** | Scope constitution, Q1 novelty framing, architecture/split/protocol ratification, thesis & Q1 manuscript sign-off, defense readiness | Ratify scope, contribution claims, `G01/G03/G05/G07/G11/G13/G15/G16/G17` approvals |
| **Data Steward / Ethics Authority** | Dataset DUAs, licenses, institutional ethics/waiver determination, PHI screening, restricted storage & archival custody | Certify lawful public/controlled dataset access and permissible figure/demo disclosure (`UD06`, `UD24`) |
| **Radiologist / Clinical Advisor** | FFDM vs ROI clinical validity, Benign/Malignant/Normal & pathology provenance review, artifact/preprocessing visual QC, blinded qualitative XAI rubric (`UD18`), clinical wording audit | Advise on radiographic validity and blinded heatmap clinical plausibility; explicitly outside clinical trials; if unavailable, mark unverified rather than substituting AI/student judgment |
| **Model & XAI Lead** | Transfer learning architecture implementations, multi-seed benchmarking, Grad-CAM & XAI comparators, faithfulness/sanity/localization harness | Cannot silently alter splits, evaluation protocols, or cherry-pick target layers after test exposure |
| **Evaluation & Reproducibility Reviewer** | `G11` freeze audit, metric/calibration/DeLong/McNemar verification, CLAIM/TRIPOD+AI compliance, clean-environment replay (`G14`) | Enforce strict test-set isolation; cannot tune models or thresholds on test outputs |
| **Writing & Release Owner** | Claim/citation verification, dual-track FYDP thesis & Q1 manuscript assembly, cover letter/rebuttal tracking, submission receipts, `ARCH####` handover | Cannot claim submission or acceptance without verifiable receipts |
| **Deployment Owner (Conditional S16)** | Conditional `web/` build, parity verification, HTTPS hosting, privacy enforcement, defense-day offline fallback & runbook (`G17`) | Cannot swap hosted model/thresholds/preprocessing/Grad-CAM logic or store user uploads beyond `UD27` |

**Human handoff contract:** Every request for human approval states the `UD##`/`GateID`, exact options and evidence, tradeoffs, blocking step, target artifact path, and verification check. Halt only dependent work while awaiting review; continue unblocked documentation or literature work. Never feed restricted patient data or credentials into unapproved external AI tools; verify all AI-assisted code, statistics, and citations against original sources and automated tests.

<a id="os-12"></a>
# 12. Daily research operations, reviews, and risk register

**Session startup:** Inspect `01_Project_Management/dashboard.md`, prior diary note (`T03`), active gate statuses (`gates.csv`), blocking `UD` items, artifact integrity, and `git status`. Select one bounded blueprint step whose prerequisites hold current `PASS`.

**Execution:** Run planning/review prompts before implementation prompts; bind repetitive screening, QC, training, XAI, or writing sessions to dated batch/RUN identifiers rather than compressing multi-day work into one opaque session.

**Session closeout:** Save hashed outputs, run verification checklists, preserve failed runs (`T16`), update owning CSV registries, sync only permitted Tier-1/Tier-3 artifacts, and log the exact next unblocked step. When blocked, log the exact blocker—never invent progress.

**Weekly & milestone reviews (`T33`):** Track RQ alignment, PRISMA/citation verification progress, dataset/external-cohort access turnaround, patient-grouping integrity, GPU compute budget, invalidated (`STALE`) gates, multi-seed completion, XAI faithfulness anomalies, CLAIM/TRIPOD+AI gaps, writing evidence completion, and backup health.

**Initial project risk themes (populate probability/impact/owners in `01_Project_Management/risk_register.csv` during STEP-001–003):**
1. *Q1 novelty saturation:* Standard CNN + vanilla Grad-CAM already widely published (mitigate via STEP-008 quantitative XAI faithfulness + external validation + calibration framing).
2. *Hidden patient/view/ROI leakage:* Official splits or multi-view images leaking patients across train/test (mitigate via connected-component grouping at `G07`).
3. *Label/paradigm ambiguity:* Conflating BI-RADS proxies with biopsy truth, mishandling Normal (BI-RADS 1) cases, or mixing FFDM with ROI crops (mitigate at `G05–G06`).
4. *Shortcut learning ("Right for the Wrong Reasons"):* CNN focusing on radiopaque view markers, borders, or pectoral muscle instead of lesions (detect via ROI localization, Adebayo sanity checks, and clinical review at `G12–G13`).
5. *Dataset DUA or external-cohort access delays:* Credentialed portals (e.g., PhysioNet/TCIA/INbreast) delaying intake (mitigate by applying early in STEP-011 and auditing multiple candidates in STEP-010).
6. *Radiologist/clinical-advisor unavailability:* Inability to obtain blinded expert XAI review (mitigate by engaging advisor early at STEP-001/014 and transparently bounding qualitative claims if unperformed).
7. *GPU/compute quota & ephemeral preemption:* Multi-architecture multi-seed training interrupted (mitigate via tested checkpoint recovery at STEP-026 and continuous off-host sync).
8. *Table 1.1 / reference citation propagation:* Copying unverified report bibliography mismatches into thesis/paper (mitigate via mandatory `UD04` primary-source audit at STEP-007).
9. *Overclaiming clinical utility or crossing Section 8 exclusions:* Framing retrospective CAD accuracy as clinical screening readiness (mitigate via `G13/G15` wording audits).
10. *Defense-day web demo outage (if `UD25` adopted):* Cold start or venue Wi-Fi failure (mitigate via container offline fallback & pre-recorded backup verified at `G17`).

<a id="os-13"></a>
# 13. Quality gates and project completion criteria

## 13.1 Assessment semantics

Every quality gate is strictly **PASS or FAIL when assessed**. Initial state **`NOT ASSESSED`** and invalidated state **`STALE`** both block dependent downstream execution exactly like `FAIL`. `PASS` requires all mandatory criteria evidenced by exact file paths, SHA-256 hashes, assessor identity, date, bound entity versions, and named human sign-off. Missing evidence is `FAIL`—never a "conditional PASS." Mandatory report objectives and metrics (`RF09`, `RF14`) cannot be waived; optional Q1 enhancements or conditional S16 deliverables may be formally declined only via documented `DEC####` dispositions before execution.

Record every assessment in `01_Project_Management/gates.csv` and a dated report `01_Project_Management/reviews/G##_assessment_<date>.md` (`T24`). Any material upstream change marks all descendant gates `STALE` until re-verified.

## 13.2 Canonical gate matrix (`G01–G17`, all initially `NOT ASSESSED`)

| Gate / owning step | PASS evidence and mandatory criteria | FAIL / blocked transition | Human reviewer |
|---|---|---|---|
| **G01** Scope, constitution & UD assignment / `STEP-001` | Verbatim title (`RF01`), `RF01–RF20` vs recommendations separated, O1–O6 & Section 8 exclusions confirmed, `UD01–UD28` assigned owners & blocking milestones, p. 11 feedback status verified | Scope drift, invented feedback, or missing owners; blocks repo policy & protocol work | Supervisor + Researchers |
| **G02** Repository, templates, registries & data runtime / `STEP-003` | Section 2 folder tree & READMEs, `.gitignore` tested on safe dummy files, `T01–T35` installed blank, 24 canonical CSV registries initialized header-only, source hashes logged, `environment/data/` pinned & smoke-tested | Missing canonical homes, unsafe Git tracking, or untested Phase-1 runtime; blocks operational intake | Research Lead |
| **G03** PRISMA literature, anomaly remediation & Q1 RQ lock / `STEP-009` | Reproducible search/screening logs, `UD04` Table 1.1 & Ref `[1]`–`[12]` anomalies resolved/quarantined, counterevidence evaluated against `RF16`, defensible Q1 contribution & bounded RQ-to-metric map ratified | Unsupported novelty claim or unverified citations; blocks final dataset selection | Supervisor |
| **G04** Mammogram dataset access, integrity & QC approval / `STEP-013` | Written licenses/DUAs & institutional ethics/waiver record (`UD06`), primary (+ external candidate if adopted) raw hashes immutable, DICOM/bit-depth/PHI/marker QC complete, counts reconciled, `DS####` card approved | Unauthorized use, unscreened PHI, irreconcilable counts, or non-mammogram data; blocks label audit | Data Steward + Supervisor |
| **G05** Label/mask audit protocol & prospective XAI governance / `STEP-015` | FFDM vs ROI paradigm (`UD07`), Benign/Malignant/Normal provenance rules (`UD08`), ROI-mask verification rules (`UD09`), prospective `XAIP####` target layers, quantitative XAI faithfulness/sanity/localization/stability protocol (`UD16–UD17`), blinded clinical review rubric (`UD18`) approved | Ambiguous labels, mixed paradigms, or post-hoc XAI rules; blocks full label audit & split | Radiologist Advisor (or documented fallback) + Supervisor |
| **G06** Verified diagnostic label & ROI-mask freeze / `STEP-018` | Pilot & full-release label/pathology concordance audited, multi-lesion/Normal exclusions reconciled, ROI-mask spatial alignment verified, immutable `LBL####` hashes frozen | Unresolved label conflicts, flipped/misaligned ROI masks, or silent relabeling; blocks splitting | Data Lead + Clinical Reviewer / Supervisor |
| **G07** Connected-component patient-level leakage-safe split / `STEP-020` | Connected-component graph over `PatientID`/laterality/views/ROIs/duplicates verified zero cross-partition overlap, deterministic `SPLIT####` manifest & seed recorded, actual counts/subgroup balance reported, internal & external test custody sealed (`UD10–UD11`) | Any cross-partition patient/view/duplicate leakage or unapproved split claim; blocks preprocessing fit & training | Supervisor + Data Lead |
| **G08** Preprocessing & immutable release integrity / `STEP-021` | Raw bytes unchanged, bit-depth/polarity/artifact/resize visual QC passed, data-dependent stats fitted on training only, augmentation strictly training-only, immutable `REL####` manifest & checksums bound (`UD12`) | Val/test-fitted scaling, pre-split augmentation, clipped lesions, or hash mismatch; blocks baseline integration | Data Lead + Model Lead |
| **G09** Transfer learning architecture roster, model runtime & pipeline readiness / `STEP-026` | `RF07` architecture discrepancy resolved (`UD13`), `environment/model/` pinned & verified (`UD14`), prospective experiment/calibration/statistical/XAI plans approved (`UD15–UD21`), `src/bc_xai/` & unit tests passing, diagnostic smoke training, checkpoint recovery, and XAI sanity harness verified | Unresolved configs, broken evaluator/XAI hooks, untested recovery, or test-data access; blocks full compute | Researchers + Method Reviewer |
| **G10** Experiment completion & checkpoint verification / `STEP-029` (repeated `STEP-030–031`) | Valid stopping rule, complete logs & effective config, verified immutable `CKPT####` reload & backup hash, registered `MODEL####` card, all attempts/failures preserved | Missing state, altered mid-run config, or deleted negative seed; blocks model eligibility for selection | Experiment Reviewer |
| **G11** Validation-only selection & final-test / XAI freeze / `STEP-032` | Completed benchmark & ablation matrix (all considered models `G10 PASS`), winning architecture/seed policy selected on validation only, decision threshold & post-hoc calibration fitted on validation only, frozen `freeze.md` manifest & hashes (internal test, external cohort, XAI, stats), clean test-access audit | Test-informed model/threshold/layer selection or unfrozen analysis code; blocks all test-set execution | Supervisor + Evaluation Reviewer |
| **G12** Final quantitative classification, statistical & XAI evaluation / `STEP-036` | 100% test coverage ledger, all 6 report metrics (`RF09`) + Q1 suite (Specificity, PR-AUC, MCC, clinical operating points, ECE/Brier), patient-clustered 95% CIs, paired DeLong/McNemar (Holm-Bonferroni) `STAT####`, quantitative XAI faithfulness/Adebayo sanity/ROI localization/stability `XAIA####`, zero-shot external validation (if adopted), and efficiency profile reconciled | Missing required metrics, omitted negative/sanity failures, unadjusted comparisons, or evaluator bugs; blocks empirical claims | Evaluation Reviewer + XAI Lead |
| **G13** Subgroup analysis, failure taxonomy & clinical alignment / `STEP-037` | Density/abnormality/view subgroup breakdown, structured FN/FP + shortcut-focus taxonomy, blinded qualitative clinical-advisor XAI review (or explicit `UD18` non-performance disclosure), bounded clinical/generalization limitations | Cherry-picked XAI figures, hidden shortcut learning, or unproven clinical utility claims; blocks final conclusions | Radiologist Advisor (or documented fallback) + Supervisor |
| **G14** Clean-environment reproducibility & CLAIM/TRIPOD+AI audit / `STEP-039` | Fresh-environment installation from locks, checksum verification, replayed predictions/metrics/stats/XAI/figures within declared tolerances (`UD23`), completed `T26` CLAIM & TRIPOD+AI checklists, lawful data/code availability statements | Unreproducible scripts, missing artifacts, or unaddressed CLAIM/TRIPOD+AI gaps; blocks submission readiness & live web deploy | Reproduction Reviewer |
| **G15** Document-scoped submission readiness / `STEP-043` (`G15 / thesis`) & `STEP-045` (`G15 / paper`) | Assessed **independently** per document: complete manuscript/thesis, verified claims/citations/figures, disclosure-cleared mammogram plates, CLAIM/TRIPOD+AI checklist, institutional or Q1 journal format & cover letter (`T29`), review responses closed, explicit author & supervisor approval | Missing evidence blocks only that document's submission; `G15 / thesis` never waits for `G15 / paper`; approved paper deferral is a disposition, never a fabricated PASS | Supervisor + Authors |
| **G16** Final project completion & handover / `STEP-047` | All applicable prior gates current `PASS`, `STEP-044` thesis submission receipt, `STEP-045` Q1 paper submission receipt OR approved disposition, `G17` PASS (if `UD25` adopted) OR approved non-adoption disposition, `STEP-046` tiered immutable `ARCH####` archive with verified restore proof | Missing required deliverable, unverified backup, or stale gate; blocks completion declaration | Researchers + Supervisor |
| **G17** Conditional hosted web demonstration readiness / `STEP-050` *(only if `UD25` adopted)* | `UD25–UD28` resolved, `DEPLOY####` linked to `G11`-frozen `MODEL####` + `PP####` + `XAIP####` + commit, startup SHA-256 verification, prediction & Grad-CAM parity vs STEP-038 within tolerance, external HTTPS smoke check, `UD27` privacy/no-storage/scrubbed-logs verified, disclosure-reviewed samples, persistent non-clinical disclaimer, tested offline container fallback & `T35` runbook, supervisor walkthrough | Model/preprocessing/Grad-CAM drift, unreviewed patient images, stored uploads without approval, missing disclaimer, or untested fallback; blocks live defense showcase (and `G16` if `UD25` adopted) | Supervisor + Deployment Owner |

## 13.3 Gate failure, recovery, and completion criteria

On any gate `FAIL`, log exact failing criteria, evidence paths, impacted descendants, owner, and remediation plan; return to the earliest responsible step rather than restarting blindly, preserve the failed assessment record, and append a fresh dated assessment after correction. **Project completion (`G16`)** certifies scientifically valid, traceable fulfillment of approved deliverables and honest conclusions—never pre-guaranteed accuracy or uncertain external journal acceptance.

<a id="os-14"></a>
# 14. Template library

## 14.1 Template contract and use

Materialize `T01–T35` as blank, versioned files in `14_Templates_Prompts/` during STEP-003. Every template carries a standard metadata header: `TemplateID, template_version, entity_id, owner, date, status, source_inputs, governing_section, sensitivity, reviewer`. Use `Unresolved / Human Decision Required` for open human choices and `not reported` for absent source facts. Filled instances belong inside their owning domain folders; master templates remain blank.

## 14.2 Operational templates (`T01–T35`)

| ID / template | Purpose / instance home | Required body fields | Verification / common mistake |
|---|---|---|---|
| **T01** `readme.md` | Folder contract / each domain folder | Purpose; owner; inputs; allowed contents; workflow/commands; outputs; sensitivity tier; related paths; governing OS section | Matches actual directory contents; never duplicates OS policy |
| **T02** `decision.md` | Resolve a `UD##` or scientific choice / `01_Project_Management/decision_log/DEC####.md` | UD ref; question; `RF##` facts; options & evidence; tradeoffs; recommendation; actual human decision; date; approver; rejected options; affected artifacts/gates; reassessment trigger | No invented approvals; preserve superseded decisions |
| **T03** `session.md` | Daily research plan & closeout / `01_Project_Management/diary/` | Step/batch ID; objective; prerequisites; planned vs actual outputs; checks run; blockers; decisions; artifact sync; next step | Clearly separates planned vs completed work |
| **T04** `search.md` | PRISMA database search log / `02_Literature/searches/` | Database; exact Boolean string; date; time range; filters; retrieved count; export hash; dedup rules; access limitations | Exact query reproducibility; never invent counts |
| **T05** `paper_summary.md` | Grounded paper extraction / `02_Literature/summaries/P####.md` | Verified citation & `ReportRef`; task/modality (FFDM vs ROI vs non-mammogram); datasets/counts; label source; split level/leakage risk; architectures; preprocessing; XAI methods & whether quantitative faithfulness/sanity/localization evaluated; classification/calibration/stat metrics with page/table locators; limitations; comparability verdict | Read full text & tables; mark missing items `not reported` |
| **T06** `gap.md` | Hypothesis-testing research gap audit / `02_Literature/gap_notes/GAP####.md` | Report theme (`RG#`); provisional statement; search coverage; supporting `P####` IDs; contradicting `P####` IDs; Q1 saturation assessment; refined contribution option; status; approved RQ links | Search absence never proves universal novelty |
| **T07** `claim.md` | Traceable scientific claim card / `02_Literature/claim_notes/CLAIM####.md` | Exact wording; claim type; scope/limits; linked `P`/`DS`/`EXP`/`EVAL`/`XAIA`/`STAT`/`FIG`/`TAB` IDs & locators; contradictions; uncertainty; verification status; manuscript locations | Never cite a planned experiment as realized evidence |
| **T08** `dataset_card.md` | Public mammogram dataset card / `03_Datasets/reports/DS####_card.md` | Origin/version (primary vs mirror); modality (FFDM/SFM); license/DUA & ethics/waiver record; population known/unknown; patient/exam/image counts; label provenance; ROI-mask availability; quality/PHI/artifact QC & exclusions; duplicate/grouping keys; biases; intended role (internal vs external); SHA-256 hashes | Measured reconciled counts; no inferred demographics |
| **T09** `label_mask_protocol.md` | Label & ROI-mask verification rules / `04_Labels_XAI_Governance/protocols/` | FFDM vs ROI paradigm (`UD07`); Benign/Malignant definition & pathology vs BI-RADS provenance (`UD08`); Normal (BI-RADS 1) & multi-lesion rules; ROI-mask coordinate/alignment checks (`UD09`); adjudication rules; acceptance thresholds | Zero silent relabeling of Normal/BI-RADS-0 cases |
| **T10** `label_audit_report.md` | Pilot & full label/mask verification / `04_Labels_XAI_Governance/reviews/LBL####_audit.md` | `DS####` parent hash; sample/full scope; pathology/BI-RADS concordance; Normal/multi-lesion exclusion counts; ROI-mask dimension/flip/empty checks; clinical-advisor spot review; adjudications; frozen `LBL####` manifest hashes | Structural check alone never substitutes visual mask overlay QA |
| **T11** `xai_protocol.md` | Prospective XAI governance contract / `04_Labels_XAI_Governance/xai_protocols/XAIP####.md` | Approved methods (Grad-CAM + comparators, `UD16`); exact target convolutional layer per CNN; logit target convention; upsampling/normalization rules; faithfulness metrics & perturbation baselines (Deletion/Insertion/ROAD); Adebayo sanity protocol; ROI localization rules (Pointing Game/EBPG/IoU); stability protocol (`UD17`); blinded clinical review rubric (`UD18`) | Frozen before test inspection; no post-hoc target-layer tuning |
| **T12** `preprocessing.md` | Mammography preprocessing & augmentation spec / `05_Preprocessing/reports/PP####.md` | Rationale; ordered steps; bit-depth/polarity (`MONOCHROME1/2`); border/marker/pectoral handling; resize/aspect-ratio; CLAHE baseline vs ablation tag; training-only fitted normalization state hash; training-only augmentation rules; raw hash invariance & visual QC | Zero val/test-fitted scaling; zero pre-split augmentation |
| **T13** `split.md` | Connected-component split & custody report / `03_Datasets/splits/SPLIT####/report.md` | Input `DS`/`LBL` hashes; connected-component keys (`PatientID`/laterality/views/ROIs/duplicates); algorithm & seed; target vs actual patient/image/class/subgroup counts; official-split overlap audit; external-cohort isolation; sealed test custody policy | Never split a patient component to force exact percentages |
| **T14** `experiment.md` | Transfer learning experiment bundle / `07_Experiments/EXP####/README.md` | RQ/hypothesis; comparison factor vs controlled invariants; `REL`/`MC`/`XAIP` hashes; 2-stage freeze/unfreeze & imbalance policy; seed; `RUN####` log; curves; failures; validation result; conclusion | Planned hypothesis never prefilled as observed result |
| **T15** `config.yaml` | Executable machine-readable config / `07_Experiments/EXP####/config.yaml` | Complete Section 5.2 fields; zero nulls/placeholders before launch | Validator rejects missing fields or accidental test-set paths |
| **T16** `failure.md` | Failed/diverged/interrupted run record / owning entity `failure_report.md` | Symptoms & timestamp; affected IDs; verified facts vs suspected cause; log excerpts; lost work; recovery plan; status | Preserve every failure; never rewrite history |
| **T17** `checkpoint.md` | Immutable checkpoint manifest / `08_Checkpoints/manifests/CKPT####.md` | `CKPT`/`EXP`/`RUN`; epoch & role; saved state components; config/model SHA-256; bytes; backup path; restore-test evidence; exact-resume limitations | Weights-only file never falsely labeled exact-resumable |
| **T18** `model_card.md` | Bounded model card / `06_Models/cards/MODEL####.md` | Architecture/library version/pretrained origin & license; `EXP`/`RUN`/`CKPT`/`REL`/`PP`/`XAIP` links; parameter/FLOPs/latency profile; `EVAL`/`XAIA` IDs; intended research CAD aid; explicit Section 8 exclusions; subgroup/generalization limits; export parity verification | Never imply clinical approval from retrospective AUC |
| **T19** `evaluation.md` | Classification, calibration & efficiency report / `09_Evaluation/EVAL####/report.md` | Freeze/model/data/protocol hashes; cohort (internal vs external); 100% coverage ledger; frozen threshold & calibrator; all 6 required metrics + Q1 suite (Specificity, PR-AUC, MCC, sensitivity-anchored operating points); ECE/Brier/reliability data; efficiency profile; deviations | All figures trace directly to immutable prediction files |
| **T20** `xai_audit.md` | Quantitative & qualitative XAI audit / `09_Evaluation/EVAL####/xai_audit_XAIA####.md` | `XAIA`/`XAIP`/`MODEL`/`EVAL`/`LBL` hashes; Deletion/Insertion/ROAD faithfulness scores vs random baseline; Adebayo cascading/independent parameter & data randomization correlations; ROI Pointing Game/EBPG/IoU/Dice (mask subset size); input-perturbation & multi-seed stability; blinded clinical-advisor Likert/notes summary (`UD18`); sanity-failure flags | Never conceal failed sanity checks or shortcut-focus findings |
| **T21** `statistical_comparison.md` | Paired statistical inference report / `09_Evaluation/EVAL####/stat_STAT####.md` | `STAT` ID; compared `EVAL`/`MODEL` pairs; cohort & patient cluster count; bootstrap settings (B, seed, CI method); patient-clustered 95% CIs; two-sided DeLong AUC test results; McNemar paired decision test results; Holm-Bonferroni adjusted p-values; effect sizes; multi-seed mean ± SD | Account for patient clustering; never omit non-significant p-values |
| **T22** `error_review.md` | Stratified subgroup & FN/FP + XAI failure review / `09_Evaluation/EVAL####/error_review.md` | Stratification variables (density A–D, mass/calcification, CC/MLO, external); sampling rule & denominators; FN/FP + shortcut-focus taxonomy counts; clinical-advisor annotations; suspected label ambiguity; disclosure status of visual plates | Never cherry-pick successes or tune test thresholds from errors |
| **T23** `figure_table.md` | Reproducible visual asset spec / `10_Figures_Tables/specs/FIG####.md` or `TAB####.md` | Purpose; source `EVAL`/`XAIA`/`STAT` hashes; script path & exact CLI command; code revision; axes/units/CI rules; caption; output path; PHI/license disclosure sign-off; manuscript locations | Never hand-edit plotted metrics; clear every mammogram image |
| **T24** `gate_audit.md` | Quality gate PASS/FAIL assessment / `01_Project_Management/reviews/G##_assessment_<date>.md` | `AssessmentID`, `GateID`, bound `EntityVersions`; itemized mandatory criteria table with evidence paths & hashes; overall PASS/FAIL; assessor/date; human sign-off; invalidated descendants | Zero prechecked boxes; missing evidence is strictly FAIL |
| **T25** `reproduce.md` | Clean-environment reproducibility audit / `12_Documentation/reproducibility_audit.md` | Fresh runtime & lock hashes; artifact retrieval & SHA-256 verification; exact CLI replay commands; predeclared numeric tolerances vs observed deltas (metrics, stats, XAI); declared reproduction level; lawful external-access limits | Distinguish inference/XAI replay from full retraining honestly |
| **T26** `claim_tripod_checklist.md` | Q1 medical-AI reporting checklists / `12_Documentation/claim_tripod_checklist.md` | Complete item-by-item CLAIM 2024 and TRIPOD+AI tables mapping every required item to exact artifact path, section/page locator, status (`reported` / `not_applicable_with_reason`), and auditor sign-off | Do not claim compliance without line-item artifact mapping |
| **T27** `writing_unit.md` | Evidence-linked section/chapter draft / `11_Writing/` | `WR####`; target document (thesis vs Q1 paper); RQs; linked `CLAIM`/`P`/`EXP`/`EVAL`/`XAIA`/`STAT`/`FIG`/`TAB` IDs; prose; explicit limitations; `[Evidence pending]` queue; review state | Zero fabricated placeholder metrics or unverified citations |
| **T28** `review_response.md` | Internal/supervisor review ledger / `11_Writing/reviews/` | Comment ID; reviewer & date; verbatim comment; classification; action; changed section/diff; evidence ID; response; disposition | Never fabricate feedback from blank page 11 lines |
| **T29** `q1_cover_rebuttal.md` | Q1 journal cover letter, highlights & peer-review rebuttal / `11_Writing/paper/reviews/` | Target journal & Aims/Scope fit; structured cover letter (novelty, clinical relevance, CLAIM/TRIPOD+AI compliance, ethical/data disclosures); highlights; point-by-point reviewer rebuttal table (`CommentID`, verbatim critique, response, manuscript diff, new `EXP`/`EVAL` ID if rerun, status) | New peer-review experiments must reenter gated pipeline (`STEP-027–036`) |
| **T30** `submission.md` | Document-scoped submission & receipt record / `11_Writing/thesis/submission.md` or `paper/submission.md` | Document & version; venue/portal instructions; exact submitted files & SHA-256 hashes; `G15` AssessmentID; author/supervisor sign-offs; submission date; portal receipt/confirmation ID (or approved deferral disposition) | Distinguish prepared, submitted (with receipt), and accepted |
| **T31** `archive.md` | Immutable archival & restoration record / `15_Archive/ARCH####.md` | `ARCH####` & Git release tag; tiered artifact inventory with SHA-256 & byte sizes; sensitivity & license classification; retention owner & period; restoration test log; submission receipts | Never place restricted mammograms in public archives |
| **T32** `prompt.md` | Bounded AI-assistance prompt spec / `14_Templates_Prompts/` | Role; objective; governing sections & inputs; allowed paths; forbidden edits; epistemic labeling rules; output schema; human boundary; verification checks | Never place PHI, restricted data, or credentials in prompts |
| **T33** `risk_meeting.md` | Risk & milestone review minutes / `01_Project_Management/meetings/` | Attendees & date; evidence-backed progress; active risks/triggers/mitigations; open `UD` items & decisions; action owners & provisional target dates | Forecasts explicitly provisional; never fabricate signatures |
| **T34** `web_deployment.md` | Conditional hosted web-demo record / `16_Web_Demo/DEPLOY####.md` | `DEPLOY####`; platform/tier; HTTPS URL; access mode; commit & container digest; `MODEL`/`PP`/`XAIP` & export hashes; secret store refs (no values); `UD27` privacy/retention settings; STEP-038 parity report; external smoke report; status; superseded ID | Changing model, export, threshold, or Grad-CAM creates a new `DEPLOY####` |
| **T35** `demo_runbook.md` | Conditional defense-day demo script / `16_Web_Demo/demo_runbook.md` | Defense date/venue/network; live HTTPS URL & warm-up protocol; disclosure-cleared sample list; talking points (validation-selected model, locked test/XAI numbers, non-clinical disclaimer); offline container fallback CLI; backup recording/screenshots path; post-defense `UD28` action | Offline fallback must be actually tested without internet |

## 14.3 Copy-ready decision, gate, and configuration skeletons

### Decision record skeleton (`T02`)

```markdown
# DEC#### — [Decision Question]
- **Status:** Unresolved / Human Decision Required
- **UD reference:** UD##
- **Owner / approver / blocking step & gate:**
- **REPORT FACT (`RF##`) locators:**
- **PLANNING RECOMMENDATION options and supporting evidence:**
- **Tradeoffs and rejected alternatives:**
- **Actual human decision / date / approval evidence:**
- **Affected entities, versions, steps, gates, and claims:**
- **Reassessment trigger and rollback/recovery rule:**
```

### Quality gate assessment skeleton (`T24`)

```markdown
# G## Assessment — [Bound Entity / Version]
- **AssessmentID:** GATE####
- **Initial status:** NOT ASSESSED
- **Assessor / date / named human reviewer:**
- **Bound EntityVersions (with SHA-256 hashes):**

| Mandatory Criterion | Evidence Path & SHA-256 Hash | PASS / FAIL | Corrective Action (if FAIL) |
|---|---|---|---|
| | | | |

- **Overall outcome:** [PASS only if 100% of mandatory criteria are evidenced; otherwise FAIL]
- **Invalidated downstream gates/artifacts (if FAIL or superseding):**
- **Reassessment / sign-off record:**
```

### Experiment & XAI configuration skeleton (`T15`)

```yaml
# Planning template ONLY. Any null executable field MUST fail validation before launch.
experiment_id: null
research_question_id: null
purpose: null                  # e.g., baseline | arch_benchmark | ablation | multi_seed | diagnostic_smoke
parent_comparison_id: null
approval_record: null          # DEC####
source_commit: null
data:
  release_id: null             # REL####
  dataset_id: null             # DS####
  label_release_id: null       # LBL####
  split_id: null               # SPLIT####
  preprocessing_id: null       # PP####
  release_manifest_sha256: null
  label_map_sha256: null       # 0=Benign, 1=Malignant
  allowed_partitions: ["train", "val"]   # test & external strictly forbidden in training configs
model:
  candidate_id: null           # MC####
  framework_and_version: null
  architecture: null           # Resolved under UD13
  pretrained_weights_tag: null
  pretrained_weights_sha256: null
  weight_license_record: null
  input_resolution: null
  transfer_learning_schedule:
    stage1_frozen_epochs: null
    stage2_unfrozen_layers: null
    stage2_unfrozen_epochs: null
training:
  seed: null
  deterministic_mode: null
  batch_size: null
  optimizer: null
  lr_stage1: null
  lr_stage2: null
  scheduler: null
  weight_decay: null
  loss_and_imbalance_policy: null
  precision_mode: null
  early_stopping_patience: null
  val_selection_metric: null
  training_only_augmentations: null
xai_linkage:
  xai_protocol_id: null        # XAIP####
  gradcam_target_layer: null
runtime:
  environment_lock_sha256: null  # environment/model/
  hardware_record: null
evaluation_protocol_sha256: null
checkpoint_policy: null
artifact_destination: null
```

<a id="appendix-a"></a>
# Appendix A. Canonical definitions

## A.1 Identifiers and naming

Use stable, zero-padded IDs; never recycle retired or failed IDs. Planning IDs defined in v1.0.0: `RF01–RF20`, `UD01–UD28`, `S01–S16`, `STEP-001` through `STEP-050`, `G01–G17`, and `T01–T35`.

| Entity | ID pattern | Canonical registry / home |
|---|---|---|
| Paper / screening / gap / claim | `P####` / `SCR####` / `GAP####` / `CLAIM####` | `02_Literature/` registries |
| Decision / risk / gate assessment | `DEC####` / `RISK####` / `GATE####` | `01_Project_Management/` registries |
| Dataset candidate / source / release | `CAND####` / `DS####` / `REL####` | `03_Datasets/` registries |
| Diagnostic label & ROI-mask release / XAI protocol | `LBL####` / `XAIP####` | `04_Labels_XAI_Governance/` registries |
| Split / preprocessing / pseudonymous image / patient group | `SPLIT####` / `PP####` / `IMG########` / `PAT########` | `03_Datasets/splits/`, `05_Preprocessing/`, restricted manifests |
| Model candidate / trained model | `MC####` / `MODEL####` | `06_Models/` registries |
| Experiment / execution run / checkpoint | `EXP####` / `RUN####` / `CKPT####` | `07_Experiments/`, `08_Checkpoints/` |
| Evaluation / XAI audit / statistical comparison | `EVAL####` / `XAIA####` / `STAT####` | `09_Evaluation/` registries |
| Figure / table / writing unit | `FIG####` / `TAB####` / `WR####` | `10_Figures_Tables/`, `11_Writing/` |
| Archived release / conditional web deployment | `ARCH####` / `DEPLOY####` | `15_Archive/`, `16_Web_Demo/` |

Use `snake_case` for general files; keep canonical prefixes uppercase. Timestamps follow ISO 8601 (`YYYY-MM-DDTHH:MM:SS±HH:MM`); all artifact digests use SHA-256. Never embed patient identifiers in shared filenames.

## A.2 Versioning and immutability

Documents and schemas use semantic versioning `vMAJOR.MINOR.PATCH`. Scientific entities (`DS`, `LBL`, `XAIP`, `SPLIT`, `PP`, `REL`, `EXP`, `CKPT`, `MODEL`, `EVAL`, `XAIA`, `STAT`, `DEPLOY`, `ARCH`) are **immutable once frozen or launched**; any methodological edit generates a new ID linked via `Supersedes` / `ParentVersion` and marks dependent gates `STALE`.

## A.3 Universal Definition of Done (Universal DoD)

A blueprint step is **Done** only when: (1) its objective and expected outputs exist with verified SHA-256 hashes; (2) actual inputs, code/environment versions, and procedure are documented in the session note; (3) every verification checklist box has objective evidence; (4) required human decisions and applicable quality gates hold current `PASS`; (5) owning CSV registries and documentation are updated without foreign-key errors; (6) permitted Tier-1/Tier-3 artifacts are durably backed up (or local backup confirmed with pending sync explicitly noted if remote is temporarily offline); and (7) a clear handoff points to the next unblocked step. STEP-001 may store initial scope/decision records prior to STEP-002's full repository bootstrap, which brings them into Git.

## A.4 Registry conventions

All canonical registries are UTF-8 CSV files with one header row, RFC 4180 quoting, and semicolon (`;`) delimiters for multi-ID fields. Append six common governance columns once to every registry schema in Appendix B: `Owner,Version,Status,Created,Updated,EvidencePath`. Numeric `0` denotes a measured zero—never a stand-in for `not reported`, `unknown`, or `Unresolved / Human Decision Required`. Initialize registries header-only in STEP-003 (populating only genuine verified STEP-001 decisions/facts); zero fabricated rows.

<a id="appendix-b"></a>
# Appendix B. Registry catalog and schemas

Append the six Appendix A.4 common columns (`Owner,Version,Status,Created,Updated,EvidencePath`) once to each of the 24 canonical CSV registries below:

| # | Registry / canonical path | Key / owner | Required domain columns beyond key and common columns |
|---|---|---|---|
| 1 | Decisions — `01_Project_Management/decisions.csv` | `DEC####` / research lead | `UD,Question,Decision,Approver,ApprovalDate,BlocksStep,OptionsEvidence,Supersedes,AffectedGates` |
| 2 | Risks — `01_Project_Management/risk_register.csv` | `RISK####` / research lead | `Description,Trigger,Probability,Impact,Mitigation,Contingency,ReviewDate` |
| 3 | Gates — `01_Project_Management/gates.csv` | `GATE####` / reviewer | `GateID,EntityVersions,Outcome,CriteriaReport,Assessor,Approval,AssessmentDate,Supersedes,Invalidates` |
| 4 | Papers — `02_Literature/papers.csv` | `P####` / literature lead | `ReportRef,Title,Authors,Year,Venue,DOI,SourceURL,SourceVersion,Access,FullTextPath,MetadataVerified,ReadingStatus,Task,Modality,Paradigm,Dataset,Models,XAIMethods,QuantitativeXAI,SplitLevel,ExternalVal,Limitations,CitationKey` |
| 5 | Screening — `02_Literature/screening.csv` | `SCR####` / literature lead | `PaperID,SearchRecord,Stage,Decision,Reason,Reviewer,ConflictResolution,DuplicateOf` |
| 6 | Research Gaps — `02_Literature/gaps.csv` | `GAP####` / literature lead | `ReportTheme,Statement,SupportingPapers,ContradictingPapers,SearchCoverage,Q1SaturationVerdict,Feasibility,ApprovedRQ,DecisionRecord` |
| 7 | Claims — `02_Literature/claims.csv` | `CLAIM####` / writing lead | `Statement,Scope,PaperIDs,SourceLocators,ExperimentIDs,EvaluationIDs,XAIAuditIDs,StatIDs,AssetIDs,Contradictions,Uncertainty,Verification,WritingIDs` |
| 8 | Dataset Candidates — `03_Datasets/candidates.csv` | `CAND####` / data lead | `Name,OriginalSourceURL,Modality,ParadigmAvailable,RoleCandidate,Access,LicenseDUA,LabelProvenance,ROIMaskAvailable,PatientGroupingMeta,SubgroupMeta,DuplicateOf,SelectionDecision` |
| 9 | Datasets — `03_Datasets/datasets.csv` | `DS####` / data steward | `CandidateID,Role,SourceVersion,Provenance,PermissionRecord,EthicsRecord,LicenseRecord,ManifestHash,ImageCount,PatientCount,CountEvidence,CardPath,RestrictedLocation` |
| 10 | Prepared Releases — `03_Datasets/releases.csv` | `REL####` / data lead | `DatasetID,DatasetVersion,LabelReleaseID,LabelMapHash,SplitID,PreprocessingID,ManifestHash,ImageCount,PatientCount,ROIMaskCount,RestrictedLocation,ParentRelease,ChangeReason` |
| 11 | Diagnostic Labels & ROI Masks — `04_Labels_XAI_Governance/label_registry.csv` | `LBL####` / data lead | `DatasetID,Paradigm,LabelProtocolVersion,LabelProvenanceRule,NormalCasePolicy,BenignCount,MalignantCount,ExcludedCount,ROIMaskCount,MaskAlignmentAudit,ClinicalReviewer,LabelMapHash,ManifestHash,ParentVersion` |
| 12 | XAI Protocols — `04_Labels_XAI_Governance/xai_protocol_registry.csv` | `XAIP####` / XAI lead | `ProtocolPath,MethodsIncluded,TargetLayerMapPath,LogitConvention,FaithfulnessMetrics,SanityCheckProtocol,LocalizationMetrics,StabilityMetrics,QualitativeRubricPath,ProtocolHash,Approver,ParentVersion` |
| 13 | Preprocessing — `05_Preprocessing/preprocessing_registry.csv` | `PP####` / implementer | `InputManifest,Operations,BitDepthPolicy,ArtifactPolicy,CLAHEFlag,ConfigPath,ConfigHash,FitPartition,FitStateHash,CodeRevision,VisualQAReport,OutputManifest` |
| 14 | Model Candidates — `06_Models/candidates.csv` | `MC####` / model lead | `Architecture,ReportDiscrepancySource,FrameworkVersion,SourceURL,PretrainedWeights,WeightLicense,NativeInputSize,ParamCount,GFLOPs,GradCAMTargetLayer,Compatibility,Limitations,SelectionDecision` |
| 15 | Trained Models — `06_Models/model_registry.csv` | `MODEL####` / model lead | `CandidateID,ExperimentID,RunID,CheckpointID,ReleaseID,LabelMapHash,PreprocessingID,XAIProtocolID,CalibratorHash,FrozenThreshold,ExportFormat,ExportHash,ArtifactLocation,CardPath,EvaluationIDs,IntendedUse` |
| 16 | Experiments — `07_Experiments/experiment_registry.csv` | `EXP####` / experiment lead | `RQ,Purpose,ParentComparison,ReleaseID,ModelCandidate,XAIProtocolID,ConfigPath,ConfigHash,SourceCommit,Seed,RunIDs,Start,End,StoppingReason,ValSelectionMetric,ValScore,FailureReport,Conclusion` |
| 17 | Checkpoints — `08_Checkpoints/checkpoint_registry.csv` | `CKPT####` / experiment lead | `ExperimentID,RunID,EpochStep,Role,StateComponents,ConfigHash,ModelHash,ArtifactPath,SHA256,Bytes,BackupPath,RestoreEvidence` |
| 18 | Evaluations — `09_Evaluation/evaluation_registry.csv` | `EVAL####` / evaluation lead | `ExperimentID,ModelID,CheckpointID,ReleaseID,CohortType,Partition,ProtocolHash,FreezeRecord,PredictionHash,CoverageReport,MetricsPath,CalibrationPath,EfficiencyPath,SubgroupPath,ReportPath,Deviations,ParentEvaluation` |
| 19 | XAI Audits — `09_Evaluation/xai_audit_registry.csv` | `XAIA####` / XAI lead | `EvaluationID,ModelID,XAIProtocolID,LabelReleaseID,CohortType,MethodsAudited,FaithfulnessPath,SanityCheckOutcome,SanityPath,LocalizationMaskCount,LocalizationPath,StabilityPath,QualitativeReviewStatus,QualitativePath,ReportPath,Deviations` |
| 20 | Statistical Comparisons — `09_Evaluation/statistical_comparisons.csv` | `STAT####` / evaluation lead | `BaselineEvalID,ComparatorEvalID,CohortType,ClusterUnit,ClusterCount,BootstrapReplicates,BootstrapSeed,PrimaryMetricDelta,CI95Low,CI95High,DeLongPValue,McNemarPValue,MultipleCompMethod,AdjustedPValue,ReportPath` |
| 21 | Assets — `10_Figures_Tables/assets.csv` | `FIG####` or `TAB####` / analyst | `Kind,SourceIDs,DataHash,SpecPath,GeneratorCommand,CodeRevision,OutputPath,Caption,Units,DisclosureReview,VisualReview,WritingIDs` |
| 22 | Writing — `11_Writing/writing_registry.csv` | `WR####` / author | `Document,Section,Topic,ClaimIDs,PaperIDs,EvaluationIDs,XAIAuditIDs,StatIDs,AssetIDs,DraftPath,Reviewer,ReviewState,Revision,MissingEvidence` |
| 23 | Archive — `15_Archive/archive_manifest.csv` | `ArchiveItemID` / release owner | `ArchiveID,ReleaseTag,ItemType,SourcePath,StoredLocation,Version,SHA256,Bytes,Sensitivity,License,Retention,RestoreEvidence,SubmissionReceipt` |
| 24 | Web Deployments (Conditional S16) — `16_Web_Demo/deployment_registry.csv` | `DEPLOY####` / deployment owner | `Platform,Tier,URL,AccessMode,SourceCommit,ImageDigest,ModelID,ExportHash,PreprocessingID,XAIProtocolID,LabelMapHash,DataPolicyRecord,ParityCheckPath,SmokeCheckPath,DeployedAt,TakenDownAt,Supersedes` |

**Subordinate manifests (not duplicate master registries):** `03_Datasets/splits/SPLIT####/manifest.csv` (`ImageID,PatientGroupID,Partition,Laterality,View,SourceHash,DuplicateGroup,AssignmentReason`), `07_Experiments/EXP####/run_manifest.json`, and `16_Web_Demo/samples_manifest.csv`.

**Foreign-key integrity:** Every `REL` resolves `DS/LBL/SPLIT/PP`; every `EXP` resolves `REL/MC/XAIP`; every `MODEL` resolves `EXP/CKPT/REL/PP/XAIP`; every `EVAL` resolves `MODEL/REL/freeze`; every `XAIA` resolves `EVAL/MODEL/XAIP/LBL`; every `STAT` resolves paired `EVAL` IDs; every `DEPLOY` resolves `MODEL/PP/XAIP/commit`; every `FIG/TAB` resolves source hashes; every empirical `CLAIM` resolves `EVAL`/`XAIA`/`STAT`. Unresolved foreign keys fail automated registry checks.

<a id="appendix-c"></a>
# Appendix C. Stage map and dependency chain

This stage map is authoritative and mirrored for navigation in the [blueprint](./BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#stage-map).

| Stage | Steps | Governing sections | Exit gate(s) |
|---|---|---|---|
| **S01** Foundation, scope constitution, and unresolved-decision assignment | 001 | §1, §11 | G01 |
| **S02** Repository architecture, templates, registries, and minimal data runtime | 002–003 | §2, §10, §14, App. A–B | G02 |
| **S03** PRISMA literature search, screening, extraction, and bibliography verification | 004–007 | §3 | Feeds G03 |
| **S04** Novelty/gap verification, Q1 contribution framing, and RQ approval | 008–009 | §1, §3 | G03 |
| **S05** Public mammogram dataset discovery (internal & external), permissions, and raw intake | 010–012 | §4, §10 | Permissions before intake; feeds G04 |
| **S06** Mammogram image integrity, artifact/privacy QC, and dataset suitability approval | 013 | §4 | G04 |
| **S07** Diagnostic label provenance, ROI-mask audit protocol, and prospective XAI governance | 014–015 | §4, §6 | G05 |
| **S08** Label/ROI-mask verification execution, pathology/BI-RADS audit, and verified label freeze | 016–018 | §4, §6 | G06 |
| **S09** Mammography preprocessing design, patient-level leakage-safe splitting, and versioned release | 019–021 | §4 | G07 (020), G08 (021) |
| **S10** Transfer learning architecture roster, model runtime, experiment/XAI/stat plan, and pipeline readiness | 022–026 | §5, §6, §7, §10 | G09 |
| **S11** Multi-architecture CNN training, controlled ablations, multi-seed runs, and checkpoint governance | 027–031 | §5, §10 | G10 (per qualifying EXP at 029, repeated 030–031) |
| **S12** Validation-only model/threshold/calibration selection, final-test freeze, and locked test inference | 032–033 | §7 | G11 (032 before testing) |
| **S13** Q1 classification metrics, calibration, statistical testing, quantitative XAI faithfulness/sanity/localization, and external validation | 034–036 | §6, §7 | G12 |
| **S14** Stratified failure & clinical-alignment XAI review, local CAD prototype, and CLAIM/TRIPOD+AI reproducibility audit | 037–039 | §6, §7, §8 | G13 (037), G14 (039) |
| **S15** Evidence-first writing, FYDP thesis submission, Q1 journal manuscript & peer-review workflow, archival, and closure | 040–047 | §9, §10, §13 | G15 (`thesis` 043; `paper` 045), G16 (047) |
| **S16** Conditional hosted web demonstration (Grad-CAM CAD showcase) for FYDP defense | 048–050 | §8.3, §10, §13 | G17 (050; feeds G16 when UD25 adopted) |

```text
001/G01 → 002–003/G02 → 004–009/G03 → 010–013/G04
→ 014–015/G05 → 016–018/G06 → 019–020/G07 → 021/G08
→ 022–026/G09 → [027 → 028 → 029/G10] → 030 multi-arch benchmark → 031 ablations & multi-seed
→ 032/G11 → 033 locked internal + external inference → [034 metrics/cal/stats + 035 quantitative XAI] → 036/G12
→ 037 subgroups/errors/clinical XAI/G13 → 038 local CAD prototype → 039 clean repro + CLAIM/TRIPOD+AI/G14
→ 040–043/G15(thesis) → 044 thesis submit → 045 Q1 paper [G15(paper) + submit/rebuttal OR approved disposition]
→ 046 tiered archive → 047/G16

Conditional parallel web branch (S16 — executed ONLY if UD25 adopted, alongside 039–044):
038 → 048 scope/model/platform/policy → 049 thin Grad-CAM web app + parity → (G14 PASS) → 050 deploy + fallback/G17 → defense
G17 (or UD25 non-adoption disposition) → 046 archive → 047/G16
Optional non-medical hosting spike (synthetic image, generic CNN, zero research evidence): any time after G02
```

<a id="appendix-d"></a>
# Appendix D. Glossary

- **2D Mammogram (FFDM / SFM):** Two-dimensional X-ray breast radiograph acquired either via Full-Field Digital Mammography (FFDM) or digitized Screen-Film Mammography (SFM), typically in Craniocaudal (CC) and Mediolateral Oblique (MLO) views.
- **BI-RADS:** Breast Imaging-Reporting and Data System standardized radiological lexicon covering assessment categories (0–6) and breast composition density (A: fatty, B: scattered, C: heterogeneously dense, D: extremely dense).
- **Pathology-Confirmed Label:** Diagnostic Benign or Malignant ground truth verified by histopathologic biopsy or surgical specimen rather than radiological suspicion alone.
- **ROI Mask / Patch:** Pixel-level lesion contour or cropped Region of Interest enclosing a mass or calcification cluster; distinct from whole-breast FFDM classification.
- **Connected-Component Grouping:** Graph-based clustering uniting all images sharing patient identity, exam, bilateral views, ROI derivatives, or near-duplicate similarity so zero linked records cross train/val/test partitions.
- **External Cross-Dataset Validation:** Zero-shot evaluation of a frozen model trained on Cohort A directly on an independent Cohort B from different acquisition sites/devices without re-tuning.
- **Grad-CAM:** Gradient-weighted Class Activation Mapping producing spatial visual heatmaps from gradients flowing into a designated convolutional feature layer.
- **XAI Faithfulness (Deletion / Insertion / ROAD):** Quantitative causal test measuring how sharply model predictions drop/rise as top-attributed pixels are removed or revealed under a debiased perturbation baseline.
- **Adebayo Sanity Check:** Model-parameter and data-label randomization test verifying that an XAI saliency map genuinely depends on learned model weights rather than acting as an edge detector.
- **Pointing Game / EBPG:** Quantitative XAI localization metrics testing whether maximum saliency pixel (Pointing Game) or proportion of positive saliency energy (Energy-Based Pointing Game) falls inside a verified lesion ROI mask.
- **Probability Calibration (ECE / Brier Score):** Agreement between predicted Malignant probabilities and empirical event frequencies; Temperature Scaling fits a single validation-only logit temperature to improve calibration without altering AUC-ROC.
- **DeLong's Test & McNemar's Test:** Non-parametric paired hypothesis tests comparing correlated AUC-ROC values (DeLong) and paired binary classification errors (McNemar) on the same test cohort.
- **CLAIM / TRIPOD+AI:** International peer-reviewed reporting checklists for medical imaging AI (CLAIM) and clinical prediction models using AI/ML (TRIPOD+AI).
- **Shortcut Learning ("Right for the Wrong Reasons"):** Accurate classification driven by non-lesion confounders (view markers, borders, scanner artifacts, pectoral muscle) rather than true breast pathology.
- **Conditional Hosted Web Demonstration:** Optional defense-day HTTPS presentation shell running the exact frozen STEP-038 CAD + Grad-CAM path if ratified under `UD25`; strictly non-clinical and non-evaluative.

<a id="appendix-e"></a>
# Appendix E. Acronyms

| Acronym | Meaning |
|---|---|
| AUC-ROC / PR-AUC | Area Under Receiver Operating Characteristic Curve / Area Under Precision-Recall Curve |
| BI-RADS | Breast Imaging-Reporting and Data System |
| CAD | Computer-Aided Diagnosis |
| CC / MLO | Craniocaudal / Mediolateral Oblique (mammographic views; prefixed L/R for laterality) |
| CI | Confidence Interval |
| CLAIM | Checklist for Artificial Intelligence in Medical Imaging |
| CLAHE | Contrast-Limited Adaptive Histogram Equalization |
| CNN | Convolutional Neural Network |
| CO / PO | Course Outcome / Program Outcome |
| DICOM | Digital Imaging and Communications in Medicine |
| DIU | Daffodil International University |
| DoD | Definition of Done |
| DUA | Data Use Agreement |
| EBPG | Energy-Based Pointing Game |
| ECE | Expected Calibration Error |
| FFDM / SFM | Full-Field Digital Mammography / Screen-Film Mammography |
| FN / FP / TN / TP | False Negative / False Positive / True Negative / True Positive |
| FYDP | Final Year Design Project |
| Grad-CAM | Gradient-weighted Class Activation Mapping |
| IoU | Intersection over Union |
| LIME / SHAP | Local Interpretable Model-agnostic Explanations / SHapley Additive exPlanations |
| MCC | Matthews Correlation Coefficient |
| PACS | Picture Archiving and Communication System (excluded by Section 8) |
| PHI | Protected Health Information |
| PRISMA | Preferred Reporting Items for Systematic Reviews and Meta-Analyses |
| QC / QA | Quality Control / Quality Assurance |
| ROAD | Remove And Debias (XAI faithfulness metric) |
| ROI | Region of Interest |
| RQ | Research Question |
| SSIM | Structural Similarity Index Measure |
| TRIPOD+AI | Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis + AI |
| XAI | Explainable Artificial Intelligence |

<a id="appendix-f"></a>
# Appendix F. Source coverage and self-review

## F.1 Complete 11-page source audit and cryptographic provenance

<a id="source-status"></a>
### Workspace source verification — 2026-11-23

All three workspace files were inspected in full prior to authoring: both governance reference Markdown templates were read completely, and all 11 physical pages of `Title_defence_evaluation_report.pdf` were rendered and visually inspected page by page (including handwritten ink citations on p. 6 and handwritten signature/dates on pp. 1 and 11). Only `Title_defence_evaluation_report.pdf` serves as scientific and project authority; the two structural Markdown files provided governance architecture and 20-field step schema only, with zero domain transfer.

| PDF page(s) | Material inspected visually | Exact treatment in this operating system |
|---|---|---|
| **p. 1** | Header (`FYDP (Title Phase) Evaluation Report [Version 2.0]`), DIU CSE Summer 2026, Project Identification I–V & VII (skipping VI): exact title, Alzubair Ahamed (232-15-591), Md Riyadul Hasan (232-15-486), Supervisor Israt Jahan, Co-Supervisor Ms Faiza Feroz, Submission Date 15 August 2026, signed certificate dated `15/8/26` | Cover page; `RF01–RF03`; certificate bounded strictly as title-phase record, not ethics/data/clinical clearance |
| **p. 2** | CO/PO mapping table (CO1→PO1, CO2→PO2, CO3→PO4) & Sec. 1 Introduction start (WHO context, mammography challenges, VGG16/ResNet50/DenseNet121/EfficientNet/InceptionV3) | `RF04`, `RF06–RF07`; preserves exact EfficientNet variant wording discrepancy |
| **p. 3** | Sec. 1 Introduction end (black-box problem; Grad-CAM, LIME, SHAP; Benign vs Malignant binary framework) | `RF05`, `RF08` |
| **p. 4** | Sec. 2 Background Study start (WHO/dense breast/biopsy context; summaries of Khalid et al. [1], Bhise et al. [2] on BreakHis histopathology, Priyanka & Sanjeev [3] review) | `RF17`, Section 3 non-mammogram comparator quarantine |
| **p. 5** | Sec. 2 Background Study end (Rautela et al. [4] review; CNN list adding MobileNetV2 & Xception; XAI list adding Integrated Gradients & Guided Backpropagation; dataset imbalance/diversity limits; Grad-CAM framework proposal) | `RF07–RF08`, `RF16`; preserves Xception & extended XAI mentions under `UD13`, `UD16` |
| **p. 6** | Table 1.1 (SL 1–10) with handwritten ink brackets `[5]`–`[10]`, duplicated printed caption string, SL 10 "Hassan et al. [10]" mismatch, non-mammogram/tabular/review rows; Sec. 3 Problem Statement start | `RF17–RF19`, `UD04`; explicit anomaly quarantine and primary-source verification protocol |
| **p. 7** | Sec. 3 Problem Statement end (provisional novelty claim that most prior research lacks XAI); Sec. 4 Preliminary Novelty Statement start (Grad-CAM + Benign/Malignant) | `RF16`; treated strictly as hypothesis to test & refine for Q1 novelty (`UD03`, STEP-008) |
| **p. 8** | Sec. 4 end (5 CNNs: VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3); Sec. 5 verbatim Research Question; Sec. 6 Objectives 1–6 (Obj. 3 adds MobileNetV2 = 6 CNNs; Obj. 4 lists 6 metrics; Obj. 5 Grad-CAM; Obj. 6 CAD); Sec. 7 Expected Outcome bullet 1 | `RF07–RF13`; preserves exact 5-vs-6 architecture discrepancy under `UD13` and all 6 required metrics (`RF09`) |
| **p. 9** | Sec. 7 Expected Outcome bullets 2–8 (including foundation for future web/mobile decision support); Sec. 8 Scope of Work (7 Inclusions, 6 Exclusions) | `RF13–RF15`; binding Section 1.3 exclusions; informs conditional research-only Section 8.3 defense showcase |
| **p. 10** | Sec. 9 References `[1]`–`[12]` (including Ref [9] missing venue, Ref [10] D. Bazazeh & R. Shubair 2016 contradicting Table 1.1 SL 10, uncited Refs [11]–[12]) | `RF18`, `UD04`; registered strictly as unverified seed leads |
| **p. 11** | Supervisor's Feedback form: comment lines 1, 2, 3 completely blank; handwritten signature (visually matching p. 1 supervisor signature) on `Examiner's Signature:` and handwritten date `15/8/26` on `Date:` | `RF20`, `UD01`; zero feedback comments invented; requires confirmation whether separate feedback exists |

Actual SHA-256 digests computed from the workspace on 2026-11-23 via PowerShell `Get-FileHash -Algorithm SHA256`:

```text
# Sole scientific and project authority:
Title_defence_evaluation_report.pdf
D427EAAE49D875610A9CDA8E8294747F717A7135D4BBE2522D9CDECC8B739AC0

# Structural and governance templates ONLY (zero domain content inherited):
OPG_RESEARCH_OPERATING_SYSTEM.md
C5DE3EE9C343D1202B07FE47A1B0B31155C392E291A23E742B969AA4635A38F0

OPG_PROJECT_EXECUTION_BLUEPRINT.md
9B4E0D31DB5094C6C519DF4667ABB4221B5CF98E6D898BA01325912C35A37975
```

## F.2 Planning-document self-review

Review scope covers planning-document source fidelity, epistemic labeling, Q1 methodological completeness, cross-document alignment, and zero domain contamination. This table is **not** scientific execution evidence and never advances `G01–G17`.

| Review dimension | Planning disposition |
|---|---|
| **Title, team & scope fidelity** | Exact title, DIU metadata, researchers, supervisors, O1–O6, and all 6 Section 8 exclusions preserved verbatim from `Title_defence_evaluation_report.pdf` |
| **Epistemic separation** | Strict three-tier labeling across `RF01–RF20`, `PLANNING RECOMMENDATION`, and `UD01–UD28`; zero invented datasets, counts, splits, hyperparameters, scores, or approvals |
| **Source anomaly preservation** | Architecture discrepancy (`RF07`), Table 1.1 handwritten brackets & SL 10/Ref [10] mismatch (`RF18`), non-mammogram comparators (`RF17`), provisional novelty hypothesis (`RF16`), and blank p. 11 comment lines with visible signature/date (`RF20`) preserved accurately |
| **Mammography & Q1 rigor** | Connected-component patient splitting, FFDM-vs-ROI & Normal-case rules, independent external validation, quantitative XAI (faithfulness/sanity/ROI localization/stability), calibration, clustered bootstrap/DeLong/McNemar tests, CLAIM/TRIPOD+AI checklists, and dual-track `G15 / thesis` + `G15 / paper` integrated |
| **Conditional web demo boundary** | Section 8.3 & Stage S16 (`G17`) explicitly gated by `UD25` as a research-only defense showcase honoring Section 8 hospital/PACS/clinical-trial exclusions |
| **Shared cross-document schema** | 16 stages (`S01–S16`), 50 steps (`STEP-001`–`STEP-050`), 17 gates (`G01–G17`), 28 `UD` items, 24 canonical CSV registries, and 35 templates (`T01–T35`) aligned 1:1 with the companion blueprint |
| **Initial execution state** | All steps `NOT STARTED`; all gates `G01–G17` `NOT ASSESSED`; human ratification pending |

**Next action:** Begin project execution at [STEP-001](./BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-001). Never mark any gate `PASS` until actual dated, hashed evidence exists.

*End of BC-XAI Research Operating System — v1.0.0.*

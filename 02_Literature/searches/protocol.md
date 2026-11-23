# PRISMA-Style Systematic Literature Search, Screening, and Quality Appraisal Protocol

| Header Field | Value |
|---|---|
| `Document` | `02_Literature/searches/protocol.md` |
| `Version / Date` | `v1.0.0` / `2026-11-23` |
| `Owner` | Alzubair Ahamed (Literature Lead, `232-15-591`) & Md Riyadul Hasan (Co-Reviewer, `232-15-486`) |
| `Governing Section` | [OS §1](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [Blueprint STEP-004](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-004) |
| `Decision Reference` | [DEC0003](../../01_Project_Management/decision_log/DEC0003.md) (`UD03` Phase 1: Search & Screening Protocol Approved; Final Q1 Novelty & RQ Lock Pending `STEP-009` / `G03`) |
| `Execution State` | **PROTOCOL APPROVED — ZERO SEARCHES CLAIMED AS EXECUTED YET** *(Actual search execution occurs in `STEP-005`)* |

---

## 1. Purpose and Hypothesis-Challenging Mandate (`RF16`, `UD03`)

The FYDP Title Phase Evaluation Report (`Title_defence_evaluation_report.pdf`, pp. 5, 7–8, `RF16`) proposes four preliminary gap themes (`RG1–RG4`), including the broad assertion that *"most previous research does not integrate Explainable Artificial Intelligence (XAI) techniques into the diagnostic process."*

For a Q1 medical imaging journal (*IEEE Transactions on Medical Imaging*, *Medical Image Analysis*, *Computers in Biology and Medicine*, *Radiology: Artificial Intelligence*), **assuming** that prior mammography studies lack Grad-CAM or XAI is scientifically indefensible. This protocol designs a falsifiable, PRISMA 2020-compliant search that:
1. **Actively hunts for counterevidence** (existing 2D mammography transfer learning + Grad-CAM / Grad-CAM++ / Score-CAM / LayerCAM / SHAP / LIME / Integrated Gradients / ViT-attention studies) so `RG1–RG4` are rigorously tested rather than echoed.
2. **Audits and quarantines every Table 1.1 and Reference `[1]`–`[12]` anomaly (`RF17–RF18`, `UD04`)** from the title report.
3. **Evaluates Q1 methodological gaps** across existing mammography + XAI papers:
   - *Quantitative XAI validation:* Do existing studies perform causal perturbation faithfulness (Deletion, Insertion, ROAD), Adebayo model/data randomization sanity checks, and lesion ROI-mask localization (Pointing Game, EBPG, IoU/Dice), or do they rely solely on cherry-picked qualitative heatmaps?
   - *Multi-center generalization & leakage:* Do existing studies enforce connected-component patient/laterality/view grouping and zero-shot cross-dataset external validation across the 6 public 2D mammogram cohorts (**CBIS-DDSM, INbreast, VinDr-Mammo, CMMD, MIAS, BCDR/DMID/RSNA**), or do they suffer from image-level split leakage and single-dataset overfitting?
   - *Clinical calibration & statistical rigor:* Do existing studies report probability calibration (ECE, Brier score, reliability diagrams), sensitivity-anchored clinical operating points, patient-clustered bootstrap 95% confidence intervals, and paired DeLong/McNemar tests with multiple-comparison correction?

---

## 2. Database Sources and Access Governance (`UD03`)

| Source ID | Database / Portal | Target Domain | Access & Logging Rule |
|---|---|---|---|
| `DB01` | **PubMed / MEDLINE** (NCBI) | Biomedical, radiology, breast imaging AI | Open search & metadata export; log exact query, date, and PMID list in `T04` |
| `DB02` | **IEEE Xplore** | Medical imaging, computer vision, transfer learning, XAI | Log exact query string, filters, and export hash; note full-text subscription boundaries |
| `DB03` | **Scopus / Web of Science / Crossref / OpenAlex** | Multidisciplinary Q1 indexing & citation metadata verification | Use accessible indexing APIs/portals; log exact service used and any institutional subscription limitation honestly |
| `DB04` | **ScienceDirect (Elsevier) & SpringerLink** | *Medical Image Analysis*, *Computers in Biology and Medicine*, *Archives of Computational Methods in Engineering*, etc. | Log exact Boolean string and publisher metadata verification |
| `DB05` | **arXiv / medRxiv / Semantic Scholar** | Recent preprints & full-text discovery | Tag preprints explicitly (`SourceVersion = preprint`); link to final peer-reviewed journal versions via `DuplicateOf` |
| `SEED` | **Title Report References `[1]`–`[12]` & Table 1.1 (`SL 1–10`)** | Mandatory primary-source verification & anomaly remediation (`UD04`) | Register every seed reference with `ReportRef = [1]..[12]` (and separate `SL10_Hassan` anomaly tracking) and `MetadataVerified = unverified` until publisher record is checked in `STEP-007` |

> **Coverage Limitation Rule:** Never infer that a paywalled or unindexed article supports our novelty claim. Record `Access = abstract_only` or `restricted_paywall` in `02_Literature/papers.csv` when lawful full text cannot be retrieved.

---

## 3. Database-Specific Boolean Query Families (`Q1–Q4`)

Every search execution in `STEP-005` must log an instance of `T04_search.md` under `02_Literature/searches/` recording the exact query ID, verbatim syntax, date, coverage window (`2016-01-01` to search execution date in `2026`, plus foundational dataset/method papers), retrieved count, and raw export SHA-256 hash.

### Query Family `Q1` — Core 2D Mammography + Transfer Learning CNNs + XAI (Direct `RF16` Challenge)
```text
(mammogram OR mammography OR FFDM OR "digital mammography" OR "breast radiograph")
AND ("breast cancer" OR "breast lesion" OR "breast mass" OR microcalcification OR "benign" OR "malignant")
AND ("deep learning" OR "transfer learning" OR "convolutional neural network" OR CNN
     OR VGG16 OR ResNet50 OR DenseNet121 OR EfficientNet OR InceptionV3 OR MobileNetV2 OR Xception
     OR ConvNeXt OR "vision transformer" OR Swin)
AND ("explainable AI" OR XAI OR "explainable artificial intelligence" OR interpretability
     OR "Grad-CAM" OR "Grad-CAM++" OR "Score-CAM" OR "LayerCAM"
     OR "Integrated Gradients" OR "Guided Backpropagation" OR LIME OR SHAP OR saliency)
```

### Query Family `Q2` — Quantitative XAI Faithfulness, Sanity Checks & Lesion ROI Localization in Mammography
```text
(mammogram OR mammography OR "breast cancer screening")
AND ("Grad-CAM" OR XAI OR saliency OR attribution OR "attention map" OR interpretability)
AND (faithfulness OR "deletion" OR "insertion" OR ROAD OR "sanity check" OR Adebayo
     OR "pointing game" OR "energy-based pointing game" OR EBPG
     OR "localization" OR "ROI mask" OR "ground truth mask" OR "radiologist trust" OR "reader study")
```

### Query Family `Q3` — Multi-Dataset / External Validation & Patient-Level Leakage across Target Public Mammogram Cohorts (`UD05`)
```text
("CBIS-DDSM" OR "INbreast" OR "VinDr-Mammo" OR "CMMD" OR "Chinese Mammography Database"
 OR "MIAS" OR "BCDR" OR "DMID" OR "RSNA Screening Mammography")
AND ("deep learning" OR CNN OR "transfer learning" OR "Grad-CAM" OR XAI)
AND ("external validation" OR "cross-dataset" OR "multi-center" OR "multi-dataset"
     OR "domain generalization" OR "patient-level split" OR "data leakage")
```

### Query Family `Q4` — Probability Calibration, Clinical Operating Points & Subgroup Stratification in Mammography AI
```text
(mammogram OR mammography)
AND ("deep learning" OR CNN OR CAD OR "computer-aided diagnosis")
AND ("calibration" OR "Expected Calibration Error" OR ECE OR "Brier score" OR "temperature scaling"
     OR "breast density" OR "BI-RADS" OR "DeLong" OR "McNemar")
```

---

## 4. Deduplication Rules (`STEP-005`)

1. Normalize DOI (lowercase, strip `https://doi.org/` prefix) and title (lowercase alphanumeric, strip punctuation/whitespace).
2. Assign one canonical `P####` ID per unique study in `02_Literature/papers.csv`.
3. When a study appears across multiple databases or as both an arXiv/medRxiv preprint and a peer-reviewed journal paper:
   - Retain the peer-reviewed journal version as the primary `P####` record.
   - Link any secondary preprint/duplicate record via `DuplicateOf = P####` in `02_Literature/screening.csv` so raw database retrieval totals reconcile without double-counting studies.

---

## 5. Two-Stage PRISMA Eligibility Criteria and Modality/Task Buckets (`STEP-006`)

### 5.1 Inclusion Criteria (`INC01–INC04`)
- **`INC01 (Primary Direct Comparator — Bucket B1):`** Peer-reviewed study (or high-relevance recent preprint explicitly tagged as preprint) performing 2D mammogram image classification (FFDM or digitized SFM; whole-breast or lesion ROI) into Benign/Malignant (or BI-RADS diagnostic categories) using deep learning / transfer learning **with** Explainable AI (Grad-CAM or other visual/attribution explanation methods).
- **`INC02 (Direct Mammography DL Baseline — Bucket B2):`** 2D mammogram deep learning classification study on one or more of the target public mammogram datasets (`CBIS-DDSM`, `INbreast`, `VinDr-Mammo`, `CMMD`, `MIAS`, `BCDR`/`DMID`/`RSNA`) providing rigorous patient-level splits, external validation, or calibration benchmarks, even if XAI is absent.
- **`INC03 (Methodological Reference — Bucket B3_METH):`** Foundational methodological paper defining an adopted XAI technique, faithfulness/sanity metric (e.g., Selvaraju et al. Grad-CAM, Chattopadhay et al. Grad-CAM++, Wang et al. Score-CAM, Jiang et al. LayerCAM, Sundararajan et al. Integrated Gradients, Adebayo et al. Sanity Checks, Rong et al. ROAD), statistical test (DeLong, McNemar), or reporting guideline (CLAIM 2024, TRIPOD+AI, PRISMA 2020).
- **`INC04 (Seed Reference / Survey Context — Bucket B4_CTX):`** Title report seed references `[1]`–`[12]` (`RF17–RF18`) retained specifically for mandatory `UD04` primary-source audit and contextual discussion, strictly segregated from direct 2D mammography performance comparison tables when they use non-mammogram data or review formats.

### 5.2 Explicit Full-Text Exclusion Codes (`EX01–EX09`)
Every record excluded at title/abstract or full-text screening in `02_Literature/screening.csv` must carry **exactly one** deterministic exclusion code:

| Code | Exclusion Reason | Operational Rule |
|---|---|---|
| `EX01_NON_MAMMO_MODALITY` | Primary task uses Histopathology (BreakHis/WSI), Ultrasound, MRI, CT, Thermography, or clinical tabular data (Wisconsin WBCD/WDBC) without 2D mammography experiments | Strictly barred from direct mammography numerical comparison tables (`RF15`, `RF17`); if part of report seed `[1]`–`[12]`, audit under `UD04` and quarantine in `B4_CTX` |
| `EX02_NON_CLASSIFICATION_TASK` | Purely breast-density estimation, pectoral-muscle segmentation, image synthesis/GAN-only, or hardware physics without Benign/Malignant or lesion diagnostic classification | Exclude from direct comparator synthesis |
| `EX03_NO_DL_OR_HANDCRAFTED_ONLY` | Uses only classical handcrafted features + traditional ML without deep learning / transfer learning | Retain only if a report seed reference (`[1]`, `[6]–[8]`, `[10]`) under `B4_CTX` |
| `EX04_DUPLICATE_OR_SUPERSEDED` | Exact duplicate or preprint superseded by an included peer-reviewed journal version | Record `DuplicateOf = P####` |
| `EX05_UNVERIFIABLE_OR_RETRACTED` | Retracted article, predatory/unverifiable bibliographic record, or mismatched citation ghost (e.g., Table 1.1 SL 10 unverified string if no primary source exists) | Quarantine explicitly in `UD04` audit report |
| `EX06_INSUFFICIENT_METHOD_DETAIL` | Extended abstract, short poster, or non-technical commentary lacking dataset, architecture, and metric definitions | Exclude at full-text screening |
| `EX07_NON_ENGLISH_NO_TRANSLATION` | Full text not available in English | Log honestly in PRISMA flow |
| `EX08_FULLTEXT_INACCESSIBLE` | Paywalled full text unavailable through institutional or legal open-access channels | Log as `Access = abstract_only`; never guess full-text methods from abstract |
| `EX09_OUT_OF_SCOPE_CLINICAL` | Oncology wet-lab, genomics, drug trial, or survival/staging-only study (`RF15`) | Exclude at title/abstract screening |

---

## 6. Mandatory Extraction Schema (`T05_paper_summary.md`) and Quality Appraisal Rubric (`STEP-007`)

For every included study (`P####`), extract the following fields from the full text, tables, figures, and supplements (writing `not reported` whenever omitted by the authors—never guessing from library defaults):
1. **Exact Locator-Backed Metadata:** Publisher-verified Authors, Title, Venue, Year, Volume/Issue/Pages, DOI, and `ReportRef` (`[1]`–`[12]` or `none`).
2. **Dataset & Paradigm Integrity:** Dataset name(s) and version, FFDM vs digitized SFM, **Whole-Breast FFDM vs Cropped Lesion ROI/Patch paradigm** (`UD07`), biopsy/pathology vs BI-RADS label definition, Normal (BI-RADS 1) handling (`UD08`), and exact patient/exam/image counts.
3. **Leakage & Generalization Audit:** Split level (`patient_grouped | study_grouped | image_random_leaky | official_split | not_reported`), whether multi-view (CC/MLO) or duplicate crops could leak across train/test, and presence/absence of **independent external cross-dataset validation**.
4. **Transfer Learning & Preprocessing:** Exact CNN/ViT architectures, pretraining source, input resolution, bit-depth handling, CLAHE/artifact removal, imbalance handling, and multi-seed reporting.
5. **XAI Depth & Quantitative Rigor (Critical Q1 Differentiator):**
   - XAI methods used (Grad-CAM, Grad-CAM++, Score-CAM, LayerCAM, Integrated Gradients, Guided Backprop, LIME, SHAP, attention).
   - Target layer reported (`yes_with_layer_name | not_reported`).
   - **Evaluation Mode:** `visual_anecdotes_only` vs `quantitative_faithfulness` (Deletion/Insertion/ROAD) vs `sanity_checked` (Adebayo randomization) vs `roi_mask_localized` (Pointing Game/EBPG/IoU/Dice) vs `clinician_reader_study`.
6. **Metrics & Statistical Rigor (with exact Page/Table/Figure Locators):** Accuracy, Precision, Recall/Sensitivity, Specificity, F1-score, AUC-ROC, PR-AUC, Confusion Matrix, Calibration (ECE/Brier), 95% CIs (patient-clustered vs image-level), and paired hypothesis tests (DeLong/McNemar).

---

## 7. Mandatory Audit Plan for Title Report Table 1.1 & References `[1]`–`[12]` (`UD04`)

During `STEP-005` (registration) and `STEP-007` (verification), execute the following forensic verification checklist on `Title_defence_evaluation_report.pdf` (pp. 4–6, 10):
1. **Handwritten Brackets (`SL 5–10`, p. 6):** Verify the handwritten ink numbers `[5]` through `[10]` in Table 1.1 against printed Section 9 References `[5]` through `[10]` (p. 10).
2. **`SL 10` Mismatch (`"Hassan et al. [10]"` vs Printed Ref `[10]`):** Table 1.1 SL 10 lists `"Hassan et al. [10] | EfficientNet + CNN | Histopathology Dataset | 99%+"`, whereas printed Reference `[10]` on p. 10 is `D. Bazazeh and R. Shubair (2016), "Comparative Study of Machine Learning Algorithms for Breast Cancer Detection"`. Register both leads separately in `STEP-005`, verify Bazazeh & Shubair (2016) from its original publication (Wisconsin tabular ML comparison), and document the `SL 10` mismatch explicitly in `02_Literature/reports/report_bibliography_audit_UD04.md`.
3. **`SL 5` Survey Mismatch (`Nahid et al. [5]`):** Verify A. A. Nahid and Y. Kong (2017) (`[5]`) as a survey paper rather than a single standalone 97% mammography CNN experiment.
4. **Non-Mammogram Comparator Quarantine (`SL 2, 5, 6, 7, 8, 9, 10` and `SL 1` check):** Verify dataset modality for every row in Table 1.1 (including verifying whether Khalid et al. `[1]`, *Diagnostics* 2023, used tabular/Wisconsin or mammogram features) and quarantine all histopathology (`BreakHis`) and tabular (`Wisconsin`) studies into `B4_CTX`.
5. **Incomplete / Uncited References (`[9]`, `[11]`, `[12]`):** Complete missing venue metadata for Tiwari et al. (`[9]`, 2020) and verify exact authoritative URLs/documents for WHO (`[11]`, 2024) and American Cancer Society (`[12]`, 2024).

---

## 8. Living Review and Search Cutoff Schedule

- **Initial Systematic Search Execution:** `STEP-005` (immediately following this `STEP-004` protocol approval).
- **Pre-Model-Selection Refresh:** Prior to `STEP-022` (`UD13`).
- **Pre-Submission Refresh:** Prior to `STEP-045` (`G15 / paper`), logging the exact final search cutoff date in the thesis and Q1 manuscript methods section.

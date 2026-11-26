# PRISMA Systematic Literature Synthesis & Hypothesis Testing (`STEP-007` & `STEP-008`)

| Header Field | Value |
|---|---|
| `DocumentID` | `LITERATURE_SYNTHESIS` |
| `Date` | `2026-11-26` |
| `Stages Covered` | [STEP-005..008](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-007) → Feeds [STEP-009](./research_questions.md) & `G03` |
| `Protocol & Registry Inputs` | [protocol.md](./searches/protocol.md), [screening_summary.md](./searches/screening_summary.md), [papers.csv](./papers.csv), [screening.csv](./screening.csv), [gaps.csv](./gaps.csv), [claims.csv](./claims.csv), [report_bibliography_audit_UD04.md](./reports/report_bibliography_audit_UD04.md) |
| `Governing Rules` | `RF01–RF20`, [OS §3.1–3.4](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md), [DEC0003](../01_Project_Management/decision_log/DEC0003.md), [DEC0004](../01_Project_Management/decision_log/DEC0004.md) |
| `Reviewers` | Alzubair Ahamed (`232-15-591`, Literature Lead) & Md Riyadul Hasan (`232-15-486`, Co-Reviewer) |
| `Gate Status` | `G03: NOT ASSESSED` (Awaiting Supervisor Ratification at `STEP-009`) |

---

## 1. PRISMA 2020 Coverage & Full-Text Verification Scope (`STEP-005`–`STEP-007`)

Across all accessible protocol databases (`GS-Q1a..GS-Q4`, `DB01_PubMed`, `DB03_OpenAlex`, `DB05_arXiv`, plus `Title_defence_evaluation_report.pdf` `SEED` `[1]–[12]` + `SL10`), **`2,207` intake records** were deduplicated (`-711 EX04`) into **`1,496` unique canonical works (`P0001–P1496`)**:

1. **Deep Full-Text `T05` Extracted Core (`48` Studies Verified Direct From PDF / EPMC JATS XML):**
   - **`42 / 42` Curated Local Core PDFs (`P0001–P0042`)**: Every study inside `Paper/` (`Q1`–`Q4`) verified page-by-page across `13` canonical `T05` fields (`02_Literature/summaries/P0001.md–P0042.md`).
   - **`6` Stage-2 Open-Access Landmarks (`P0156`, `P0385`, `P0675`, `P0810`, `P1030`, `P1433`)**: Retrieved lawfully into gitignored `02_Literature/full_texts/` via Europe PMC JATS XML / arXiv / PLOS ONE PDFs and extracted to `T05` cards (`2025–2026` flagship benchmarks on `VinDr-Mammo`, `CMMD`, `EMBED`, `CBIS-DDSM`, and PRISMA XAI rigor).
2. **`UD04` Seed Bibliography Forensic Audit (`13` Leads: `P0063–P0075`):**
   - All `10` rows in `Title_defence_evaluation_report.pdf` `Table 1.1` (`SL 1–10`) plus `[11]` (WHO 2024) and `[12]` (ACS 2024) were audited against primary publisher portals (including `PMC10572157` EPMC XML for `P0063`). All `SL 1–10` rows are formally **retired as quantitative DL benchmarks and quarantined under `B4_CTX` / `Excluded_EX01/EX05/EX06`** ([report_bibliography_audit_UD04.md](./reports/report_bibliography_audit_UD04.md)).
3. **Stage-2 Residual Boundary (`908` Unextracted Stage-1 Candidates):**
   - Out of `914` Stage-1 Open-DB advancing abstracts (`P0076–P1496`), `6` flagship OA works spanning Q1/Q2/Q3/Q4 gaps were verified in full (`P0156, P0385, P0675, P0810, P1030, P1433`). The remaining `908` (`542` residual OA links + `366` paywalled `abstract_only`, alongside `DB02` IEEE Xplore and `DB04` ScienceDirect/SpringerLink institutional subscription blocks logged in `T04_DB02` / `T04_DB04`) remain explicitly labeled `Pending_FullText_*` (`excluded from numeric baseline claims`).

---

## 2. Rigorous Hypothesis Test of Provisional Report Claim (`RF16`)

In `Title_defence_evaluation_report.pdf` (`Sec. 2 p. 5; Sec. 3–4 pp. 7–8`), the provisional hypothesis (`RF16`) asserted that *"most previous research does not integrate Explainable Artificial Intelligence (XAI) techniques into the diagnostic process"*, focuses solely on accuracy, and lacks large/diverse datasets.

| `RF16` Assertion Component | Empirical Evidence & Counterevidence Found | Test Verdict | Verified Replacement Framing (`GAP0001–GAP0005`) |
|---|---|---|---|
| *"Most research omits XAI / Grad-CAM"* | **Refuted numerically:** `335` Stage-1 DB candidates + `17` core PDFs (`P0004–P0024`) + SLRs (`P0003, P0006, P0017, P0018, P0020, P0022, P0156`) apply `Grad-CAM`, `SHAP`, or `LIME` widely. | **PARTIALLY REFUTED / NARROWED** | **Plausibility-vs-Faithfulness & Verification Gap (`GAP0001`, `CLAIM0001`, `CLAIM0003`):** Generic `Grad-CAM` achieves `0.115–0.41` Pointing Game; `~33/35` test box plausibility (`Coherence`), only `8/35` test `Correctness`, `2/14` test external XAI, and **`0` whole-image FFDM studies combine perturbation faithfulness + `Adebayo` checks + ROI localization + calibration**. |
| *"High accuracy without trustworthy evaluation / clinical calibration"* | **Strongly Confirmed:** Leaky pipelines claim `96–99%` (`P0004, P0005, P0023`), while side-level vs patient-level evaluation inflates AUC by **`+17.5` points** (`P0385`); `3/35` assess uncertainty (`P0022`); external shift explodes `ECE` to `0.186–0.446` (`P0034`). | **CONFIRMED & QUANTIFIED** | **Leakage-Controlled Granularity + Calibration Co-Audit Gap (`GAP0002`, `GAP0003`, `CLAIM0002`, `CLAIM0004`)**. |
| *"Limited / imbalanced / low-diversity datasets"* | **Confirmed & Refined:** Only `12%` of datasets report race (`P0022`); `18.5%` validate externally (`P0018`); hardware shift (`Philips vs GE`, `p<0.001`, `P0037`; `SFM vs FFDM`, `P0008, P0034`) breaks transfer; dense Asian tissue (`89.96%` VinDr `C+D`) degrades saliency `-37.3 pp` (`P0810`). | **CONFIRMED & MECHANISTICALLY DEFINED** | **Multi-Vendor Cross-Population Shift & Dense-Breast XAI Fairness Gap (`GAP0003`, `GAP0004`, `CLAIM0005`, `CLAIM0007`, `CLAIM0008`)**. |

---

## 3. Thematic Quantitative Evidence Synthesis (Segregated by Bucket `B1–B4_CTX`)

### 3.1 `Bucket B1` — Direct 2D Mammography DL + XAI Benchmarks (`n = 19` Verified Full Texts: `17` GS + `2` OA `P1030, P1433` + `P0675`)

> **Clean vs Flagged Separation (`GAP0002`):** Studies with pre-split oversampling, unverified patient grouping, or ROI-only cropping are explicitly tagged so `98–99%` leaky artifacts are never averaged with leak-free `0.77–0.90` whole-image benchmarks.

| ID | Study | Dataset(s) & Split Integrity | Paradigm & Resolution | Models | Best Reported AUC / F1 / Acc | XAI Methods & Quantitative Audit | Calibration (`ECE/Brier`) | Verdict |
|---|---|---|---|---|---|---|---|---|
| **`P1030`** | Quy et al. (2026) | `VinDr-Mammo` excl. B3 (`19,070`, `15,256/3,814` official patient/exam split; **no ext**) | Whole FFDM `1024x512` (3-class triage) | **`LENS-B`**, `Swin-B`, `ConvNeXt-B`, `DINOv2-B`, `GMIC` | `LENS-B`: Acc `85.5%`, Macro-F1 `79.6%`, `Macro-AUC 87.6%`; `Swin-B`: `90.2%` | Top-k token routing: **`PG 73.1%` (`86.5%` TPs)**, `Top-8 Hit 81.9%`, `IoU 0.245`; **zero Deletion/Adebayo** | `none` | **Flagship Clean `VinDr` Hybrid** |
| **`P1433`** | Garcia et al. (2026) | `VinDr-Mammo` (`20,000`, `16k/4k` split + `1,410` healthy CF train; **no ext**) | Whole FFDM `1520x912` (binary screening) | `Mammo-CLIP`, `FPN-MIL`, `ConvNeXt`, `ViT` | `Mammo-CLIP`: `AUC 0.848`, `Rec@80Spec 74.7%`; `ConvNeXt 0.802`; `ViT 0.784` | CF data aug only; **zero classifier inference XAI** | `none` | **Clean Full-FFDM Baseline** |
| **`P0012`** | Cerekci et al. (2024) | Private 3-center Turkey (`2,992` women, **patient 75/25**; **no ext**) | Multi-view FFDM | 2-ch `ResNet-50` | Reported `~80%` Acc (`Discussion` typo `88%`) | **`Pointing Game`**: **`Grad-CAM 0.41`**, `Eigen-CAM 0.35`, `Grad-CAM++ 0.30` | `none` | **Core PG Baseline** |
| **`P0013`** | Camurdan et al. (2025) | Turkey `1,976` pts + Ext Siemens `4,276` pts (**patient-disjoint + cross-vendor ext**) | Patch-curriculum FFDM | `ResNeXt50_32x4d` (10 seeds) | Internal `AUC 0.87`, External **`AUC 0.85`** | `Grad-CAM` overlap **`60.26–64.18%`** (int) -> **`57.2–62.88%`** (ext) | `none` | **Strong External FFDM** |
| **`P0014`** | Pertuz et al. (2023) | Finnish External (`382` women / `1,582` imgs, **external test**) | Whole FFDM | `GMIC`, `GLAM`, `DMV-CNN`, `End2End` | External only (modest AUC drop) | Median `Grad-CAM` **Dice vs contour**: `DMV 0.380`, `GMIC 0.291`, `GLAM 0.108`, `End2End 0.042` | `none` | **External XAI Decay Proof** |
| **`P0016`** | Kag et al. (2026) | `CBIS-DDSM` (patient), `Mini-MIAS`, **ext `INbreast` & `VinDr-Mammo`** | Whole image `224x224` + U-Net | `EffNet-B0 (SE/CBAM)`, `Mammo-CLIP`, `GMIC`, `Attn U-Net`, `nnU-Net` | Classification secondary to localization | **CAM PG `<=11.5%`** on `224x224` (`nnU-Net/Attn U-Net >80%`); omits Adebayo/Deletion | `none` | **Flagship Leakage-Free XAI Audit** |
| **`P0675`** | Moffett et al. (2025) | `Duke` (`516` train) -> **Ext `EMBED` (`58` pts) & `iCAD` (`207` pts)** | Mass ROI (`+100 px`) | **`IAIA-BL`**, `ProtoPNet`, `VGG-16` | Malignancy `Duke->EMBED`: `IAIA 0.84->0.74`, `VGG 0.88->0.80`; Margin `0.95->0.63` | **Activation Precision**: `IAIA 0.94->1.00->0.92`; **`VGG Grad-CAM` collapses `0.64->0.16` (iCAD)** | Score shift (`65/76` FP on EMBED); no `ECE` | **External XAI Generalization Proof** |
| **`P0015`** | Kumar et al. (2026) | `CBIS-DDSM` (`90/10` no holdout test), **ext `INbreast`** (+ `BUSI` US!) | Mixed `224x224` | `ExViT-Breast`, `ResNet-50`, `ViT` | High internal `90/10` (`caveat: BUSI mix & 224 res`) | `Grad-CAM++ / LayerCAM / T-LRP`: `Del/Ins 0.62–0.71 (CBIS)`, `0.60–0.70 (INbreast)`, `PG 71.4–80.1%` | Deep ensemble uncertainty | **Mixed-Modality Caveat + Del/Ins Ref** |
| **`P0011`** | Takahashi et al. (2026) | `TOMPEI-CMMD` (`2,436` MLO, patient 3-fold; **no ext**) | Whole MLO `2048x2048` (scratch) | `Masked SwinT V2`, `Masked ViT`, `ResNet50` | Shape guidance helps scratch Transformer | `Grad-CAM` / MSA maps (Appendix overlap numbers omitted) | `none` | **MLO-Only High-Res Reference** |
| **`P0007–P0008`** | Kang (2021); Shia (2025) | Gangnam `821` pts (temp split); Changhua `1,837` -> **ext `CBIS-DDSM`** | Microcalc ROI patches | `5-CNN Ensemble`; `EffNet B0–B4`, `ResNet` | `P0008` crashes **`87% -> 49%`** FFDM->SFM | Qualitative `Grad-CAM` only (`zero PG/Del`) | `none` | **Microcalc FFDM->SFM Collapse** |
| **`P0004, P0005, P0023, P0024`** | Ergun 2025; Ahmmed 2026; Abdelsabour 2026; Sharma 2025 | **`FLAGGED LEAKY / CONFLICTED`:** pre-split aug (`266->1064`, `P0004`); `24->3,937` BI-RADS 5 (`P0023`); unknown splits & `Table 3 vs 4` contradiction (`P0024`) | Mixed whole / ROI | `BCECNN`, `LBNet`, `MobileNetV1+ViT`, `FCCS/GLAM` | Inflated `92–99.0%` claims | Visual anecdotes only (or single-doctor opinion) | `P0024` un-tabulated narrative only | **Methodological Trap Exemplars (`GAP0002`)** |

---

### 3.2 `Bucket B2` & `B3_METH` — Generalization, Calibration, Evaluation Granularity & Density Fairness Anchors

1. **Cross-Sensor & Prevalence Calibration Benchmark (`P0034` Gabbualoy et al., 2026):**
   - Patient-disjoint `CBIS-DDSM (518x518)` trained across `5` backbones (`ResNet-50 0.867` > `Mammo-CLIP B5 0.847` > `Mammo-FM 0.846` > `DINOv2-B14 0.813` > `Rad-DINO 0.703`) collapses zero-shot externally on `CMMD (0.568)`, `DMID (0.547)`, and `MIAS (0.630)`, with **`ECE` surging to `0.186–0.446`** (`temp scaling T=1.38–2.11 reduces ECE by <= 0.049`). **`DAF` density-weighted loss worsens AUC (`0.836->0.806`) and doubles `ECE` (`0.104–0.116`)**. Leaves **zero XAI** audited.
2. **Side-Level vs Patient-Level Granularity Law (`P0385` Mabrok et al., 2026):**
   - Across `16` (`backbone x fusion`) setups on `CMMD` (`706` 4-view patients), **side-level AUC (`0.946`) inflates patient-level AUC (`0.770`) by `+17.5` points**, while `CMMD`'s `96.2%` patient prevalence renders specificity near zero (`0.033–0.220`) and collapses standard BI-RADS probability-averaging to `0.000 macro-AUC`. Demonstrates `ViT-B/16` (`0.874`) trails CNNs (`0.959–0.966`) on modest cohorts and shows `DeLong` overcomes 5-fold Wilcoxon's `p = 0.0625` floor.
3. **Dense-Breast Saliency Fairness Audit (`P0810` Jaheen, 2026):**
   - Exposes `34.1%` naive PG masking a **`-37.3` percentage-point collapse (`p=0.008`)** in chance-normalized `Delta-PG` for `DenseNet-121 Grad-CAM` in dense `CBIS-DDSM` breasts (`98%` glandular parenchyma failures).
4. **Hardware Vendor Drift & `DeLong + Holm-Bonferroni` (`P0037` Rothwell et al., UK NHS `134,217` women):**
   - Proves off-the-shelf Hologic-trained `Mirai` drops significantly on **Philips (`C-index 0.65`, Yr3 `0.62`) vs GE (`C-index 0.74`, Yr3 `0.71`, `p < 0.001`)**, linking `60.8%` of interval cancers to dense tissue (`C+D`) and calling for vendor-specific calibration + validated saliency maps.
5. **High-Sensitivity Clinical Biopsy Triage Metric (`P0038` Liu et al., 2024) & Intrinsic Asymmetry (`P0035` Donnelly et al., 2024):**
   - `P0038` formalizes `Specificity@95%/99%/100% Sensitivity` (`33% Spec@95%Sens`, `AUC 0.72`) with `LIBRA` masking + `DeLong`; `P0035` exposes `-0.05` diagnostic-exam leakage inside Mirai and uses `AsymMirai` prediction windows (`1/25` area) to uncover implant/positioning/calcification confounders.
6. **`CO-12` & `4-Tier` XAI Validation Syntheses (`P0019`, `P0020`, `P0021`, `P0022`, `P0156`) & Dataset FAIR/Metadata Audits (`P0039`, `P0040`, `P0036`, `P0041`, `P0042`):**
   - Define our non-negotiable XAI evaluation contract (`Adebayo` randomization + `Deletion/Insertion/ROAD` + chance-normalized localization + external stability) and dictate dataset segregation (`biopsy vs BI-RADS triage` per `P0039`/`P0040`).

---

### 3.3 `Bucket B4_CTX` — Strictly Segregated & Quarantined Literature

1. **Multimodal Synthetic-Clinical Comparator (`P0033` Ibrahim et al., 2026):** Image-only ablation (`AUC 0.912`) vs multimodal fusion (`0.963`) relies on **synthetically generated clinical tabular attributes** (`out of O6 imaging-only scope`), though `Table 7` (`BI-RADS A 0.978 -> D 0.921`) and reader survey (`42.9%` found cross-modal maps hard) remain helpful contextual references.
2. **Mixed-Modality Dual-Cohort Studies (`P0001` Rana `CBIS+BUSI`, `P0002` Liu `Mini-DDSM+BreakHis` with Fig. 5 mislabeled mammograms):** Off-modality arms quarantined per `RF15`.
3. **Systematic Reviews & Risk/Density Special Tasks (`P0003, P0006, P0010, P0017, P0018, P0156, P0035–P0037, P0041`):** Inform bias (`only 19.15% low QUADAS-2 risk in P0010`), missing external tests (`18.5%` in `P0018`), racial density equity (`P0036` `WashU->EMBED` `42%` Black), and Asian dense-breast epidemiology (`P0041`).
4. **Quarantined `UD04` Seed Leads (`P0063–P0075`):** Zero `SL 1–10` rows retained as numerical baselines ([report_bibliography_audit_UD04.md](./reports/report_bibliography_audit_UD04.md)).

---

## 4. Three Bounded Q1 Contribution Options (Within `O1–O6` & `RF15`) for `G03` Ratification

Per [DEC0003](../01_Project_Management/decision_log/DEC0003.md) Phase 2 (`UD03`) and hard exclusions (`RF15`: no US/MRI/histopath, no staging/survival, no clinical trials, no hospital PACS), the team presents three strictly bounded, feasible Q1 experimental contribution options for Supervisor ratification at **`G03`**:

| Option | Core Q1 Contribution Design (`Inside O1–O6 & RF15`) | Gaps Targeted | Minimum Multi-Dataset Track (`UD05`) | Comparative Rigor & Tradeoffs |
|---|---|---|---|---|
| **Option 1 *(Recommended Flagship Q1 Path)*** | **Calibrated Multi-Architecture 2D Mammography Benchmark With Joint Quantitative XAI Verification & External/Density Audit:** Benchmark the resolved transfer-learning CNN roster (`VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3, MobileNetV2` per `O3`) alongside modern baselines (`ConvNeXt-Tiny`, `Swin-Tiny` / aspect-preserving higher-res `>=512` input) under strict **connected-component patient splits** (`both patient-level & side-level AUCs` per `P0385`), isolated **biopsy pathology (`CMMD, INbreast, CBIS-DDSM, MIAS`) vs BI-RADS screening triage (`VinDr-Mammo`)** tracks (`>=5` cohorts under `UD05`), **probability calibration (`ECE, Brier, Temp Scaling`) + `Spec@95%Sens`**, **zero-shot cross-sensor transfer**, **BI-RADS `A–D` density fairness**, AND **4-pillar quantitative XAI (`Deletion/Insertion/ROAD` faithfulness + `Adebayo` randomization checks + chance-normalized `Delta-PG / EBPG / IoU` across `Grad-CAM, Grad-CAM++, LayerCAM, Score-CAM, IG` + seed stability)** + bounded blinded clinical review. | `GAP0001`, `GAP0002`, `GAP0003`, `GAP0004` | `VinDr-Mammo` (FFDM 3-vendor + boxes + A-D density) + `CMMD` (FFDM biopsy) + `INbreast` (FFDM biopsy + masks) + `CBIS-DDSM` (SFM biopsy + masks + density) + `MIAS` / `DMID` (`>=5` public cohorts) | **Highest Q1 venue fit (*Medical Image Analysis*, *IEEE TMI*, *CIBM*, *Scientific Reports*)**: directly bridges `P0034` (`calibration + shift, no XAI`), `P0675` (`external XAI on ROIs, no ECE`), `P0810` (`dense SFM Delta-PG`), `P0385` (`side-vs-patient`), and `P1030` (`VinDr hybrids, no ext/ECE/Adebayo`). Highest compute/discipline requirement, well within `S05–S15`. |
| **Option 2 *(Focused XAI-Faithfulness & Preprocessing Depth Path)*** | **Resolution, CLAHE & XAI-Method Benchmark Across `3–4` Leak-Free Cohorts (`CBIS-DDSM, INbreast, VinDr-Mammo, CMMD`):** Narrower model set (report's 5–6 ImageNet CNNs + `ConvNeXt`), deeper emphasis on controlled preprocessing ablations (`224x224` vs `512x512`/`1024x512`, `CLAHE vs raw 16-bit`, `loss weighting vs unweighted`) and comparing `5+` CAM/gradient/perturbation XAI methods on `Adebayo` sanity + `Deletion/Insertion` + `Delta-PG`. | `GAP0001`, `GAP0002`, `GAP0004` | `VinDr-Mammo`, `CBIS-DDSM`, `INbreast`, `CMMD` | Faster GPU turnaround than adding Swin/ConvNeXt multi-seed across 6 cohorts; slightly narrower external SFM/population breadth (`MIAS/DMID` omitted or optional). |
| **Option 3 *(Conservative FYDP + Core Calibration Baseline Path)*** | **Leak-Free 6-CNN Transfer Learning + Grad-CAM Sanity/Localization + Calibration Baseline:** Implements all mandatory `RF06–RF14` deliverables (`6` CNNs, `Grad-CAM` + `Grad-CAM++`, patient-disjoint internal + 1 external transfer cohort, `ECE/Brier`, `Pointing Game`, `Deletion AUC`, `Adebayo` sanity check, local CAD prototype + conditional demo). | `GAP0001`, `GAP0002` (partial `GAP0003`) | `CBIS-DDSM` + `INbreast` + `VinDr-Mammo` + `CMMD` | Cleanly satisfies DIU FYDP defense & solid `Sci Rep`/peer-reviewed reproducibility standards, though less competitive for top decile *MedIA / IEEE TMI* without dense-tissue fairness & modern hybrid baselines. |

> **Recommendation for `G03`:** Adopt **Option 1** while sequencing `S05–S11` cleanly so the core `O3` CNN suite runs first on locked `VinDr-Mammo` / `CMMD` / `CBIS-DDSM` / `INbreast` / `MIAS` tracks, followed by the controlled modern-backbone (`ConvNeXt-T / Swin-T`) and resolution/CLAHE ablations under `UD12–UD16`.

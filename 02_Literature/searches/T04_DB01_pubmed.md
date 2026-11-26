# Search Log (`T04`) — `DB01` PubMed (`PM-Q1` to `PM-Q4`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T04` (`T04_search.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DB01_PubMed` |
| `owner` | Alzubair Ahamed (Literature Lead, `232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `EXECUTED_API_EXPORT_AND_STAGE1_SCREENED` |
| `source_inputs` | [protocol.md](./protocol.md) (`DB01`, `Q1–Q4`); [raw_exports/export_sha256_manifest.json](./raw_exports/export_sha256_manifest.json) |
| `governing_section` | [OS §3.1, §14.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | Tier-1 Metadata Log |
| `reviewer` | Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`) |

---

## 1. Database / source

- **`DB01` — PubMed** (`https://pubmed.ncbi.nlm.nih.gov/`), queried reproducibly via NCBI E-utilities (`esearch.fcgi` + `efetch.fcgi` XML) across approved query families `Q1–Q4`.

## 2. Exact Boolean query string

```text
PM-Q1: (mammogram[tiab] OR mammography[tiab] OR FFDM[tiab] OR "digital mammography"[tiab] OR "breast radiograph"[tiab]) AND ("breast cancer"[tiab] OR "breast lesion"[tiab] OR "breast mass"[tiab] OR microcalcification[tiab] OR benign[tiab] OR malignant[tiab]) AND ("deep learning"[tiab] OR "transfer learning"[tiab] OR "convolutional neural network"[tiab] OR CNN[tiab] OR VGG16[tiab] OR ResNet50[tiab] OR DenseNet121[tiab] OR EfficientNet[tiab] OR InceptionV3[tiab] OR MobileNetV2[tiab] OR Xception[tiab] OR ConvNeXt[tiab] OR "vision transformer"[tiab] OR Swin[tiab]) AND ("explainable AI"[tiab] OR XAI[tiab] OR "explainable artificial intelligence"[tiab] OR interpretability[tiab] OR "Grad-CAM"[tiab] OR "Grad-CAM++"[tiab] OR "Score-CAM"[tiab] OR "LayerCAM"[tiab] OR "Integrated Gradients"[tiab] OR "Guided Backpropagation"[tiab] OR LIME[tiab] OR SHAP[tiab] OR saliency[tiab]) AND ("2016/01/01"[PDAT] : "2026/12/31"[PDAT]) AND English[lang]

PM-Q2: (mammogram[tiab] OR mammography[tiab] OR "breast cancer screening"[tiab]) AND ("Grad-CAM"[tiab] OR XAI[tiab] OR saliency[tiab] OR attribution[tiab] OR "attention map"[tiab] OR interpretability[tiab]) AND (faithfulness[tiab] OR deletion[tiab] OR insertion[tiab] OR ROAD[tiab] OR "sanity check"[tiab] OR Adebayo[tiab] OR "pointing game"[tiab] OR "energy-based pointing game"[tiab] OR EBPG[tiab] OR localization[tiab] OR "ROI mask"[tiab] OR "ground truth mask"[tiab] OR "radiologist trust"[tiab] OR "reader study"[tiab]) AND ("2016/01/01"[PDAT] : "2026/12/31"[PDAT]) AND English[lang]

PM-Q3: ("CBIS-DDSM"[tiab] OR INbreast[tiab] OR "VinDr-Mammo"[tiab] OR CMMD[tiab] OR "Chinese Mammography Database"[tiab] OR MIAS[tiab] OR BCDR[tiab] OR DMID[tiab] OR "RSNA Screening Mammography"[tiab]) AND ("deep learning"[tiab] OR CNN[tiab] OR "transfer learning"[tiab] OR "Grad-CAM"[tiab] OR XAI[tiab]) AND ("external validation"[tiab] OR "cross-dataset"[tiab] OR "multi-center"[tiab] OR "multi-dataset"[tiab] OR "domain generalization"[tiab] OR "patient-level split"[tiab] OR "data leakage"[tiab]) AND ("2016/01/01"[PDAT] : "2026/12/31"[PDAT]) AND English[lang]

PM-Q4: (mammogram[tiab] OR mammography[tiab]) AND ("deep learning"[tiab] OR CNN[tiab] OR CAD[tiab] OR "computer-aided diagnosis"[tiab]) AND (calibration[tiab] OR "Expected Calibration Error"[tiab] OR "Brier score"[tiab] OR "temperature scaling"[tiab] OR "breast density"[tiab] OR "BI-RADS"[tiab] OR DeLong[tiab] OR McNemar[tiab]) AND ("2016/01/01"[PDAT] : "2026/12/31"[PDAT]) AND English[lang]
```

## 3. Execution date

- `2026-11-26` (`pubmed_Q1..Q4.json` exported via NCBI E-utilities; Stage-1 `title_abstract` screening completed `2026-11-26`).

## 4. Coverage time window

- `2016-01-01` to `2026-12-31` (`[PDAT]` filter enforced in API queries).

## 5. Filters and language constraints

- `English[lang]` filter applied directly in each E-utilities query; title/abstract `[tiab]` field tags used per [protocol.md](./protocol.md) §2.

## 6. Retrieved record count

| Query | PubMed ESearch Total | Exported Records | Dup vs Existing (`P0001–P0075`) | Cross-Query Dup (New) | Net-New Canonical | Stage-1 Advance (`STEP-007`) | Stage-1 Excluded | Raw Export File (SHA-256 prefix) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `PM-Q1` | 87 | 87 | 11 | 0 | 76 | 64 | 12 | `pubmed_Q1.json` (`fef4cfbd7f6cba23...`) |
| `PM-Q2` | 17 | 17 | 2 | 10 | 5 | 4 | 1 | `pubmed_Q2.json` (`09db28db60301467...`) |
| `PM-Q3` | 20 | 20 | 3 | 5 | 12 | 11 | 1 | `pubmed_Q3.json` (`1dcdeae6b8f2cd4e...`) |
| `PM-Q4` | 242 | 242 | 11 | 12 | 219 | 149 | 70 | `pubmed_Q4.json` (`6202f5175c15ea98...`) |
| **Total (`DB01`)** | **366** | **366** | **27** | **27** | **312** | **228** (`OA:164`, `Abs:64`) | **84** | All 4 verified below |

## 7. Raw export path and SHA-256 hash

- `02_Literature/searches/raw_exports/pubmed_Q1.json` — `SHA256: fef4cfbd7f6cba23db55daf34bfa4f3222f69843ab6a16954c5dc6b25a15e8fe`
- `02_Literature/searches/raw_exports/pubmed_Q2.json` — `SHA256: 09db28db60301467dd0829bdb822b7bdf40f9bfa50a3c25dd13f80da5c6c1a60`
- `02_Literature/searches/raw_exports/pubmed_Q3.json` — `SHA256: 1dcdeae6b8f2cd4efbbddd279147f549698c857f4cb887800ca3a7e0bbeb3651`
- `02_Literature/searches/raw_exports/pubmed_Q4.json` — `SHA256: 6202f5175c15ea9815be6f88099ea2c0bbec76a57f7d99a20eea32f11ba59781`
- Consolidated manifest: `02_Literature/searches/raw_exports/export_sha256_manifest.json`

## 8. Deduplication rules applied

- Deterministic matching by normalized DOI, PMID, arXiv ID, and normalized title against baseline `P0001–P0075` (`27` matches linked via `DuplicateOf`) and across `PM/OA/AX` query exports (`27` internal/cross-DB duplicates linked in `02_Literature/screening.csv`). Peer-reviewed PubMed records were prioritized over repository preprints (`protocol.md` §4).

## 9. Supplementary / snowball search notes

- `PM-Q1..Q4` form the biomedical peer-reviewed anchor alongside `DB03_OpenAlex` and `DB05_arXiv`. Full-text retrieval and `T05` extraction of the `228` Stage-1 advancing candidates (`B1=60`, `B2=128`, `B3_METH=2`, `B4_CTX=38`) proceed in `STEP-007`.

## 10. Access and coverage limitations

- All `366` records returned structured metadata and abstracts/PMIDs; `164 / 228` Stage-1 advancing studies already carry open-access PDF/PMC links in metadata, whereas `64` remain `Access = abstract_only` pending institutional/publisher resolution or honest `EX08_FULLTEXT_INACCESSIBLE` coding in `STEP-007`.

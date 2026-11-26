# Search Log (`T04`) — `DB03` OpenAlex (`OA-Q1` to `OA-Q4`; Institutional Scopus/WoS Substitute)

| Header Field | Value |
|---|---|
| `TemplateID` | `T04` (`T04_search.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DB03_OpenAlex` |
| `owner` | Alzubair Ahamed (Literature Lead, `232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `EXECUTED_API_EXPORT_AND_STAGE1_SCREENED` |
| `source_inputs` | [protocol.md](./protocol.md) (`DB03`, `Q1–Q4`); [raw_exports/export_sha256_manifest.json](./raw_exports/export_sha256_manifest.json) |
| `governing_section` | [OS §3.1, §14.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | Tier-1 Metadata Log |
| `reviewer` | Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`) |

---

## 1. Database / source

- **`DB03` — OpenAlex** (`https://api.openalex.org/works`), executed as the documented open bibliometric substitute for paywalled **Scopus / Web of Science Core Collection** institutional portals (`protocol.md` §2).

## 2. Exact Boolean query string

```text
OA-Q1 filter: title_and_abstract.search:(mammogram OR mammography OR FFDM OR "digital mammography" OR "breast radiograph") AND ("breast cancer" OR "breast lesion" OR "breast mass" OR microcalcification OR benign OR malignant) AND ("deep learning" OR "transfer learning" OR "convolutional neural network" OR CNN OR VGG16 OR ResNet50 OR DenseNet121 OR EfficientNet OR InceptionV3 OR MobileNetV2 OR Xception OR ConvNeXt OR "vision transformer" OR Swin) AND ("explainable AI" OR XAI OR "explainable artificial intelligence" OR interpretability OR "Grad-CAM" OR "Grad-CAM++" OR "Score-CAM" OR "LayerCAM" OR "Integrated Gradients" OR "Guided Backpropagation" OR LIME OR SHAP OR saliency),publication_year:2016-2026,language:en

OA-Q2 filter: title_and_abstract.search:(mammogram OR mammography OR "breast cancer screening") AND ("Grad-CAM" OR XAI OR saliency OR attribution OR "attention map" OR interpretability) AND (faithfulness OR deletion OR insertion OR ROAD OR "sanity check" OR Adebayo OR "pointing game" OR "energy-based pointing game" OR EBPG OR localization OR "ROI mask" OR "ground truth mask" OR "radiologist trust" OR "reader study"),publication_year:2016-2026,language:en

OA-Q3 filter: title_and_abstract.search:("CBIS-DDSM" OR INbreast OR "VinDr-Mammo" OR CMMD OR "Chinese Mammography Database" OR MIAS OR BCDR OR DMID OR "RSNA Screening Mammography") AND ("deep learning" OR CNN OR "transfer learning" OR "Grad-CAM" OR XAI) AND ("external validation" OR "cross-dataset" OR "multi-center" OR "multi-dataset" OR "domain generalization" OR "patient-level split" OR "data leakage"),publication_year:2016-2026,language:en

OA-Q4 filter: title_and_abstract.search:(mammogram OR mammography) AND ("deep learning" OR CNN OR CAD OR "computer-aided diagnosis") AND (calibration OR "Expected Calibration Error" OR "Brier score" OR "temperature scaling" OR "breast density" OR "BI-RADS" OR DeLong OR McNemar),publication_year:2016-2026,language:en
```

## 3. Execution date

- `2026-11-26` (full paged JSON exports completed `2026-11-26`; Stage-1 `title_abstract` screening completed `2026-11-26`).

## 4. Coverage time window

- `2016` to `2026` (`publication_year:2016-2026`).

## 5. Filters and language constraints

- `language:en` filter applied in OpenAlex API; `title_and_abstract.search` across all works; explicit post-export checks retained `EX07_NON_ENGLISH_NO_TRANSLATION` where OpenAlex misclassified bilingual/non-English items (`4` detected).

## 6. Retrieved record count

| Query | OpenAlex Total Count | Exported Records | Dup vs Existing (`P0001–P0075`) | Cross-Query Dup (New) | Net-New Canonical | Stage-1 Advance (`STEP-007`) | Stage-1 Excluded | Raw Export File (SHA-256 prefix) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `OA-Q1` | 640 | 640 | 20 | 87 | 533 | 370 | 163 | `openalex_Q1.json` (`76eeacfb81513cce...`) |
| `OA-Q2` | 206 | 206 | 7 | 82 | 117 | 50 | 67 | `openalex_Q2.json` (`ea98917bcb47fe37...`) |
| `OA-Q3` | 79 | 79 | 4 | 22 | 53 | 29 | 24 | `openalex_Q3.json` (`fef80670c795eacf...`) |
| `OA-Q4` | 669 | 669 | 15 | 279 | 375 | 214 | 161 | `openalex_Q4.json` (`3b23e68be5f7a018...`) |
| **Total (`DB03`)** | **1594** | **1594** | **46** | **470** | **1078** | **663** (`OA:361`, `Abs:302`) | **415** | All 4 verified below |

## 7. Raw export path and SHA-256 hash

- `02_Literature/searches/raw_exports/openalex_Q1.json` — `SHA256: 76eeacfb81513cce1f41a5e81196f82f454f350abcb1c50407d92918b48a8216`
- `02_Literature/searches/raw_exports/openalex_Q2.json` — `SHA256: ea98917bcb47fe37ea8f693cfe987cbd9c3dac9ef7732526b3c7153138d82658`
- `02_Literature/searches/raw_exports/openalex_Q3.json` — `SHA256: fef80670c795eacf6d37c002c619413a774619f34ed542289494f516802815f6`
- `02_Literature/searches/raw_exports/openalex_Q4.json` — `SHA256: 3b23e68be5f7a01893015f8595dbeb3af9c4a8498c8f14116c9a02b3ed188c86`

## 8. Deduplication rules applied

- Deduplicated by normalized DOI, true arXiv ID, normalized title, and preprint-to-journal author+title clustering against `P0001–P0075` (`46` duplicates) and `DB01_PubMed`/`DB05_arXiv`/intra-OpenAlex overlap (`470` duplicates). Published journal/conference versions systematically took canonical precedence over repository preprints (`protocol.md` §4).

## 9. Supplementary / snowball search notes

- `DB03_OpenAlex` captures broad cross-publisher coverage (including IEEE Access/conferences, Springer LNCS, Elsevier, MDPI, Nature/Scientific Reports, arXiv/medRxiv/Research Square). Remaining `663` Stage-1 candidates (`B1=267`, `B2=324`, `B3_METH=2`, `B4_CTX=70`) advance to `STEP-007` full-text assessment.

## 10. Access and coverage limitations

- **Scopus & Web of Science limitation:** Direct Scopus / WoS native exports require institutional subscription credentials (`Elsevier Scopus API` / Clarivate `WoS` entitlement), which are unavailable in the local workspace; `DB03_OpenAlex` serves as the transparent open-index substitute per `protocol.md` §2.
- **Abstract inversion limitation:** OpenAlex omits `abstract_inverted_index` on a subset of publisher-restricted DOIs (particularly some Springer/Elsevier works). Rather than falsely excluding those records, Stage-1 screening conservatively advanced title/venue-consistent records to `STEP-007` for direct landing-page/full-text verification.

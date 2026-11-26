# Search Log (`T04`) — `DB05` arXiv (`AX-Q1` to `AX-Q4`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T04` (`T04_search.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DB05_arXiv` |
| `owner` | Alzubair Ahamed (Literature Lead, `232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `EXECUTED_API_EXPORT_AND_STAGE1_SCREENED` |
| `source_inputs` | [protocol.md](./protocol.md) (`DB05`, `Q1–Q4`); [raw_exports/export_sha256_manifest.json](./raw_exports/export_sha256_manifest.json) |
| `governing_section` | [OS §3.1, §14.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | Tier-1 Metadata Log |
| `reviewer` | Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`) |

---

## 1. Database / source

- **`DB05` — arXiv** (`https://export.arxiv.org/api/query`) covering preprint grey-literature computer vision and medical-imaging XAI manuscripts (`2016–2026`). (Note: dedicated `medRxiv` standalone API search returned no native full-Boolean endpoint equivalent and is captured alongside `OpenAlex` repository records.)

## 2. Exact Boolean query string

```text
AX-Q1: (all:mammogram OR all:mammography OR all:FFDM) AND (all:"deep learning" OR all:"transfer learning" OR all:CNN) AND (all:"explainable AI" OR all:XAI OR all:"Grad-CAM" OR all:saliency OR all:interpretability OR all:SHAP OR all:LIME)

AX-Q2: (all:mammogram OR all:mammography) AND (all:"Grad-CAM" OR all:XAI OR all:saliency OR all:interpretability) AND (all:faithfulness OR all:"pointing game" OR all:localization OR all:"sanity check" OR all:"ROI mask")

AX-Q3: (all:"CBIS-DDSM" OR all:INbreast OR all:"VinDr-Mammo" OR all:CMMD OR all:MIAS OR all:BCDR OR all:DMID) AND (all:"deep learning" OR all:CNN OR all:XAI) AND (all:"external validation" OR all:"cross-dataset" OR all:"domain generalization" OR all:"data leakage")

AX-Q4: (all:mammogram OR all:mammography) AND (all:"deep learning" OR all:CNN OR all:CAD) AND (all:calibration OR all:"Expected Calibration Error" OR all:"Brier score" OR all:"breast density" OR all:"BI-RADS" OR all:DeLong OR all:McNemar)
```

## 3. Execution date

- `2026-11-26` (`arxiv_Q1..Q4.json` exported `2026-11-26`; Stage-1 screening completed `2026-11-26`).

## 4. Coverage time window

- `2016-01-01` to `2026-11-26` (post-query publication year filter `2016–2026`; `1` pre-2016 record in `AX-Q2` filtered out of `139` raw hits leaving `138` records).

## 5. Filters and language constraints

- English arXiv submissions; full metadata (`id`, `published`, `title`, `summary`, `authors`, optional `doi` link) captured.

## 6. Retrieved record count

| Query | arXiv Raw Hits | 2016–2026 Exported | Dup vs Existing (`P0001–P0075`) | Cross-Query/Published Dup (New) | Net-New Canonical | Stage-1 Advance (`STEP-007`) | Stage-1 Excluded | Raw Export File (SHA-256 prefix) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `AX-Q1` | 59 | 59 | 2 | 35 | 22 | 18 | 4 | `arxiv_Q1.json` (`2f23432dd9e09e3d...`) |
| `AX-Q2` | 29 | 28 | 0 | 22 | 6 | 3 | 3 | `arxiv_Q2.json` (`865815bba321c5a8...`) |
| `AX-Q3` | 3 | 3 | 0 | 3 | 0 | 0 | 0 | `arxiv_Q3.json` (`4dd86e84d3b2b9e4...`) |
| `AX-Q4` | 48 | 48 | 1 | 44 | 3 | 2 | 1 | `arxiv_Q4.json` (`b79dba926b6dd569...`) |
| **Total (`DB05`)** | **139** | **138** | **3** | **104** | **31** | **23** (`OA:23`) | **8** | All 4 verified below |

## 7. Raw export path and SHA-256 hash

- `02_Literature/searches/raw_exports/arxiv_Q1.json` — `SHA256: 2f23432dd9e09e3db2849c250805fbf4c38cf09aeb6c5220423b1d119cbb6fbe`
- `02_Literature/searches/raw_exports/arxiv_Q2.json` — `SHA256: 865815bba321c5a89b86712683f1db452dfc222c1772c74a576502ec2f4aaa9e`
- `02_Literature/searches/raw_exports/arxiv_Q3.json` — `SHA256: 4dd86e84d3b2b9e4952a79d51c2fba5ff8108b5af3a60725c25ce72d2eb8e542`
- `02_Literature/searches/raw_exports/arxiv_Q4.json` — `SHA256: b79dba926b6dd569cd8b8832a4e767beb23ff8f56073c943d5d69cecbb12a057`

## 8. Deduplication rules applied

- Per `protocol.md` §4 rule 3, whenever an arXiv preprint also appeared as a peer-reviewed journal or conference paper in `P0001–P0075`, `DB01_PubMed`, or `DB03_OpenAlex` (e.g., McKinney 2020 *Nature Medicine*, Barnett/IAIA-BL 2021 *Nature Machine Intelligence*, Matthews 2021 *Radiology: AI*, Nguyen 2023 *VinDr-Mammo*), the peer-reviewed version was retained canonically (`3` existing + `104` superseded/overlap duplicates linked via `DuplicateOf`). Only `31` standalone un-superseded arXiv records remain canonical (`SourceVersion = preprint`).

## 9. Supplementary / snowball search notes

- `23` Stage-1 advancing arXiv preprints carry direct `/pdf/` links (`Access = open_access_available`) and are tagged `SourceVersion = preprint` so un-refereed claims are clearly isolated during `STEP-007` synthesis.

## 10. Access and coverage limitations

- `DB05_arXiv` provides full open-access PDFs for all retained records, but standalone preprints are non-peer-reviewed (`preprint`) and must not be pooled indistinguishably with peer-reviewed benchmarks without version disclosure (`protocol.md` §4, §5.1).

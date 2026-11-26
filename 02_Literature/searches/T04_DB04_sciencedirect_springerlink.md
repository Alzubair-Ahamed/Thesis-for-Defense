# Search Log (`T04`) — `DB04` ScienceDirect / SpringerLink (`ACCESS_LIMITATION_LOG`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T04` (`T04_search.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DB04_ScienceDirect_SpringerLink` |
| `owner` | Alzubair Ahamed (Literature Lead, `232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `ACCESS_BLOCKED_INSTITUTIONAL_SUBSCRIPTION_REQUIRED` |
| `source_inputs` | [protocol.md](./protocol.md) (`DB04`, §2); [T04_DB03_openalex.md](./T04_DB03_openalex.md) |
| `governing_section` | [OS §3.1, §14.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | Tier-1 Metadata Log |
| `reviewer` | Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`) |

---

## 1. Database / source

- **`DB04` — Elsevier ScienceDirect & SpringerLink / Nature Portfolio** (`https://www.sciencedirect.com/`, `https://link.springer.com/`).

## 2. Exact Boolean query string

- Mapped to protocol query families `Q1–Q4` adapted to Elsevier/Springer syntax (respecting ScienceDirect max 8 Boolean connectors per query clause) per [protocol.md §2](./protocol.md).

## 3. Execution date

- `2026-11-26` (institutional API entitlement check audited; direct publisher bulk export blocked without institutional API keys).

## 4. Coverage time window

- `2016–2026` (per protocol).

## 5. Filters and language constraints

- English language; peer-reviewed research/review articles and LNCS/conference chapters (`2016–2026`).

## 6. Retrieved record count

- **Native ScienceDirect / SpringerLink Export:** `0` direct native publisher export files (blocked — requires Elsevier Developer/Institutional `X-ELS-APIKey` and Springer Nature institutional API token; DO NOT fabricate hit counts).
- **Mitigated Coverage Observed in Executed Corpus:** Elsevier (`European Journal of Radiology`, `Medical Image Analysis`, `Computers in Biology and Medicine`, `CMPB`, etc.) and Springer/Nature (`Scientific Reports`, `Scientific Data`, `Insights into Imaging`, `Artificial Intelligence Review`, `Discover Artificial Intelligence`, `LNCS`, etc.) records were extensively captured via **`DB01_PubMed`** (`366` records), **`DB03_OpenAlex`** (`1,594` records), and **`GS`** (`P0004`–`P0042` open-access PDFs).

## 7. Raw export path and SHA-256 hash

- `none` (direct publisher export blocked; Elsevier/Springer bibliographic records retrieved via `DB01_PubMed` and `DB03_OpenAlex` JSON exports in `02_Literature/searches/raw_exports/`).

## 8. Deduplication rules applied

- Not applicable for native `DB04` file; if institutional portal RIS exports are added later, normalized DOI (`10.1016/...`, `10.1007/...`, `10.1038/...`) deduplication applies cleanly against `02_Literature/papers.csv`.

## 9. Supplementary / snowball search notes

- Paywalled Elsevier/Springer articles without legal open-access PDFs are explicitly marked `Access = abstract_only` in `02_Literature/papers.csv` and will be audited for institutional availability vs `EX08_FULLTEXT_INACCESSIBLE` during `STEP-007`.

## 10. Access and coverage limitations

- **Honest Block Disclosure:** Automated/bulk harvesting from ScienceDirect and SpringerLink requires paid publisher API keys/institutional tokens and connector-limited UI queries; furthermore, Crossref/OpenAlex omits full abstracts on a subset of publisher-restricted Elsevier/Springer DOIs. Stage-1 screening conservatively preserved `abstract_only` missing-abstract candidates whose titles matched mammography DL/XAI criteria (`STEP-007` verification pending).

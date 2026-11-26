# Search Log (`T04`) — `DB02` IEEE Xplore (`ACCESS_LIMITATION_LOG`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T04` (`T04_search.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DB02_IEEE_Xplore` |
| `owner` | Alzubair Ahamed (Literature Lead, `232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `ACCESS_BLOCKED_INSTITUTIONAL_API_KEY_REQUIRED` |
| `source_inputs` | [protocol.md](./protocol.md) (`DB02`, §2); [T04_DB03_openalex.md](./T04_DB03_openalex.md) |
| `governing_section` | [OS §3.1, §14.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | Tier-1 Metadata Log |
| `reviewer` | Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`) |

---

## 1. Database / source

- **`DB02` — IEEE Xplore Digital Library** (`https://ieeexplore.ieee.org/` / `https://ieeexploreapi.ieee.org/api/v1/search/articles`).

## 2. Exact Boolean query string

- Mapped to protocol query families `Q1–Q4` using IEEE Xplore `"All Metadata":...` syntax as defined in [protocol.md §2](./protocol.md).

## 3. Execution date

- `2026-11-26` (API/portal access check audited; direct native export blocked without institutional/developer API key).

## 4. Coverage time window

- `2016–2026` (per protocol).

## 5. Filters and language constraints

- English language; journals and conference proceedings (`2016–2026`).

## 6. Retrieved record count

- **Native IEEE Xplore Portal/API Export:** `0` direct native export files (blocked — no IEEE Xplore API key or institutional subscription session available in workspace; DO NOT fabricate hit counts).
- **Mitigated Coverage Observed in Executed Corpus:** Direct IEEE journals/conferences (`IEEE Access`, `IEEE JBHI`, `IEEE TMI`, `ISBI`, `EMBC`, `CVPRW`) were indexed and retrieved via **`DB03_OpenAlex`** (`1,594` records) and open-access **`Google Scholar`** (`GS` batch, e.g. `P0002`, `P0003`, `P0016`, `P0025`, `P0026`).

## 7. Raw export path and SHA-256 hash

- `none` (direct IEEE Xplore export blocked; proxy IEEE coverage logged inside `02_Literature/searches/raw_exports/openalex_Q1..Q4.json` and `gs_download_manifest.csv`).

## 8. Deduplication rules applied

- Not applicable for native `DB02` file; any future manual institutional export will be deduplicated by normalized DOI (`10.1109/...`) against `02_Literature/papers.csv`.

## 9. Supplementary / snowball search notes

- Institutional library login (if activated before `G03` / thesis defense) or `IEEE Xplore` developer API key can run [protocol.md §2](./protocol.md) `Q1–Q4` directly and merge delta DOIs seamlessly into `02_Literature/papers.csv` and `02_Literature/screening.csv`.

## 10. Access and coverage limitations

- **Honest Block Disclosure:** Programmatic bulk export from IEEE Xplore requires a registered `IEEE Xplore API` key and subscriber institutional entitlement to retrieve paywalled IEEE full-text PDFs. Per OS §1.5 & `protocol.md` §2, this limitation is documented explicitly rather than guessing portal counts; **`DB03_OpenAlex`** partially mitigates metadata indexing gaps.

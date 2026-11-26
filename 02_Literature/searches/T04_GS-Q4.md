# Search Log (`T04`) — GS-Q4 (`Q4` Family, Google Scholar)

| Header Field | Value |
|---|---|
| `TemplateID` | `T04` (`T04_search.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `GS-Q4` |
| `owner` | Alzubair Ahamed (Literature Lead, `232-15-591`) |
| `date` | `2026-11-25` |
| `status` | `EXECUTED_GOOGLE_SCHOLAR_BATCH` |
| `source_inputs` | [protocol.md](./protocol.md) (`Q4`); `Paper/` curated PDF download batch (`2026-11-25`) |
| `governing_section` | [OS §3.1, §14.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | Tier-1 Metadata Log (Copyrighted PDFs excluded from Git via `.gitignore`) |
| `reviewer` | Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`) |

---

## 1. Database / source

- Google Scholar (`https://scholar.google.com/`) — Supplementary full-text PDF discovery query `GS-Q4` mapped to PRISMA protocol family `Q4`.

## 2. Exact Boolean query string

```text
(mammogram OR mammography) ("deep learning" OR CNN OR CAD) (calibration OR "Expected Calibration Error" OR "Brier score" OR "temperature scaling" OR "breast density" OR "BI-RADS" OR DeLong OR McNemar)
```

## 3. Execution date

- `2026-11-25` (downloaded locally into `Paper/` between `2026-11-24` and `2026-11-25`).

## 4. Coverage time window

- `2016-01-01` to `2026-11-25` (Custom range: `2016–2026`).

## 5. Filters and language constraints

- Custom date range `2016–2026`; patents excluded; English language; open-access / lawful full-text PDF retrieval only.

## 6. Retrieved record count

- **Total Google Scholar UI hit estimate ("About N results"):** `not reported` (no bulk RIS/BibTeX export performed; full-text PDFs were downloaded directly from top-ranked accessible results).
- **Downloaded full-text PDFs in this query batch:** `12` (`10` primary unique records assigned here; `2` cross-query duplicate occurrences; `8` primary records retained in the 42-paper curated local corpus).

## 7. Raw export path and SHA-256 hash

- **Tier-1 Download Manifest:** `02_Literature/searches/gs_download_manifest.csv` (`SHA256: bbeb91e65dc181cbab3c52a831e72860f06852020cc9769ac94f30ca93d38f24`).
- **Local PDF Storage (Gitignored):** `Paper/` (`00_paper_index.csv` records per-PDF SHA-256 digests for all 42 retained PDFs).

## 8. Deduplication rules applied

- Exact SHA-256 digest matching across all 96 downloaded PDFs (`33` exact binary duplicates removed across query batches) followed by normalized DOI and normalized title verification (`1` additional semantic duplicate `1-s2.0-S0720048X2400072X-main.pdf` between `GS-Q1a` and `GS-Q1b` linked via `DuplicateOf = P0012`).

## 9. Supplementary / snowball search notes

- `GS-Q4` is an adapted `<256`-character Google Scholar sub-query derived from approved query family `Q4` in `02_Literature/searches/protocol.md` to prevent Google Scholar query-string truncation.

## 10. Access and coverage limitations

- Paywalled publisher records without accessible OA/institutional PDFs were not retrieved in this batch (`DB01–DB05` structured bibliographic exports from PubMed, IEEE Xplore, OpenAlex/Scopus/WoS, ScienceDirect/SpringerLink, and arXiv/medRxiv remain pending for complete `STEP-005` coverage before `G03`).

# PRISMA 2020 Multi-Database Screening Summary (`STEP-005` & `STEP-006`)

| Header Field | Value |
|---|---|
| `DocumentID` | `PRISMA_SCREENING_SUMMARY` |
| `Date` | `2026-11-26` |
| `StageCompleted` | `STEP-005` (Accessible DBs + GS + SEED) & `STEP-006` (Deduplication + Stage-1 `title_abstract` + GS Full-Text) |
| `ProtocolRef` | [protocol.md](./protocol.md) (`v1.0.0`, `Q1–Q4`, `INC01–INC04`, `EX01–EX09`) |
| `GateStatus` | `G03: NOT ASSESSED` (Full-text OA retrieval, `T05` extraction, and `UD04` seed audit execute in `STEP-007`) |
| `Reviewers` | Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`) |

---

## 1. PRISMA 2020 Quantitative Flow Reconciliation (`GS + DB01 + DB03 + DB05 + SEED`)

Every arithmetic identity below is verified deterministically against [02_Literature/papers.csv](../papers.csv) (`1496` unique records: `P0001–P1496`) and [02_Literature/screening.csv](../screening.csv) (`2207` total screening/dedup rows: `SCR0001–SCR2207`).

```text
+-----------------------------------------------------------------------------+
| PRISMA IDENTIFICATION (ALL SOURCES REGISTERED IN STEP-005)                  |
|                                                                             |
|  * Google Scholar Full-Text Batch (GS-Q1a..GS-Q4):         96 PDFs          |
|  * DB01 PubMed (PM-Q1..PM-Q4, 2016-2026 English):         366 records       |
|  * DB03 OpenAlex (OA-Q1..OA-Q4, 2016-2026 English):     1,594 records       |
|  * DB05 arXiv (AX-Q1..AX-Q4, 139 raw -> 2016-2026):       138 records       |
|  * DB02 IEEE Xplore / DB04 ScienceDirect-Springer:          0 native (paywall/API logged) |
|  -------------------------------------------------------------------------  |
|  Database & Search Exports Total:                       2,194 records       |
|  + Title Defense Report Seed Leads (SEED [1]-[12]+SL10):   13 leads         |
|  =========================================================================  |
|  TOTAL INTAKE RECORDS LOGGED IN screening.csv:          2,207 records       |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| PRISMA DEDUPLICATION (EX04_DUPLICATE_OR_SUPERSEDED)                         |
|                                                                             |
|  * GS Batch Binary SHA-256 + Semantic Duplicates:          34 removed       |
|  * Open-DB Matches vs Existing GS Corpus (P0001-P0062):    76 removed       |
|  * Open-DB Cross-Query / Cross-DB / Preprint Merges:      601 removed       |
|  -------------------------------------------------------------------------  |
|  TOTAL DUPLICATES REMOVED (EX04):                        -711 records       |
|  =========================================================================  |
|  UNIQUE RECORDS ENTERING SCREENING:                     1,496 studies       |
|    (62 GS PDFs + 1,421 Open-DB + 13 Unverified SEED)                        |
+-----------------------------------------------------------------------------+
             |                               |                         |
             v                               v                         v
+-------------------------+   +-----------------------------+   +-------------+
| GS LOCAL FULL-TEXT      |   | OPEN-DB STAGE-1 SCREENING   |   | REPORT SEED |
| SCREENING (COMPLETE)    |   | (title_abstract COMPLETE)   |   | (UD04 QUEUE)|
|                         |   |                             |   |             |
| Assessed Full-Text:  62 |   | Screened Title/Abs:   1,421 |   | Registered  |
| Excluded Full-Text: -20 |   | Excluded Title/Abs:    -507 |   | Unverified: |
| ----------------------- |   | --------------------------- |   |          13 |
| INCLUDED & VERIFIED: 42 |   | ADVANCE TO FULL-TEXT:   914 |   |             |
|   B1=17, B2=9,          |   |   OA URL Avail:         548 |   | (Pending    |
|   B3_METH=6, B4_CTX=10  |   |   Abstract-Only/Paywall:366 |   |  STEP-007   |
| (In Paper/, gitignored) |   | (Pending STEP-007 Full-Text)|   |  UD04 Audit)|
+-------------------------+   +-----------------------------+   +-------------+
```

### Exact Mathematical Reconciliation Checks
1. **Raw Intake Check:** `96 (GS) + 366 (DB01) + 1,594 (DB03) + 138 (DB05) + 13 (SEED) = 2,207` rows (`SCR0001–SCR2207`).
2. **Deduplication Balance:** `2,207 - (34 + 76 + 601) = 1,496` unique canonical studies (`P0001–P1496`).
3. **Screening Coverage Balance:** `62 (GS full-text) + 1,421 (DB title/abstract) + 13 (SEED intake) = 1,496` studies (`100%` of `papers.csv` accounted for with zero unscreened orphans).
4. **Full-Text Queue Entering `STEP-007`:** `42` (already retrieved & verified local PDFs awaiting `T05` deep extraction) `+ 914` (`Pending_FullText` candidates from `DB01+DB03+DB05`, including `548` with open-access URLs and `366` marked `Access = abstract_only`) `+ 13` (`SEED` `UD04` verification targets).

---

## 2. Database & Query Coverage Breakdown

| Source ID | Source Portal / Batch | Status | Raw Exported | Dup vs Existing | Cross/Self Dup | Net-New Unique | Stage-1 Advance (`STEP-007`) | Stage-1/FT Excluded | Search Log (`T04`) |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `GS-Q1a..GS-Q4` | Google Scholar Curated PDF Batch | Complete (Full-Text) | 96 | 0 | 34 | 62 | 42 *(Included)* | 20 *(Full-Text)* | [T04_GS-Q1a..Q4](./T04_GS-Q1a.md) |
| `DB01` | PubMed (`PM-Q1..Q4`, `2016–2026`, English) | Complete (Stage 1) | 366 | 27 | 27 | 312 | 228 | 84 | [T04_DB01_pubmed.md](./T04_DB01_pubmed.md) |
| `DB02` | IEEE Xplore | Blocked (No API key) | 0 | 0 | 0 | 0 | 0 | 0 | [T04_DB02_ieee_xplore.md](./T04_DB02_ieee_xplore.md) |
| `DB03` | OpenAlex (`OA-Q1..Q4`, Scopus/WoS open proxy) | Complete (Stage 1) | 1,594 | 46 | 470 | 1,078 | 663 | 415 | [T04_DB03_openalex.md](./T04_DB03_openalex.md) |
| `DB04` | ScienceDirect / SpringerLink | Blocked (Subscription) | 0 | 0 | 0 | 0 | 0 | 0 | [T04_DB04_sciencedirect_springerlink.md](./T04_DB04_sciencedirect_springerlink.md) |
| `DB05` | arXiv (`AX-Q1..Q4`, 139 raw -> `2016–2026`) | Complete (Stage 1) | 138 | 3 | 104 | 31 | 23 | 8 | [T04_DB05_arxiv.md](./T04_DB05_arxiv.md) |
| `SEED` | `Title_defence_evaluation_report.pdf` `[1]–[12]`+`SL10` | Registered (`UD04` queue) | 13 | 0 | 0 | 13 | 13 *(UD04 pending)* | 0 | [T04_SEED_title_report.md](./T04_SEED_title_report.md) |
| **ALL** | **Total Portfolio** | **STEP-005/006 Done** | **2,207** | **76** | **635** | **1,496** | **42 FT + 914 TA + 13 SEED** | **527** (`507 TA + 20 FT`) | **Verified** |

- **Publication Version Composition across the `1,421` Net-New DB Studies:** `1244` peer-reviewed/published articles or proceedings (`journal_published`) and `177` preprints (`preprint`, retained strictly when no published equivalent existed).

---

## 3. Inclusion Buckets Breakdown

| Bucket / Decision | Description (`protocol.md` §5.1) | GS Full-Text Verified (`P0001–P0042`) | Open-DB Stage-1 Advance (`Pending_FullText`) | Combined Pre-Extraction Pool |
|---|---|---:|---:|---:|
| `INC01` -> **`B1`** | Primary Direct Comparator (2D Mammography + DL + XAI) | 17 | 335 | 352 |
| `INC02` -> **`B2`** | Direct Mammography DL / Benchmark / External Val / Calibration Comparator | 9 | 466 | 475 |
| `INC03` -> **`B3_METH`** | XAI Evaluation Framework / Faithfulness / Dataset / Reporting Methods | 6 | 4 | 10 |
| `INC04` -> **`B4_CTX`** | Systematic Reviews / Multi-Modal Quarantine Context | 10 | 109 | 119 |
| **Total Included / Advanced** | | **42** | **914** | **956** |

---

## 4. Explicit Exclusion Reason Breakdown (`EX01–EX09`)

| Exclusion Code (`protocol.md` §5.2) | Operational Reason | GS Full-Text Excluded | Open-DB Title/Abstract Excluded | Total Excluded |
|---|---|---:|---:|---:|
| `EX01_NON_MAMMO_MODALITY` | Off-modality (US/Histopath/MRI/Thermography/CT/DBT-only/CEM-only/Non-breast/NLP) | 10 | 233 | 243 |
| `EX02_NON_CLASSIFICATION_TASK` | Pectoral/glandular segmentation, synthesis/GAN/QA, or density-only without benchmark/XAI | 2 | 75 | 77 |
| `EX03_NO_DL_OR_HANDCRAFTED_ONLY` | Handcrafted features + classical ML only or no AI/DL model | 0 | 51 | 51 |
| `EX05_UNVERIFIABLE_OR_RETRACTED` | Integrity red flags, paratext stubs, retractions, or errata | 3 | 2 | 5 |
| `EX06_INSUFFICIENT_METHOD_DETAIL` | Editorial, letter, conference abstract, dataset/code stub, dissertation, textbook chapter, or method-deficit | 5 | 118 | 123 |
| `EX07_NON_ENGLISH_NO_TRANSLATION` | Non-English full text | 0 | 4 | 4 |
| `EX08_FULLTEXT_INACCESSIBLE` | Reserved strictly for Stage-2 Full-Text Assessment (`STEP-007`) | 0 | 0 *(366 `abstract_only` flagged for `STEP-007`)* | 0 |
| `EX09_OUT_OF_SCOPE_CLINICAL` | NAC/pCR, ALN metastasis, molecular receptor prediction, BAC/cardiovascular, or awareness surveys | 0 | 24 | 24 |
| **Total Excluded (excl. `EX04` dups)** | | **20** | **507** | **527** |

*(Plus `711` deduplicated `EX04_DUPLICATE_OR_SUPERSEDED` rows: `34` GS binary/semantic duplicates + `76` open-DB matches against `P0001–P0062` + `601` cross-query/cross-DB/preprint merges.)*

---

## 5. Governance Handoff to `STEP-007` (`G03` Prerequisite)

1. **`P0001–P0042` (`42` local PDFs in gitignored `Paper/`):** Ready immediately for deep locator-backed `T05` extraction (`02_Literature/notes/`), Risk-of-Bias / PROBAST / QUADAS-2 coding (`UD01–UD11`), and `Paper/00_PAPER_INDEX.md` reconciliation.
2. **`P0076–P1496` Stage-1 Advancing Queue (`914` records; `548` OA URLs + `366` `abstract_only`):** Prioritize high-relevance `B1` (`335`), `B3_METH` (`4`), and external-validation/calibration `B2` (`466`) studies with accessible OA full text (e.g., *Diagnostics 2026 Mammography XAI SLR*, *Do Saliency Maps Fail Dense Breasts? 2026*, *CMMD 4-View Side-vs-Patient Benchmark 2026*, *DMID 2024*, *IAIA-BL 2021*, *GMIC 2021*), retrieve full texts via lawful OA channels, and assign final Stage-2 `Included` vs `EX08_FULLTEXT_INACCESSIBLE` / `EX06` decisions before grading **`G03`**.
3. **`P0063–P0075` (`13` Title Report `SEED` Leads):** Resolve `[1]`–`[12]` and `SL10_Hassan` against `Title_defence_evaluation_report.pdf` and primary publisher metadata (`UD04` Audit Report) before locking Chapter 2 (`literature review`) citations.
4. **Git Hygiene Invariant:** All copyrighted/local PDFs inside `Paper/` and `02_Literature/full_texts/` remain strictly excluded from Git via `.gitignore`; only Tier-1 metadata logs, SHA-256 export manifests, BibTeX metadata, and CSV registries live in the repository.

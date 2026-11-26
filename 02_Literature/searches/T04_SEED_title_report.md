# Search Log (`T04`) — SEED (`Title_defence_evaluation_report.pdf` `[1]`–`[12]` & Table 1.1)

| Header Field | Value |
|---|---|
| `TemplateID` | `T04` (`T04_search.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `SEED` |
| `owner` | Alzubair Ahamed (Literature Lead, `232-15-591`) |
| `date` | `2026-11-25` |
| `status` | `REGISTERED_UNVERIFIED_PENDING_STEP-007` |
| `source_inputs` | [protocol.md](./protocol.md) (`SEED`, §7); [OS §1.2 & Appendix F.1](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [DEC0003](../../01_Project_Management/decision_log/DEC0003.md) |
| `governing_section` | [OS §3.2, §14.2](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | Tier-1 Metadata Log |
| `reviewer` | Alzubair Ahamed (`232-15-591`) & Md Riyadul Hasan (`232-15-486`) |

---

## 1. Database / source

- `SEED` — `Title_defence_evaluation_report.pdf` (p. 6 Table 1.1 `SL 1–10` and p. 10 Section 9 References `[1]`–`[12]`) registered for mandatory `UD04` primary-source verification.

## 2. Exact Boolean query string

- `not applicable` (manual seed-reference extraction from approved FYDP Title Defense report per `RF17–RF18` and `protocol.md` §7).

## 3. Execution date

- `2026-11-25` (seed leads `P0063–P0075` registered in `02_Literature/papers.csv`).

## 4. Coverage time window

- `2016–2024` (spanning printed seed references `[1]`–`[12]` plus `SL 10` `"Hassan et al."` anomaly lead).

## 5. Filters and language constraints

- All 12 printed reference entries `[1]`–`[12]` plus distinct `SL10_Hassan` tracking entry retained regardless of modality pending `UD04` audit and `B4_CTX` quarantine.

## 6. Retrieved record count

- `13` seed leads registered (`P0063–P0074` for `[1]`–`[12]`, where `P0072` is Ref `[10]` D. Bazazeh & R. Shubair 2016, plus `P0073` for Table 1.1 `SL 10` `"Hassan et al. [10]"` tracked separately per `protocol.md` §7; `P0074` = WHO `[11]`, `P0075` = ACS `[12]`).

## 7. Raw export path and SHA-256 hash

- Source PDF `Title_defence_evaluation_report.pdf` (`SHA256: D427EAAE49D875610A9CDA8E8294747F717A7135D4BBE2522D9CDECC8B739AC0`, logged in `DEC0001.md` and `OS Appendix F.1`; local gitignored copy resides outside this checkout).

## 8. Deduplication rules applied

- Explicitly prevented premature merging of `SL10_Hassan` (`P0073`) with printed Ref `[10]` Bazazeh & Shubair (`P0072`).

## 9. Supplementary / snowball search notes

- Cross-checking against primary publisher portals and `Title_defence_evaluation_report.pdf` p. 10 for `[6]`–`[8]` exact authors/titles occurs in `STEP-007` (`UD04`).

## 10. Access and coverage limitations

- `Title_defence_evaluation_report.pdf` is excluded from Git by `.gitignore` and is not present in the current working copy; therefore exact bibliographic strings for `[6]`–`[8]` and missing venue/URL details for `[1]`–`[4]`, `[9]`, `[11]`, `[12]` remain `MetadataVerified = unverified` until `STEP-007`.

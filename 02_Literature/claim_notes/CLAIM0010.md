# Claim Record (`T07`) — `CLAIM0010`

| Header Field | Value |
|---|---|
| `TemplateID` | `T07` (`claim.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `CLAIM0010` |
| `owner` | Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `VERIFIED_FROM_LITERATURE` |
| `source_inputs` | `02_Literature/reports/report_bibliography_audit_UD04.md;02_Literature/summaries/P0063.md` |
| `governing_section` | [OS §1.2 `RF17–RF18`](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [DEC0004](../../01_Project_Management/decision_log/DEC0004.md) |

## Statement
All ten existing-work rows (`SL 1–10`) in `Title_defence_evaluation_report.pdf` `Table 1.1` fail eligibility as primary 2D mammography deep-learning comparators due to out-of-scope modalities (`WDBC/WBCD` tabular csvs, `BreakHis`/histopathology), review-article conflation, broken/handwritten citations (`SL10` `Hassan` vs `[10]` `Bazazeh`), and an Abstract-vs-Results `WDBC` mismatch in `[1]` Khalid et al. (2023).

## Exact Primary-Source Evidence (`PaperIDs` & `SourceLocators`)
- `P0063` (`[1]` Khalid et al., *Diagnostics* 2023, `PMC10572157`): Abstract claims `3,002` digital mammograms, yet `Sec. 4 Table 3` & `Sec. 5` prove `Kaggle WDBC` (`569` tabular rows) was evaluated using classical ML (`Random Forest = 96.49%`), directly invalidating `Table 1.1 SL 1` (`[P0063.md](../summaries/P0063.md)`).
- `P0064` (`[2]` Bhise et al. 2021, *IJERT* `10(07)`): `BreakHis` histopathology (`RF15` excluded).
- `P0065` (`[3]` Priyanka & Sanjeev 2021) & `P0066` (`[4]` Rautela et al. 2022): Systematic/literature reviews (`RF17`, `RF19`).
- `P0067` (`[5]` Nahid & Kong 2017): Survey paper mismatched against `SL 5` `"97% CNN"` claim (`RF18`).
- `P0068–P0072` (`[6]–[10]`): Wisconsin tabular comparators (`P0071` Tiwari 2020 omits venue; `P0072` Bazazeh & Shubair 2016 *IEEE ICEDSA* contradicts `P0073` `SL10_Hassan`).
- `P0074–P0075` (`[11]` WHO 2024; `[12]` ACS 2024): Valid epidemiological background sources uncited in body (`RF18`).

## Contradictions & Boundaries
- All `Table 1.1` numerical entries are quarantined (`B4_CTX` / `Excluded`); replaced in full by verified `P0001–P0042` + Stage-2 OA studies (`P0156`, `P0385`, `P0675`, `P0810`, `P1030`, `P1433`). Printed p. 10 strings for `[6]–[8]` await visual check on the local external PDF at `G03`.

# Research Diary (`T03`) — `2026-11-27`: `STEP-011` License, DUA, Custody & Ethics Waiver Audit (`UD06`)

| Header Field | Value |
|---|---|
| `TemplateID` | `T03` (`session.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DIARY_2026-11-27_STEP011_UD06` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Data Steward) & Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-27` |
| `status` | `STEP-011_DOCS_PREPARED_PENDING_HUMAN_AUTHORIZATIONS` |
| `source_inputs` | [access_decision.md](../../03_Datasets/reports/access_decision.md); [DEC0006](../decision_log/DEC0006.md); [candidates.csv](../../03_Datasets/candidates.csv) |

---

## 1. Completed Audit Work (`STEP-011`)
1. Audited primary-source license/DUA terms across all `7` shortlisted `CAND` collections into `03_Datasets/licenses/` and compiled the 5-dimension custody matrix in [access_decision.md](../../03_Datasets/reports/access_decision.md).
2. Identified critical compliance constraints:
   - `CMMD`, `CBIS-DDSM`, `DMID`, and `MIAS v1.21` (`Cambridge Apollo DOI: 10.17863/CAM.105113`) carry open `CC BY` terms (`ready for STEP-012 immediately upon written DIU ethics/waiver determination`).
   - `VinDr-Mammo` (`PhysioNet 1.5.0`) mandates **individual CITI certification**, open-access analysis code, strict private-compute custody, and no public web-demo DICOM redistribution.
   - `INbreast` legacy `inescporto.pt` portal downtime requires direct INESC TEC custodian inquiry (unofficial Kaggle copies explicitly banned).
   - `EMBED` (`Emory RUA`) prohibits public release of trained model weights if trained/finetuned on EMBED -> constrained strictly to **zero-shot held-out external evaluation only** if authorized.
3. Drafted [DEC0006](../decision_log/DEC0006.md) with zero fabricated approval numbers/dates (`ready for DIU Ethics Waiver, PhysioNet CITI, and INESC TEC email submissions`).

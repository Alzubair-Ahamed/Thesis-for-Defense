# Claim Record (`T07`) — `CLAIM0002`

| Header Field | Value |
|---|---|
| `TemplateID` | `T07` (`claim.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `CLAIM0002` |
| `owner` | Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `VERIFIED_FROM_LITERATURE` |
| `source_inputs` | `02_Literature/summaries/{P0004,P0005,P0009,P0023,P0024,P0035,P0385}.md` |
| `governing_section` | [OS §3.2, §4.5](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-007](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-007) |

## Statement
Evaluation granularity mixing (`side-level vs patient-level`), pre-split augmentation/oversampling leakage, diagnostic-vs-screening cohort leakage, and enriched-cohort prevalence distort reported mammography AUC/accuracy by `5–17.5+` percentage points.

## Exact Primary-Source Evidence (`PaperIDs` & `SourceLocators`)
- `P0385` (Mabrok et al., *Future Sci OA* 2026, `Tables 2–4, Sec. 4.4, 5.6`): Across `16` configurations on `706` 4-view `CMMD` patients, side-level AUC averages **`0.946`** (`ConvNeXt-T 0.975`) vs patient-level **`0.770`** (**`+17.5` AUC inflation**, range `12.7–22.4`); `96.2%` patient malignancy prevalence pushes patient-level Specificity to `0.033–0.220` while trivial majority-class gives `96%` accuracy. Single CV fold shifts up to `15%` (`0.989 -> 0.833`).
- `P0035` (Donnelly et al., *Radiology* 2024, `p. 4`): Excluding diagnostic exams leaked in Mirai's original `EMBED` validation reduced 5-year AUC by **`-0.05`** (`0.76 -> 0.71`).
- `P0023` (Abdelsabour et al., *Sci Rep* 2026, `Table 2 p. 6` vs `Fig. 6a p. 19`): Evaluates `9,943` oversampled images (`3,937` BI-RADS 5) from only **`24` raw BI-RADS 5 images (`6` patients)**, inflating accuracy to `99.0%` headline (`vs 98.02%` 5-fold mean).
- `P0004` (Ergun et al., *BMC Med Inform* 2025, `pp. 6–8`): Augmenting `266 -> 1,064` before `90/10` image split leaks near-identical augmented twins into test.
- `P0005` (Ahmmed et al., *Sci Rep* 2026): Pre-CV augmentation and unknown patient deduplication yield `98–99%` claims inconsistent with clean full-image baselines (`0.78–0.90` in `P1030`/`P1433`).

## Contradictions & Boundaries
- Clean patient-level whole-FFDM benchmarks (`P0012` `0.81`, `P0014` `0.62–0.85`, `P0013` `0.87`, `P1030` `0.876–0.902`, `P1433` `0.778–0.848`) consistently establish realistic leak-free operating baselines `10–20` points below ungrouped/augmented-first papers.

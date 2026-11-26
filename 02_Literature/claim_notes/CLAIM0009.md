# Claim Record (`T07`) — `CLAIM0009`

| Header Field | Value |
|---|---|
| `TemplateID` | `T07` (`claim.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `CLAIM0009` |
| `owner` | Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `VERIFIED_FROM_LITERATURE` |
| `source_inputs` | `02_Literature/summaries/{P0004,P0007,P0008,P0034,P0035,P0037,P0038,P0041,P0042,P0385,P1030}.md` |
| `governing_section` | [OS §3.2, §7.4](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-007](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-007) |

## Statement
Methodologically rigorous Q1 statistical inference in mammography requires patient-clustered bootstrap `95%` CIs, paired `DeLong` (`AUC`) and `McNemar`/permutation tests with multiplicity adjustment (`Holm-Bonferroni` or `BH-FDR`), multi-seed variance reporting, and fixed-sensitivity operating points (`Spec@95%Sens` / `Sens@FPR10`).

## Exact Primary-Source Evidence (`PaperIDs` & `SourceLocators`)
- `P0385` (Mabrok et al. 2026, `Sec. 4.6–4.7`): Proves `5-fold Wilcoxon` signed-rank test has a theoretical **`p = 0.0625` floor** (resolving `0/120` model pairs), whereas pooled paired **`DeLong`** (`N=1,412`) resolves `77/120` pairs (`38/78` CNN-CNN); single-split folds swing `±15%` AUC.
- `P0034` (Gabbualoy et al. 2026, `p. 9`): Combines **`5,000` patient-cluster bootstrap resamples**, paired `DeLong`, Stouffer per-seed meta-analysis (`3` seeds), and **`BH-FDR`** adjusted `p`-values + `Sens@95%Spec`.
- `P0037` (Rothwell et al., `p. 9`) & `P0041` (Chen et al. 2025, `Table 4`): Apply **`Holm-Bonferroni`** multiplicity control (`10,000` bootstraps in `P0037`), while `P0041`/`P0042` illustrate why naive normal Wald formulas produce impossible `CI > 1.000` (`1.007, 1.174`) or ignore patient clustering.
- `P1030` (`LENS`, `10,000` paired bootstraps + two-sided permutation + McNemar + `Sen@FPR10`) & `P0038` (Liu et al. 2024, `Specificity@95%/99%/100% Sensitivity` + `DeLong`): Anchor clinical triage thresholding metrics.

## Contradictions & Boundaries
- Most typical Q1–Q2 deep-learning papers (`P0004`, `P0005`, `P0023` non-sig `p=0.6805`, `P0011` single seed per fold, `P1433` point metrics only) omit clustered CIs, multiplicity adjustment, and sensitivity-anchored specificity.

# Claim Record (`T07`) — `CLAIM0005`

| Header Field | Value |
|---|---|
| `TemplateID` | `T07` (`claim.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `CLAIM0005` |
| `owner` | Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `VERIFIED_FROM_LITERATURE` |
| `source_inputs` | `02_Literature/summaries/{P0033,P0034,P0036,P0037,P0039,P0041,P0810}.md` |
| `governing_section` | [OS §3.2, §7.5](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-007](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-007) |

## Statement
Elevated mammographic breast density (`BI-RADS C/D`, comprising `~90%` of East Asian cohorts `VinDr-Mammo` and `Taizhou`) degrades lesion classification discrimination and severely impairs gradient-saliency localization under confounder-aware metrics, while naive density-aware loss weighting (`DAF`) degrades overall AUC and worsens calibration.

## Exact Primary-Source Evidence (`PaperIDs` & `SourceLocators`)
- `P0810` (Jaheen, `arXiv:2611.05909v1`, 2026, `Abstract, Sec. 4`): Chance-normalized `Delta-PG` for `DenseNet-121 Grad-CAM` on `CBIS-DDSM` masses drops by **`-37.3` percentage points** (`p = 0.008` in dense tissue vs `34.1%` naive PG) when adjusted for random chance and breast-mask confounding; `98%` of failures are spurious high-density tissue saliency rather than pectoral edge leaks.
- `P0033` (Ibrahim et al., *Sci Rep* 2026, `Table 7 p. 18`): Classification AUC drops monotonically with increasing BI-RADS density: `BI-RADS A 0.978 -> B 0.968 -> C 0.946 -> D 0.921` (`-0.057` AUC gap).
- `P0034` (Gabbualoy et al., *Sensors* 2026, `Tables 3–4`): Replacing standard CE with **Density-Aware Focal Loss (`DAF`)** monotonically degrades overall `CBIS-DDSM` AUC (`0.836 -> 0.806`) and **doubles calibration error (`ECE 0.104–0.116`)**.
- `P0039` (Nguyen et al. 2023, `Table 4 p. 5`) & `P0041` (Chen et al. 2025, `Table 1 p. 4`): Asian FFDM cohorts exhibit **`89.96%` dense (`C+D`: `VinDr-Mammo`)** and **`89.1%` dense (`Taizhou`)** epidemiology, vs Western cohorts (`WashU 38.9%` in `P0036`; `UK NHS 37.8%` with `60.8%` of ICs in dense breasts in `P0037`).

## Contradictions & Boundaries
- **Nuance (`P0037`):** For future *interval cancer risk* (distinct from present lesion classification), `Mirai` shows no statistically significant AUC gap between low `a+b (0.65)` and high `c+d (0.66)` density (`DeLong p = 0.68`), though `Table 2 (0.56–0.68)` vs text `p. 12 (0.56)` requires caution. `P0013`, `P0016`, `P1030`, and `P1433` omit density-stratified XAI/AUC reporting altogether.

# Claim Record (`T07`) — `CLAIM0003`

| Header Field | Value |
|---|---|
| `TemplateID` | `T07` (`claim.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `CLAIM0003` |
| `owner` | Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `VERIFIED_FROM_LITERATURE` |
| `source_inputs` | `02_Literature/summaries/{P0015,P0016,P0020,P0021,P0022,P0156,P0675,P1030}.md` |
| `governing_section` | [OS §3.2, §6.3](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-007](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-007) |

## Statement
Mammography XAI evaluation remains disproportionately focused on qualitative inspection or lesion-box plausibility (`Coherence`), whereas causal perturbation faithfulness (`Correctness`), `Adebayo` weight-randomization sanity checks, and external cross-site explanation transportability are rarely co-verified—and high lesion focus alone does not guarantee external diagnostic generalization.

## Exact Primary-Source Evidence (`PaperIDs` & `SourceLocators`)
- `P0022` (Ciardiello et al., *Artif Intell Rev* 2026, `Table 1 pp. 24–25`, `Fig. 3`): Among `n=35` `CO-12`-coded mammography XAI papers, `~33` assess `Coherence` vs only `8` testing `Correctness` (faithfulness), `3` testing `Confidence` (uncertainty), and `0` testing `Controllability`; warns plausible heatmaps highlight non-causal suppressor variables (`Wilming 2023`, `Haufe 2024`) and urges mandatory `Adebayo 2018` randomization checks (`p. 12`).
- `P0156` (Pesapane et al., *Diagnostics* 2026 SLR, `Table 4`): Out of `14` peer-reviewed mammography XAI studies (`2015–Jan 2026`), `5/14` remain Tier-1 qualitative only, `7/14` Tier-2 internal quantitative, only **`2/14` (`14.3%`)** reach Tier-3 external interpretability validation, and **`0/14`** complete Tier-4 workflow/reader impact trials.
- `P0020` (Ghauth & Kustiawan 2026, `46` cancer imaging studies): `58.7%` remain qualitative-only (`17.4%` IoU/DSC, `10.9%` strictly quantitative).
- `P0675` (Moffett et al., *PLOS ONE* 2025, `pp. 14–16`): Proves empirically that even when `IAIA-BL` keeps **`0.92–1.00`** `Activation Precision` externally across `Emory` and `iCAD`, malignancy AUC still drops `-0.10` (`0.84 -> 0.74`) under distributional shifts.
- `P0015` (Kumar et al., *Cancer Imaging* 2026) reports internal + `INbreast` `Deletion/Insertion` (`0.60–0.71`) + `PG`, yet omits `Adebayo` checks; `P0016` and `P1030` explicitly list causal perturbation faithfulness and `Adebayo` checks as unresolved future work.

## Contradictions & Boundaries
- Zero reviewed primary empirical papers in the entire corpus simultaneously evaluate all four Q1 XAI pillars (causal `Deletion/Insertion/ROAD` + `Adebayo` model/data randomization + `Pointing Game/IoU` localization + external cross-site audit) on full-image FFDM.

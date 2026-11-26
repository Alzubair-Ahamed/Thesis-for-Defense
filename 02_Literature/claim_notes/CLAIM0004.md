# Claim Record (`T07`) — `CLAIM0004`

| Header Field | Value |
|---|---|
| `TemplateID` | `T07` (`claim.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `CLAIM0004` |
| `owner` | Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `VERIFIED_FROM_LITERATURE` |
| `source_inputs` | `02_Literature/summaries/{P0008,P0015,P0019,P0034,P0037,P0038,P0385,P0675,P1030}.md` |
| `governing_section` | [OS §3.2, §7.3](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-007](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-007) |

## Statement
Probability calibration (`ECE`, `Brier score`) is nearly absent across mammography XAI literature, and under cross-sensor/prevalence shift predicted risk probabilities miscalibrate drastically (`ECE 0.186–0.446`), causing fixed internal operating thresholds to fail externally even after post-hoc temperature scaling.

## Exact Primary-Source Evidence (`PaperIDs` & `SourceLocators`)
- `P0034` (Gabbualoy et al., *Sensors* 2026, `Tables 2–7 pp. 10–17`): On in-distribution `CBIS-DDSM`, `ResNet-50` attains `ECE 0.055, Brier 0.147` (`Mammo-CLIP 0.105`). Under zero-shot external transfer (`CMMD`, `DMID`, `MIAS`), AUC drops `-0.165` to `-0.320` AND **`ECE` explodes to `0.186–0.446`**; standard temperature scaling (`T=1.38–2.11`) trims `ECE` by only `-0.009` to `-0.049`.
- `P0675` (Moffett et al., *PLOS ONE* 2025, `Table 4 p. 12`, `Fig. 7 p. 13`): Locking `IAIA-BL`'s `<20% FPR` threshold (`0.03` on Duke) misclassifies **`65/76` (`85.5%`) benign Emory masses as malignant**, shifting mean benign score from `0.04 ± 0.10 (Duke)` to **`0.37 ± 0.43 (Emory)`**!
- `P0037` (Rothwell et al., UK NHS `134,217` women, `pp. 14–15`): Identifies system-specific calibration drift across `Philips` vs `GE` as an unmet safety prerequisite.
- `P0019` (Borra et al., *Cancers* 2026) & `P0022` (Ciardiello et al. 2026, `Table 1`): Only `3/35` mammography XAI studies report `Confidence` (uncertainty/calibration). Zero local primary studies with `VinDr-Mammo` + XAI (`P0016`, `P1030`, `P1433`) measure `ECE`/`Brier`.

## Contradictions & Boundaries
- `P0024` (Sharma et al. 2025, `Sec. 4.7.4 p. 15`) asserts temperature-scaled `GLAM-Net ECE = 2.8%`, but provides zero calibration table/curve and exhibits severe internal metric conflicts across `Table 3`/`Table 4`/`Fig. 3`; `P0015` (Kumar 2026) evaluates deep-ensemble uncertainty alongside `ExViT`, but omits multi-vendor FFDM external transfer of calibration (`INbreast` only).

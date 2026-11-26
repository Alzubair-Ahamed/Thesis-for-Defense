# Claim Record (`T07`) — `CLAIM0001`

| Header Field | Value |
|---|---|
| `TemplateID` | `T07` (`claim.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `CLAIM0001` |
| `owner` | Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `VERIFIED_FROM_LITERATURE` |
| `source_inputs` | `02_Literature/summaries/{P0012,P0014,P0016,P0022,P0156,P0675}.md` |
| `governing_section` | [OS §3.2–3.3](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-007](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-007) |

## Statement
Post-hoc CNN saliency methods (`Grad-CAM`, `Grad-CAM++`, `Eigen-CAM`, `Score-CAM`, `LayerCAM`) exhibit low quantitative lesion localization reliability in leakage-controlled 2D mammography benchmarks, refuting the assumption that visual overlays establish trustworthy lesion localization.

## Exact Primary-Source Evidence (`PaperIDs` & `SourceLocators`)
- `P0012` (Cerekci et al., *Eur J Radiol* 2024, `p. 4 Table 1`): Pointing Game (`tau=15`) = `0.41` (`Grad-CAM`), `0.30` (`Grad-CAM++`), `0.35` (`Eigen-CAM`) on `2,992`-woman patient-split screening FFDM.
- `P0014` (Pertuz et al., *Sci Rep* 2023, `Table 2 / Results`): Median Grad-CAM Dice overlap vs radiologist contours = `0.042` (`End2End`), `0.108` (`GLAM`), `0.291` (`GMIC`), `0.380` (`DMV-CNN`) on Finnish external FFDM (`370` contours).
- `P0016` (Kag et al., *IEEE Access* 2026, `Tables V–VI / Results`): Leakage-free `224x224` EfficientNet/SE/CBAM CAM Pointing Game `<= 11.5%` vs supervised Attention U-Net (`>80%`), showing severe localization gap across `CBIS-DDSM`, `Mini-MIAS`, `INbreast`, and `VinDr-Mammo`.
- `P0156` (Pesapane et al., *Diagnostics* 2026 SLR, `Sec. 3.1, Table 3`): Reaffirms `0.30–0.41` modest pointing reliability vs `73.1%` in lesion-aware `LENS` (`P1030`).
- `P0675` (Moffett et al., *PLOS ONE* 2025, `Table 3` p. 9): `VGG-16 + Grad-CAM` Activation Precision drops from `0.64 (Duke)` -> `0.16 (0.14–0.18, iCAD)` externally (`Grad-CAM++: 0.70 -> 0.43`).

## Contradictions & Boundaries
- **Nuance:** Lesion-aware / fine-annotation models yield materially higher internal/external localization than vanilla CNN `Grad-CAM`: `IAIA-BL` achieves `0.92–1.00` Activation Precision (`P0675`), `Camurdan 2025` reports `60.26–64.18%` overlap ratio via curriculum learning (`P0013`), `LENS-B` achieves `73.1%` PG (`86.5%` on TPs, `P1030`), and `ExViT-Breast` reports `71.4–80.1%` PG (`P0015`, caveat: `90/10` CBIS split & downsampled `224x224`).

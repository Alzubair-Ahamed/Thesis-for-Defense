# Claim Record (`T07`) — `CLAIM0007`

| Header Field | Value |
|---|---|
| `TemplateID` | `T07` (`claim.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `CLAIM0007` |
| `owner` | Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `VERIFIED_FROM_LITERATURE` |
| `source_inputs` | `02_Literature/summaries/{P0008,P0013,P0014,P0016,P0018,P0034,P0037,P0675}.md` |
| `governing_section` | [OS §3.2, §7.5](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-007](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-007) |

## Statement
External validation remains rare in breast imaging AI (`~18.5%` overall), and cross-scanner (`Philips` vs `GE`/`Hologic`), modality (`SFM` vs `FFDM`), and geographic population shifts consistently induce major AUC (`-0.08` to `-0.38`) and localization degradation.

## Exact Primary-Source Evidence (`PaperIDs` & `SourceLocators`)
- `P0018` (Sabry et al., *Cancers* 2026 PRISMA+PROBAST SLR): Only **`18.5%` (`12/65`)** of breast imaging AI studies perform independent external validation.
- `P0034` (Gabbualoy et al., *Sensors* 2026, `Tables 5–7`): Zero-shot transfer from digitized film `CBIS-DDSM` (`0.867`) to external `CMMD` (`0.568`), `DMID` (`0.547`), and `MIAS` (`0.630`) suffers **`-0.165` to `-0.320` AUC collapse** across all 5 architectures.
- `P0008` (Shia, *Sci Rep* 2025): `FFDM`-trained `EfficientNet` drops from `~87%` internally to **`~49%` on `CBIS-DDSM` digitized film**.
- `P0037` (Rothwell et al., UK NHS `134,217` women, `Table 2 p. 20`): Hologic-trained `Mirai` transfers significantly worse onto **Philips (`C-index 0.65`, Yr3 `0.62`)** than **GE (`C-index 0.74`, Yr3 `0.71`; `p < 0.001`)**.
- `P0675` (Moffett et al., *PLOS ONE* 2025, `Fig. 6`, `Table 3`): Malignancy AUC drops `-0.08` to `-0.19` (`Duke -> Emory EMBED`) and mass-margin AUC drops `0.95 -> 0.63–0.70`, while `VGG-16 Grad-CAM` Activation Precision drops `0.64 -> 0.16` on `iCAD`.

## Contradictions & Boundaries
- `P0013` (Camurdan et al., *Insights Imaging* 2025) preserves closer AUC (`0.87 -> 0.85`) and Grad-CAM overlap (`60.3–64.2% -> 57.2–62.9%`) when moving within the same **FFDM country/clinical task (`4,276`-woman Siemens external cohort)** via curriculum training, demonstrating that **same-modality FFDM + curriculum regularization** mitigates some transfer loss vs `SFM -> FFDM` jumps.

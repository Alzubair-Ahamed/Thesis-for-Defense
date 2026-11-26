# Claim Record (`T07`) — `CLAIM0006`

| Header Field | Value |
|---|---|
| `TemplateID` | `T07` (`claim.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `CLAIM0006` |
| `owner` | Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `VERIFIED_FROM_LITERATURE` |
| `source_inputs` | `02_Literature/summaries/{P0009,P0011,P0015,P0034,P0385,P1030,P1433}.md` |
| `governing_section` | [OS §3.2, §5.1](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-007](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-007) |

## Statement
Under leak-free, small-to-moderate mammography sample regimes, standard ImageNet-pretrained CNNs (`ResNet-50`, `EfficientNet-B0`, `ConvNeXt-Tiny/Base`, `DenseNet-121`) match or outperform vanilla `ViT-B/16` and unadapted self-supervised foundation models (`DINOv2`, `Rad-DINO`, `Mammo-CLIP`), whereas aspect-preserving hybrid CNN-Transformers (`LENS`, `Swin-B` at `1024x512`) regain top screening Macro-F1 and AUC.

## Exact Primary-Source Evidence (`PaperIDs` & `SourceLocators`)
- `P0385` (Mabrok et al., *Future Sci OA* 2026, `Table 2, Sec. 4.5, 5.2`): On `CMMD` (`706` pts), top CNNs cluster tightly within `0.007` side-level AUC (`ResNet-50 0.966`, `EffNet-B0 0.965`, `ConvNeXt-T 0.962`, `ResNet-18 0.960`, `DenseNet-121 0.959`), whereas **`ViT-B/16` trails by `8–10%` (`0.874` avg; patient AUC `0.670–0.707` vs `EffNet-B0 0.842`)**.
- `P0034` (Gabbualoy et al., *Sensors* 2026, `Table 2 p. 10`): On `CBIS-DDSM`, **`ResNet-50` (`0.867 ± 0.006`)** significantly beats `Mammo-CLIP B5` (`0.847, p_adj=0.047`), `Mammo-FM` (`0.846, p_adj=0.031`), **`DINOv2-B14` (`0.813, p<0.001`)**, and **`Rad-DINO` (`0.703, p<0.001`)**.
- `P0009` (Cantone et al., *Sensors* 2023): On `15,696` `OMI-DB` FFDM images, increasing resolution (`256x128 -> 2048x1024`) lifts modern CNNs/SwinV2 above `224x224` vanilla ViT.
- `P1030` (Quy et al., *PLOS ONE* 2026, `Tables 4–6`): At **`1,024 x 512`** on `VinDr-Mammo`, hybrid CNN-Transformer **`LENS-B`** leads `Macro-F1` (**`79.6%`**, `MCC 0.65`, `Macro-AUC 87.6%`, `48.6G` FLOPs) while `Swin-B` reaches `90.2% Macro-AUC` and `ConvNeXt-B` `88.4%`, all clearly exceeding `DINOv2-B` (`Macro-F1 69.4%`, `703.9G` FLOPs).

## Contradictions & Boundaries
- `P0011` (Takahashi 2026) trains from scratch on small `TOMPEI-CMMD` (`2,436` imgs) yielding low random-init performance; `P0015` shows cross-view `ExViT` improves over single-view `ViT`/`ResNet-50` at `224x224` (`90/10` split caveat).

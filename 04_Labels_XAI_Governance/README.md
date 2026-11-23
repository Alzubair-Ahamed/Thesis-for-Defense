# Diagnostic Label Verification, ROI Masks, and Prospective XAI Governance (`04_Labels_XAI_Governance/`)

| Field | Value |
|---|---|
| `TemplateID` | `T01` (`readme.md`) |
| `Folder` | `04_Labels_XAI_Governance/` |
| `Owner` | Md Riyadul Hasan (Label/Mask Audit Lead) & Alzubair Ahamed (XAI Governance Lead) |
| `Governing Section` | [OS §4.3](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §6](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [Blueprint STEP-014–018](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-014) |
| `Sensitivity Tier` | Mixed: Protocols, registries, and aggregate audits in Tier-1 Git; raw/pixel ROI masks and patient-linked visual overlays in Tier-2 Restricted Storage |

## Purpose
Governs FFDM-vs-ROI paradigm rules (`UD07`), pathology-vs-BI-RADS Benign/Malignant & Normal-case rules (`UD08`), lesion ROI-mask spatial alignment audits (`UD09`, `label_registry.csv`, `LBL####`), and prospective XAI governance (`xai_protocol_registry.csv`, `XAIP####`, target convolutional layer maps, perturbation faithfulness, Adebayo sanity checks, ROI localization, and blinded clinical review rubric `UD16–UD18`).

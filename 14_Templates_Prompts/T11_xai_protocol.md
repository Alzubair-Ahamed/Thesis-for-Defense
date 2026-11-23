# T11 Template — T11_xai_protocol.md

| Header Field | Value |
|---|---|
| `TemplateID` | `T11` (`T11_xai_protocol.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `Unresolved / Human Decision Required` |
| `owner` | `Unresolved / Human Decision Required` |
| `date` | `YYYY-MM-DD` |
| `status` | `BLANK_TEMPLATE` |
| `source_inputs` | `not reported` |
| `governing_section` | [OS §6.2-6.4, §14.2](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | `Unresolved / Human Decision Required` |
| `reviewer` | `Unresolved / Human Decision Required` |

> **Usage Contract (Prospective XAI governance contract / 04_Labels_XAI_Governance/xai_protocols/XAIP####.md):** Copy this blank template to its owning domain folder before filling. Never leave placeholder numbers or fabricate approvals; use `Unresolved / Human Decision Required` for open human choices and `not reported` for missing source facts.

---

## 1. Approved XAI method suite (mandatory Grad-CAM baseline + adopted comparators; UD16)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 2. Architecture-specific target convolutional layer map (bound per MC####)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 3. Target logit convention (raw pre-sigmoid/pre-softmax Malignant logit) and upsampling/normalization rules

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 4. Zero/collapsed attribution map handling rule

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 5. Quantitative Faithfulness protocol (Deletion AUC, Insertion AUC, ROAD perturbation schedule & random baseline; UD17)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 6. Adebayo Sanity Check protocol (cascading & independent layer randomization + data randomization; UD17)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 7. ROI-Mask Localization protocol (Pointing Game, EBPG, thresholded IoU/Dice on verified mask subsets; UD17)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 8. Perturbation and multi-seed explanation stability metrics (UD17)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 9. Bounded blinded radiologist/clinical-advisor qualitative review rubric and fallback rule (UD18)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 10. Protocol version, SHA-256 hash, and pre-test freeze commitment

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

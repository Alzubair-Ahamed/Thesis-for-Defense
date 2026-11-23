# T20 Template — T20_xai_audit.md

| Header Field | Value |
|---|---|
| `TemplateID` | `T20` (`T20_xai_audit.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `Unresolved / Human Decision Required` |
| `owner` | `Unresolved / Human Decision Required` |
| `date` | `YYYY-MM-DD` |
| `status` | `BLANK_TEMPLATE` |
| `source_inputs` | `not reported` |
| `governing_section` | [OS §6.3-6.4, §14.2](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | `Unresolved / Human Decision Required` |
| `reviewer` | `Unresolved / Human Decision Required` |

> **Usage Contract (Quantitative faithfulness, sanity, localization, stability, and clinical XAI audit / 09_Evaluation/EVAL####/xai_audit_XAIA####.md):** Copy this blank template to its owning domain folder before filling. Never leave placeholder numbers or fabricate approvals; use `Unresolved / Human Decision Required` for open human choices and `not reported` for missing source facts.

---

## 1. XAIAuditID (XAIA####), EvaluationID (EVAL####), ModelID (MODEL####), XAIProtocolID (XAIP####), LabelReleaseID (LBL####)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 2. Audited XAI methods (Grad-CAM baseline + adopted comparators) and target convolutional layers

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 3. Zero/collapsed attribution map count reconciliation

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 4. Faithfulness results: Deletion AUC, Insertion AUC, and ROAD curves/scores vs random-mask baseline (with patient-clustered 95% CIs)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 5. Adebayo Sanity Check results: cascading & independent parameter randomization + data randomization rank-correlation/SSIM decay and PASS/SANITY_FAILED verdict

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 6. Lesion ROI-Mask Localization results: Pointing Game accuracy, EBPG, and thresholded Heatmap-ROI IoU/Dice (with exact mask-subset n disclosed)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 7. Perturbation and multi-seed heatmap stability & inter-XAI agreement scores

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 8. Bounded blinded radiologist/clinical-advisor qualitative review summary (or explicit UD18 not_performed_unavailable disclosure)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 9. Honest failure and shortcut-learning findings

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

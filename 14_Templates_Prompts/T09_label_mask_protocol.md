# T09 Template — T09_label_mask_protocol.md

| Header Field | Value |
|---|---|
| `TemplateID` | `T09` (`T09_label_mask_protocol.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `Unresolved / Human Decision Required` |
| `owner` | `Unresolved / Human Decision Required` |
| `date` | `YYYY-MM-DD` |
| `status` | `BLANK_TEMPLATE` |
| `source_inputs` | `not reported` |
| `governing_section` | [OS §4.3, §6.1, §14.2](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | `Unresolved / Human Decision Required` |
| `reviewer` | `Unresolved / Human Decision Required` |

> **Usage Contract (Diagnostic label and ROI-mask verification rules / 04_Labels_XAI_Governance/protocols/):** Copy this blank template to its owning domain folder before filling. Never leave placeholder numbers or fabricate approvals; use `Unresolved / Human Decision Required` for open human choices and `not reported` for missing source facts.

---

## 1. Classification paradigm rule (FFDM whole-breast vs lesion ROI/patch; UD07)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 2. Binary ground-truth label mapping (0 = Benign, 1 = Malignant) and pathology vs BI-RADS provenance (UD08)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 3. Explicit inclusion/exclusion rules for Normal/Negative (BI-RADS 1), BI-RADS 0, and unconfirmed cases

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 4. Multi-lesion precedence rule (malignant dominance on same breast/image)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 5. Lesion ROI-mask coordinate convention, orientation alignment, and multi-ROI union rules (UD09)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 6. Strict post-hoc-only XAI localization boundary (zero mask leakage into classification training/inference)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 7. Pilot sample stratification, adjudication roles, and acceptance thresholds

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 8. Protocol version, SHA-256 hash, and human approvers

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

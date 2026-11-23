# T12 Template — T12_preprocessing.md

| Header Field | Value |
|---|---|
| `TemplateID` | `T12` (`T12_preprocessing.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `Unresolved / Human Decision Required` |
| `owner` | `Unresolved / Human Decision Required` |
| `date` | `YYYY-MM-DD` |
| `status` | `BLANK_TEMPLATE` |
| `source_inputs` | `not reported` |
| `governing_section` | [OS §4.4, §14.2](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md) |
| `sensitivity` | `Unresolved / Human Decision Required` |
| `reviewer` | `Unresolved / Human Decision Required` |

> **Usage Contract (Mammography preprocessing and augmentation specification / 05_Preprocessing/reports/PP####.md):** Copy this blank template to its owning domain folder before filling. Never leave placeholder numbers or fabricate approvals; use `Unresolved / Human Decision Required` for open human choices and `not reported` for missing source facts.

---

## 1. Scientific rationale and baseline vs ablation role (e.g., minimal baseline vs CLAHE ablation; UD12)

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 2. Ordered deterministic operations and exact parameters

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 3. DICOM bit-depth scaling and MONOCHROME1 -> MONOCHROME2 polarity standardization

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 4. Border, radiopaque marker, and pectoral-muscle handling with zero-clipped-lesion verification

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 5. Aspect-ratio preservation, target input dimensions, and 1:1 ROI-mask spatial co-transform verification

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 6. Training-only fitted normalization statistics (FitPartition = train) and serialized state SHA-256

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 7. Radiographically valid training-only stochastic augmentation bounds

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

## 8. Raw DS#### hash invariance check, visual QA summary, and output manifest SHA-256

- `Unresolved / Human Decision Required` (or `not reported` if absent in source)

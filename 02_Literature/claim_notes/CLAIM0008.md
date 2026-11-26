# Claim Record (`T07`) — `CLAIM0008`

| Header Field | Value |
|---|---|
| `TemplateID` | `T07` (`claim.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `CLAIM0008` |
| `owner` | Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-26` |
| `status` | `VERIFIED_FROM_LITERATURE` |
| `source_inputs` | `02_Literature/summaries/{P0039,P0040,P0385,P1030,P1433}.md` |
| `governing_section` | [OS §3.2, §4.3, §6.1](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md); [STEP-007](../../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md#step-007) |

## Statement
Public 2D mammography datasets (`CBIS-DDSM`, `INbreast`, `VinDr-Mammo`, `CMMD`, `MIAS`, `BCDR`, `DMID`) differ fundamentally in ground-truth provenance (`histopathologic biopsy` vs `BI-RADS radiologist consensus`), imaging physics (`SFM` vs `FFDM`), prevalence structure, and lesion bounding-box availability, barring naive label pooling without explicit task segregation.

## Exact Primary-Source Evidence (`PaperIDs` & `SourceLocators`)
- `P0039` (Nguyen et al., *Sci Data* 2023 `VinDr-Mammo`, `Usage Notes p. 7`, `Tables 3–5`): Explicitly states `VinDr-Mammo` has **zero biopsy-confirmed pathology (`no BI-RADS 6`)**, warns it *"should not be used to directly evaluate CAD for diagnosis purposes"* (must frame as **3-class BI-RADS screening triage** `BI-RADS 1 / 2 / Recall 3–5` or `4–5`, as in `P1030`), lacks bounding boxes for `BI-RADS 2` benign lesions, and is not strictly DICOM-compliant (`p. 7`).
- `P0040` (Logan et al., *Sci Data* 2023 FAIR Audit, `Tables 1–2`, `Fig. 2`): Documents `MIAS` relies on uncertain/opinion labels & coarse circles (`322` film), `DDSM/CBIS-DDSM` contain film scanning noise & inaccurate legacy polygons (`requiring re-curated polygons`), **`INbreast`** offers gold-standard `410` FFDM DICOMS + polygonal OSIRIX XML + histology, and **`CMMD`** provides biopsy-confirmed pathology + molecular subtypes (`CMMD2`) **but ZERO lesion bounding boxes and ZERO breast density metadata**.
- `P0385` (Mabrok et al. 2026, `Sec. 3.1.1, 5.6`): Proves `CMMD`'s 4-view cohort is `96.2%` malignant at patient level (`683` `BI-RADS 0` normal contralateral breasts), yielding meaningless screening PPVs if treated as a screening population.

## Contradictions & Boundaries
- **Design Implication (`UD05/UD07/UD08`):** Multi-dataset evaluation (`>=5` cohorts) must partition roles cleanly by ground-truth schema (`biopsy pathology tracks`: `CMMD` + `INbreast` + `CBIS-DDSM`; `screening triage + localization track`: `VinDr-Mammo`; `background/film shift track`: `MIAS/DMID`) rather than flattening `BI-RADS 4–5` and biopsy-malignant labels blindly into one pooled CSV.

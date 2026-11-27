# Bounded Blinded Qualitative Radiologist XAI Review Rubric (`STEP-015` / `UD18`)

| Field | Value |
|---|---|
| `DocumentID` | `QUALITATIVE_REVIEW_RUBRIC_v1.0.0` |
| `Governing Protocol` | [XAIP0001.md](./XAIP0001.md) (`§9`); [DEC0018.md](../../01_Project_Management/decision_log/DEC0018.md) |
| `Scope Guardrail (`RF15`)` | Strictly retrospective blinded qualitative audit — **NOT** a clinical trial, prospective workflow study, or diagnostic efficacy claim (`OS §6.4`, §8`) |

---

## 1. Stratified Sample Construction (`N = 40`, Never Cherry-Picked)
Drawn deterministically using a fixed seed (`after G11 test freeze` at `STEP-037`) from the locked evaluation cohorts (`preferentially cohorts with ACR density & verified lesion localization`):
- **`10` True Positives (`TP`):** Correctly detected Malignant exams (stratified `5` dense `C/D` + `5` non-dense `A/B`; mass + calcification).
- **`10` False Negatives (`FN`):** Missed cancers — **highest clinical safety priority**.
- **`10` False Positives (`FP`):** Benign / Normal images erroneously flagged Malignant.
- **`10` True Negatives (`TN`):** Correctly cleared Benign / Normal controls.

## 2. Blinding & Privacy Hygiene
- Strip all `PatientID`, hospital dates, filename tokens, ground-truth labels, and model predicted probabilities from presentation plates; identify cases solely by randomized blinded indices `CASE_01..CASE_40`.
- Reviewer inspects (`a`) clean de-identified mammogram alongside (`b`) `Grad-CAM` (`and LayerCAM / comparator overlay`) without knowing TP/FN/FP/TN bucket.

## 3. Structured `1–5` Likert Evaluation Criteria (`Per Case`)

| Dimension | `1` (Unacceptable) | `3` (Borderline / Partial) | `5` (Clinically Aligned) |
|---|---|---|---|
| **Q1. Anatomical Localization Precision** | Focus completely off-breast, on air/edge, or opposite quadrant | Broad diffuse lobe overlap near target quadrant | Tight focus centered on primary suspicious/benign parenchymal structure |
| **Q2. Artifact & Shortcut Absence** | Primary saliency anchored on lead tags (`R ML`), corner text (`RCC`), or scanner strip (`RISK0004`) | Mixed tissue + peripheral pectoral/border glare | Zero reliance on markers, borders, or film edges (`pure breast parenchyma`) |
| **Q3. Radiological Plausibility** | Highlights biologically meaningless air/skin artifact | Highlights dense normal stroma alongside finding | Aligns with clinically suspicious morphology (spiculated mass, pleomorphic calcifications, architectural distortion) |
| **Q4. Interpretability Support Value** | Misleading visual cue (`would confuse review`) | Ambiguous / uninformative heatmap | Clear, interpretable visual explanation distinguishing model decision rationale (`incl. FN/FP error diagnosis`) |

- **Qualitative Categorization (`Shortcut Taxonomy`):** Reviewer checks one primary cause on `FN`/`FP` plates (`True_Parenchyma_Error`, `Dense_Masking`, `Pectoral_Focus`, `Lead_Marker_Or_Border_Shortcut`, `Diffuse_Uninterpretable`).

## 4. Non-Availability Fallback Disclosure (`OS §6.4` Non-Fabrication Rule)
- Record reviewer specialty, years of breast-imaging experience, and date outside PHI when completed (`QualitativeReviewStatus = Completed_Blinded_Audit`).
- If a qualified breast radiologist cannot complete blinded scoring before `G13` (`STEP-037`), record **`QualitativeReviewStatus = Unresolved_NotPerformed_AdvisorUnavailable`** explicitly in `UD18`, thesis Ch. 4–5 limitations, and `CLAIM####` cards — **never fabricate ratings or substitute non-radiologist/LLM opinions as clinical validation**.

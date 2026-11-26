# Research Use Agreement Record — `EMBED` AWS Open `20%` Subset (`CAND0010`)

- **Custodian:** Emory University School of Medicine (Health Innovation and Translational Informatics Lab / Dr. Hari Trivedi) via AWS Open Data (`s3://embed-dataset-open`, `us-west-2`)
- **Descriptor:** Jeong et al., *Radiology: Artificial Intelligence* **5**(1):e220047 (2023)
- **License / DUA:** **Emory EMBED Research Use Agreement (RUA)** + AWS Open Data terms

## Critical Restrictions Audited (`STEP-011`)
1. **Non-Commercial Research Only:** Strictly limited to non-commercial academic research; every researcher accessing S3 data must individually register and agree to the Emory RUA (`zero redistribution`).
2. **CRITICAL TRAINED-WEIGHT BAN (`UD24` Impact):** Under Emory RUA terms, users **may NOT publicly release or commercialize trained models, model weights, or embedding representations derived from training/fine-tuning on ANY portion of EMBED** without separate written permission from Emory University.
   - **Research Governance Implication:** If `EMBED` is acquired after RUA approval, **reserve `EMBED` strictly as a zero-shot external test set** (`models trained only on CC-BY/PhysioNet cohorts`) OR keep any EMBED-touched weights private under restricted `UD24` archival tiers. Never include `DBT` slices (`exclude non-2D per RF15`).
3. **Current Status (`2026-11-27`):** **`BLOCKED_PENDING_EMORY_RUA_AND_STORAGE_EVALUATION`** — Conditional external cohort (`evaluate after primary DIU ethics waiver + TCIA/Figshare/PhysioNet downloads`).

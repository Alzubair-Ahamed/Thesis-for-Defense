# Credentialed Data Use Agreement Record — `VinDr-Mammo` (`CAND0001`)

- **Custodian:** PhysioNet (`https://physionet.org/content/vindr-mammo/1.0.0/`, `DOI: 10.13026/br2v-7517`)
- **Primary Descriptor:** Nguyen et al., *Scientific Data* **10**:277 (2023), `DOI: 10.1038/s41597-023-02100-7`
- **License / DUA:** **PhysioNet Credentialed Health Data License 1.5.0** & **Data Use Agreement 1.5.0**

## Mandatory Binding Requirements Audited (`STEP-011`)
1. **Individual Credentialing + CITI Training (`BLOCKER FOR STEP-012`):**
   - Each researcher accessing raw DICOMs (**both** `Md Riyadul Hasan` and `Alzubair Ahamed`) must hold an individual **PhysioNet credentialed account**, complete required **CITI Program** human-research/data training (*"Data or Specimens Only Research"*), and individually sign the DUA. Sharing account credentials or copying raw `VinDr-Mammo` DICOMs to uncredentialed users is strictly prohibited.
2. **Privacy & PHI Discovery Reporting:** Zero re-identification attempts; any accidental PHI discovery must be reported immediately to `PHI-report@physionet.org` and quarantined per [OS §4.6](../../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04).
3. **Compute Custody:** Local workstations and private access-controlled institutional/cloud VMs with strict authentication/encryption are permitted; **uploading raw `VinDr-Mammo` images to public datasets/buckets (e.g., public Kaggle Datasets, public HF Spaces, open Colab public drives) is strictly FORBIDDEN.**
4. **Open-Code Clause:** Publicly disseminated papers/results derived from PhysioNet data must release associated analysis code openly (aligns with MIT analysis code planned under `UD24`).
5. **Figures & Conditional Web Demo (`UD27`):** De-identified cropped/masked heatmap figures in publications must prevent patient/hospital identification. For any conditional defense web showcase (`UD27`), do **not** expose raw redistributable `VinDr-Mammo` DICOMs publicly—prefer `CC BY` showcase examples (`CBIS-DDSM`/`CMMD`/`DMID`) unless explicit non-exporting in-memory preview is verified compliant.
6. **Current Status (`2026-11-27`):** **`BLOCKED_PENDING_INDIVIDUAL_CITI_AND_PHYSIONET_SIGNUP`** — Do **NOT** download until PhysioNet approval receipts are logged in restricted custody.

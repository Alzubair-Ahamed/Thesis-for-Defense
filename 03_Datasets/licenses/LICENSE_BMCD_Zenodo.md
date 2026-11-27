# License Record — `BMCD` (`CAND0012`) on Zenodo

- **Dataset:** Breast Micro-Calcifications Dataset with Precisely Annotated Sequential Mammograms (`BMCD`)
- **Primary Repository DOI:** `10.5281/zenodo.5036062` (`https://zenodo.org/records/5036062`)
- **Primary Descriptor Paper:** Loizidou et al., *European Radiology Experimental* **5**:40 (2021), `DOI: 10.1186/s41747-021-00238-w`
- **Ethics Approval (Original Collection):** Cyprus National Bioethics Committee (`#EEBK EΠ 2020.01.144`), retrospective informed consent collected
- **License:** **Creative Commons Attribution 4.0 International (`CC BY 4.0`)** (`verified in Zenodo API metadata`)

## Governing Terms Audited (`STEP-011`)
1. **Permissions:** Free to download, copy, transform, preprocess, model, and redistribute derivatives (including thesis figures and trained model weights under `UD24`) for academic and research purposes with mandatory attribution to Loizidou et al. (`DOI: 10.5281/zenodo.5036062`, `10.1186/s41747-021-00238-w`).
2. **Modality & Scope Check (`RF15`, `OS §4.1`):** Contains `400` pure 2D `FFDM` mammograms (`8-bit` DICOM `.dcm`: `100` subjects x `2` screening rounds x `CC` + `MLO` views) plus `400` `*_GT.jpg` radiologist-consensus micro-calcification ground-truth overlays (*described as `.png` in `README.txt` / `P1497`, distributed as `.jpg` inside `Dataset.zip`*) and `Description.xlsx` clinical/biopsy metadata (`50` normal/benign + `50` suspicious cases; `32` with biopsy confirmation). Zero ultrasound, MRI, DBT, or patient overlap with `MIAS`, `CMMD`, or `CBIS-DDSM`.
3. **Intake Readiness:** **Open direct HTTPS download** with MD5 verification (`d2d927a23e6b1ad991074dc55d5f5eac`), cleared for `STEP-012` under Supervisor Israt Jahan's `2026-11-27` DIU secondary-data waiver (`DEC0006`).

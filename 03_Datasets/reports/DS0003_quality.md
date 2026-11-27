# DS0003 (CMMD) — Technical Quality, Integrity & PHI Audit (`STEP-013`)

- **Generated:** `2026-11-27 23:55:00`
- **Raw Linkage SHA-256 Verified (`Pre / Post QC`):** `0` / `0` errors (`read-only invariance confirmed`)
- **Manifest SHA-256 Reference:** `b933e5f7efb3767ea92143a0bc652d5c81fdc33f024df6f5fefee98537c4f6ed`
- **Tier-2 Per-File CSV (Gitignored):** `03_Datasets/cache/qc/DS0003_qc_details.csv`
- **Tier-2 Contact Sheet (Gitignored):** `03_Datasets/images/qc_contact_sheets/DS0003_qc_grid.png`

## 1. Accounting Reconciliation (`Acquired = Retained + Excluded + Quarantined`)

- **Primary Track Image Accounting:** `5202` = **`5196` Retained** + **`0` Excluded** + **`6` Quarantined** (`exact sum check: True`)
- **Total Raw Files Inventoried:** `8757`
- **Pseudonymous Patient Groups (`PatientGroupID` in primary track):** `1775` (`DICOM PatientID tags: 1775`; `DICOM StudyInstanceUIDs: 1775`)

| Disposition (`All Raw Files`) | Count |
|---|---:|
| `Quarantined_CrossLabelPixelCloneConflict` | 2 |
| `Quarantined_PixelCloneAcrossPatients` | 4 |
| `Retained` | 5196 |
| `Supporting_NonImageAsset` | 3555 |

## 2. Pixel Format, Decode, Polarity & Normalization Audit (`Primary Track`)

- **Decode Status:** `{'ok': 5202}`
- **Bit Depths / DTypes:** `{'8b_uint8': 5200, '16b_uint16': 2}`
- **Photometric Interpretation / PIL Mode:** `{'MONOCHROME2': 5202}`
- **DICOM Transfer Syntaxes:** `{'Explicit VR Little Endian': 5202}`
- **RescaleSlope / RescaleIntercept:** `{'slope=1,intercept=0': 5202}`
- **VOI LUT Sequences / Window Tags:** `VOILUT=0`, `WindowCenter=5202`
- **RGB Channel Check (`SamplesPerPixel >= 3`):** `identical_R_eq_G_eq_B=0`, `nonzero_diff=0`
- **Top Image Dimensions (`W x H`):** `{'1914x2294': 5202}`

## 3. Privacy / DICOM Header PHI & Duplicate Screen

- **Non-Pseudonymous Sensitive PHI Tags Present:** `None populated`
- **Pseudonym Echo Tags (`PatientName == PatientID`):** `{'PatientName': 5202}`
- **Demographic / Date Tags Present:** `{'AcquisitionDate': 5202, 'PatientAge': 5202, 'PatientSex': 5202, 'SeriesDate': 5202, 'StudyDate': 5202}` (`StudyYears: {'2008': 2, '2009': 8, '2010': 2586, '2011': 2482, '2012': 124}`)
- **BurnedInAnnotation Tag:** `{'NO': 5202}`
- **Within-Cohort Exact SHA-256 Duplicate Clusters:** `2`
- **Within-Cohort Near-Duplicate Pairs (`dHash <= 4`):** `142284` (`cross-patient`: `142259`, `polarity-flipped >= 60`: `0`)

## 4. Cohort-Specific Verification Notes

- Mixed bit-depth finding: `5,200` DICOMs are `8-bit uint8` (`WindowCenter=128`), while `2` DICOMs (`IMG00003519`, `IMG00003520` of `PAT00000840`) are `16-bit uint16` (`WindowCenter=32768`, `PixelMax=65535`); `STEP-021` preprocessing must scale dynamically by header/dtype rather than hardcoding `/255`.
- CRITICAL bit-exact pixel-clone finding: (`1`) `D1-0202` (`PAT00000122`, 4 views) and `D2-0284` (`PAT00001310`, 4 views) are 100% bit-exact raw pixel clones (`IMG00005967-5970` quarantined); (`2`) `D1-0808` (`IMG00001999`, `Benign`) and `D1-1292` (`IMG00003418`, `Malignant`) share 100% bit-exact DICOM pixels with contradictory biopsy truth (companion view corr=0.9933) — both `IMG00001999` and `IMG00003418` quarantined under `Quarantined_CrossLabelPixelCloneConflict` and patients linked for `STEP-020` (`5,196` Retained / `6` Quarantined).

# DS0005 (BMCD) — Technical Quality, Integrity & PHI Audit (`STEP-013`)

- **Generated:** `2026-11-27 23:55:00`
- **Raw Linkage SHA-256 Verified (`Pre / Post QC`):** `0` / `0` errors (`read-only invariance confirmed`)
- **Manifest SHA-256 Reference:** `4a1faa4ceeb921b6694c0458e4a7ce6702b5471deda259d9784121a08e989efe`
- **Tier-2 Per-File CSV (Gitignored):** `03_Datasets/cache/qc/DS0005_qc_details.csv`
- **Tier-2 Contact Sheet (Gitignored):** `03_Datasets/images/qc_contact_sheets/DS0005_qc_grid.png`

## 1. Accounting Reconciliation (`Acquired = Retained + Excluded + Quarantined`)

- **Primary Track Image Accounting:** `400` = **`392` Retained** + **`0` Excluded** + **`8` Quarantined** (`exact sum check: True`)
- **Total Raw Files Inventoried:** `802`
- **Pseudonymous Patient Groups (`PatientGroupID` in primary track):** `100` (`DICOM PatientID tags: 0`; `DICOM StudyInstanceUIDs: 200`)

| Disposition (`All Raw Files`) | Count |
|---|---:|
| `Excluded_OverlayGT_NotRawInput` | 400 |
| `Quarantined_CrossLabelPixelCloneConflict` | 8 |
| `Retained` | 392 |
| `Supporting_NonImageAsset` | 2 |

## 2. Pixel Format, Decode, Polarity & Normalization Audit (`Primary Track`)

- **Decode Status:** `{'ok': 400}`
- **Bit Depths / DTypes:** `{'12b_uint16': 400}`
- **Photometric Interpretation / PIL Mode:** `{'MONOCHROME2': 400}`
- **DICOM Transfer Syntaxes:** `{'Explicit VR Little Endian': 400}`
- **RescaleSlope / RescaleIntercept:** `{'slope=1,intercept=0': 400}`
- **VOI LUT Sequences / Window Tags:** `VOILUT=0`, `WindowCenter=400`
- **RGB Channel Check (`SamplesPerPixel >= 3`):** `identical_R_eq_G_eq_B=0`, `nonzero_diff=0`
- **Top Image Dimensions (`W x H`):** `{'3328x4096': 368, '2560x3328': 28, '3328x4084': 4}`

## 3. Privacy / DICOM Header PHI & Duplicate Screen

- **Non-Pseudonymous Sensitive PHI Tags Present:** `None populated`
- **Pseudonym Echo Tags (`PatientName == PatientID`):** `None`
- **Demographic / Date Tags Present:** `{'AcquisitionDate': 400, 'SeriesDate': 400, 'StudyDate': 400}` (`StudyYears: {'1970': 400}`)
- **BurnedInAnnotation Tag:** `{'NO': 400}`
- **Within-Cohort Exact SHA-256 Duplicate Clusters:** `1`
- **Within-Cohort Near-Duplicate Pairs (`dHash <= 4`):** `270` (`cross-patient`: `231`, `polarity-flipped >= 60`: `0`)

## 4. Cohort-Specific Verification Notes

- BMCD cohort structure: 200 Normal_cases DICOMs + 200 Suspicious_cases DICOMs; 400 *_GT.jpg overlays decoded (`Excluded_OverlayGT_NotRawInput` for raw modeling).
- BMCD *_GT.jpg overlay resolutions: {'645x794': 219, '1059x1303': 46, '671x826': 25, '3328x4096': 18, '1352x1664': 17}.
- CRITICAL cross-label pixel-clone conflict: `Dataset/Normal_cases/40` (`BI-RADS 2`, density `c`, uppercase `.DCM`) and `Dataset/Suspicious_cases/16` (`BI-RADS 4a`, density `b`, lowercase `.dcm`, both Biopsy `NOT AVAILABLE`) share 100% bit-exact DICOM pixels across all 4 CC/MLO prior/recent views (`8` files `IMG00000273/275/277/279` & `IMG00000457/459/461/463` quarantined -> `392` Retained across `98` clean patient folders).
- Visual contact sheet & header audit: tiny digital corner stamps (`RCC/LCC/RMLO/LMLO`) present in upper outer corners; `StudyDate=1970` (de-identified epoch); `100%` `12-bit uint16` (`MONOCHROME2`).

# DS0001 (MIAS v1.21) — Technical Quality, Integrity & PHI Audit (`STEP-013`)

- **Generated:** `2026-11-27 23:55:00`
- **Raw Linkage SHA-256 Verified (`Pre / Post QC`):** `0` / `0` errors (`read-only invariance confirmed`)
- **Manifest SHA-256 Reference:** `2e3f8559ed425aee3d716174767558d2e8adf41c017915eecefb81da9ec9fdf1`
- **Tier-2 Per-File CSV (Gitignored):** `03_Datasets/cache/qc/DS0001_qc_details.csv`
- **Tier-2 Contact Sheet (Gitignored):** `03_Datasets/images/qc_contact_sheets/DS0001_qc_grid.png`

## 1. Accounting Reconciliation (`Acquired = Retained + Excluded + Quarantined`)

- **Primary Track Image Accounting:** `322` = **`322` Retained** + **`0` Excluded** + **`0` Quarantined** (`exact sum check: True`)
- **Total Raw Files Inventoried:** `327`
- **Pseudonymous Patient Groups (`PatientGroupID` in primary track):** `322` (`DICOM PatientID tags: 0`; `DICOM StudyInstanceUIDs: 0`)

| Disposition (`All Raw Files`) | Count |
|---|---:|
| `Retained` | 322 |
| `Supporting_NonImageAsset` | 5 |

## 2. Pixel Format, Decode, Polarity & Normalization Audit (`Primary Track`)

- **Decode Status:** `{'ok': 322}`
- **Bit Depths / DTypes:** `{'8b_uint8': 322}`
- **Photometric Interpretation / PIL Mode:** `{'L': 322}`
- **DICOM Transfer Syntaxes:** `{'raster_non_dicom': 322}`
- **RescaleSlope / RescaleIntercept:** `N/A (non-DICOM)`
- **VOI LUT Sequences / Window Tags:** `VOILUT=0`, `WindowCenter=0`
- **RGB Channel Check (`SamplesPerPixel >= 3`):** `identical_R_eq_G_eq_B=0`, `nonzero_diff=0`
- **Top Image Dimensions (`W x H`):** `{'4320x2600': 149, '4320x2048': 101, '4320x1600': 48, '5200x4000': 24}`

## 3. Privacy / DICOM Header PHI & Duplicate Screen

- **Non-Pseudonymous Sensitive PHI Tags Present:** `None populated`
- **Pseudonym Echo Tags (`PatientName == PatientID`):** `None`
- **Demographic / Date Tags Present:** `None` (`StudyYears: None`)
- **BurnedInAnnotation Tag:** `N/A`
- **Within-Cohort Exact SHA-256 Duplicate Clusters:** `0`
- **Within-Cohort Near-Duplicate Pairs (`dHash <= 4`):** `3` (`cross-patient`: `3`, `polarity-flipped >= 60`: `0`)

## 4. Cohort-Specific Verification Notes

- Visual contact sheet audit: visible white corner film labels (`R ML`, `L ML`, `L MED-LAT OBL`), numeric film tags, and horizontal film-scanner padding bars confirmed (`RISK0004` shortcut-learning audit target). Zero exact SHA-256 duplicates and zero pixel clones.

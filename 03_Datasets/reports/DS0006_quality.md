# DS0006 (CDD-CESM (LE Track)) — Technical Quality, Integrity & PHI Audit (`STEP-013`)

- **Generated:** `2026-11-27 23:55:00`
- **Raw Linkage SHA-256 Verified (`Pre / Post QC`):** `0` / `0` errors (`read-only invariance confirmed`)
- **Manifest SHA-256 Reference:** `e1732776952a7562a811b16800924563a33cc645f72fd33aa056a38a0919ecd4`
- **Tier-2 Per-File CSV (Gitignored):** `03_Datasets/cache/qc/DS0006_qc_details.csv`
- **Tier-2 Contact Sheet (Gitignored):** `03_Datasets/images/qc_contact_sheets/DS0006_qc_grid.png`

## 1. Accounting Reconciliation (`Acquired = Retained + Excluded + Quarantined`)

- **Primary Track Image Accounting:** `1003` = **`1003` Retained** + **`0` Excluded** + **`0` Quarantined** (`exact sum check: True`)
- **Total Raw Files Inventoried:** `2337`
- **Pseudonymous Patient Groups (`PatientGroupID` in primary track):** `326` (`DICOM PatientID tags: 0`; `DICOM StudyInstanceUIDs: 0`)

| Disposition (`All Raw Files`) | Count |
|---|---:|
| `Excluded_OSSystemFile` | 1 |
| `Excluded_SubtractedCESM_RF15` | 1003 |
| `Excluded_WordTempLock` | 1 |
| `Retained` | 1003 |
| `Supporting_NonImageAsset` | 329 |

## 2. Pixel Format, Decode, Polarity & Normalization Audit (`Primary Track`)

- **Decode Status:** `{'ok': 1003}`
- **Bit Depths / DTypes:** `{'8b_uint8': 1003}`
- **Photometric Interpretation / PIL Mode:** `{'RGB': 1003}`
- **DICOM Transfer Syntaxes:** `{'raster_non_dicom': 1003}`
- **RescaleSlope / RescaleIntercept:** `N/A (non-DICOM)`
- **VOI LUT Sequences / Window Tags:** `VOILUT=0`, `WindowCenter=0`
- **RGB Channel Check (`SamplesPerPixel >= 3`):** `identical_R_eq_G_eq_B=1003`, `nonzero_diff=0`
- **Top Image Dimensions (`W x H`):** `{'2394x3062': 2, '1308x2316': 1, '1312x2249': 1, '1493x2518': 1, '1522x2456': 1, '1479x2564': 1, '1567x2437': 1, '1570x2457': 1, '1721x2672': 1, '664x1816': 1, '1050x2331': 1, '920x1820': 1}`

## 3. Privacy / DICOM Header PHI & Duplicate Screen

- **Non-Pseudonymous Sensitive PHI Tags Present:** `None populated`
- **Pseudonym Echo Tags (`PatientName == PatientID`):** `None`
- **Demographic / Date Tags Present:** `None` (`StudyYears: None`)
- **BurnedInAnnotation Tag:** `N/A`
- **Within-Cohort Exact SHA-256 Duplicate Clusters:** `0`
- **Within-Cohort Near-Duplicate Pairs (`dHash <= 4`):** `42` (`cross-patient`: `42`, `polarity-flipped >= 60`: `0`)

## 4. Cohort-Specific Verification Notes

- CDD-CESM RF15 isolation: 1003 Low-Energy DM JPEGs retained vs 1003 Subtracted CESM images excluded; 2 non-medical artifacts excluded (desktop.ini, ~$P54.docx).
- CDD-CESM Low-Energy unique resolutions count: 1002 (top 5: {'2394x3062': 2, '1308x2316': 1, '1312x2249': 1, '1493x2518': 1, '1522x2456': 1}).
- Visual contact sheet & exhaustive pixel SHA-256 check: zero exact duplicates and zero pixel clones; all `1,003` Low-Energy `DM` JPEGs cleanly isolated from `1,003` Subtracted `CESM` images (`RF15`), with `1,002` distinct WxH crops.

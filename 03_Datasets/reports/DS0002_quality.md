# DS0002 (DMID) — Technical Quality, Integrity & PHI Audit (`STEP-013`)

- **Generated:** `2026-11-27 23:55:00`
- **Raw Linkage SHA-256 Verified (`Pre / Post QC`):** `0` / `0` errors (`read-only invariance confirmed`)
- **Manifest SHA-256 Reference:** `40882b4e5506f11675acccee1776e7469de1713bad0fabe9a33d0898892cf5da`
- **Tier-2 Per-File CSV (Gitignored):** `03_Datasets/cache/qc/DS0002_qc_details.csv`
- **Tier-2 Contact Sheet (Gitignored):** `03_Datasets/images/qc_contact_sheets/DS0002_qc_grid.png`

## 1. Accounting Reconciliation (`Acquired = Retained + Excluded + Quarantined`)

- **Primary Track Image Accounting:** `510` = **`507` Retained** + **`0` Excluded** + **`3` Quarantined** (`exact sum check: True`)
- **Total Raw Files Inventoried:** `2072`
- **Pseudonymous Patient Groups (`PatientGroupID` in primary track):** `510` (`DICOM PatientID tags: 0`; `DICOM StudyInstanceUIDs: 510`)

| Disposition (`All Raw Files`) | Count |
|---|---:|
| `Excluded_MirrorTIFF_CopyArtifact` | 1 |
| `Quarantined_LossyPixelClone` | 3 |
| `Retained` | 507 |
| `Supporting_MirrorTIFF_Secondary` | 510 |
| `Supporting_NonImageAsset` | 513 |
| `Supporting_ROIMask` | 538 |

## 2. Pixel Format, Decode, Polarity & Normalization Audit (`Primary Track`)

- **Decode Status:** `{'ok': 510}`
- **Bit Depths / DTypes:** `{'8b_uint8': 510}`
- **Photometric Interpretation / PIL Mode:** `{'RGB': 488, 'MONOCHROME2': 22}`
- **DICOM Transfer Syntaxes:** `{'JPEG Lossless, Non-Hierarchical, First-Order Prediction (Process 14 [Selection Value 1])': 510}`
- **RescaleSlope / RescaleIntercept:** `{'slope=None,intercept=None': 488, 'slope=1,intercept=0': 22}`
- **VOI LUT Sequences / Window Tags:** `VOILUT=0`, `WindowCenter=0`
- **RGB Channel Check (`SamplesPerPixel >= 3`):** `identical_R_eq_G_eq_B=488`, `nonzero_diff=0`
- **Top Image Dimensions (`W x H`):** `{'4747x6000': 71, '4751x6000': 61, '4752x6000': 61, '4744x6000': 51, '4748x6000': 48, '4753x6000': 39, '4746x6000': 31, '4745x6000': 25, '4750x6000': 15, '3521x4784': 12, '4754x6000': 9, '4749x6000': 8}`

## 3. Privacy / DICOM Header PHI & Duplicate Screen

- **Non-Pseudonymous Sensitive PHI Tags Present:** `None populated`
- **Pseudonym Echo Tags (`PatientName == PatientID`):** `None`
- **Demographic / Date Tags Present:** `{'StudyDate': 510}` (`StudyYears: {'2022': 510}`)
- **BurnedInAnnotation Tag:** `{'absent': 510}`
- **Within-Cohort Exact SHA-256 Duplicate Clusters:** `4`
- **Within-Cohort Near-Duplicate Pairs (`dHash <= 4`):** `144` (`cross-patient`: `144`, `polarity-flipped >= 60`: `0`)

## 4. Cohort-Specific Verification Notes

- DMID format audit: 510 DICOMs vs 511 TIFFs inspected read-only.
- DMID DCM-vs-TIFF paired audit: 510 dimension matches (115 identical dHash), 0 mismatched/missing.
- DMID DICOM header PatientID populated in 0/510 files; 510/510 carry StudyInstanceUID.
- TIFF vs DICOM audit: `TIFF Images/IMG279 - Copy.tif` (`EXACT_DS0002_COPY_000`) excluded; all 510 DICOMs decoded cleanly (`488` identical-channel RGB + `22` MONOCHROME2) with `0` major DCM-vs-TIFF intensity divergences and `1` BB radiopaque skin marker observed visually (`IMG00000140`).
- CRITICAL pixel-clone finding: `3` hidden re-encoded DICOM clone pairs detected across distinct IMG IDs (`IMG019<->IMG318` r=0.999996 with conflicting XLS/TXT `N/4a` vs `B/3`, `IMG021<->IMG319` r=1.0, `IMG034<->IMG172` r=0.999998 with `CIRC+SPIC r=301` vs `CIRC r=202`); second clone copies (`IMG00000318`, `IMG00000319`, `IMG00000172`) quarantined (`507` Retained / `3` Quarantined).
- Mask format note: `Pixel-level annotation/*.tif` (`538` files) are full-resolution `RGBA` annotated mammogram overlays (`RGBMaxChannelDiff > 0`), requiring color/contour isolation in `S07 / STEP-014`.

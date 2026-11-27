# Research Diary (`T03`) — `2026-11-27`: `DEC0006` Waiver Ratification, `STEP-012` Inventory Tooling & Batch A Intake Start

| Header Field | Value |
|---|---|
| `TemplateID` | `T03` (`session.md`) |
| `template_version` | `v1.0.0` |
| `entity_id` | `DIARY_2026-11-27_STEP012_START` |
| `owner` | Md Riyadul Hasan (`232-15-486`, Data Steward) & Alzubair Ahamed (`232-15-591`) |
| `date` | `2026-11-27` |
| `status` | `STEP-012_TOOLING_TESTED_BATCH_A_INTAKE_ACTIVE` |
| `source_inputs` | [DEC0006](../decision_log/DEC0006.md); [inventory.py](../../src/bc_xai/data/inventory.py); [tcia_fetch.py](../../src/bc_xai/data/tcia_fetch.py); [test_inventory.py](../../tests/test_inventory.py); [test_tcia_fetch.py](../../tests/test_tcia_fetch.py) |

---

## 1. Completed Scope in This Session
1. **`DEC0006` Batch A Approval Recorded (`2026-11-27`):** Logged Supervisor Israt Jahan's approval of the DIU secondary-data ethics waiver in [DEC0006](../decision_log/DEC0006.md), [decisions.csv](../decisions.csv), [access_decision.md](../../03_Datasets/reports/access_decision.md), and [candidates.csv](../../03_Datasets/candidates.csv), unlocking open `CC BY` Batch A (`CMMD`, `CBIS-DDSM`, `DMID`, `MIAS v1.21`) while keeping credentialed Batch B (`VinDr-Mammo`, `INbreast`, `EMBED`) strictly blocked pending individual CITI/DUAs.
2. **Implemented & Tested `STEP-012` Modules:** Authored [inventory.py](../../src/bc_xai/data/inventory.py) (streaming SHA-256 hashing, pseudonymous `IMG########`/`PAT########` assignment, segregated private linkage tables, `ManifestHash`, loud count-mismatch failure, tampering verifier) + [tcia_fetch.py](../../src/bc_xai/data/tcia_fetch.py) (resumable multi-threaded TCIA NBIA REST client with `SeriesDescription` filtering and ZIP CRC check).
3. **Storage & Live Portal Sizing Audit (`2026-11-27`):**
   - Verified drive capacities: `E:\` (`156.85 GB` free), `D:\` (`137.40 GB` free), `C:\` (`15.93 GB` free — keep clean!).
   - Measured live Batch A sizes: `MIAS v1.21` (`1.54 GB` Apollo `HTTP 200`), `DMID` (`10.92 GB` across 6 Figshare files), `CMMD` (`21.29 GB`, `1,775` series / `5,202` images), `CBIS-DDSM` (`152.28 GB`: `95.58 GB` full mammograms + `56.63 GB` ROI masks + `0.07 GB` cropped). Because `CMMD + DMID + MIAS + CBIS-DDSM` totals `~186 GB > E:'s 156.85 GB`, `CBIS-DDSM` full mammograms (`95.58 GB`) map cleanly to `D:\` (or dedicated external Tier-2 path) while `MIAS`, `DMID`, `CMMD`, and `CBIS-DDSM` masks/CSVs reside on `E:\`.
   - **`DS0001_MIAS` Completed & Inventoried:** `miasdbv1.21.zip` (`1,542.4 MB`, exact MD5 `d790185baed18ab199efc85388b75dfc`) + `322` 50-micron PGMs (`161` L/R patient pairs verified in `00README.pdf`) + docs (`327` files, `ManifestHash=2e3f8559ed425aee3d716174767558d2e8adf41c017915eecefb81da9ec9fdf1`), registered in `03_Datasets/datasets.csv`.
   - **`DS0003_CMMD` Completed & Inventoried:** All **`1,775 / 1,775` series (`5,202 / 5,202` `.dcm` files)** downloaded cleanly via [tcia_fetch.py](../../src/bc_xai/data/tcia_fetch.py), `1,775` redundant ZIPs (`4.63 GiB`) pruned after verification, and re-inventoried (`8,757` total files incl. clinical xlsx/manifests, `1,775` patient tokens, `ManifestHash=b933e5f7efb3767ea92143a0bc652d5c81fdc33f024df6f5fefee98537c4f6ed`), registered in `03_Datasets/datasets.csv`.
   - **`DS0004_CBIS_DDSM` Partial Intake Active:** Official `.tcia` manifest, 4 case CSVs, and all `107 / 107` `cropped images` series (`0.07 GiB` uncompressed, `0` failed) downloaded cleanly into `03_Datasets/raw/DS0004_CBIS_DDSM/`. Remaining subsets (`ROI mask images` `56.63 GB`, `full mammogram images` `95.58 GB`) await user `D:`/`E:` split confirmation.
   - **Awaiting User Action (`DMID` + `CBIS-DDSM` Split):** Awaiting browser download of `6` Figshare files (`10.92 GB`) into `03_Datasets/raw/DS0002_DMID/` (CloudFront WAF gated) and user confirmation to store `CBIS-DDSM` `ROI mask images` (`56.63 GB`) on `E:\` and `full mammogram images` (`95.58 GB`) on `D:\`.

# Provisional Research Execution Timeline

- **Document:** `01_Project_Management/timeline.md`
- **Version / Date:** `v1.0.1` / `2026-11-26`
- **Governing Section:** [OS §12](../BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-12); [Blueprint How to Use](../BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md)

> **Provisional Planning Note:** Durations below are provisional working estimates for bounded execution sessions. External DUA approval turnaround (`STEP-011`), clinical-advisor/supervisor review latency, and multi-architecture/multi-seed GPU training time (`STEP-028–031`) are updated dynamically at milestone reviews (`T33`).

| Phase / Stage | Steps | Target Gate | Provisional Effort Estimate | Current Status |
|---|---|---|---|---|
| **S01 Foundation & Scope** | `STEP-001` | `G01` | 2–4 hours | **DONE (`2026-11-23`)** |
| **S02 Repository, Templates & Registries** | `STEP-002–003` | `G02` | 7–11 hours | **DONE (`2026-11-23`)** |
| **S03–S04 PRISMA Literature & Q1 RQs** | `STEP-004–009` | `G03` | 15–25 hours across search/extraction batches | **DONE (`G03 PASS`, `2026-11-27`)** |
| **S05–S06 6-Dataset Discovery, DUAs & QC** | `STEP-010–013` | `G04` | 12–20 hours + portal DUA turnaround | **IN PROGRESS (`STEP-010` Done `2026-11-27`; `STEP-011` DUA/Ethics Next)** |
| **S07–S08 Label/ROI-Mask Audit & XAIP Lock** | `STEP-014–018` | `G05`, `G06` | 15–25 hours | `PENDING` |
| **S09 Preprocessing, Patient Split & Release** | `STEP-019–021` | `G07`, `G08` | 11–17 hours + materialization runtime | `PENDING` |
| **S10 CNN Roster, Phase-2 Env & Core Package** | `STEP-022–026` | `G09` | 20–35 hours development & smoke testing | `PENDING` |
| **S11 Multi-CNN Benchmark, Ablations & Seeds** | `STEP-027–031` | `G10` | 12–20 hours active + GPU wall-clock training | `PENDING` |
| **S12–S13 Test Freeze, Stats & Quantitative XAI** | `STEP-032–036` | `G11`, `G12` | 16–25 hours + attribution/bootstrap compute | `PENDING` |
| **S14 Subgroups/Errors, CAD Prototype & Repro** | `STEP-037–039` | `G13`, `G14` | 15–24 hours + clinical review | `PENDING` |
| **S15 Dual-Track FYDP Thesis & Q1 Paper + Archive** | `STEP-040–047` | `G15`, `G16` | 30–50 hours across writing/revision rounds | `PENDING` |
| **S16 Conditional Defense Hosted Web Demo** | `STEP-048–050` | `G17` | 17–30 hours (parallel with S15 after `STEP-038`) | `PENDING` |

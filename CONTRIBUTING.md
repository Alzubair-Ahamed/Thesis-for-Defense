# Contributing and Research Governance Guide

This repository enforces the epistemic, reproducibility, and medical-data privacy standards of [BC_XAI_RESEARCH_OPERATING_SYSTEM.md](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md) and [BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md](./BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md).

## 1. Three-Tier Epistemic Discipline ([OS §1.1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01))
Every decision log, protocol, code comment, and manuscript draft must distinguish:
1. **`REPORT FACT (RF##)`:** Explicitly stated in `Title_defence_evaluation_report.pdf` with exact physical PDF page (1–11) and section/table locator.
2. **`PLANNING RECOMMENDATION`:** Methodological, statistical, or XAI rules introduced by this operating system; adopted only via a human-approved `DEC####` record.
3. **`Unresolved / Human Decision Required (UD##)`:** Open scientific or operational choices that block their designated milestone until resolved with evidence. Library defaults never silently resolve a `UD##` item.

## 2. Storage-Tier Firewall ([OS §10.2](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10))
- **Never commit Tier-2 or Tier-3 binary/restricted artifacts to Git:** Raw mammograms/DICOMs (`03_Datasets/raw/`), processed images (`05_Preprocessing/processed/`), restricted lesion ROI masks, private patient linkage tables, model checkpoints (`08_Checkpoints/*.pt|*.pth|*.h5|*.ckpt|*.onnx`), raw XAI attribution arrays, or credentials (`.env`).
- **Always inspect `git status` and `git diff --cached` before committing** to confirm only Tier-1 source code, configurations, non-sensitive CSV registries, aggregate reports, and hash manifests are staged.

## 3. Git Commit Conventions ([OS §10.1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10))
- **Repo-Local Author Identity:** Commits in this repository use `Alzubair Ahamed <Alzubair-Ahamed@users.noreply.github.com>`.
- **Semantic Commit Prefixes:** Use `docs(STEP-###):`, `research(STEP-###):`, `data(STEP-###):`, `labels(STEP-###):`, `xai(STEP-###):`, `experiment(STEP-###):`, `evaluation(STEP-###):`, `writing(STEP-###):`, `web(STEP-###):`, or `fix(STEP-###):`.
- **Step-by-Step Synchronization:** Execute one bounded blueprint step at a time, run its verification checklist, update its session diary note (`01_Project_Management/diary/`), and commit & push to `origin main`.

## 4. Universal Definition of Done ([OS Appendix A.3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a))
No step may be marked complete until:
1. All specified outputs exist at their canonical paths with verified SHA-256 digests.
2. Verification checklist items are backed by objective command or review evidence.
3. Required human decisions (`DEC####`) and prerequisite quality gates (`G01–G17`) hold current `PASS`.
4. Owning CSV registries and session diary notes (`T03`) are updated without foreign-key errors.

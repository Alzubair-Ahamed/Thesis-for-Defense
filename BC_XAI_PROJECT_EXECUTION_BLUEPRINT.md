# BC-XAI PROJECT EXECUTION BLUEPRINT

## Cover page

**Approved research title:** Explainable Deep Learning-Based Early Breast Cancer Detection Using Mammogram Images

| Field | Value |
|---|---|
| Document | BC_XAI_PROJECT_EXECUTION_BLUEPRINT.md |
| Version / date | v1.0.0 / 2026-11-23 |
| Type | Sequential Q1-grade research execution manual |
| Governing handbook | [BC-XAI Research Operating System](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md), v1.0.0 |
| Primary scientific authority | `Title_defence_evaluation_report.pdf` (11 physical pages inspected; see [source provenance](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#source-status)) |
| Status | Complete planning document; execution NOT VERIFIED; all steps NOT STARTED; all gates NOT ASSESSED |
| Coverage | 16 stages (`S01–S16`); 50 sequential step types (`STEP-001` through `STEP-050`), with bounded repeatable sessions for PRISMA reading, label/mask auditing, multi-architecture/multi-seed training, XAI auditing, and writing |
| Researchers | Alzubair Ahamed (ID: 232-15-591); Md Riyadul Hasan (ID: 232-15-486) (report cover, p. 1) |
| Supervisors | Supervisor: Israt Jahan, Lecturer (Senior Scale); Co-Supervisor: Ms Faiza Feroz, Lecturer (report cover, p. 1) |
| Intended system | Reproducible, quantitatively evaluated Explainable Deep Learning CAD research framework for 2D mammogram Benign vs Malignant classification (Grad-CAM baseline + approved XAI comparators), FYDP thesis, Q1 journal manuscript pathway, and conditional hosted defense web showcase (S16, gated by UD25) |

## Version history

| Version | Date | Change | Approval |
|---|---|---|---|
| v1.0.0 | 2026-11-23 | Initial 16-stage, 50-step, 17-gate Q1 execution blueprint aligned 1:1 with `BC_XAI_RESEARCH_OPERATING_SYSTEM.md` v1.0.0 | Proposed; human adoption pending; all gates NOT ASSESSED |

## How to use this blueprint

1. Read [OS §1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01) first. **REPORT FACT (`RF01–RF20`)**, **PLANNING RECOMMENDATION**, and **Unresolved / Human Decision Required (`UD01–UD28`)** carry identical epistemic discipline in both documents. Treat the report's novelty/gap claims (`RF16`) strictly as hypotheses to test and potentially refine for Q1 publication.
2. Start at `STEP-001` and advance sequentially only when prerequisites carry verifiable evidence. Every step starts **NOT STARTED**; unchecked boxes (`- [ ]`) are future verification duties, never completed work; all gates `G01–G17` start **NOT ASSESSED**.
3. The Operating System defines policy; this Blueprint sequences execution. Its [repository contracts](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02), [canonical schemas](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b), [templates (`T01–T35`)](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-14), and [Universal DoD](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a) apply to every step.
4. For each working session, log `STEP-###` plus a dated batch or `RUN####` identifier in `01_Project_Management/diary/`. Time estimates below are **provisional planning estimates** excluding external DUA turnaround, clinical-advisor/supervisor review delays, and measured GPU training wall-clock time.
5. `Parallelizable` permits independent work only after all prerequisites pass and never authorizes crossing a `NOT ASSESSED`, `FAIL`, or `STALE` gate or editing canonical CSV registries concurrently without serialized ID assignment.
6. Execute the **Planning/review prompt** before the **Implementation prompt**. Never treat library defaults as tacit resolution of a `UD##` item.
7. Gate `PASS` requires dated, hash-verified evidence bound to exact entity versions in `01_Project_Management/gates.csv` ([OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13)). A methodologically sound experiment with modest AUC or imperfect XAI localization still passes its validity gate when reported honestly.
8. Only the two planning Markdown files exist right now; all listed repository directories, scripts, registries, and outputs are future execution contracts.

## Source-specific execution constraints

- **Binary 2D mammography scope (`RF05`, `RF14–RF15`):** Classify 2D mammograms into Benign vs Malignant only. Strictly exclude MRI, CT, Ultrasound, Histopathology, staging/treatment/survival analysis, hospital/PACS integration, mobile/IoT apps, real-patient clinical trials, and automated medication/treatment recommendations.
- **No pre-selected datasets or split ratios (`RF19`):** Public mammogram collections (e.g., CBIS-DDSM, INbreast, VinDr-Mammo, CMMD, MIAS, Mini-DDSM, RSNA) are discovery candidates under `UD05`. No split ratio is stated in the report; lock connected-component patient/view/duplicate grouping and split design under `UD10–UD11` (and evaluate an independent external-validation cohort for Q1 rigor).
- **Architecture discrepancy preserved (`RF07`):** Sec. 4 lists 5 CNNs, Obj. 3 lists 6 (adding MobileNetV2), and Sec. 2 also mentions Xception. Resolve the exact roster (plus any optional Q1 modern baseline) formally under `UD13` in `STEP-022`.
- **Six mandatory metrics + Q1 suite (`RF09`, `UD19–UD20`):** Always report Accuracy, Precision, Recall (Sensitivity), F1-score, AUC-ROC, and Confusion Matrix, augmented by prospectively approved Specificity, PR-AUC, calibration (ECE/Brier), patient-clustered 95% CIs, and paired DeLong/McNemar tests.
- **Quantitative XAI is non-negotiable for Q1 (`RF08`, `UD16–UD18`):** Grad-CAM is mandatory; visual overlays alone are insufficient. Prospectively freeze target layers, perturbation faithfulness (Deletion/Insertion/ROAD), Adebayo sanity checks, ROI-mask localization (Pointing Game/EBPG/IoU), stability, and bounded blinded clinical-advisor review.
- **Table 1.1 / reference anomalies & blank feedback (`RF17–RF18`, `RF20`):** Audit all seed references `[1]`–`[12]`, quarantine handwritten-bracket/SL 10 Hassan-vs-Bazazeh mismatches and non-mammogram comparators (`UD04`), and never invent examiner feedback for Page 11's blank comment lines (`UD01`).
- **Conditional FYDP defense web demo (`UD25`, §8.3):** Stage S16 (`STEP-048–050`, `G17`) runs **only** if adopted under `UD25`. It is a thin, research-only defense showcase calling the frozen `STEP-038` CAD+Grad-CAM path—never hospital deployment and never evaluation evidence.

<a id="stage-map"></a>
## Stage-to-step map and contents

| Stage | Steps / navigation | Governing handbook | Exit gate(s) |
|---|---|---|---|
| S01 Foundation, scope constitution, and unresolved-decision assignment | [001](#step-001) | §1, §11 | G01 |
| S02 Repository architecture, templates, registries, and minimal data runtime | [002](#step-002)–[003](#step-003) | §2, §10, §14, App. A–B | G02 |
| S03 PRISMA literature search, screening, extraction, and bibliography verification | [004](#step-004)–[007](#step-007) | §3 | Feeds G03 |
| S04 Novelty/gap verification, Q1 contribution framing, and RQ approval | [008](#step-008)–[009](#step-009) | §1, §3 | G03 |
| S05 Public mammogram dataset discovery (internal & external), permissions, and raw intake | [010](#step-010)–[012](#step-012) | §4, §10 | Permissions before intake; feeds G04 |
| S06 Mammogram image integrity, artifact/privacy QC, and dataset suitability approval | [013](#step-013) | §4 | G04 |
| S07 Diagnostic label provenance, ROI-mask audit protocol, and prospective XAI governance | [014](#step-014)–[015](#step-015) | §4, §6 | G05 |
| S08 Label/ROI-mask verification execution, pathology/BI-RADS audit, and verified label freeze | [016](#step-016)–[018](#step-018) | §4, §6 | G06 |
| S09 Mammography preprocessing design, patient-level leakage-safe splitting, and versioned release | [019](#step-019)–[021](#step-021) | §4 | G07, G08 |
| S10 Transfer learning architecture roster, model runtime, experiment/XAI/stat plan, and pipeline readiness | [022](#step-022)–[026](#step-026) | §5, §6, §7, §10 | G09 |
| S11 Multi-architecture CNN training, controlled ablations, multi-seed runs, and checkpoint governance | [027](#step-027)–[031](#step-031) | §5, §10 | G10 per qualifying EXP |
| S12 Validation-only model/threshold/calibration selection, final-test freeze, and locked test inference | [032](#step-032)–[033](#step-033) | §7 | G11 before testing |
| S13 Q1 classification metrics, calibration, statistical testing, quantitative XAI faithfulness/sanity/localization, and external validation | [034](#step-034)–[036](#step-036) | §6, §7 | G12 |
| S14 Stratified failure & clinical-alignment XAI review, local CAD prototype, and CLAIM/TRIPOD+AI reproducibility audit | [037](#step-037)–[039](#step-039) | §6, §7, §8 | G13, G14 |
| S15 Evidence-first writing, FYDP thesis submission, Q1 journal manuscript & peer-review workflow, archival, and closure | [040](#step-040)–[047](#step-047) | §9, §10, §13 | G15 (`thesis`/`paper`), G16 |
| S16 Conditional hosted web demonstration (Grad-CAM CAD showcase) for FYDP defense | [048](#step-048)–[050](#step-050) | §8.3, §10, §13 | G17 (feeds G16 if UD25 adopted) |

## Master dependency chain

```text
001/G01 → 002–003/G02 → 004–009/G03 → 010–013/G04
→ 014–015/G05 → 016–018/G06 → 019–020/G07 → 021/G08
→ 022–026/G09 → [027 → 028 → 029/G10] → 030 multi-arch benchmark → 031 ablations & multi-seed
→ 032/G11 → 033 locked internal + external inference → [034 metrics/cal/stats + 035 quantitative XAI] → 036/G12
→ 037 subgroups/errors/clinical XAI/G13 → 038 local CAD prototype → 039 clean repro + CLAIM/TRIPOD+AI/G14
→ 040–043/G15(thesis) → 044 thesis submit → 045 Q1 paper [G15(paper) + submit/rebuttal OR approved disposition]
→ 046 tiered archive → 047/G16

Conditional parallel web branch (S16 — executed ONLY if UD25 adopted, alongside 039–044):
038 → 048 scope/model/platform/policy → 049 thin Grad-CAM web app + parity → (G14 PASS) → 050 deploy + fallback/G17 → defense
G17 (or UD25 non-adoption disposition) → 046 archive → 047/G16
Optional non-medical hosting spike (synthetic image, generic CNN, zero research evidence): any time after G02
```

Phase 1 data tooling (`environment/data/`, `STEP-002`) is verified at `G02`; Phase 2 DL/XAI tooling (`environment/model/`, `STEP-023`) is locked after architecture selection without overwriting Phase 1 provenance. Connected-component patient splitting (`G07`) strictly precedes training-only preprocessing fitting (`G08`) and all training augmentation. `STEP-030` and `STEP-031` iterate `STEP-027–029` under unique `EXP####` IDs without touching held-out internal or external test sets.

## Universal session and artifact expectations

Every step inherits [Universal DoD](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a). Log actual input hashes, commands, outputs, verification evidence, decisions (`T02`), deviations, and next action in `01_Project_Management/diary/` (`T03`), using `T32` for any versioned AI-assistance prompts and `T33` for milestone/risk reviews. Source-control rules cover Tier-1 safe metadata only; raw mammograms, ROI masks, patient linkage tables, checkpoints, full predictions, and raw XAI arrays reside in approved Tier-2/Tier-3 storage with SHA-256 checksums.

Standing constraint for all **Planning/review prompts**: read governing OS sections and live registries, preserve the `RF##` / `PLANNING RECOMMENDATION` / `UD##` distinction, list blockers honestly, and never assert unperformed work. Standing constraint for all **Implementation prompts**: follow ratified decisions only, preserve immutable raw/source artifacts, fail loudly on unresolved nulls or hash mismatches, record exact code/environment hashes, and emit verifiable check outputs.

---

<a id="step-001"></a>
## STEP-001 — Confirm the research mandate, team roles, and unresolved-decision register

**Objective:** Ratify the approved mammography XAI scope, assign team operational leads and deadlines across `UD01–UD28`, and pass `G01` without prematurely guessing unknown scientific choices.

**Why this step exists:** `Title_defence_evaluation_report.pdf` approves the topic, binary task, and high-level objectives, but leaves datasets, image paradigm, split design, architecture roster reconciliation, XAI metrics, and Q1 journal target unresolved.

**Governing section references:** [OS §1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §11](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** Both planning documents and `Title_defence_evaluation_report.pdf` available; researchers (Alzubair Ahamed, Md Riyadul Hasan) and supervisors (Israt Jahan, Ms Faiza Feroz) available to ratify scope; zero research execution assumed.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours plus supervisor review turnaround.

**Parallelizable:** No for formal scope ratification; preliminary Q1 journal shortlist and clinical-advisor outreach planning may be drafted in parallel.

**Inputs:** `Title_defence_evaluation_report.pdf` (`RF01–RF20`), `UD01–UD28` register, institutional FYDP calendar/requirements, and supervisor confirmation of any separate title-defense comments.

**Expected outputs:** Ratified scope constitution (`scope.md`), named role assignments for team members, initialized `UD01–UD28` ownership/milestone ledger, verified p. 11 feedback-status note, initial clinical-advisor outreach log, conditional web-demo inquiry (`UD25`), and `G01` assessment.

**Repository/file changes:** Create `01_Project_Management/scope.md`, `01_Project_Management/decisions.csv`, `01_Project_Management/decision_log/DEC0001.md`, and `01_Project_Management/reviews/G01_assessment_<date>.md` (permitted prior to STEP-002's full skeleton).

**Execution procedure:**

1. Verify verbatim title (`RF01`), researchers/supervisors (`RF02`), O1–O6 (`RF12`), and Section 8 exclusions (`RF15`) with the supervisor; separate the p. 1 signed certificate (`RF03`) from approval of new Q1 planning policies.
2. Confirm explicitly with the supervisor whether any verbal or written title-defense feedback exists beyond the blank comment lines on Page 11 (`RF20`); record only actual feedback or explicit confirmation that none was supplied (`UD01`).
3. Assign named team leads (Literature, Data Steward, Model/XAI, Evaluation, Writing/Release, Conditional Deployment) and blocking milestones for every `UD01–UD28` entry while leaving downstream scientific values unresolved.
4. Initiate early inquiries for (a) a qualified breast radiologist / clinical advisor (`UD18`), (b) preliminary target Q1 journal alignment (`UD02`), and (c) whether a conditional FYDP defense hosted web demo is desired (`UD25`).
5. Obtain supervisor sign-off on scope and operating-system adoption; record dated `G01` PASS/FAIL assessment.

**Planning/review prompt:**

> Audit `BC_XAI_RESEARCH_OPERATING_SYSTEM.md` §1 against `Title_defence_evaluation_report.pdf` (`RF01–RF20`). Prepare a concise scope ratification and role-assignment brief listing only decisions required at `G01` (`UD01`, initial `UD02`/`UD25` inquiries) and preserving all downstream `UD` items as explicitly unresolved.

**Implementation prompt:**

> Documentation only: create `scope.md`, initial `decisions.csv` rows for actual `G01` decisions, `DEC0001.md`, and the blank-until-signed `G01` review file. Do not select datasets, architectures, or split ratios, and never pre-mark `G01` as PASS.

**Human-only actions and decisions:** Researchers and supervisor ratify scope, role ownership, actual feedback status (`UD01`), preliminary Q1 paper intent (`UD02`), and initial defense web-demo intent (`UD25`).

**Version-control/artifact expectations:** Keep `Title_defence_evaluation_report.pdf` immutable and verified against its SHA-256 hash; save `01_Project_Management/` initial records durably for Git initialization in STEP-002.

**Documentation updates:** Update planning cover approval status only after actual ratification; initialize `scope.md` and `decisions.csv`.

**Verification checklist:**

- [ ] Verbatim approved title, team/supervisor identities, O1–O6, and all 6 Section 8 exclusions confirmed.
- [ ] All `UD01–UD28` items assigned named owners and blocking milestones without inventing scientific values.
- [ ] Page 11 blank comment lines verified honestly; zero fabricated examiner feedback.
- [ ] `G01` assessment contains dated supervisor approval evidence.

**Common mistakes:** Treating the p. 1 title-defense certificate as ethics or dataset clearance; silently resolving the 5-vs-6 CNN discrepancy or guessing a 70/15/15 split ratio during kickoff.

**Recovery procedure:** Issue a superseding `DEC####` correcting scope or role errors, preserve earlier wording intact, and reassess `G01` before starting STEP-002.

**Definition of Done:** Scope constitution, role ownership, and decision governance ratified with dated `G01 PASS`. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-002](#step-002)

---

<a id="step-002"></a>
## STEP-002 — Instantiate repository skeleton, storage-tier controls, and minimal data-tool environment

**Objective:** Establish canonical folder homes, Git privacy safeguards, approved restricted storage tiers, and a pinned, smoke-tested Phase 1 data-tool environment (`environment/data/`).

**Why this step exists:** Mammography DICOMs, masks, patient linkage tables, and checkpoints require storage isolation before intake, and early QC/splitting scripts require a reproducible runtime separate from the later GPU/DL stack.

**Governing section references:** [OS §2](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-001` complete; `G01 PASS`; `UD14` storage-tier, private Git remote, and Phase-1 runtime choices approved.

**Estimated difficulty and time (provisional):** Moderate; 4–6 hours including minimal runtime smoke checks.

**Parallelizable:** Drafting individual folder `README.md` (`T01`) files may run in parallel; Git initialization, `.gitignore` testing, and `environment/data/` lock verification are serialized.

**Inputs:** OS Section 2 folder contracts, Section 10 storage/environment policy, `STEP-001` records, and approved `UD14` storage/access decision.

**Expected outputs:** Complete canonical directory skeleton, root governance files (`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `.gitignore`, `.gitattributes`), folder READMEs, documented storage-tier access map, and pinned, smoke-tested `environment/data/`.

**Repository/file changes:** Create `src/bc_xai/`, `tests/`, `environment/data/` (lockfile + `verification.md`), `01_Project_Management/` through `15_Archive/` (and `web/` + `16_Web_Demo/` placeholders only if `UD25` remains open/adopted), root Git governance files, and `12_Documentation/installation.md` + `pipeline.md` storage section; bring `STEP-001` files under Git.

**Execution procedure:**

1. Verify SHA-256 hashes of all existing planning and source files; initialize local Git repository and approved private remote (`UD14`)—never a public remote before release clearance.
2. Materialize Section 2 domain folders with `T01` folder READMEs and empty `src/bc_xai/` + `tests/` package scaffolding without choosing a deep learning framework yet.
3. Configure `.gitignore` and `.gitattributes` to block raw mammograms/DICOMs, processed releases, ROI masks, checkpoints, patient linkage tables, secrets, and raw XAI arrays; verify ignore rules with safe dummy filenames.
4. Build and lock `environment/data/` (minimal Python data/CSV/image/DICOM/graph-component/pytest tools); run synthetic smoke tests verifying CSV validation, image decoding, SHA-256 hashing, and connected-component grouping, recording results in `environment/data/verification.md`.
5. Document Tier 1–4 storage locations, access permissions, and backup procedures in `12_Documentation/pipeline.md`; omit `LICENSE` until `UD24` is ratified.

**Planning/review prompt:**

> Convert OS §2 and §10 into an exact repository bootstrap checklist, `.gitignore` safety specification, and Phase-1 `environment/data/` dependency specification. List every sensitive mammography artifact pattern that must be excluded from Git.

**Implementation prompt:**

> Create the approved directory tree, folder READMEs, root governance files, tested `.gitignore`, and pinned `environment/data/` environment. Execute synthetic smoke checks and save actual command output to `environment/data/verification.md`; defer PyTorch/TensorFlow and GPU packages to `STEP-023`.

**Human-only actions and decisions:** Researchers approve private Git remote/access, Tier-2/Tier-3 storage destinations, and backup locations (`UD14`).

**Version-control/artifact expectations:** Commit initial safe skeleton, `STEP-001` records, and `environment/data/` lock; inspect `git status` and staged diff to verify zero restricted files or credentials.

**Documentation updates:** Root `README.md`, `CHANGELOG.md`, `12_Documentation/installation.md`, `12_Documentation/pipeline.md`, and `environment/data/verification.md`.

**Verification checklist:**

- [ ] Directory names and folder READMEs match OS §2.1–2.2 exactly.
- [ ] `.gitignore` verified with synthetic dummy DICOM, checkpoint, and linkage paths.
- [ ] `environment/data/` lockfile and synthetic smoke tests pass and are recorded.
- [ ] Zero deep-learning framework or GPU assumptions leaked into Phase 1 environment.
- [ ] Source PDF and planning file hashes verified untouched.

**Common mistakes:** Pushing to a public GitHub repo prematurely; installing heavy DL/CUDA libraries into `environment/data/`; forgetting `.gitignore` does not untrack files committed earlier.

**Recovery procedure:** Remove misclassified tracked files safely before remote push, repair `.gitignore`, rebuild clean `environment/data/` lock, and re-run smoke checks.

**Definition of Done:** Safe, documented repository skeleton, storage-tier policy, and smoke-tested `environment/data/` runtime exist; ready for registry bootstrap. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-003](#step-003)

---

<a id="step-003"></a>
## STEP-003 — Install blank templates, canonical CSV registries, and validation checks

**Objective:** Materialize all 35 blank templates (`T01–T35`), initialize all 24 canonical CSV registries header-only, implement automated schema/link checks, and pass `G02`.

**Why this step exists:** Uniform schemas and automated foreign-key/hash validators prevent divergent spreadsheets, broken lineage, and fabricated placeholder rows across multi-month execution.

**Governing section references:** [OS §2](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS §14](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-002` complete; storage policy and smoke-tested `environment/data/` verified.

**Estimated difficulty and time (provisional):** Moderate; 3–5 hours.

**Parallelizable:** Drafting individual blank templates (`T01–T35`) may be divided; canonical CSV headers, validator logic, and `G02` audit are reviewed centrally.

**Inputs:** OS §14 (`T01–T35`), Appendix A.4 common columns, Appendix B 24 registry schemas, and actual `STEP-001` decisions.

**Expected outputs:** Blank versioned `T01–T35` files, 24 canonical CSV registries with exact Appendix B + common headers, automated registry/link validator under `13_Automation/`, `dashboard.md`, `timeline.md`, initialized `risk_register.csv`, and `G02` assessment.

**Repository/file changes:** Populate `14_Templates_Prompts/` (`T01–T35`), initialize all 24 CSV files listed in Appendix B, create `01_Project_Management/dashboard.md`, `timeline.md`, `13_Automation/validate_registries.py`, unit tests in `tests/test_registries.py`, and `01_Project_Management/reviews/G02_assessment_<date>.md`.

**Execution procedure:**

1. Author blank field-complete templates `T01–T35` in `14_Templates_Prompts/` with common headers and explicit `Unresolved / Human Decision Required` / `not reported` instructions.
2. Create all 24 canonical CSV files matching Appendix B + Appendix A.4 common columns exactly; populate only genuinely evidenced `STEP-001` decisions, initial `risk_register.csv` themes (status unassessed until evaluated), and `G01–G17` rows in `gates.csv` (`NOT ASSESSED` except evidenced `G01`).
3. Implement `13_Automation/validate_registries.py` using `environment/data/` to verify exact column headers, unique IDs, valid foreign keys, absence of dummy scientific rows, and intact folder READMEs; test it with `pytest`.
4. Run validator, verify `environment/data/verification.md` currency, and perform the dated `G02` assessment.

**Planning/review prompt:**

> Cross-check all 24 Appendix B CSV schemas and `T01–T35` template fields against OS §14 and Appendix B. Identify any column mismatch, missing foreign-key check, or status implying premature research completion.

**Implementation prompt:**

> Materialize blank `T01–T35` templates, exact header-only CSV registries (retaining real `STEP-001` entries only), and `13_Automation/validate_registries.py` with synthetic `pytest` fixtures. Execute validation and log actual outputs.

**Human-only actions and decisions:** Research lead verifies schema ownership, validator output, and signs off `G02`.

**Version-control/artifact expectations:** Commit templates, schemas, validator, tests, and `G02` audit as `docs: initialize BC-XAI templates, registries, and G02 readiness`.

**Documentation updates:** Template index, registry owner table, `dashboard.md`, `timeline.md`, and `gates.csv`.

**Verification checklist:**

- [ ] All 24 CSV paths and column headers match OS Appendix B + A.4 verbatim.
- [ ] All 35 templates (`T01–T35`) exist, are blank, and include common metadata headers.
- [ ] Zero dummy papers, datasets, experiments, or pre-marked `PASS` gates exist.
- [ ] Automated validator and `pytest` pass inside `environment/data/`.
- [ ] `G02` mandatory criteria evidenced and signed.

**Common mistakes:** Creating competing summary spreadsheets alongside canonical CSVs; leaving example dummy rows inside registries; skipping automated foreign-key validation.

**Recovery procedure:** Consolidate duplicate files into canonical Appendix B paths, purge any synthetic test entries from live registries, re-run validator, and reassess `G02`.

**Definition of Done:** `G02 PASS` with complete templates, canonical registries, passing validator, and verified Phase-1 runtime. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-004](#step-004)

---

<a id="step-004"></a>
## STEP-004 — Approve PRISMA-style systematic literature search and screening protocol

**Objective:** Establish a reproducible PRISMA literature search and eligibility protocol specifically designed to test—and challenge—the title report's novelty and XAI gap assumptions (`RF16`).

**Why this step exists:** Q1 journals reject literature reviews that ignore existing mammography XAI benchmarks or mix non-mammogram histopathology/tabular studies into direct comparators.

**Governing section references:** [OS §1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-003` complete; `G01–G02 PASS`; provisional RQs bounded by O1–O6 (`RF12`).

**Estimated difficulty and time (provisional):** Moderate; 3–4 hours.

**Parallelizable:** Database-specific syntax translations (PubMed, IEEE Xplore, Scopus, ScienceDirect, SpringerLink, arXiv/medRxiv) may be drafted in parallel after shared eligibility rules are approved.

**Inputs:** Report seed references `[1]`–`[12]` (`RF17–RF18`), provisional gap themes (`RG1–RG4`), candidate RQs, institutional database access list, and `UD03`.

**Expected outputs:** Approved PRISMA search protocol, database-specific Boolean strings, two-stage screening eligibility criteria, exclusion code table, modality/paradigm separation rules, and quality appraisal checklist.

**Repository/file changes:** Create `02_Literature/searches/protocol.md`, `02_Literature/research_questions.md` (marked *provisional*), and `DEC####` resolving search-scope portion of `UD03`.

**Execution procedure:**

1. Define exact Boolean queries per accessible database actively targeting: (a) 2D mammography transfer learning + XAI (Grad-CAM, Grad-CAM++, Score-CAM, LayerCAM, SHAP, LIME, Integrated Gradients, ViT attention), (b) quantitative XAI faithfulness/sanity/localization studies in mammography, and (c) external cross-dataset validation and calibration in breast cancer screening AI.
2. Specify date window, language policy, preprint tagging rules, deduplication keys (DOI/title/preprint-to-journal linking), and explicit full-text exclusion codes.
3. Establish strict taxonomic buckets separating **Direct 2D Mammography + XAI**, **Direct 2D Mammography DL (non-XAI)**, **Non-Mammogram Breast Imaging (histopathology/BreakHis/ultrasound/MRI)**, **Tabular Datasets (Wisconsin)**, and **Surveys/Reviews**.
4. Define methodological appraisal fields (patient-level vs image-level split, FFDM vs ROI paradigm, biopsy vs BI-RADS labels, external cohort presence, quantitative vs purely visual XAI, calibration/statistical testing, code availability) rather than citation-count cutoffs.
5. Obtain literature lead and supervisor approval before executing searches.

**Planning/review prompt:**

> Design a PRISMA search protocol capable of refuting `RF16` ("most previous research does not integrate XAI"). Specify exact database queries, modality/task separation rules, and quantitative-XAI extraction fields without claiming any search has been run yet.

**Implementation prompt:**

> Documentation only: save approved `02_Literature/searches/protocol.md` and provisional `research_questions.md`; log inaccessible databases honestly as coverage limits. Do not fabricate retrieved counts or citations.

**Human-only actions and decisions:** Literature lead and supervisor approve search databases, date cutoff, eligibility criteria, and database access constraints (`UD03`).

**Version-control/artifact expectations:** Commit protocol and search templates as `research: approve PRISMA mammography XAI search protocol`.

**Documentation updates:** `02_Literature/searches/protocol.md`, `decisions.csv` (`UD03` search portion), and `dashboard.md`.

**Verification checklist:**

- [ ] Exact database queries actively seek existing mammography + XAI and faithfulness benchmarks.
- [ ] Modality/task separation quarantines histopathology and tabular studies from direct comparators.
- [ ] Exclusion codes, deduplication rules, and quality appraisal criteria frozen prior to screening.
- [ ] Zero search results claimed as executed yet.

**Common mistakes:** Treating Table 1.1's 10 entries as a sufficient literature baseline; querying only papers lacking XAI to confirm `RF16`; omitting quantitative-XAI keywords.

**Recovery procedure:** Amend biased or syntactically broken queries via versioned protocol revision with logged rationale and rerun affected searches cleanly.

**Definition of Done:** Approved, reproducible PRISMA search and screening protocol ready for execution. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-005](#step-005)

---

<a id="step-005"></a>
## STEP-005 — Execute database searches and register deduplicated candidate papers

**Objective:** Run all approved database queries, capture raw search exports, ingest report seed references `[1]`–`[12]`, and build a deduplicated, auditable candidate registry.

**Why this step exists:** PRISMA flow reproducibility and duplicate elimination require exact retrieval logs before screening begins.

**Governing section references:** [OS §3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-004` protocol approved; institutional/public database access confirmed.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours per database batch, repeated until protocol coverage is complete.

**Parallelizable:** Running independent database queries can proceed in parallel; serialize `P####` ID allocation and cross-database deduplication.

**Inputs:** Approved queries (`02_Literature/searches/protocol.md`), report seed references `[1]`–`[12]` (`RF18`), and lawful database export tools.

**Expected outputs:** Dated search logs (`T04`), raw export files with SHA-256 hashes, deduplicated `02_Literature/papers.csv` entries, seed-reference tags (`ReportRef`), and lawful full-text storage pointers.

**Repository/file changes:** Populate `02_Literature/searches/` (`T04` logs + exports), `02_Literature/papers.csv`, initial `02_Literature/references.bib` (metadata verification flagged `pending`), and permitted full-text PDFs/restricted pointers.

**Execution procedure:**

1. Execute each approved query verbatim; record exact syntax, date, filters, retrieved count, and raw export hash using `T04`.
2. Register all 12 report seed references `[1]`–`[12]` with `ReportRef = [1]..[12]` and `MetadataVerified = unverified` (explicitly logging Table 1.1 SL 10 "Hassan et al." separately as an unresolved anomaly lead under `UD04` rather than merging it with Bazazeh & Shubair `[10]`).
3. Deduplicate across databases by DOI, normalized title, and preprint-to-journal pairs; record `DuplicateOf` links without erasing retrieved counts.
4. Retrieve legal full texts via institutional subscriptions or open-access repositories; log paywalled/inaccessible items honestly without bypassing access controls.

**Planning/review prompt:**

> Audit search export logs and deduplication results against `02_Literature/searches/protocol.md`. Verify every seed reference `[1]`–`[12]` and Table 1.1 SL 10 anomaly is tracked distinctly with `MetadataVerified = unverified`.

**Implementation prompt:**

> Ingest actual search exports into `02_Literature/papers.csv` and save `T04` logs with export SHA-256 hashes. Keep unverified bibliographic fields marked `unverified`/`unknown`; never summarize unread papers or fabricate DOIs.

**Human-only actions and decisions:** Researchers execute lawful institutional retrieval and approve any interlibrary/access requests without bypassing paywalls.

**Version-control/artifact expectations:** Commit `T04` search logs, `papers.csv`, and safe export metadata; keep copyrighted full-text PDFs outside public Git.

**Documentation updates:** `02_Literature/papers.csv`, `02_Literature/searches/`, and PRISMA identification counts.

**Verification checklist:**

- [ ] Every `P####` record traces to a dated `T04` search log or `ReportRef` seed.
- [ ] Preprints and published versions linked via `DuplicateOf`, never double-counted.
- [ ] Table 1.1 SL 10 ("Hassan et al.") tracked distinctly from Ref `[10]` (Bazazeh & Shubair) pending `UD04` audit.
- [ ] Zero fabricated DOIs, authors, or retrieval counts.

**Common mistakes:** Dropping duplicate counts before logging raw PRISMA totals; silently overwriting report seed references without preserving anomaly history; committing copyrighted bulk PDFs to Git.

**Recovery procedure:** Re-export unlogged queries, reconcile deduplication keys deterministically, and re-run `validate_registries.py`.

**Definition of Done:** All planned search batches executed, logged, deduplicated, and registered with explicit access limits. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-006](#step-006)

---

<a id="step-006"></a>
## STEP-006 — Screen candidate records and document PRISMA eligibility

**Objective:** Execute transparent two-stage screening (title/abstract, then full text) with explicit exclusion codes and strict modality/task separation.

**Why this step exists:** Auditable screening prevents confirmation bias (such as excluding strong mammography XAI papers that challenge `RF16`) and creates exact counts for the Q1 PRISMA flow diagram.

**Governing section references:** [OS §3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-005` deduplicated batch registered; approved screening criteria from `STEP-004`.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours per screening batch depending on retrieval volume.

**Parallelizable:** Dual independent screening across disjoint batches or paired reviewers; reconcile conflicts serially before finalizing `screening.csv`.

**Inputs:** Registered titles/abstracts, accessible full texts, and `02_Literature/searches/protocol.md` eligibility criteria.

**Expected outputs:** Complete `02_Literature/screening.csv` (`SCR####`) decisions, full-text exclusion reasons, conflict resolutions, reconciled PRISMA flow numbers, and categorized inclusion sets.

**Repository/file changes:** Populate `02_Literature/screening.csv`, update `ReadingStatus` in `02_Literature/papers.csv`, and write `02_Literature/searches/screening_summary.md`.

**Execution procedure:**

1. Screen all unique records at title/abstract stage, advancing uncertain records conservatively to full-text review.
2. Screen accessible full texts and classify included records into **Direct 2D Mammography + XAI**, **Direct 2D Mammography DL (non-XAI)**, **Contextual Non-Mammogram/Tabular**, or **Systematic Review/Survey**; assign one exact exclusion code for every excluded full text.
3. Explicitly preserve strong competing mammography + XAI / faithfulness / external-validation papers even when they narrow `RF16`.
4. Reconcile reviewer disagreements in `ConflictResolution` and verify exact arithmetic reconciliation of PRISMA counts (`Retrieved - Duplicates = Screened; Screened - TitleAbsExcluded = FullTextAssessed; FullTextAssessed - FullTextExcluded = Included`).

**Planning/review prompt:**

> Audit `screening.csv` against `protocol.md` to detect biased exclusions, hidden counterevidence against `RF16`, or any histopathology/BreakHis/Wisconsin study mistakenly placed in the direct mammography comparator bucket.

**Implementation prompt:**

> Record actual screening decisions in `screening.csv`, compute reconciled PRISMA flow counts via script, and save `02_Literature/searches/screening_summary.md`.

**Human-only actions and decisions:** Researchers resolve screening conflicts and escalate boundary eligibility questions to the supervisor.

**Version-control/artifact expectations:** Commit `screening.csv`, updated `papers.csv`, and `screening_summary.md`.

**Documentation updates:** PRISMA flow counts, inclusion taxonomy, and inaccessible full-text list.

**Verification checklist:**

- [ ] Every unique record has explicit stage, decision, and exclusion reason where excluded.
- [ ] PRISMA counts reconcile arithmetically without double-counting duplicates.
- [ ] Competing mammography + XAI benchmarks explicitly retained.
- [ ] Non-mammogram and tabular papers segregated from direct mammography comparators.

**Common mistakes:** Excluding strong prior XAI papers to inflate novelty; dropping inaccessible records silently instead of reporting them in the PRISMA flow.

**Recovery procedure:** Reopen misclassified `SCR####` rows, document corrected eligibility decisions, regenerate PRISMA totals, and update downstream queues transparently.

**Definition of Done:** Current search corpus fully screened with reconciled PRISMA counts and transparent modality/task separation. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-007](#step-007)

---

<a id="step-007"></a>
## STEP-007 — Extract verified evidence from included studies and audit report bibliography anomalies

**Objective:** Produce source-grounded methodological extractions (`T05`) from full texts and formally verify/remediate all Table 1.1 and Reference `[1]`–`[12]` anomalies (`UD04`).

**Why this step exists:** Reported accuracy figures in mammography DL are uninterpretable without inspecting dataset version, FFDM-vs-ROI paradigm, patient-level leakage, XAI faithfulness validation, and publisher-verified citations.

**Governing section references:** [OS §3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-006` included studies; accessible full texts/supplements and publisher metadata portals.

**Estimated difficulty and time (provisional):** Hard; 1–3 hours per paper provisionally; repeated across all direct included studies and seed references `[1]`–`[12]`.

**Parallelizable:** Yes by assigned `P####` paper; cross-check critical numerical and `UD04` audit entries with a second reviewer.

**Inputs:** Included full texts/supplements, `T05` template, `Title_defence_evaluation_report.pdf` Table 1.1 (p. 6) & Section 9 References `[1]`–`[12]` (p. 10), and `UD04`.

**Expected outputs:** Structured `P####.md` extraction cards (`T05`), publisher-verified `references.bib`, complete `UD04` bibliography anomaly audit memo, and source-linked claim cards (`T07`) in `claims.csv`.

**Repository/file changes:** Create `02_Literature/summaries/P####.md`, `02_Literature/reports/report_bibliography_audit_UD04.md`, and `01_Project_Management/decision_log/DEC####.md` (`UD04`); update `papers.csv`, `references.bib`, and `claims.csv`.

**Execution procedure:**

1. Read full methods, tables, figures, and supplements of each included paper; extract dataset(s), FFDM vs ROI paradigm, label provenance, patient vs image split level, leakage risk, external validation, CNN/ViT models, preprocessing, XAI methods, quantitative XAI metrics (if any), classification/calibration/stat metrics with exact page/table locators, code access, and limitations (`T05`). Mark omitted fields `not reported`.
2. Conduct the mandatory `UD04` publisher audit of all 12 report references `[1]`–`[12]` and Table 1.1 rows SL 1–10: verify actual authors, titles, venues, years, DOIs, and datasets (specifically resolving handwritten brackets `[5]`–`[10]`, SL 10 "Hassan et al." vs printed Ref `[10]` Bazazeh & Shubair 2016, SL 5 Nahid & Kong 2017 survey, Ref `[9]` Tiwari et al. missing venue, Ref `[1]` Khalid et al. actual dataset, and Refs `[11]`–`[12]` WHO/ACS primary URLs).
3. Quarantine non-mammogram comparators (BreakHis histopathology, Wisconsin tabular) and unresolved/mismatched seed rows from direct mammography benchmarking tables.
4. Update `references.bib` with verified metadata only; record every empirical comparative statement in `claims.csv` with exact page/table locators.

**Planning/review prompt:**

> Extract `P####` using `T05` with exact page/table locators. Assess explicitly: (a) whether split leakage or ROI-only cropping inflates reported scores, (b) whether XAI was evaluated quantitatively or visually only, and (c) whether the study is directly comparable to 2D Benign-vs-Malignant mammogram classification.

**Implementation prompt:**

> Save verified `02_Literature/summaries/P####.md`, `report_bibliography_audit_UD04.md`, verified `references.bib` entries, and `claims.csv` candidates. Mark unverified fields explicitly; never guess unreported split levels or hyperparameters.

**Human-only actions and decisions:** Literature lead and co-researcher cross-verify all `UD04` bibliographic corrections and quarantine verdicts.

**Version-control/artifact expectations:** Commit summaries, `UD04` audit report, verified `references.bib`, and `papers.csv`/`claims.csv` updates; keep raw PDFs restricted where copyrighted.

**Documentation updates:** `papers.csv` (`MetadataVerified`, `ReadingStatus`), `references.bib`, `claims.csv`, and `DEC####` resolving `UD04`.

**Verification checklist:**

- [ ] Every extracted numerical result has an exact page/table/figure locator.
- [ ] Split level, paradigm (FFDM vs ROI), external validation, and quantitative XAI status extracted or marked `not reported`.
- [ ] All 12 report seed references and Table 1.1 anomalies (`RF17–RF18`) audited against primary publisher records (`UD04`).
- [ ] Non-mammogram/tabular/survey entries quarantined from direct mammography superiority tables.

**Common mistakes:** Copying Table 1.1 accuracy numbers unverified; citing SL 10 "Hassan et al. [10]" alongside Ref `[10]` Bazazeh & Shubair; comparing ROI-patch accuracy directly against whole-breast FFDM AUC without noting paradigm differences.

**Recovery procedure:** Downgrade any claim lacking a verified primary locator, re-check original publisher PDF/DOI, log corrections in `P####.md` history, and update `claims.csv`.

**Definition of Done:** Included direct corpus extracted with verified locators and all `UD04` report bibliography anomalies audited and remediated. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-008](#step-008)

---

<a id="step-008"></a>
## STEP-008 — Synthesize evidence, test the provisional XAI/novelty gap, and formulate Q1 contribution options

**Objective:** Rigorously test the report's preliminary novelty claims (`RF16`) against extracted counterevidence and design defensible Q1-grade scientific contribution options within the approved title and scope.

**Why this step exists:** Claiming "most prior work lacks XAI" will trigger immediate desk rejection at a Q1 journal if dozens of CNN + Grad-CAM mammography papers exist; genuine Q1 novelty requires identifying an evidenced methodological gap (e.g., quantitative XAI faithfulness/sanity/localization, leakage-free external generalization, calibration, or controlled ablation).

**Governing section references:** [OS §1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-007` extractions sufficient across direct mammography + XAI, leakage/external-validation, and calibration themes; `UD04` anomalies audited.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours per synthesis cycle.

**Parallelizable:** Thematic synthesis tables (architectures, datasets/splits, quantitative XAI, calibration) can be compiled independently before joint gap adjudication.

**Inputs:** Verified `P####.md` summaries, PRISMA screening coverage, `RG1–RG4` provisional themes, `UD02` target Q1 journal shortlist, and `T06` gap template.

**Expected outputs:** Evidence-backed `GAP####` records (`02_Literature/gaps.csv`, `gap_notes/GAP####.md`) with supporting and contradicting papers, thematic `synthesis.md`, and 2–3 concrete Q1 contribution options bounded by O1–O6 and Section 8 exclusions.

**Repository/file changes:** Populate `02_Literature/gaps.csv`, `02_Literature/gap_notes/GAP####.md`, `02_Literature/synthesis.md`, and update `claims.csv`.

**Execution procedure:**

1. Tabulate all direct 2D mammography + XAI papers by dataset, paradigm (FFDM vs ROI), patient-level split rigor, external validation, architectures, calibration, and whether XAI was validated quantitatively (faithfulness, Adebayo sanity checks, ROI localization) vs qualitative screenshots only.
2. Test `RG1–RG4` (`RF16`) directly against counterevidence; classify each `GAP####` honestly as `supported-within-search`, `narrowed`, `refuted`, or `unresolved` with explicit contradicting `P####` IDs.
3. Retain refuted or narrowed preliminary claims transparently in the audit log rather than deleting them.
4. Draft concrete, feasible Q1 scientific contribution options strictly inside the approved title and Section 8 exclusions (e.g., rigorous multi-architecture quantitative XAI faithfulness + Adebayo sanity + ROI localization + calibration + zero-shot external validation benchmark, plus an optional controlled preprocessing/loss/attention ablation).

**Planning/review prompt:**

> Challenge `RG1–RG4` (`RF16`) aggressively using our verified `P####` corpus. Quantify how many direct mammography papers already apply CNN + Grad-CAM, how many suffer from missing patient-level splits or external cohorts, and how many actually perform quantitative XAI faithfulness and sanity checks. Propose bounded Q1 contribution options staying strictly within O1–O6.

**Implementation prompt:**

> Documentation only: save `02_Literature/gaps.csv`, `gap_notes/GAP####.md`, and `02_Literature/synthesis.md` grounded exclusively in verified `P####` IDs. Preserve counterevidence and narrowed/refuted hypotheses explicitly.

**Human-only actions and decisions:** Researchers synthesize evidence; supervisor reviews Q1 contribution framing and feasibility against compute and timeline (`UD03`).

**Version-control/artifact expectations:** Commit `gaps.csv`, `gap_notes/`, `synthesis.md`, and updated `claims.csv` as `research: complete evidence-backed Q1 gap synthesis`.

**Documentation updates:** `gaps.csv`, `synthesis.md`, `claims.csv`, and candidate Q1 contribution brief for `STEP-009`.

**Verification checklist:**

- [ ] Every `GAP####` lists search coverage, supporting `P####`, and contradicting `P####`.
- [ ] Broad "absence of XAI in mammography" claim tested rigorously rather than accepted at face value.
- [ ] Zero cross-modality (histopathology/tabular) numerical superiority claims appear in synthesis.
- [ ] Proposed Q1 contribution options align 100% with approved title, O1–O6, and Section 8 exclusions.

**Common mistakes:** Counting citations as proof of novelty; erasing a refuted preliminary gap from the log; proposing an out-of-scope modality (ultrasound/MRI) or clinical trial to chase novelty.

**Recovery procedure:** Narrow unsupported wording, run targeted supplementary searches if coverage gaps emerge, log new `T04` searches, and revise `synthesis.md` before `STEP-009`.

**Definition of Done:** Evidence-backed gap analysis and feasible Q1 contribution options ready for supervisor ratification. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-009](#step-009)

---

<a id="step-009"></a>
## STEP-009 — Approve bounded research questions, Q1 contribution framing, and pass G03

**Objective:** Lock final operational Research Questions mapped to O1–O6, ratify the defensible Q1 scientific contribution, close `UD03–UD04`, and pass `G03`.

**Why this step exists:** Downstream dataset choice, external-cohort requirements, model roster, quantitative XAI protocol, and statistical tests must be driven by ratified RQs rather than ad-hoc exploration.

**Governing section references:** [OS §1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-008` synthesis complete; `STEP-004–007` PRISMA logs and `UD04` bibliography audit complete; `G01–G02` current `PASS`.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours plus supervisor ratification meeting.

**Parallelizable:** No for final scientific ratification; ongoing living-review alerts may continue afterward.

**Inputs:** O1–O6 (`RF12`), overarching report question (`RF11`), verified `GAP####`/`CLAIM####` records, `UD04` audit report, candidate Q1 contribution options, and preliminary `UD02` journal target list.

**Expected outputs:** Ratified `02_Literature/research_questions.md` (RQ-to-objective-to-metric traceability matrix), signed `DEC####` records resolving `UD03` and `UD04`, locked search cutoff date, and `G03` assessment.

**Repository/file changes:** Finalize `02_Literature/research_questions.md`; update `decisions.csv`, `decision_log/DEC####.md`, `claims.csv`, `gates.csv`, and `01_Project_Management/reviews/G03_assessment_<date>.md`.

**Execution procedure:**

1. Finalize stable `RQ1–RQ#` definitions translating `RF11` and O1–O6 into measurable discrimination, calibration, external-generalization, quantitative XAI (faithfulness/sanity/localization/stability), and controlled ablation questions without promising favorable outcomes.
2. Confirm `UD04` closure: verify every citation supporting `synthesis.md` and `research_questions.md` has primary-source verification; quarantine any remaining unverified report entries.
3. Ratify the bounded Q1 contribution statement with the supervisor (`UD03`) and record the exact literature search cutoff date.
4. Perform itemized `G03` audit (`T24`) verifying PRISMA reproducibility, counterevidence handling, `UD04` remediation, and supervisor sign-off.

**Planning/review prompt:**

> Audit the complete literature package (`STEP-004–008`) and verify that every finalized `RQ` maps cleanly to O1–O6, required dataset/mask properties, quantitative classification/XAI metrics, and explicit claim limits without inventing numeric targets or pre-selecting datasets.

**Implementation prompt:**

> Documentation only: save ratified `research_questions.md`, close `UD03–UD04` decision records, update `claims.csv`, and record the actual dated `G03` assessment outcome in `gates.csv`.

**Human-only actions and decisions:** Supervisor approves final RQs, Q1 contribution framing (`UD03`), `UD04` remediation disposition, and signs `G03`.

**Version-control/artifact expectations:** Commit finalized literature milestone, `research_questions.md`, and `G03` audit as `research: approve Q1 RQs and pass G03 literature gate`.

**Documentation updates:** `research_questions.md`, `decisions.csv`, `claims.csv`, `dashboard.md`, and `gates.csv`.

**Verification checklist:**

- [ ] Every approved RQ maps explicitly to O1–O6, verified `GAP####`, and testable evidence.
- [ ] Zero unsupported or refuted broad novelty claims survive unrevised.
- [ ] `UD04` Table 1.1 / Ref `[1]`–`[12]` anomalies resolved or quarantined with primary-source proof.
- [ ] PRISMA logs, screening counts, cutoff date, and supervisor-signed `G03` assessment complete.

**Common mistakes:** Requiring every proposal gap to be confirmed true before passing `G03`; phrasing RQs to assume a particular CNN will outperform all others; advancing to dataset downloads without ratified external-validation and ROI-mask requirements.

**Recovery procedure:** Keep `G03 FAIL`, return to `STEP-007/008` to verify missing citations or refine contribution bounds, and re-audit `G03`.

**Definition of Done:** `G03 PASS` with ratified RQs, defensible Q1 contribution bounds, and verified literature foundation. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-010](#step-010)

---

<a id="step-010"></a>
## STEP-010 — Discover and compare public 2D mammogram dataset candidates (internal & external)

**Objective:** Systematically audit public 2D mammogram collections to shortlist both a primary development/internal-test benchmark and an independent external cross-dataset validation candidate (`UD05`).

**Why this step exists:** `Title_defence_evaluation_report.pdf` selects no dataset (`RF19`), and Q1 medical imaging journals require verified primary provenance, reliable patient-level metadata, biopsy/BI-RADS label clarity, ROI-mask availability for XAI localization, and ideally an independent external validation cohort.

**Governing section references:** [OS §3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-009` complete; `G03 PASS`; approved RQs defining paradigm, ROI-mask, and external-cohort needs.

**Estimated difficulty and time (provisional):** Moderate; 4–6 hours across discovery and documentation review.

**Parallelizable:** Auditing candidate documentation portals (e.g., TCIA, PhysioNet, institutional archives) can run in parallel; consolidate provenance and mirror deduplication serially.

**Inputs:** Approved RQs (`02_Literature/research_questions.md`), literature dataset survey (`STEP-007`), original dataset papers/portals, and `UD05`.

**Expected outputs:** Evidence-backed `03_Datasets/candidates.csv` (`CAND####`), mirror-to-primary lineage mapping, and `candidate_comparison.md` shortlisting conditional primary and external candidates.

**Repository/file changes:** Populate `03_Datasets/candidates.csv` and create `03_Datasets/reports/candidate_comparison.md`.

**Execution procedure:**

1. Audit original authoritative sources (not unverified Kaggle/GitHub re-uploads) for candidate 2D mammogram repositories (such as CBIS-DDSM, INbreast, VinDr-Mammo, CMMD, MIAS, Mini-DDSM, RSNA screening, and any newly identified sources from `STEP-005–007`).
2. Record documented facts only (marking missing items `unknown` / `not reported`): modality (FFDM vs digitized SFM), original URL/DOI, access route/DUA, Benign/Malignant/Normal label provenance (biopsy vs BI-RADS), lesion ROI-mask/contour availability, `PatientID`/laterality/view metadata, BI-RADS breast density & mass/calcification metadata, and reported counts.
3. Explicitly detect and flag repackaged mirrors or subsets sharing upstream patients (e.g., DDSM vs CBIS-DDSM vs Mini-DDSM) via `DuplicateOf` so an overlapping derivative is **never** shortlisted as an independent external validation cohort.
4. Shortlist conditional primary and independent external candidates matching RQ requirements; formulate exact license/ethics questions for `STEP-011` without downloading restricted data yet.

**Planning/review prompt:**

> Compare audited public 2D mammogram candidates strictly from primary documentation. Evaluate each on patient-level grouping reliability, pathology vs BI-RADS ground truth, ROI-mask support for quantitative XAI localization, subgroup metadata (density/mass/calcification), and independence for Q1 external validation. Never invent sample counts or treat mirrors as independent cohorts.

**Implementation prompt:**

> Populate `03_Datasets/candidates.csv` and `03_Datasets/reports/candidate_comparison.md` with primary-source URLs, mirror links, and explicit unknowns. Do not download controlled medical datasets until `STEP-011` permissions are resolved.

**Human-only actions and decisions:** Researchers and supervisor approve the conditional primary and external validation shortlist (`UD05` discovery stage).

**Version-control/artifact expectations:** Commit safe metadata (`candidates.csv`, `candidate_comparison.md`); retain rejected candidates and rationale transparently.

**Documentation updates:** `03_Datasets/candidates.csv`, `candidate_comparison.md`, and `UD05`/`UD06` status in `decisions.csv`.

**Verification checklist:**

- [ ] Every candidate links to its original authoritative portal/paper or flags provenance gaps explicitly.
- [ ] Zero non-mammogram (histopathology/ultrasound/MRI/tabular) collections shortlisted (`RF15`).
- [ ] Mirrors/derivatives linked via `DuplicateOf` so zero overlap exists between shortlisted primary and external candidates.
- [ ] Label provenance, ROI-mask support, patient metadata, and license unknowns recorded honestly.

**Common mistakes:** Grabbing a preprocessed Kaggle folder lacking `PatientID`s; treating Mini-DDSM as an independent external validation set for CBIS-DDSM; conflating BI-RADS screening labels with biopsy-confirmed ground truth.

**Recovery procedure:** Trace original archive citations, reject unverifiable mirrors, expand primary-source discovery if needed, and update `candidates.csv`.

**Definition of Done:** Evidence-backed shortlist of conditional primary and external 2D mammogram candidates ready for formal license/DUA and ethics verification. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-011](#step-011)

---

<a id="step-011"></a>
## STEP-011 — Verify licenses, data-use agreements, institutional ethics/waiver, and custody controls

**Objective:** Obtain written licensing/DUA clearance, institutional ethics/waiver determinations, figure-disclosure permissions, and compute/storage custody approval prior to downloading any shortlisted dataset (`UD06`).

**Why this step exists:** Publicly hosted medical imaging archives (e.g., PhysioNet credentialed datasets, TCIA collections, institutional repositories) carry binding non-redistribution, credentialing, citation, and privacy clauses that Q1 journals verify at submission.

**Governing section references:** [OS §1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §11](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-010` shortlist complete; original dataset license/DUA texts and DIU institutional ethics/research-office contact routes available.

**Estimated difficulty and time (provisional):** Hard; 2–4 hours preparation plus external portal DUA / institutional ethics turnaround (unknown duration).

**Parallelizable:** DUA applications and license audits for independent primary and external candidates can run concurrently; intake remains strictly blocked until authorization arrives.

**Inputs:** `03_Datasets/reports/candidate_comparison.md`, verbatim license/DUA terms, Tier-2/Tier-3 storage plan (`STEP-002`), and institutional secondary-data ethics policy.

**Expected outputs:** Archived license/DUA texts or controlled receipts, institutional ethics/waiver determination record, compute-host permission audit, figure/demo redistribution rights matrix, and `DEC####` resolving `UD06`.

**Repository/file changes:** Create `03_Datasets/licenses/` records, `03_Datasets/reports/access_decision.md`, and `01_Project_Management/decision_log/DEC####.md` (`UD06`); update `candidates.csv` and `decisions.csv`.

**Execution procedure:**

1. Inspect each shortlisted dataset's exact terms separately for: (a) academic research download/processing, (b) remote/cloud GPU compute upload permissions (critical if using cloud notebooks/clusters!), (c) publication of de-identified example mammograms/Grad-CAM plates in a Q1 journal or thesis, (d) bundling sample images in a conditional web demo (`UD27`), and (e) sharing derived trained weights (`UD24`).
2. Submit required credentialing or DUA applications (e.g., PhysioNet training/DUA, institutional data-request forms) under researchers' real institutional credentials; never bypass access controls.
3. Obtain and document DIU institutional ethics review or secondary de-identified public-data waiver determination for the study.
4. Record explicit authorized download versions and permitted compute/storage hosts; keep pending or denied datasets blocked from `STEP-012`.

**Planning/review prompt:**

> Build a rights-and-custody matrix from actual verbatim license/DUA documents for every shortlisted primary and external candidate. Flag any restriction on cloud compute uploads, Q1 journal example figures, or trained-weight sharing without rendering legal or ethics approval yourself.

**Implementation prompt:**

> Documentation only: archive verbatim license texts and actual ethics/DUA determination references under `03_Datasets/licenses/` and `reports/access_decision.md`. Never fabricate approval numbers, dates, or waiver signatures.

**Human-only actions and decisions:** Data steward, supervisor, and institutional ethics authority provide written ethics/waiver determinations and approve lawful dataset access (`UD06`).

**Version-control/artifact expectations:** Commit public license texts and safe determination metadata; store signed personal DUAs or portal credentials strictly outside Git.

**Documentation updates:** `03_Datasets/licenses/`, `access_decision.md`, `decisions.csv` (`UD06`), and `candidates.csv`.

**Verification checklist:**

- [ ] Acquisition, preprocessing, and modeling explicitly permitted by verbatim license/DUA.
- [ ] Institutional ethics/waiver determination recorded (not inferred from public availability).
- [ ] Permitted compute destinations (local vs university vs cloud GPU) verified against DUA terms.
- [ ] Publication figure and model-weight sharing rights documented separately; denied/pending sources blocked.

**Common mistakes:** Assuming "publicly downloadable" allows uploading controlled medical datasets to third-party cloud tools or republishing sample mammograms online; treating the p. 1 title-defense certificate as ethics clearance.

**Recovery procedure:** Halt intake for any source with unclear or denied rights, request written custodian clarification, or pivot to an authorized candidate from `STEP-010` while logging the denied decision.

**Definition of Done:** Written DUA/license and institutional ethics/waiver authorizations sufficient for specific primary (and external) dataset intake exist, with residual restrictions explicitly logged. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-012](#step-012)

---

<a id="step-012"></a>
## STEP-012 — Acquire, hash, and lock immutable raw mammogram inventories

**Objective:** Download exact authorized primary (and external) mammogram archives into restricted immutable storage, generate complete SHA-256 inventories, and bind provenance (`DS####`).

**Why this step exists:** Downstream labels, ROI masks, splits, and models lose reproducibility if raw DICOM/image bytes change silently or transfer corruptions go undetected.

**Governing section references:** [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-011` written permissions complete (`UD06`) for specific authorized version(s); Tier-2 restricted storage ready; `G02` (`environment/data/`) current `PASS`.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours active work per dataset plus network transfer and hashing duration.

**Parallelizable:** Independent authorized datasets (primary vs external) may be acquired concurrently; assign `DS####` IDs and merge `datasets.csv` serially.

**Inputs:** Authorized portal URLs/versions (`STEP-011`), `environment/data/` hashing/inventory scripts, and Tier-2 storage paths.

**Expected outputs:** Immutable raw files in restricted `03_Datasets/raw/DS####/`, archive & per-file SHA-256 manifests (`DS####_images.csv`), transfer receipt, backup verification, and populated `03_Datasets/datasets.csv` (`Role = primary_internal | external_validation`).

**Repository/file changes:** Populate restricted Tier-2 `03_Datasets/raw/DS####/` and `manifests/DS####_images.csv`; commit safe metadata in `03_Datasets/datasets.csv` and `03_Datasets/reports/DS####_intake_receipt.md`; add inventory utility in `src/bc_xai/data/inventory.py` + `tests/`.

**Execution procedure:**

1. Download exact authorized dataset version(s) via official transfer protocol; record download timestamp, source URL/DOI/release tag, and archive-level SHA-256 digests.
2. Extract archives untouched into read-only restricted storage `03_Datasets/raw/DS####/` (preserving original directory hierarchy, metadata CSVs/XMLs, and ROI-mask archives verbatim).
3. Run read-only inventory tooling (`environment/data/`) assigning pseudonymous `ImageID` (`IMG########`) and `PatientGroupID` (`PAT########`), recording per-file SHA-256, byte size, file extension, and raw status while segregating any identifying original paths/linkage tables in restricted storage.
4. Verify transferred file counts against official release manifests and confirm an off-disk encrypted backup copy in Tier-2 storage with spot-checked SHA-256 verification.

**Planning/review prompt:**

> Design a read-only mammogram intake and SHA-256 inventory procedure for the authorized dataset(s). Specify how original DICOM/image files, official metadata CSVs, and ROI masks are preserved untouched and how identifying filename mappings stay segregated.

**Implementation prompt:**

> Implement and execute `src/bc_xai/data/inventory.py` inside `environment/data/` to hash and inventory every acquired file (including corrupted or unexpected files) without altering a single raw byte. Emit `DS####_images.csv` and intake receipt; fail loudly on transfer count mismatch.

**Human-only actions and decisions:** Data steward handles authenticated portal downloads, confirms exact authorized version receipt, and verifies restricted backup custody.

**Version-control/artifact expectations:** Zero image/DICOM bytes or private linkage tables in Git; commit `src/bc_xai/data/inventory.py`, tests, safe `datasets.csv` rows, and aggregate `DS####_intake_receipt.md`.

**Documentation updates:** `03_Datasets/datasets.csv`, `DS####_intake_receipt.md`, and `dashboard.md`.

**Verification checklist:**

- [ ] Archive and per-file SHA-256 checksums recorded and raw files set read-only.
- [ ] Every acquired file (images, masks, metadata tables, unreadable files) accounted for.
- [ ] Pseudonymous `ImageID`/`PatientGroupID` mapping segregated from shareable Git metadata.
- [ ] Independent Tier-2 backup verified by checksum; zero usability or label quality claimed yet.

**Common mistakes:** Renaming or converting raw DICOMs to PNG in place; deleting unreadable files silently before inventory; assuming portal advertised counts equal downloaded file counts.

**Recovery procedure:** Quarantine truncated or checksum-mismatched downloads, re-acquire from official portal, preserve transfer failure logs, and regenerate immutable `DS####` manifest.

**Definition of Done:** Immutable primary (and external) `DS####` raw inventories acquired, checksummed, backed up, and registered. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-013](#step-013)

---

<a id="step-013"></a>
## STEP-013 — Audit mammogram decoding, bit-depth/polarity integrity, PHI/artifacts, and approve datasets (G04)

**Objective:** Execute comprehensive technical, privacy, and radiographic quality control on acquired mammogram datasets, complete `DS####` dataset cards (`T08`), finalize `UD05`, and pass `G04`.

**Why this step exists:** Mammogram archives frequently contain inverted photometric polarity (`MONOCHROME1`), 16-bit truncation quirks, burned-in text/PHI markers, blank frames, or exact/near-duplicate scans that corrupt training and XAI maps if undetected.

**Governing section references:** [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-012` immutable `DS####` inventories complete; `UD06` permissions current; `environment/data/` verified; clinical/human visual QC reviewer arranged.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours per dataset plus visual QC sample review.

**Parallelizable:** Automated DICOM/image QC and duplicate detection can run independently per `DS####` cohort; final suitability decision and `G04` audit consolidate all cohorts.

**Inputs:** `DS####` raw inventories (`STEP-012`), DICOM headers/image files, official metadata tables, `T08` dataset card template, and `UD05` selection criteria.

**Expected outputs:** Automated QC & integrity reports (`DS####_quality.md`), exact & perceptual near-duplicate candidate tables, explicit exclusion/quarantine ledger, reconciled `Acquired = Retained + Excluded + Quarantined` counts, completed `DS####_card.md` (`T08`), `DEC####` finalizing `UD05`, and `G04` assessment.

**Repository/file changes:** Implement `src/bc_xai/data/qc.py` + `tests/test_qc.py`; write `03_Datasets/reports/DS####_quality.md`, `DS####_card.md`, `01_Project_Management/decision_log/DEC####.md` (`UD05`), and `01_Project_Management/reviews/G04_assessment_<date>.md`; update `datasets.csv`, `decisions.csv`, and `gates.csv`.

**Execution procedure:**

1. Run read-only automated QC (`src/bc_xai/data/qc.py`) across 100% of files checking: decode success, pixel dimensions/aspect ratios, bit depth (8/12/16-bit), DICOM `PhotometricInterpretation` (`MONOCHROME1` vs `MONOCHROME2`), `RescaleSlope`/`Intercept`, VOI LUT tags, dynamic range / empty or saturated frames, and DICOM header PHI tag audit.
2. Compute exact SHA-256 and perceptual near-duplicate clusters across all images (and **cross-cohort** between primary and external datasets to prove zero overlap!).
3. Conduct a stratified human/clinical visual sample inspecting burned-in pixel PHI, radiopaque markers (`LCC`/`RMLO`), film borders, pectoral muscle framing, breast implants, biopsy clips, and overall diagnostic visibility.
4. Define explicit, objective pre-modeling technical exclusion rules (e.g., corrupted unreadable files, blank frames, non-mammogram scout/test images); reconcile exact patient and image totals (`Acquired = Retained + Excluded + Quarantined`) and confirm raw hashes remained unchanged.
5. Complete `DS####_card.md` (`T08`) for primary (and external) datasets, finalize `UD05` selection, and perform itemized `G04` assessment.

**Planning/review prompt:**

> Design the mammography QC protocol checking DICOM photometric polarity, bit-depth dynamic range, burned-in PHI/text markers, cross-dataset duplicate leakage, and objective exclusion criteria. Distinguish technical exclusions from post-hoc difficulty filtering.

**Implementation prompt:**

> Implement and run read-only `src/bc_xai/data/qc.py` inside `environment/data/` on all acquired `DS####` cohorts. Emit reconciled count tables, duplicate candidate clusters, and `DS####_quality.md`; keep all raw bytes strictly untouched and store private visual QC contact sheets in Tier-2 storage.

**Human-only actions and decisions:** Data steward and supervisor approve final dataset suitability (`UD05`) and sign `G04`; radiologist/clinical advisor reviews visual QC sample if available.

**Version-control/artifact expectations:** Commit `src/bc_xai/data/qc.py`, unit tests, aggregate `DS####_quality.md`, `DS####_card.md`, and `G04` review; keep private contact sheets and duplicate linkage tables in Tier-2 storage.

**Documentation updates:** `03_Datasets/datasets.csv`, `DS####_card.md`, `decisions.csv` (`UD05`), `gates.csv` (`G04`), and `risk_register.csv`.

**Verification checklist:**

- [ ] `Acquired = Retained + Excluded + Quarantined` reconciles arithmetically at image and patient levels.
- [ ] Raw file SHA-256 hashes verified 100% unchanged after QC.
- [ ] DICOM polarity (`MONOCHROME1/2`), bit-depth, burned-in PHI, and cross-cohort duplicate checks completed.
- [ ] All `G04` permission, ethics, relevance, and quality criteria evidenced and signed.

**Common mistakes:** Silently excluding blurry or dense-breast mammograms that represent genuine clinical difficulty; missing `MONOCHROME1` polarity inversions; forgetting to run cross-cohort duplicate checks between primary and external datasets.

**Recovery procedure:** Fix QC script bugs, quarantine newly uncovered corrupted/PHI records, document updated counts honestly, or select an alternate authorized dataset from `STEP-010` before re-auditing `G04`.

**Definition of Done:** `G04 PASS` for finalized primary (and external) `DS####` version(s) with complete `T08` dataset cards and verified raw integrity. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-014](#step-014)

---

<a id="step-014"></a>
## STEP-014 — Define classification paradigm (FFDM vs ROI), ground-truth provenance, Normal-case policy, and ROI-mask scope

**Objective:** Resolve core mammography task semantics—FFDM whole-breast vs lesion ROI/patch paradigm (`UD07`), pathology vs BI-RADS Benign/Malignant & Normal-case rules (`UD08`), and lesion ROI-mask scope for XAI localization (`UD09`).

**Why this step exists:** Mixing whole-breast FFDM images with pre-cropped lesion ROIs or silently folding Normal (BI-RADS 1) scans into "Benign" invalidates clinical interpretation and triggers immediate Q1 peer-review rejection.

**Governing section references:** [OS §1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-013` complete; `G04 PASS`; official dataset metadata & ROI-mask schemas inspected; radiologist/clinical advisor and supervisor consulted.

**Estimated difficulty and time (provisional):** Hard; 3–5 hours plus clinical/supervisor review.

**Parallelizable:** Paradigm drafting (`UD07`), label mapping (`UD08`), and ROI-mask inventory (`UD09`) may be drafted concurrently before unified approval.

**Inputs:** `DS####_card.md`, dataset official label/pathology/BI-RADS CSVs, ROI-mask metadata, approved RQs (`G03`), `RF05` binary Benign-vs-Malignant scope, and `UD07–UD09`.

**Expected outputs:** Draft `04_Labels_XAI_Governance/protocols/label_mask_protocol_v1.0.0.md` (`T09`), exact label mapping table (`0 = Benign`, `1 = Malignant`, explicit exclusion/disposition rules for Normal/BI-RADS-0/unconfirmed/multi-lesion exams), ROI-mask geometry specification, and proposed `DEC####` records for `UD07–UD09`.

**Repository/file changes:** Create `04_Labels_XAI_Governance/protocols/label_mask_protocol_v1.0.0.md` (draft pending `G05`), label-mapping schema files, and draft `DEC####` records (`UD07–UD09`).

**Execution procedure:**

1. Decide the exact image classification paradigm (`UD07`): whole-breast FFDM/SFM image classification vs lesion-level ROI/patch classification (or explicitly segregated dual tracks with separate `REL####` and `EVAL####` pipelines—never pooled!). Document exact implications for clinical screening claims.
2. Audit every raw label field in primary and external datasets (`UD08`): distinguish histopathologic biopsy confirmation from BI-RADS radiological scores; define exact mapping to binary `0 = Benign` and `1 = Malignant`, exact disposition of Normal/Negative (BI-RADS 1) and incomplete (BI-RADS 0) cases, and strict malignant-dominance rules when one breast/image carries both benign and malignant findings.
3. Inventory lesion ROI masks/contours/boxes across primary and external cohorts (`UD09`): document mask coordinate convention, file format (DICOM mask, PNG, XML contour), multi-lesion union rule, and explicit restriction that masks are used **strictly for post-hoc XAI localization evaluation**—never leaked as training/inference inputs.
4. Draft acceptance criteria and pilot visual audit sample size for `STEP-016` verification.

**Planning/review prompt:**

> Draft `T09` (`label_mask_protocol_v1.0.0.md`) for the acquired `DS####` cohort(s). Resolve FFDM vs ROI paradigm (`UD07`), pathology vs BI-RADS Benign/Malignant mapping and Normal-case handling (`UD08`), multi-lesion precedence, and post-hoc ROI-mask alignment rules (`UD09`), flagging every clinical trade-off for supervisor and radiologist review.

**Implementation prompt:**

> Documentation only: save draft `label_mask_protocol_v1.0.0.md` and `UD07–UD09` decision drafts grounded in measured metadata values from `DS####`. Do not relabel or modify raw dataset files.

**Human-only actions and decisions:** Radiologist/clinical advisor (where engaged) and supervisor ratify `UD07`, `UD08`, and `UD09`.

**Version-control/artifact expectations:** Commit protocol and mapping schemas; keep raw patient-level metadata files in Tier-2 storage.

**Documentation updates:** `04_Labels_XAI_Governance/protocols/`, `decisions.csv` (`UD07–UD09`), and `dashboard.md`.

**Verification checklist:**

- [ ] FFDM/whole-breast vs ROI/patch paradigm unambiguously chosen with zero silent mixing.
- [ ] Biopsy/pathology vs BI-RADS label provenance distinguished for both primary and external cohorts.
- [ ] Normal (BI-RADS 1), BI-RADS 0, unconfirmed, and multi-lesion cases governed by deterministic rules.
- [ ] ROI-mask scope, union convention, and strict post-hoc-only non-leakage rule documented.

**Common mistakes:** Silently relabeling Normal (BI-RADS 1) images as "Benign" without clinical disclosure; pooling benign+malignant dual-finding mammograms under both classes; accidentally leaking ROI crop coordinates into whole-breast classifiers.

**Recovery procedure:** Revise ambiguous rules with supervisor/clinical input, version the protocol cleanly, and re-verify alignment with `RF05` before `STEP-015`.

**Definition of Done:** Complete, clinically reviewed `T09` label and ROI-mask verification protocol ready for unified `G05` approval alongside XAI governance. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-015](#step-015)

---

<a id="step-015"></a>
## STEP-015 — Approve label/ROI-mask verification protocol and prospective XAI governance plan (G05)

**Objective:** Prospectively lock the complete XAI methodology (`XAIP####`)—Grad-CAM baseline, optional comparators, quantitative faithfulness/sanity/localization/stability metrics, and bounded clinical review rubric—alongside `T09` and pass `G05`.

**Why this step exists:** Choosing XAI target layers, perturbation baselines, or qualitative display examples *after* inspecting test heatmaps introduces severe post-hoc bias; Q1 rigor demands pre-specifying XAI evaluation prospectively before training.

**Governing section references:** [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS §14](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-014` draft `T09` complete; `G04` current `PASS`; `UD16–UD18` stakeholder input gathered.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours plus supervisor and clinical-advisor review.

**Parallelizable:** Drafting quantitative XAI metric formulas (`UD17`) and blinded clinical rubric (`UD18`) may proceed in parallel; unified `XAIP####` and `G05` approval are serialized.

**Inputs:** Draft `T09` (`STEP-014`), `RF08` XAI scope, `T11` XAI protocol template, approved RQs (`G03`), and `UD16–UD18`.

**Expected outputs:** Ratified `label_mask_protocol_v1.0.0.md` (`T09`), ratified prospective XAI protocol `XAIP0001.md` (`T11`), registered row in `xai_protocol_registry.csv`, finalized `DEC####` records (`UD07–UD09`, initial `UD16–UD18`), and `G05` assessment.

**Repository/file changes:** Finalize `04_Labels_XAI_Governance/protocols/label_mask_protocol_v1.0.0.md`, create `04_Labels_XAI_Governance/xai_protocols/XAIP0001.md` and `qualitative_review_rubric.md`, populate `xai_protocol_registry.csv`, update `decisions.csv`/`gates.csv`, and save `01_Project_Management/reviews/G05_assessment_<date>.md`.

**Execution procedure:**

1. Finalize and freeze `label_mask_protocol_v1.0.0.md` (`UD07–UD09`) with exact automated checks and pilot visual sampling criteria.
2. Specify the prospective XAI suite (`UD16`): mandatory **Grad-CAM** baseline (`RF08`) plus approved Q1 comparators (e.g., Grad-CAM++, Score-CAM, LayerCAM, Integrated Gradients, Guided Backpropagation, LIME/SHAP—or explicit rationale for non-adoption), pre-sigmoid/pre-softmax Malignant logit target convention, normalization/colormap rules, and exact handling of all-zero/ReLU-collapsed maps. (Exact layer names per final architecture bind when `UD13` closes in `STEP-022` and freeze at `G11`.)
3. Freeze quantitative XAI evaluation specifications (`UD17`): (a) **Faithfulness** (Deletion AUC, Insertion AUC, ROAD linear-imputation perturbation schedule, and random-mask baseline), (b) **Sanity Checks** (Adebayo cascading & independent layer randomization + label-randomization correlation metrics), (c) **ROI-Mask Localization** (Pointing Game, EBPG, thresholded IoU/Dice on verified mask subsets), and (d) **Stability** (input-perturbation SSIM/Spearman + multi-seed consistency).
4. Finalize the bounded blinded clinical-advisor qualitative review rubric (`UD18`: stratified TP/TN/FP/FN sampling frame, de-identification rules, Likert scoring criteria, explicit non-clinical-trial disclaimer, and honest contingency if an advisor is unavailable).
5. Compute SHA-256 hashes of finalized `T09` and `XAIP0001`, register `XAIP0001`, and execute itemized `G05` assessment.

**Planning/review prompt:**

> Audit `label_mask_protocol_v1.0.0.md` and `XAIP0001.md` against Q1 medical imaging XAI standards. Verify that perturbation baselines avoid zero-masking artifacts (e.g., ROAD/blur), Adebayo sanity checks are genuinely discriminative, ROI masks cannot leak into classification, and the clinical review rubric explicitly respects Section 8's non-trial exclusion.

**Implementation prompt:**

> Documentation only: save finalized `T09`, `XAIP0001.md`, `qualitative_review_rubric.md`, SHA-256 hashes, `xai_protocol_registry.csv` row, and `DEC####` records (`UD07–UD09`, `UD16–UD18`). Leave architecture-specific layer bindings linked to `UD13` and do not pre-mark `G05 PASS`.

**Human-only actions and decisions:** Supervisor and radiologist/clinical advisor ratify `T09`, `XAIP0001`, `UD07–UD09`, `UD16–UD18`, and sign `G05`.

**Version-control/artifact expectations:** Commit finalized versioned protocols, rubric, registry entries, and `G05` assessment as `labels: approve T09 label protocol, XAIP0001, and G05`.

**Documentation updates:** `xai_protocol_registry.csv`, `decisions.csv`, `gates.csv`, and `dashboard.md`.

**Verification checklist:**

- [ ] `T09` resolves FFDM vs ROI, pathology vs BI-RADS, Normal-case handling, and ROI-mask rules (`UD07–UD09`).
- [ ] `XAIP0001` mandates Grad-CAM and prospectively specifies faithfulness, Adebayo sanity, ROI localization, and stability protocols (`UD16–UD17`).
- [ ] Blinded clinical review rubric (`UD18`) separates retrospective qualitative evaluation strictly from clinical trials (`RF15`).
- [ ] `G05` PASS supported by named supervisor/advisor sign-off and protocol hashes.

**Common mistakes:** Deferring XAI evaluation rules until after seeing heatmaps; omitting random-baseline or sanity controls; promising radiologist review without confirming reviewer commitment or documenting the honest fallback.

**Recovery procedure:** Revise ambiguous rules cleanly under a version bump (`v1.1.0` / `XAIP0002`), obtain renewed approval, and reassess `G05`.

**Definition of Done:** `G05 PASS` locking both the diagnostic label/ROI-mask verification protocol and the prospective Q1 XAI governance contract. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-016](#step-016)

---

<a id="step-016"></a>
## STEP-016 — Run pilot audit of diagnostic labels, pathology/BI-RADS concordance, and lesion ROI-mask alignment

**Objective:** Test the `G05`-approved `T09` label and ROI-mask verification rules on a prospectively stratified pilot sample to catch metadata parsing defects, polarity/flip errors, or mask misalignments before full-dataset execution.

**Why this step exists:** Public mammogram datasets commonly contain subtle traps—such as transposed/flipped ROI masks, mismatched DICOM UID joins, ambiguous `BENIGN_WITHOUT_CALLBACK` sub-labels, or multi-lesion duplicates—that silently corrupt datasets if discovered late.

**Governing section references:** [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-015` complete; `G05 PASS`; `DS####` raw inventories (`G04`) available; `environment/data/` verified.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours plus clinical-advisor/supervisor visual inspection of pilot overlays.

**Parallelizable:** Automated metadata parsing checks and visual ROI-mask overlay inspection may proceed on assigned pilot batches; adjudication reconciles serially.

**Inputs:** `label_mask_protocol_v1.0.0.md`, `DS####` raw metadata CSVs/XMLs and ROI masks, and prospectively selected stratified pilot sample (covering Benign, Malignant, mass, calcification, Normal/excluded edge cases, and multi-lesion scans across primary and external cohorts).

**Expected outputs:** Pilot verification scripts & unit tests, pilot label/pathology concordance report, pilot mammogram-plus-ROI-mask overlay contact sheets (restricted Tier-2), discrepancy/adjudication log, and pilot acceptance or protocol-refinement decision.

**Repository/file changes:** Implement `src/bc_xai/labels/verify.py` + `tests/test_label_verify.py`; save `04_Labels_XAI_Governance/reviews/pilot_label_mask_audit.md` and restricted pilot overlays in Tier-2 storage.

**Execution procedure:**

1. Draw the prospectively defined stratified pilot sample (recording exact sampling seed and strata counts) across Benign, Malignant, mass, calcification, multi-lesion, and Normal/excluded edge cases.
2. Execute `src/bc_xai/labels/verify.py` to join metadata tables to `DS####_images.csv`, check label-mapping edge cases (e.g., `BENIGN_WITHOUT_CALLBACK`, BI-RADS 3/4A ambiguities, conflicting multi-ROI labels on one breast), and check ROI-mask spatial dimensions, binary pixel values, and empty masks.
3. Render restricted Tier-2 visual overlays superimposing raw mammograms and ROI masks across all sampled views (LCC, RCC, LMLO, RMLO) and inspect for left/right flips, vertical inversions, 90° rotations, or shifted crops.
4. Adjudicate every discrepancy with the supervisor/clinical advisor; if `T09` requires rule clarification, update `T09`, re-ratify `G05`, and re-test the pilot before advancing to `STEP-017`.

**Planning/review prompt:**

> Audit the pilot label/pathology concordance and ROI-mask alignment results against `label_mask_protocol_v1.0.0.md`. Distinguish metadata-join software bugs, source dataset label ambiguity, and geometric mask flips/offsets without silently patching raw source files.

**Implementation prompt:**

> Implement and execute `src/bc_xai/labels/verify.py` inside `environment/data/` on the stratified pilot sample, producing machine-readable anomaly tables and restricted Tier-2 visual mask overlay plates. Fail loudly on unmatched image/mask UIDs or unmapped source label tokens.

**Human-only actions and decisions:** Data lead and radiologist/clinical advisor (or supervisor) inspect pilot ROI overlays, adjudicate ambiguous source labels, and approve pilot pass.

**Version-control/artifact expectations:** Commit `src/bc_xai/labels/verify.py`, synthetic `pytest` fixtures, and safe aggregate `pilot_label_mask_audit.md`; keep visual mammogram overlays strictly in restricted Tier-2 storage.

**Documentation updates:** `pilot_label_mask_audit.md`, `adjudications/`, and any updated `T09` clarification version.

**Verification checklist:**

- [ ] Stratified pilot sample seed and coverage recorded explicitly.
- [ ] Zero unmapped label tokens or silent multi-lesion conflicts remain unresolved.
- [ ] Visual ROI-mask overlay checks verified across all views (LCC/RCC/LMLO/RMLO) for flips/transpositions.
- [ ] Pilot accepted under `G05`-current `T09`, or `T09` updated and re-approved under `G05`.

**Common mistakes:** Trusting mask shape equality (`H×W == H×W`) without visually checking horizontal/vertical flips; letting multi-lesion rows duplicate an image into both Benign and Malignant classes.

**Recovery procedure:** Fix parser/orientation rules in code or `T09`, re-approve `G05` if protocol semantics changed, and re-run pilot verification on fresh overlays.

**Definition of Done:** Label/pathology concordance and ROI-mask geometry verified cleanly on the stratified pilot under the current `G05` protocol. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-017](#step-017)

---

<a id="step-017"></a>
## STEP-017 — Execute full-dataset label/ROI-mask verification, adjudication, and spot review

**Objective:** Apply the pilot-validated verification pipeline to 100% of acquired primary and external mammogram records, adjudicate every flagged anomaly, and complete stratified clinical spot review.

**Why this step exists:** Complete coverage ensures every training, validation, internal-test, external-test, and XAI-localization record carries an auditable, conflict-free diagnostic label and verified geometry.

**Governing section references:** [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-016` pilot accepted; `G04–G05` current `PASS`; verified `src/bc_xai/labels/verify.py`.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours across full automated audit, adjudication logging, and stratified visual spot checks.

**Parallelizable:** Automated verification runs independently per `DS####` cohort; adjudication and final manifest assembly are consolidated serially.

**Inputs:** 100% of `DS####` inventories, source pathology/BI-RADS tables, source ROI masks, accepted `T09` protocol, and `src/bc_xai/labels/verify.py`.

**Expected outputs:** Full-dataset verified label tables, reconciled Normal/BI-RADS-0/unconfirmed/corrupt exclusion logs, full ROI-mask alignment summary, adjudication records for every edge case, and stratified spot-review evidence.

**Repository/file changes:** Emit restricted Tier-2 verified label & ROI-mask manifests; save safe summary logs under `04_Labels_XAI_Governance/reviews/` and `04_Labels_XAI_Governance/adjudications/`.

**Execution procedure:**

1. Run `src/bc_xai/labels/verify.py` across 100% of retained images in primary and external `DS####` cohorts, generating deterministic `0 = Benign`, `1 = Malignant`, and explicit `Excluded` reason tags.
2. Flag and quarantine every anomaly: missing pathology confirmation, conflicting multi-lesion labels, duplicate UIDs, missing/empty/dimension-mismatched ROI masks, or ambiguous BI-RADS records.
3. Adjudicate every flagged anomaly explicitly under `T09` rules (recording `ImageID`, original raw tokens, decision rule, reviewer, and date in `04_Labels_XAI_Governance/adjudications/`). Never silently drop or overwrite an anomalous row.
4. Perform a class-, density-, and abnormality-stratified visual spot review of mammogram + ROI-mask overlays across the full cohort (recording exact sample size, seed, observed error rate, and any clinical-advisor comments).

**Planning/review prompt:**

> Audit full-dataset label verification outputs and anomaly adjudications against `T09`. Confirm arithmetic reconciliation across Benign, Malignant, and Excluded buckets, check multi-lesion precedence integrity, and verify ROI-mask coverage per cohort.

**Implementation prompt:**

> Execute full-corpus `src/bc_xai/labels/verify.py` inside `environment/data/`, emitting restricted verified label/mask manifests and safe aggregate audit reports. Fail explicitly on any unadjudicated anomaly or unmapped label value.

**Human-only actions and decisions:** Data lead executes adjudications under `T09`; supervisor and radiologist/clinical advisor review escalated edge cases and stratified visual spot checks.

**Version-control/artifact expectations:** Store per-patient label/mask manifests and visual contact sheets in restricted Tier-2 storage with SHA-256 checksums; commit safe aggregate summaries and adjudication logs to Git.

**Documentation updates:** Full-dataset review logs, adjudication ledger, and measured class/mask/subgroup counts.

**Verification checklist:**

- [ ] 100% of retained `DS####` images accounted for (`Benign + Malignant + ProtocolExcluded = Retained`).
- [ ] Zero unadjudicated label conflicts, unmapped tokens, or corrupted ROI masks remain.
- [ ] Stratified visual spot review completed with recorded seed, coverage, and residual uncertainty.
- [ ] Primary and external cohorts audited separately with zero cross-cohort label contamination.

**Common mistakes:** Counting ROI rows as distinct images when multiple lesions appear on one mammogram; quietly dropping images lacking ROI masks from classification instead of separating classification-eligible vs localization-eligible subsets cleanly.

**Recovery procedure:** Reopen affected cohort subset, resolve parser or adjudication errors, log correction lineage, and re-run full-corpus verification before freezing.

**Definition of Done:** Full-corpus label and ROI-mask verification completed with closed adjudications and stratified spot-review evidence, ready for `LBL####` freeze. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-018](#step-018)

---

<a id="step-018"></a>
## STEP-018 — Freeze verified diagnostic label and ROI-mask release (LBL####) and pass G06

**Objective:** Package verified diagnostic labels and aligned ROI masks into an immutable, hash-locked release (`LBL####`), register it in `label_registry.csv`, and pass `G06`.

**Why this step exists:** Splitting, preprocessing, training, and XAI localization all depend on a single immutable ground-truth reference; any post-freeze change must create a new versioned `LBL####` and invalidate downstream gates.

**Governing section references:** [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-017` full-corpus verification and adjudications closed; `G04–G05` current `PASS`.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours plus final review sign-off.

**Parallelizable:** Automated hash generation and `T10` audit report drafting may run in parallel; `LBL####` freeze and `G06` sign-off are serialized.

**Inputs:** Full-corpus verified label/mask manifests (`STEP-017`), adjudication logs, spot-review evidence, `T10` template, and `DS####` parent hashes.

**Expected outputs:** Immutable `LBL####` release manifest(s) and canonical label-map JSON (`0 = Benign`, `1 = Malignant`) with SHA-256 digests, completed `LBL####_audit.md` (`T10`), populated `04_Labels_XAI_Governance/label_registry.csv`, and `G06` assessment.

**Repository/file changes:** Lock restricted Tier-2 `LBL####` label & ROI-mask manifests; commit `04_Labels_XAI_Governance/label_registry.csv`, `04_Labels_XAI_Governance/reviews/LBL####_audit.md`, `label_map.json`, and `01_Project_Management/reviews/G06_assessment_<date>.md`; update `gates.csv`.

**Execution procedure:**

1. Run final automated integrity assertions verifying 100% `ImageID` correspondence with `DS####`, unique keys, valid binary targets (`0`/`1`), verified ROI-mask geometry/hashes, and zero orphan or unreviewed records.
2. Export canonical `label_map.json` (`{"0": "Benign", "1": "Malignant"}`) and compute SHA-256 hashes of `label_map.json`, verified label manifests, and ROI-mask archives.
3. Write `04_Labels_XAI_Governance/reviews/LBL####_audit.md` (`T10`) summarizing exact Benign/Malignant/Excluded counts, pathology vs BI-RADS breakdown, ROI-mask coverage subset, subgroup metadata completeness (density/view/mass/calcification), and residual label uncertainty.
4. Register immutable `LBL####` row(s) in `label_registry.csv` (one per cohort: primary internal and external if adopted), verify Tier-2 backup, and perform itemized `G06` assessment.

**Planning/review prompt:**

> Audit `LBL####_audit.md` and integrity logs against every `G06` criterion. Confirm label provenance, Normal/multi-lesion reconciliation, ROI-mask alignment, and honest reporting of residual uncertainty without claiming 100% perfection of public source labels.

**Implementation prompt:**

> Run final immutability & checksum lock inside `environment/data/`, generate `label_map.json` + SHA-256 manifest, update `label_registry.csv`, run `validate_registries.py`, and save `LBL####_audit.md`.

**Human-only actions and decisions:** Data lead and supervisor (plus radiologist/clinical advisor where engaged) approve `LBL####` freeze and sign `G06`.

**Version-control/artifact expectations:** Archive immutable `LBL####` manifests and ROI-mask bundles in Tier-2 storage; commit safe `label_registry.csv`, `label_map.json`, `LBL####_audit.md`, and `G06` audit to Git.

**Documentation updates:** `label_registry.csv`, `LBL####_audit.md`, `gates.csv` (`G06`), and `dashboard.md`.

**Verification checklist:**

- [ ] Zero unresolved invalid, orphan, or conflicting labels/masks exist in `LBL####`.
- [ ] Benign, Malignant, Excluded, and ROI-mask subset counts reconcile exactly to `DS####`.
- [ ] Canonical `label_map.json` and `LBL####` manifest SHA-256 hashes frozen and backed up.
- [ ] `G06 PASS` tied to exact `DS####` and `LBL####` hashes with named human sign-off.

**Common mistakes:** Freezing labels without locking ROI-mask hashes for later XAI localization; forgetting to create a separate `LBL####` entry for the independent external validation dataset.

**Recovery procedure:** Quarantine faulty `LBL####`, fix adjudications/alignment under `STEP-017`, emit a superseding `LBL####` version, mark downstream artifacts `STALE`, and reassess `G06`.

**Definition of Done:** `G06 PASS` establishing an immutable, checksum-locked diagnostic label and ROI-mask release ready for preprocessing design and connected-component patient splitting. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-019](#step-019)

---

<a id="step-019"></a>
## STEP-019 — Design mammography preprocessing pipeline and radiographically valid augmentation rules

**Objective:** Specify deterministic mammography preprocessing (bit-depth/polarity standardization, artifact/border handling, aspect-ratio resizing, CLAHE baseline vs ablation design) and training-only radiographic augmentation rules (`UD12`).

**Why this step exists:** Naive natural-image preprocessing (such as arbitrary cropping, destructive contrast clipping, or dataset-wide scaling before splitting) can erase subtle microcalcifications, distort breast morphology, or leak validation/test intensity distributions.

**Governing section references:** [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-018` complete; `G06 PASS`; `DS####_quality.md` polarity/bit-depth/artifact findings available.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours including synthetic/sample visual verification design.

**Parallelizable:** Designing deterministic preprocessing (`PP####` baseline vs CLAHE ablation spec) and drafting training-only augmentation constraints can run in parallel; unified parameter review is serialized.

**Inputs:** `DS####_quality.md`, `LBL####` ROI-mask geometry, `RF10` report preprocessing concepts (resizing, normalization, augmentation), and `UD12`.

**Expected outputs:** Approved preprocessing spec (`05_Preprocessing/specs/pipeline.md`), baseline + ablation YAML configs (`configs/`), ROI-mask co-transform specification (preserving exact spatial alignment between preprocessed images and post-hoc ROI masks!), training-only fit & augmentation rules, and `DEC####` resolving `UD12`.

**Repository/file changes:** Create `05_Preprocessing/specs/pipeline.md`, `05_Preprocessing/configs/pp_baseline.yaml` (and optional `pp_clahe_ablation.yaml`), `src/bc_xai/preprocess/transforms.py` + `tests/test_preprocess.py`, and `DEC####` (`UD12`).

**Execution procedure:**

1. Define deterministic per-image mammography standardization: `MONOCHROME1` → `MONOCHROME2` polarity alignment, 12/16-bit dynamic-range scaling / DICOM VOI LUT handling, and consistent 3-channel conversion for ImageNet-pretrained CNNs.
2. Specify breast-foreground cropping / border & radiopaque-marker handling with strict lesion-safety checks (verifying against verified ROI masks in `LBL####` that zero target lesions are clipped!).
3. Define aspect-ratio-preserving pad-and-resize vs direct resize, exact spatial co-transform applied to post-hoc ROI masks so XAI localization evaluation maps 1:1 to model input coordinates, and normalization policy (ImageNet stats vs training-partition-fitted stats).
4. Keep baseline `PP####` clean and minimal; isolate contrast enhancement (e.g., **CLAHE**) explicitly as a separate, testable ablation `PP####` variant rather than assuming benefit (`UD12`).
5. Specify radiographically valid **training-only** stochastic augmentations (e.g., horizontal flip with awareness of laterality/orientation, small rotations, mild shift/scale, bounded intensity jitter; forbidding extreme crops/warps that erase microcalcifications or create unrealistic anatomy) and enforce zero fitting or materialization before `G07` split lock.

**Planning/review prompt:**

> Design a mammography-specific preprocessing and augmentation specification grounded in `DS####_quality.md` and `LBL####` ROI-mask coverage. Prove how ROI masks co-transform identically for post-hoc XAI localization, why CLAHE is isolated as an ablation, and how zero validation/test statistics can leak prior to `G07`.

**Implementation prompt:**

> Implement deterministic transforms and ROI-mask co-transform geometry tests in `src/bc_xai/preprocess/transforms.py` and `tests/test_preprocess.py` inside `environment/data/` using synthetic fixtures. Do **not** fit dataset-level statistics or materialize split-dependent processed images before `STEP-020` (`G07`).

**Human-only actions and decisions:** Implementer, supervisor, and radiologist/clinical advisor (where engaged) approve `UD12` visibility-preserving preprocessing and augmentation bounds.

**Version-control/artifact expectations:** Commit specs, configs, transform module, and synthetic tests; keep any visual preview plates in restricted Tier-2 storage and raw images untouched.

**Documentation updates:** `05_Preprocessing/specs/pipeline.md`, `decisions.csv` (`UD12`), and `dashboard.md`.

**Verification checklist:**

- [ ] Every transform step has documented rationale, exact parameters, and library pin.
- [ ] ROI-mask co-transform verified mathematically via `pytest` so post-hoc XAI localization stays pixel-aligned.
- [ ] CLAHE/contrast enhancement explicitly separated as a controlled ablation rather than an untested mandate.
- [ ] Data-dependent normalization strictly restricted to post-`G07` training partition; augmentation strictly training-only.

**Common mistakes:** Fitting z-score mean/std across the entire dataset before splitting; augmenting images before splitting; clipping peripheral chest-wall/axillary lesions during automated background cropping; failing to apply identical crop/pad/resize geometry to ROI masks.

**Recovery procedure:** Disable lesion-clipping or distorting transforms, repair co-transform geometry tests, version the updated `PP` specification, and re-verify on sample overlays.

**Definition of Done:** Reviewed, unit-tested mammography preprocessing and augmentation specification exists with `UD12` approved; training-only fitting remains blocked until `G07 PASS`. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-020](#step-020)

---

<a id="step-020"></a>
## STEP-020 — Build connected-component patient/view/duplicate graph, lock leakage-safe split, and pass G07

**Objective:** Construct a connected-component patient-level grouping graph, lock deterministic train/validation/held-out-test partitions (`SPLIT####`), verify zero overlap with any external validation cohort, seal test custody, and pass `G07`.

**Why this step exists:** Multi-view mammograms (LCC, RCC, LMLO, RMLO), bilateral scans, longitudinal exams, same-patient ROI crops, and near duplicates cause catastrophic optimism if split at the image level; the title report specifies no split ratio (`RF19`), so proportions and CV/holdout structure must be chosen explicitly (`UD10–UD11`).

**Governing section references:** [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-019` design complete; `G04–G06` current `PASS`; `DS####` duplicate clusters and `LBL####` verified patient/laterality/view/class/subgroup metadata available.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours plus supervisor approval.

**Parallelizable:** No competing split trials based on model outcomes; metadata graph auditing and official-split overlap checking precede one deterministic assignment.

**Inputs:** `DS####` raw manifests & duplicate clusters, `LBL####` verified labels & subgroup tags, `T13` split report template, and `UD10–UD11`.

**Expected outputs:** Deterministic `03_Datasets/splits/SPLIT####/manifest.csv`, split algorithm/seed config, official-split overlap audit (if dataset supplies one), target vs actual patient/image/class/subgroup balance table, cross-cohort external-isolation verification, sealed test custody rules, `T13` `report.md`, `DEC####` (`UD10–UD11`), and `G07` assessment.

**Repository/file changes:** Implement `src/bc_xai/data/split.py` + `tests/test_split.py`; create `03_Datasets/splits/SPLIT####/manifest.csv` (restricted if group IDs sensitive; safe aggregate report committed), `config.yaml`, `report.md`, `DEC####` (`UD10–UD11`), and `01_Project_Management/reviews/G07_assessment_<date>.md`; update `decisions.csv` and `gates.csv`.

**Execution procedure:**

1. Construct an undirected equivalence graph (`src/bc_xai/data/split.py`) connecting any two images sharing `PatientID`, exam/study accession, bilateral laterality pair, same-patient ROI parentage, or exact/perceptual near-duplicate match (`UD10`); extract atomic connected components (`PatientGroupID`).
2. If the primary dataset provides an official benchmark split, audit it explicitly against the connected-component graph and log every overlapping patient/view/crop found before deciding whether to adopt a corrected split or dual-report with explicit disclosure.
3. Execute the `UD11`-approved deterministic grouped splitting strategy (e.g., stratified group train/val/held-out-test or nested/repeated stratified group K-fold + held-out test, fixed random seed, stratified by Benign/Malignant and key subgroups such as density/abnormality type) assigning whole connected components atomically without ever splitting a patient group to force exact percentages.
4. Run automated assertions verifying **zero** `PatientGroupID`, `ImageID`, source hash, or perceptual near-duplicate overlap across `train`/`val`/`test` AND **zero** overlap with the independent external validation `DS####` cohort (if adopted).
5. Seal internal held-out test and external validation manifests under strict access custody (no inspection by model selection/tuning until `G11`), complete `T13` `report.md`, and execute itemized `G07` assessment.

**Planning/review prompt:**

> Audit the connected-component graph and resulting `SPLIT####` distribution. Verify zero patient, bilateral-view, ROI-crop, or perceptual-duplicate leakage across partitions and external cohorts; report actual proportions, class balance, ROI-mask support, and subgroup counts honestly alongside any residual identity metadata limitations.

**Implementation prompt:**

> Implement and run `src/bc_xai/data/split.py` inside `environment/data/` with `pytest` leak-injection tests verifying the splitter crashes if any shared patient, view, or duplicate bridges partitions. Emit immutable `SPLIT####/manifest.csv`, SHA-256 checksums, and `report.md`.

**Human-only actions and decisions:** Data lead and supervisor ratify `UD10` grouping policy, `UD11` split design/proportions, any residual metadata limitations, sealed test custody, and sign `G07`.

**Version-control/artifact expectations:** Commit `src/bc_xai/data/split.py`, tests, split config, aggregate `report.md`, and `G07` audit; classify `manifest.csv` storage according to `PatientGroupID` sensitivity (`UD06`). Never overwrite an existing `SPLIT####`.

**Documentation updates:** `03_Datasets/splits/SPLIT####/report.md`, `decisions.csv` (`UD10–UD11`), `gates.csv` (`G07`), and `dashboard.md`.

**Verification checklist:**

- [ ] Zero connected components (`PatientID`, bilateral views, repeat exams, ROI crops, exact/near duplicates) bridge train/val/test or external cohorts.
- [ ] Re-running `split.py` with identical inputs/seed reproduces identical `manifest.csv` SHA-256.
- [ ] Target vs actual patient, image, class, ROI-mask, and subgroup counts reported honestly.
- [ ] Internal held-out test and external validation custody sealed; `G07 PASS` signed.

**Common mistakes:** Splitting multi-view mammograms (CC/MLO) randomly at the image level; assuming an official benchmark split has zero patient overlap without auditing it; breaking a patient cluster to hit round percentages.

**Recovery procedure:** Invalidate any leaky `SPLIT####` and all descendants, repair grouping rules, generate a new `SPLIT####` ID, disclose any prior test exposure, and reassess `G07`.

**Definition of Done:** `G07 PASS` locking a zero-leakage, deterministic connected-component split and sealed test custody. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-021](#step-021)

---

<a id="step-021"></a>
## STEP-021 — Fit training-only preprocessing states, materialize immutable release (REL####), and pass G08

**Objective:** Fit any data-dependent preprocessing parameters strictly on the training partition, materialize immutable prepared dataset release(s) (`REL####`) including co-transformed ROI masks, verify visual and checksum integrity, and pass `G08`.

**Why this step exists:** Training, ablation, and external validation require one immutable, hash-locked prepared dataset release proving zero validation/test statistical leakage and exact image-to-ROI-mask alignment.

**Governing section references:** [OS §4](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-020` complete; `G06–G07` current `PASS`; `UD12` approved `PP####` config(s) ready; `environment/data/` verified.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours plus image materialization compute time.

**Parallelizable:** Deterministic transformation of validation, internal-test, and external-cohort partitions may execute independently *after* the training-only state is fitted and frozen.

**Inputs:** Immutable `DS####`, `LBL####`, `SPLIT####` hashes, approved `PP####` config(s) (`STEP-019`), `T12` preprocessing report template.

**Expected outputs:** Serialized training-only fitted preprocessing state(s) with SHA-256, immutable prepared images and co-transformed post-hoc ROI masks in restricted `05_Preprocessing/processed/REL####/`, `T12` `PP####.md` report + visual QC confirmation, registered rows in `preprocessing_registry.csv` and `03_Datasets/releases.csv`, and `G08` assessment.

**Repository/file changes:** Run `src/bc_xai/preprocess/materialize.py`; populate restricted Tier-2 `05_Preprocessing/processed/REL####/`; commit `05_Preprocessing/preprocessing_registry.csv`, `05_Preprocessing/reports/PP####.md`, `03_Datasets/releases.csv`, and `01_Project_Management/reviews/G08_assessment_<date>.md`; update `gates.csv`.

**Execution procedure:**

1. Fit any data-dependent intensity/normalization parameters **strictly on `SPLIT####` training rows only** (`FitPartition = train`) and serialize the fitted state file with SHA-256 hash.
2. Apply deterministic `PP####` transformations to train, val, internal test, and independent external cohort (if adopted) with **zero stochastic augmentation** materialized into disk files; apply identical deterministic crop/pad/resize geometry to post-hoc ROI masks.
3. Run automated verification assertions checking: raw `DS####` hashes 100% unchanged, 100% image/label/ROI-mask count reconciliation, valid intensity ranges (zero NaNs/infs/all-black outputs), non-empty preserved lesion masks (verifying zero lesions were clipped out!), and exact manifest SHA-256 generation.
4. Perform stratified visual QC comparing raw vs preprocessed mammograms and co-transformed ROI overlays (with clinical-advisor review where engaged) to verify microcalcification and mass visibility.
5. Register `PP####` and `REL####` (creating separate `REL####` IDs for primary baseline, optional CLAHE ablation, and external cohort—never overwriting!), back up to Tier-2 storage, and execute itemized `G08` assessment.

**Planning/review prompt:**

> Audit `PP####` and `REL####` lineage hashes and visual QC outputs. Verify that zero validation or test data influenced fitted states, zero stochastic augmentations were pre-materialized, zero ROI lesion masks were clipped, and raw source bytes remain bit-identical.

**Implementation prompt:**

> Implement and run `src/bc_xai/preprocess/materialize.py` inside `environment/data/` producing immutable `REL####` outputs, serialized training-only fitted states, co-transformed ROI masks, checksum manifests, and `PP####.md`. Fail explicitly on any hash mismatch, NaN pixel, or empty clipped ROI mask.

**Human-only actions and decisions:** Data lead and model lead verify integrity and sign `G08`; radiologist/clinical advisor reviews visual visibility QC where available.

**Version-control/artifact expectations:** Processed image/mask bytes stay in Tier-2 storage with verified backup; commit `materialize.py`, `PP####.md`, `preprocessing_registry.csv`, `releases.csv`, and `G08` review to Git.

**Documentation updates:** `05_Preprocessing/preprocessing_registry.csv`, `03_Datasets/releases.csv`, `PP####.md`, `gates.csv` (`G08`), and `dashboard.md`.

**Verification checklist:**

- [ ] `FitPartition = train` verified in code and manifest; zero val/test statistics leaked.
- [ ] Raw `DS####` SHA-256 hashes verified unchanged; zero pre-split or materialized augmentation.
- [ ] Co-transformed ROI masks align 1:1 with preprocessed mammograms with zero clipped lesions.
- [ ] `REL####` binds exact `DS`/`LBL`/`SPLIT`/`PP` hashes; `G08 PASS` signed.

**Common mistakes:** Overwriting an existing `REL####` after tweaking resize or CLAHE settings; forgetting to process the independent external cohort using the **exact** primary training-fitted `PP####` state; silently dropping an image whose lesion mask became empty after cropping.

**Recovery procedure:** Quarantine defective derivative, repair preprocessing/co-transform code, issue a fresh `PP####`/`REL####` version, preserve failure logs, and reassess `G08`.

**Definition of Done:** `G08 PASS` certifying immutable, leakage-free prepared dataset release(s) ready for transfer learning modeling. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-022](#step-022)

---

<a id="step-022"></a>
## STEP-022 — Resolve candidate CNN architecture discrepancy and select transfer learning benchmark roster

**Objective:** Formally resolve the report's architecture list discrepancy (`RF07`), lock the exact transfer learning CNN benchmark roster (plus any supervisor-approved Q1 modern baseline or refinement), verify pretrained weight licenses, and map exact Grad-CAM target layers (`UD13`).

**Why this step exists:** `Title_defence_evaluation_report.pdf` lists 5 CNNs in Sec. 4, 6 CNNs in Obj. 3 (adding MobileNetV2), and mentions Xception in Sec. 2 (`RF07`), without naming libraries, weight revisions, or target XAI layers.

**Governing section references:** [OS §1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-021` complete; `G03` and `G08` current `PASS`; available GPU/compute budget (`UD14`) and literature synthesis (`STEP-008`) reviewed.

**Estimated difficulty and time (provisional):** Moderate; 3–5 hours plus supervisor decision.

**Parallelizable:** Documenting candidate model specs, parameter/FLOPs estimates, licenses, and Grad-CAM target layers may proceed concurrently; final roster ratification is one `DEC####`.

**Inputs:** `RF07` architecture discrepancy, approved RQs (`G03`), official library docs (e.g., PyTorch/`torchvision`/`timm` vs TensorFlow/`keras.applications`), `REL####` input resolution, `XAIP0001`, and `UD13`.

**Expected outputs:** Complete `06_Models/candidates.csv` (`MC####`), exact resolution of `RF07` discrepancy, approved `06_Models/baseline_plan.md`, architecture-to-Grad-CAM target-layer mapping table binding `XAIP0001`, and `DEC####` resolving `UD13`.

**Repository/file changes:** Populate `06_Models/candidates.csv`, create `06_Models/baseline_plan.md`, update `04_Labels_XAI_Governance/xai_protocols/target_layer_map.yaml`, and add `DEC####` (`UD13`) to `decisions.csv` + `decision_log/`.

**Execution procedure:**

1. Audit official source documentation for every report-named CNN family (`VGG16`, `ResNet50`, `DenseNet121`, `EfficientNetB0`, `InceptionV3`, `MobileNetV2`, `Xception`) plus any proposed Q1 modern baseline (e.g., `ConvNeXt-Tiny`, `Swin-Tiny`, or `ViT-Small` if ratified) and any justified controlled refinement (e.g., lightweight attention head or calibrated focal-loss variant).
2. Document for each `MC####` in `candidates.csv`: exact library & version, official pretrained weight tag & license (ImageNet-1K or medical pretraining if lawful), native resolution compatibility (checking if InceptionV3 requires 299×299 or if uniform resolution is used—if resolution changes `PP`, route cleanly back through `STEP-019/021` for a new `REL####`!), parameter count, GFLOPs, and exact final convolutional target layer name for Grad-CAM (and any multi-scale LayerCAM layer).
3. Select the exact **primary reference baseline architecture** (e.g., `ResNet50` or `DenseNet121`—decided explicitly, not assumed) and the full controlled multi-architecture benchmark roster resolving `RF07` transparently.
4. Confirm weight licensing permits research use, archival (`UD24`), and potential defense web hosting (`UD28` if `UD25` adopted).

**Planning/review prompt:**

> Compare all report-named CNN candidates (`RF07`) plus 1–2 modern Q1 reference architectures against our approved RQs, compute limits, and Grad-CAM target-layer spatial resolution (noting how coarse 7×7 feature maps impact microcalcification localization). Recommend a concrete `UD13` roster without fabricating prior accuracy scores.

**Implementation prompt:**

> Documentation only until ratified: populate `06_Models/candidates.csv`, draft `06_Models/baseline_plan.md` and `target_layer_map.yaml`, and save `DEC####` (`UD13`) once supervisor approval is obtained. Do not silently download unverified weights.

**Human-only actions and decisions:** Model lead and supervisor resolve `RF07` discrepancy, approve the exact benchmark roster, choose the baseline architecture, and ratify pretrained weight licenses (`UD13`).

**Version-control/artifact expectations:** Commit `candidates.csv`, `baseline_plan.md`, `target_layer_map.yaml`, and `DEC####`; download approved pretrained weights only into Tier-3 artifact cache with SHA-256 hashes logged.

**Documentation updates:** `06_Models/candidates.csv`, `baseline_plan.md`, `xai_protocol_registry.csv` (layer map update), and `decisions.csv` (`UD13`).

**Verification checklist:**

- [ ] `RF07` discrepancy (5 vs 6 vs 7 CNNs across Sec. 1/2/4/Obj. 3) resolved explicitly with documented rationale.
- [ ] Every selected `MC####` has exact library version, pretrained weight provenance, and verified license.
- [ ] Exact Grad-CAM target layer (and spatial feature-map resolution) mapped for every selected architecture.
- [ ] Any resolution requirement departing from `REL0001` explicitly routed to create a versioned `PP`/`REL` with renewed `G08`.

**Common mistakes:** Writing "EfficientNet" without specifying `B0` and weight revision; overlooking InceptionV3's auxiliary logits or native input dimension; forgetting to check whether modern ViT/Swin models need token-reshape hooks for Grad-CAM.

**Recovery procedure:** Replace incompatible or unlicensed candidates via superseding `DEC####`, update `target_layer_map.yaml`, and regenerate `REL####` if input geometry changed.

**Definition of Done:** Ratified `UD13` benchmark architecture roster, primary baseline choice, verified weight licenses, and exact Grad-CAM target-layer map exist. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-023](#step-023)

---

<a id="step-023"></a>
## STEP-023 — Pin and verify the deep learning, XAI, and statistical runtime environment (environment/model/)

**Objective:** Build, pin, and smoke-test the Phase-2 deep learning, GPU, XAI, calibration, and statistical runtime under `environment/model/` while preserving Phase-1 `environment/data/` untouched (`UD14`).

**Why this step exists:** Framework, CUDA/cuDNN, and XAI package drift break checkpoint loading, alter floating-point determinism, and undermine Q1 clean-environment reproducibility (`G14`).

**Governing section references:** [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §8](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-022` complete (`UD13` framework & architecture roster ratified); authorized compute hardware/GPU destination confirmed against dataset DUAs (`UD06`, `UD14`).

**Estimated difficulty and time (provisional):** Moderate to hard; 3–6 hours depending on CUDA/driver compatibility.

**Parallelizable:** Documentation and artifact-storage connectivity checks may proceed alongside installation; final lock and hardware verification are sequential.

**Inputs:** `UD13` framework/library requirements, actual compute hardware specs, `UD06` permitted compute hosts, and preserved `environment/data/` lock.

**Expected outputs:** Pinned `environment/model/` dependency lockfile, exact OS/Python/CUDA/cuDNN/GPU hardware inventory (`versions.md`), import + GPU + Grad-CAM + statistical-package smoke log, updated `12_Documentation/installation.md`, and `DEC####` finalizing `UD14`.

**Repository/file changes:** Create `environment/model/` (lockfile, `versions.md`, `verification.md`), update `12_Documentation/installation.md`, and add `DEC####` (`UD14`); leave `environment/data/` untouched.

**Execution procedure:**

1. Confirm the actual GPU/CPU compute host complies with every dataset DUA (`UD06`); never move restricted medical images onto an unauthorized host.
2. Create an isolated Phase-2 environment installing exact pinned versions of the chosen DL framework (e.g., PyTorch + `torchvision`/`timm` or TensorFlow/Keras), XAI packages (e.g., `pytorch-grad-cam` / `captum` / verified custom modules), calibration/statistics (`scikit-learn`, `scipy`, `statsmodels`), and plotting libraries.
3. Capture exact hardware & driver inventory (CPU model, RAM, GPU model, VRAM, NVIDIA driver, CUDA, cuDNN, OS kernel) and lockfile SHA-256 into `environment/model/versions.md`.
4. Run synthetic smoke tests (zero patient/test data!) verifying GPU tensor ops, deterministic seeding behavior, forward/backward pass + Grad-CAM hook extraction on a synthetic tensor for each `MC####`, and Tier-3 checkpoint write/read connectivity; record actual outputs in `environment/model/verification.md`.
5. Confirm `environment/data/` remains preserved intact; if shared library upgrades alter `PP####` outputs, test hash parity and version `PP`/`REL` with renewed `G08`.

**Planning/review prompt:**

> Audit the proposed `environment/model/` lockfile against `UD13` architectures, `XAIP0001` XAI methods, and `UD06` compute-host restrictions. Identify CUDA determinism caveats and verify that `environment/data/` provenance stays completely separate.

**Implementation prompt:**

> Install and pin `environment/model/`, record observed hardware/driver/package versions in `versions.md`, execute synthetic GPU/Grad-CAM/storage smoke checks into `verification.md`, and update `12_Documentation/installation.md`. Never claim GPU availability or determinism without observed output.

**Human-only actions and decisions:** Researchers ratify compute host, GPU quota/cost plan, and `environment/model/` lock (`UD14`).

**Version-control/artifact expectations:** Commit lockfiles, `versions.md`, `verification.md`, and installation instructions; exclude `.venv`/conda caches and credentials.

**Documentation updates:** `environment/model/`, `12_Documentation/installation.md`, `decisions.csv` (`UD14`), and `dashboard.md`.

**Verification checklist:**

- [ ] Exact observed OS, Python, framework, CUDA/cuDNN, and GPU specs recorded (not assumed).
- [ ] Synthetic forward/backward pass and Grad-CAM hook test pass for every `MC####` family.
- [ ] `environment/data/` lock preserved untouched.
- [ ] Compute host verified compliant with `UD06` dataset DUAs; zero test data accessed.

**Common mistakes:** Relying on ephemeral unpinned notebook images (e.g., changing Colab/Kaggle base images without capturing `pip freeze`); omitting CUDA/cuDNN driver versions; silently modifying `environment/data/`.

**Recovery procedure:** Pin conflicting transitive packages, recreate environment cleanly from `installation.md`, verify smoke checks, and record the new lock SHA-256.

**Definition of Done:** Pinned, smoke-tested Phase-2 `environment/model/` runtime documented and verified on authorized hardware. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-024](#step-024)

---

<a id="step-024"></a>
## STEP-024 — Approve prospective experiment matrix, training schedule, statistical/calibration plan, and XAI evaluation protocol

**Objective:** Prospectively lock the complete multi-architecture benchmark & ablation matrix, two-stage transfer learning & imbalance schedule, calibration & paired statistical testing protocol, and executable YAML config schema (`UD15–UD21`) before full training.

**Why this step exists:** Pre-registering exact training budgets, multi-seed counts, validation selection rules, operating-point rules, calibration methods, and Holm-Bonferroni comparisons eliminates p-hacking and post-hoc threshold bias required for Q1 review.

**Governing section references:** [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-022` (`UD13`) and `STEP-023` (`UD14`) complete; `G03`, `G05`, `G08` current `PASS`; dataset class imbalance & subgroup counts from `SPLIT####` known.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours plus supervisor methodological sign-off.

**Parallelizable:** Drafting training schedules (`UD15`), calibration/statistical specs (`UD19–UD20`), and finalizing architecture-bound XAI metrics (`UD16–UD17`) may proceed concurrently; final unified sign-off is serialized.

**Inputs:** Approved RQs (`G03`), `baseline_plan.md` (`UD13`), `SPLIT####` counts, `XAIP0001` (`G05`), hardware specs (`STEP-023`), and `UD15–UD21`.

**Expected outputs:** Approved `07_Experiments/experiment_plan.md` (complete benchmark + controlled ablation + multi-seed matrix), approved `09_Evaluation/protocol.md` (all 6 required metrics + Q1 suite, validation-only threshold & calibration rules, patient-clustered bootstrap/DeLong/McNemar/Holm-Bonferroni tests, efficiency profiling, subgroup plan), finalized `XAIP####` with bound layer map, finalized `T15` YAML validation schema, and `DEC####` records (`UD15–UD21`).

**Repository/file changes:** Create `07_Experiments/experiment_plan.md`, `09_Evaluation/protocol.md`, updated `04_Labels_XAI_Governance/xai_protocols/XAIP####.md` (binding exact `UD13` target layers), `src/bc_xai/config_schema.py`, and `DEC####` records (`UD15–UD21`).

**Execution procedure:**

1. Define the **exact experiment matrix** (`experiment_plan.md`, `UD15`): (a) primary baseline architecture run, (b) controlled comparison across every `UD13`-approved CNN architecture (and optional modern baseline) under matched `REL####`/`SPLIT####` and compute budget, (c) pre-registered single-factor ablations (e.g., CLAHE vs minimal `PP`, focal/class-weighted vs unweighted loss, two-stage unfrozen vs frozen-backbone fine-tuning, or justified attention refinement), and (d) exact multi-seed count (e.g., 3 or 5 fixed seeds) applied consistently.
2. Lock two-stage transfer learning hyperparameters & rules (`UD15`): Stage 1 frozen-backbone epochs/LR, Stage 2 unfrozen layers/LR/scheduler/weight-decay, training-only class-imbalance handling, batch size, mixed precision, early-stopping patience, and single primary validation selection metric (e.g., validation AUC-ROC or PR-AUC).
3. Lock the complete **Q1 Evaluation & Statistical Protocol** (`09_Evaluation/protocol.md`, `UD19–UD20`): all 6 mandatory report metrics (`RF09`), Specificity, PR-AUC, Balanced Accuracy, MCC, sensitivity-anchored operating points (e.g., Specificity at 90%/95% Sensitivity), validation-only threshold selection rule (Youden's J or clinical sensitivity target), ECE/Brier/reliability calibration + validation-fitted Temperature/Platt scaling, patient-clustered bootstrap 95% CIs (exact $B$ replicates & seed), two-sided DeLong & McNemar paired tests with Holm-Bonferroni adjustment, efficiency profiling (params, GFLOPs, classification-only & Grad-CAM latency), and stratified subgroup variables (density A–D, mass vs calcification, CC vs MLO, zero-shot external cohort).
4. Bind exact `UD13` target convolutional layers into `XAIP####`, confirm quantitative XAI protocol (`UD16–UD17`), and record any optional supervisor numeric target under `UD21` (explicitly separate from gate PASS/FAIL).

**Planning/review prompt:**

> Review `experiment_plan.md`, `09_Evaluation/protocol.md`, and bound `XAIP####` as a Q1 *IEEE TMI* / *Medical Image Analysis* statistical reviewer. Check for missing multi-seed variance plans, unclustered bootstraps on multi-view patients, threshold leakage, undefined perturbation baselines, or confounded ablations.

**Implementation prompt:**

> Save ratified `experiment_plan.md`, `09_Evaluation/protocol.md`, bound `XAIP####`, and `src/bc_xai/config_schema.py` enforcing zero null/placeholder fields and blocking `test`/`external` partition paths inside training configs.

**Human-only actions and decisions:** Supervisor and researchers ratify `UD15–UD21`, multi-seed compute budget, validation selection metric, and statistical/XAI analysis plan.

**Version-control/artifact expectations:** Commit timestamped pre-registered plans and schema validator before full training; any post-registration change is versioned explicitly as prospective amendment or post-hoc exploratory note.

**Documentation updates:** `07_Experiments/experiment_plan.md`, `09_Evaluation/protocol.md`, `xai_protocol_registry.csv`, `decisions.csv` (`UD15–UD21`), and `dashboard.md`.

**Verification checklist:**

- [ ] Every matrix row maps explicitly to an approved RQ (`G03`) with one controlled changed factor.
- [ ] All 6 required report metrics (`RF09`) plus Q1 calibration, clustered bootstrap, DeLong/McNemar, and Holm-Bonferroni rules locked.
- [ ] Validation-only threshold and calibration rules defined without touching test data.
- [ ] `XAIP####` target layers, faithfulness/sanity/localization/stability rules bound to every `MC####`.

**Common mistakes:** Picking the best seed instead of aggregating all planned seeds; treating multiple mammographic views per patient as independent samples in bootstrap CIs; omitting multiple-comparison adjustment across 6+ CNN architectures.

**Recovery procedure:** Close every unresolved setting before `G09`; record formal amendments with date and rationale rather than retroactively claiming preregistration.

**Definition of Done:** Complete, supervisor-ratified prospective experiment, statistical, calibration, and XAI protocol ready for pipeline implementation. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-025](#step-025)

---

<a id="step-025"></a>
## STEP-025 — Implement configuration-driven data loaders, multi-architecture trainers, XAI extractors, and evaluators

**Objective:** Build the clean, modular, unit-tested `src/bc_xai/` package implementing data loading, multi-architecture transfer learning, Grad-CAM & comparator XAI extraction, quantitative XAI faithfulness/sanity/localization metrics, calibration, and statistical testing.

**Why this step exists:** Centralized, tested modules prevent hidden notebook discrepancies across 6+ CNN architectures, ensure mathematically valid DeLong/McNemar/clustered-bootstrap statistics, and guarantee consistent Grad-CAM and ROAD/Adebayo computations.

**Governing section references:** [OS §2](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-024` ratified plans & config schema; `STEP-023` `environment/model/` ready; `G08` `REL####` available.

**Estimated difficulty and time (provisional):** Hard; 2–4 focused development days split across loader/trainer, XAI engine, and evaluation/statistics modules.

**Parallelizable:** Data loader/trainer (`src/bc_xai/train/`), XAI engine (`src/bc_xai/xai/`), and metric/statistical evaluator (`src/bc_xai/eval/`) can be built in parallel against agreed JSON/CSV schemas, then integrated.

**Inputs:** `experiment_plan.md`, `09_Evaluation/protocol.md`, bound `XAIP####`, `REL####` manifest schema, `config_schema.py`, and `environment/model/`.

**Expected outputs:** Complete modular `src/bc_xai/` package, thin `13_Automation/` CLI entry points, and comprehensive `tests/` suite passing on synthetic and manually verified analytical test cases.

**Repository/file changes:** Implement `src/bc_xai/{data,models,train,xai,eval}/`, thin CLIs in `13_Automation/`, unit tests in `tests/test_{loader,trainer,xai,metrics,stats}.py`, and update `12_Documentation/pipeline.md`.

**Execution procedure:**

1. **Data loader & partition guard (`src/bc_xai/data/`):** Enforce `REL####`/`SPLIT####`/`LBL####` SHA-256 checks at load time, apply training-only stochastic augmentations strictly on `train`, and raise hard exceptions if a training config requests `test` or `external` partitions.
2. **Multi-architecture trainer & checkpoint manager (`src/bc_xai/models/`, `train/`):** Support every `UD13` architecture cleanly via unified factory, two-stage freeze/unfreeze scheduler, training-only class-imbalance loss/sampler, effective-config dumping, structured per-epoch CSV/JSON logs, and atomic immutable `CKPT####` saving (weights, optimizer, scheduler, scaler, epoch, RNG states).
3. **XAI generator & quantitative XAI suite (`src/bc_xai/xai/`):** Implement Grad-CAM (and all `UD16`-approved comparators) using bound `target_layer_map.yaml` against raw Malignant logits; implement Deletion AUC, Insertion AUC, ROAD perturbation faithfulness, Adebayo cascading/independent layer randomization tests, ROI-mask Pointing Game / EBPG / IoU / Dice, and perturbation/multi-seed stability metrics.
4. **Classification, calibration & statistical evaluator (`src/bc_xai/eval/`):** Implement all 6 report metrics + Specificity, PR-AUC, Balanced Accuracy, MCC, sensitivity-anchored operating points, ECE/Brier/reliability binning, validation-only Temperature/Platt scaling, patient-clustered bootstrap 95% CIs, DeLong paired AUC test, McNemar paired test, Holm-Bonferroni correction, and params/GFLOPs/latency profiler.
5. **Known-answer unit testing (`tests/`):** Verify on analytical synthetic cases: perfect/random/inverted classifiers, zero-denominator Precision/Recall (`N/A`), patient-clustered vs unclustered bootstrap behavior, exact DeLong/McNemar reference values, Adebayo randomization correlation drop on a synthetic localized pattern, and Pointing Game / EBPG exact scores on synthetic binary masks.

**Planning/review prompt:**

> Audit the module interfaces and unit-test plan for `src/bc_xai/`. Verify how partition isolation blocks accidental test access during training, how pre-sigmoid Malignant logits feed Grad-CAM cleanly, and how patient clustering is enforced inside bootstrap resampling and statistical tests.

**Implementation prompt:**

> Implement modular `src/bc_xai/` components, thin `13_Automation/` CLIs, and analytical `tests/` inside `environment/model/`. Keep zero hyperparameters hardcoded outside YAML configs; run `pytest` on all synthetic/known-answer fixtures and record actual passing output.

**Human-only actions and decisions:** Method and evaluation reviewers inspect analytical unit tests for DeLong, McNemar, clustered bootstrap, ECE, and XAI faithfulness/localization formulas.

**Version-control/artifact expectations:** Commit source code, synthetic fixtures, `pytest` suite, and `12_Documentation/pipeline.md`; zero real mammograms or weight binaries in Git.

**Documentation updates:** `12_Documentation/pipeline.md` (CLI contracts, schemas, module inventory) and test summary.

**Verification checklist:**

- [ ] Data loader aborts immediately on `REL`/`SPLIT`/`LBL` hash mismatch or test-set path in training config.
- [ ] All `UD13` architectures instantiate, forward-pass, and emit valid Grad-CAM tensors without NaNs.
- [ ] Known-answer `pytest` tests pass for all 6 required metrics, ECE/Brier, clustered bootstrap, DeLong, McNemar, Holm-Bonferroni, Deletion/Insertion/ROAD, Adebayo randomization, and Pointing Game/EBPG.
- [ ] Zero held-out test or external dataset images accessed during development.

**Common mistakes:** Computing Grad-CAM after sigmoid saturation (causing vanishing gradients); applying training augmentations inside the validation DataLoader; computing image-level bootstrap ignoring `PatientGroupID` clusters; mishandling InceptionV3 auxiliary output tuples during training.

**Recovery procedure:** Fix failing module or analytical discrepancy, add a regression unit test locking the bug fix, and re-run the entire `pytest` suite before `STEP-026`.

**Definition of Done:** Configuration-driven `src/bc_xai/` pipeline implemented and passing all analytical/synthetic unit tests inside `environment/model/`. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-026](#step-026)

---

<a id="step-026"></a>
## STEP-026 — Execute diagnostic smoke training, checkpoint recovery test, and XAI harness verification (G09)

**Objective:** Prove end-to-end training, interruption/checkpoint recovery, backup retrieval, validation metric computation, and XAI faithfulness/sanity execution on an approved train/val smoke subset, and pass `G09`.

**Why this step exists:** Discovering broken checkpoint resumption, silent VRAM OOMs, NaN Grad-CAM hooks, or missing remote backup sync halfway through a multi-architecture multi-seed benchmark wastes compute and invalidates comparisons.

**Governing section references:** [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-025` `pytest` suite passing; `G05–G08` current `PASS`; `environment/model/` verified; Tier-3 checkpoint storage accessible.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours including short GPU smoke run and interruption drill.

**Parallelizable:** Writing `checkpoint_policy.md` may run alongside smoke setup; interruption/restore and XAI harness validation follow smoke checkpoint creation.

**Inputs:** Tiny approved train/val subset of `REL####` (zero test/external access!), validated smoke `config.yaml`, `environment/model/`, and `T17` checkpoint template.

**Expected outputs:** Ratified `08_Checkpoints/checkpoint_policy.md`, labeled diagnostic smoke experiment bundle (`EXP0000_smoke` / `purpose = diagnostic_smoke`), interruption & exact-resume audit log, Tier-3 backup fetch/SHA-256 proof, smoke XAI faithfulness/sanity/localization output check, and `G09` assessment.

**Repository/file changes:** Create `08_Checkpoints/checkpoint_policy.md`, diagnostic smoke bundle under `07_Experiments/`, `08_Checkpoints/manifests/`, and `01_Project_Management/reviews/G09_assessment_<date>.md`; update `gates.csv`.

**Execution procedure:**

1. Finalize `08_Checkpoints/checkpoint_policy.md` defining immutable naming, saved state components, periodic recovery cadence, Tier-3 off-host sync, and retention rules.
2. Execute a prospectively labeled `diagnostic_smoke` run (train/val subset only) for the baseline architecture (plus a 1-batch forward/backward + Grad-CAM smoke check across every remaining `UD13` architecture to catch VRAM or shape traps early). Verify finite loss, tiny-batch overfit diagnostic sanity, and complete effective-config capture.
3. Intentionally interrupt the smoke run mid-epoch/mid-schedule, sync checkpoint to Tier-3 backup, fetch it back into a fresh process, verify SHA-256, reload weights/optimizer/scheduler/scaler/RNG state, continue training, and document honestly whether resume is bitwise exact or non-deterministic within CUDA tolerance.
4. Run the full validation metric + calibration + Grad-CAM + Deletion/Insertion/ROAD + Adebayo randomization + ROI-mask Pointing Game harness on the smoke checkpoint (validation subset only) to verify finite, schema-valid outputs with zero crashes.
5. Perform itemized `G09` assessment verifying every prerequisite gate (`G01–G08`), config validator, recovery proof, and zero test-set access.

**Planning/review prompt:**

> Audit smoke-training, checkpoint-recovery, backup-fetch, and XAI-harness outputs against every `G09` criterion. Confirm all `UD13` architectures pass 1-batch VRAM/Grad-CAM checks and that exact-resume limitations are documented honestly rather than overstated.

**Implementation prompt:**

> Run the prospectively tagged `diagnostic_smoke` script and intentional interruption/restore drill inside `environment/model/` using `train`/`val` subsets only. Verify Tier-3 backup SHA-256 retrieval, execute smoke XAI harness checks, save logs, and compile `G09` evidence.

**Human-only actions and decisions:** Researchers and method reviewer inspect recovery proof and sign `G09` authorizing full compute spend.

**Version-control/artifact expectations:** Commit `checkpoint_policy.md`, diagnostic smoke metadata/config/report, and `G09` audit; store binary smoke checkpoint in Tier-3 storage (marked `diagnostic_smoke` so it is never eligible for `G11` model selection).

**Documentation updates:** `08_Checkpoints/checkpoint_policy.md`, `experiment_registry.csv` (`diagnostic_smoke` tag), `gates.csv` (`G09`), and `dashboard.md`.

**Verification checklist:**

- [ ] Tiny-batch sanity overfit and full multi-architecture 1-batch VRAM/Grad-CAM smoke checks pass.
- [ ] Intentional interruption, Tier-3 backup fetch, SHA-256 verification, and checkpoint restoration demonstrated.
- [ ] Smoke XAI faithfulness, Adebayo sanity, and ROI localization harness produces finite schema-valid outputs.
- [ ] Zero held-out test or external dataset files touched; `G09 PASS` signed.

**Common mistakes:** Retroactively reclassifying a failed full run as a smoke test; forgetting to test VRAM peaks on the heaviest architecture (e.g., VGG16 or DenseNet121 at higher resolution); ignoring Tier-3 transfer verification before long cloud GPU sessions.

**Recovery procedure:** Preserve diagnostic failure logs (`T16`), repair loader, memory/gradient-accumulation, XAI hook, or checkpoint serialization bug, rerun smoke verification under a fresh diagnostic ID, and re-audit `G09`.

**Definition of Done:** `G09 PASS` certifying an end-to-end verified training, recovery, evaluation, and XAI pipeline ready for full benchmark execution. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-027](#step-027)

---

<a id="step-027"></a>
## STEP-027 — Register and validate an immutable experiment configuration (EXP####)

**Objective:** Create a fully resolved, schema-validated, immutable experiment bundle (`EXP####`) bound to exact data, code, model, and XAI protocol hashes before spending GPU compute.

**Why this step exists:** Unfrozen configs or implicit CLI overrides destroy fair multi-architecture benchmarking and make Q1 peer-review verification impossible.

**Governing section references:** [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-026` complete; `G09 PASS`; approved `experiment_plan.md` matrix row (`STEP-024`) and current `REL####`/`XAIP####`; for repeats/architectures/ablations, `STEP-030` or `STEP-031` authorization.

**Estimated difficulty and time (provisional):** Moderate; 1–2 hours per experiment family.

**Parallelizable:** Preparing configs for independent matrix rows can proceed in parallel; serialize `EXP####` ID assignment in `experiment_registry.csv`.

**Inputs:** Approved row in `07_Experiments/experiment_plan.md`, `REL####`/`MC####`/`XAIP####` IDs and hashes, `T14`/`T15` templates, current clean Git commit hash, and `environment/model/` lock hash.

**Expected outputs:** Validated immutable `07_Experiments/EXP####/config.yaml`, `README.md` (`T14`), initialized `run_manifest.json`, registered `experiment_registry.csv` row (`Status = ready`), and launch checklist verification.

**Repository/file changes:** Create `07_Experiments/EXP####/config.yaml`, `README.md`, `run_manifest.json`; update `07_Experiments/experiment_registry.csv`.

**Execution procedure:**

1. Assign a unique zero-padded `EXP####` ID linking exact `RQ`, `Purpose` (`baseline | arch_benchmark | ablation | multi_seed`), `ParentComparison`, changed factor, and held-constant invariants.
2. Resolve 100% of Section 5.2 fields in `config.yaml` (`T15`): `REL`/`DS`/`LBL`/`SPLIT`/`PP` hashes, `MC####` & pretrained weight hash, two-stage freeze/unfreeze epochs & LRs, class-imbalance policy, seed, `XAIP####` + exact `gradcam_target_layer`, `environment/model/` hash, and Tier-3 destination.
3. Run `src/bc_xai/config_schema.py` validator confirming zero nulls, valid foreign keys, matching SHA-256 digests, clean Git commit recorded inside `run_manifest.json`, and strictly `allowed_partitions: ["train", "val"]` (blocking test/external access).
4. Record `config.yaml` SHA-256 in `experiment_registry.csv` and verify Tier-3 storage quota before authorizing compute launch.

**Planning/review prompt:**

> Audit `EXP####/config.yaml` against `experiment_plan.md` and Section 5.1 fair-benchmarking invariants. Confirm exactly one intended factor varies relative to `ParentComparison`, zero nulls exist, `allowed_partitions` excludes `test`/`external`, and all parent gates (`G01–G09`) are current `PASS`.

**Implementation prompt:**

> Generate `07_Experiments/EXP####/{config.yaml,README.md,run_manifest.json}`, execute `config_schema.py` and `validate_registries.py`, log the config SHA-256 in `experiment_registry.csv`, and stop prior to launching training if any check fails.

**Human-only actions and decisions:** Experiment lead authorizes the validated matrix row and GPU allocation; supervisor approves any departure from `experiment_plan.md`.

**Version-control/artifact expectations:** Commit immutable pre-launch `config.yaml`, `README.md`, and `experiment_registry.csv` row before launching GPU compute; never modify a launched `config.yaml`.

**Documentation updates:** `experiment_registry.csv`, `EXP####/README.md`, and `dashboard.md`.

**Verification checklist:**

- [ ] Every foreign key (`REL`, `MC`, `XAIP`, `ParentComparison`) resolves and parent SHA-256 hashes match.
- [ ] Zero null/placeholder fields in `config.yaml`; `test` and `external` partitions explicitly blocked.
- [ ] Two-stage schedule, imbalance rule, seed, and validation selection metric match `experiment_plan.md`.
- [ ] All parent gates (`G01–G09`) current `PASS` and Tier-3 storage space verified.

**Common mistakes:** Passing ad-hoc CLI overrides (`--lr 1e-4`) that diverge from `config.yaml`; comparing a new architecture against a baseline trained on an older `REL####`; editing a previously launched `config.yaml` in place.

**Recovery procedure:** Fix pre-launch errors and revalidate; if an error is discovered *after* launch, preserve the launched `EXP####` with failure/deviation notes and register a clean new `EXP####`.

**Definition of Done:** Validated, hash-locked immutable `EXP####` bundle registered and authorized for training execution. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-028](#step-028)

---

<a id="step-028"></a>
## STEP-028 — Train the registered transfer learning model and preserve every run attempt

**Objective:** Execute the registered `EXP####` training and validation workflow cleanly, persisting per-epoch metrics, effective runtime settings, immutable checkpoints, and honest interruption/failure logs.

**Why this step exists:** Multi-architecture transfer learning on mammograms is vulnerable to GPU preemption, overfitting on limited medical samples, and gradient divergence; durable logging and immutable checkpointing guarantee every attempt remains auditable.

**Governing section references:** [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §12](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-12); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-027` launch checklist verified (`Status = ready`); `G01–G09` current `PASS`; authorized DUA-compliant GPU runtime ready.

**Estimated difficulty and time (provisional):** Hard; 1–2 hours active monitoring per run plus measured GPU training time (unknown until executed).

**Parallelizable:** Independent registered `EXP####` runs may train concurrently on separate GPUs without sharing output directories or accessing test data.

**Inputs:** Frozen `EXP####/config.yaml`, `REL####` `train`/`val` partitions only, `environment/model/` runtime, and `checkpoint_policy.md`.

**Expected outputs:** `RUN####` execution entries in `run_manifest.json`, complete per-epoch train/val CSV curves (loss, AUC-ROC, PR-AUC, Sensitivity, Specificity, F1, LR, VRAM, epoch seconds), immutable `CKPT####` artifacts in Tier-3 storage (`best`, `last`, recovery), validation logit exports, and explicit stop/failure status.

**Repository/file changes:** Populate `07_Experiments/EXP####/` (`run_manifest.json`, `metrics_history.csv`, `effective_config.yaml`, `observations.md`, and `failure_report.md` if failed); append rows to `08_Checkpoints/checkpoint_registry.csv`; save checkpoint binaries in Tier-3 storage.

**Execution procedure:**

1. Verify `config.yaml`, `REL####`, `LBL####`, and `environment/model/` SHA-256 hashes at startup; emit `effective_config.yaml` capturing resolved framework defaults and exact GPU/CUDA runtime.
2. Execute Stage 1 (frozen-backbone warm-up) and Stage 2 (unfrozen fine-tuning) strictly on `train`, evaluating `val` per epoch using deterministic preprocessing and zero test-set access; monitor the pre-declared validation selection metric (`UD15`).
3. Persist immutable `CKPT####` files (never overwriting prior best/recovery objects) and sync logs/checkpoints off ephemeral compute to Tier-3 durable storage during training.
4. On GPU preemption, OOM, or NaN loss: log exact symptoms (`T16`), verify recovery checkpoint integrity, and resume under a linked `RUN####` only if exact-resume conditions from `STEP-026` hold; otherwise record termination honestly without altering batch size or LR mid-run.
5. Verify SHA-256 digests of all transferred logs and checkpoints before releasing the GPU session.

**Planning/review prompt:**

> Review the execution runbook for `EXP####` prior to GPU launch. Confirm monitored overfitting/divergence triggers, exact off-host checkpoint sync commands, and zero permitted mid-run hyperparameter modifications.

**Implementation prompt:**

> Launch `13_Automation/run_train.py --config 07_Experiments/EXP####/config.yaml` inside `environment/model/`. Emit `effective_config.yaml`, complete per-epoch train/val curves, immutable `CKPT####` artifacts with SHA-256 manifests, and explicit termination status in `run_manifest.json`.

**Human-only actions and decisions:** Experiment lead monitors hardware safety/quotas and decides whether to abort a diverged run; any scientific config fix requires a new `EXP####` (`STEP-027`).

**Version-control/artifact expectations:** Commit safe text logs, `metrics_history.csv`, `effective_config.yaml`, `run_manifest.json`, and `checkpoint_registry.csv` metadata; keep binary checkpoints and per-image validation arrays in Tier-3 durable storage.

**Documentation updates:** `EXP####/run_manifest.json`, `observations.md`, `08_Checkpoints/checkpoint_registry.csv`, and `failure_report.md` (`T16`) if applicable.

**Verification checklist:**

- [ ] `effective_config.yaml` matches registered `config.yaml` without unlogged overrides.
- [ ] Strictly `train` and `val` partitions accessed; internal test and external cohort untouched.
- [ ] All per-epoch curves, warnings, stop reason, and `RUN####` attempts preserved completely.
- [ ] Immutable `CKPT####` binaries synced to Tier-3 storage and verified by SHA-256.

**Common mistakes:** Keeping sole checkpoint copies on ephemeral Colab/Kaggle disks; silently shrinking batch size after an OOM without opening a new `EXP####`; deleting a low-validation-AUC run.

**Recovery procedure:** Log exact failure/loss in `failure_report.md`, verify last intact Tier-3 checkpoint backup, resume under new `RUN####` if valid or start a clean new `EXP####` with adjusted config—never fabricate missing epoch rows.

**Definition of Done:** Registered training run reaches pre-declared stop condition or documented failure with 100% durable, checksummed logs and checkpoints ready for `G10` audit. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-029](#step-029)

---

<a id="step-029"></a>
## STEP-029 — Audit experiment completion, verify checkpoints/exports, register MODEL####, and assess G10

**Objective:** Audit `EXP####` completeness and checkpoint reloadability, profile model efficiency, register eligible `MODEL####` with its model card (`T18`), and record the `G10` assessment for this experiment.

**Why this step exists:** A saved weight file alone does not prove valid convergence, intact provenance, or unbiased eligibility for downstream validation selection (`G11`).

**Governing section references:** [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-028` terminated with durable logs and Tier-3 checkpoints; original `EXP####` config and parent hashes intact.

**Estimated difficulty and time (provisional):** Moderate; 2–3 hours per experiment.

**Parallelizable:** Checksum/reload testing and `T18` model-card drafting may run concurrently; final `G10` disposition requires all checks complete.

**Inputs:** `EXP####` logs, `effective_config.yaml`, `run_manifest.json`, `CKPT####` files in Tier-3 storage, `T17` checkpoint manifest, `T18` model card template, and `T24` gate audit template.

**Expected outputs:** Verified `CKPT####` manifest (`T17`), reloaded validation prediction parity check, parameter/GFLOPs/latency efficiency record, registered `MODEL####` and `06_Models/cards/MODEL####.md` (`T18`, if eligible), `EXP####` conclusion or failure analysis, and itemized `G10` assessment bound to `EXP####`.

**Repository/file changes:** Create `08_Checkpoints/manifests/CKPT####.md`, `06_Models/cards/MODEL####.md`, and `01_Project_Management/reviews/G10_EXP####_assessment_<date>.md`; update `experiment_registry.csv`, `checkpoint_registry.csv`, `model_registry.csv`, and `gates.csv`.

**Execution procedure:**

1. Reconcile full training history, Stage 1/2 transitions, stopping reason (max epochs, early stopping, or failure), and `effective_config.yaml` fidelity against `config.yaml`.
2. Fetch the selected validation-best `CKPT####` from Tier-3 backup, verify SHA-256, reload it in a clean inference script (`environment/model/`), and confirm reloaded validation logits match end-of-training validation metrics within floating-point tolerance.
3. Measure and record computational efficiency metadata on recorded hardware: trainable/total parameters, GFLOPs at target input resolution, checkpoint MB, and validation-sample single-image latency (classification-only AND classification + Grad-CAM).
4. If the run is scientifically valid and complete, register `MODEL####` in `06_Models/model_registry.csv` with `06_Models/cards/MODEL####.md` (`T18`) linking `EXP`/`RUN`/`CKPT`/`REL`/`PP`/`XAIP` hashes and weight licenses. (Validate any ONNX/TorchScript export parity if exported.)
5. Assess `G10` specifically for `EXP####` in `gates.csv`: `PASS` certifies eligibility for validation comparison (even if validation AUC is modest!); invalid/corrupted/aborted runs receive `G10 FAIL`, stay preserved in `experiment_registry.csv`, and are excluded from `G11`.

**Planning/review prompt:**

> Audit `EXP####` against every `G10` criterion. Confirm checkpoint backup integrity, exact validation reload parity, complete efficiency metrics, and clear separation between valid low-scoring runs (eligible) and technically invalid runs (ineligible).

**Implementation prompt:**

> Run reload-parity and efficiency profiling scripts inside `environment/model/`, generate `CKPT####.md` and `MODEL####.md`, update `experiment_registry.csv`, `checkpoint_registry.csv`, and `model_registry.csv`, run `validate_registries.py`, and write the `G10` review for `EXP####`.

**Human-only actions and decisions:** Experiment reviewer verifies integrity/reload evidence and signs `G10` for `EXP####`.

**Version-control/artifact expectations:** Commit safe registry rows, `CKPT####.md`, `MODEL####.md`, `EXP####/README.md` conclusions, and `G10` audit; preserve all binaries and failed runs durably in Tier-3 storage.

**Documentation updates:** `experiment_registry.csv`, `checkpoint_registry.csv`, `model_registry.csv`, `gates.csv` (`G10` bound to `EXP####`), and `dashboard.md`.

**Verification checklist:**

- [ ] `config.yaml`, `effective_config.yaml`, logs, and stop reason reconcile completely.
- [ ] Tier-3 backup `CKPT####` SHA-256 verified and reloaded validation predictions match training logs.
- [ ] Parameters, GFLOPs, disk size, and single-image classification + Grad-CAM timing recorded.
- [ ] `MODEL####` card links all parent hashes; `G10` bound explicitly to `EXP####` and signed.

**Common mistakes:** Registering a model from the final epoch instead of the pre-declared validation-best checkpoint; omitting failed runs from `experiment_registry.csv`; exporting ONNX without checking logit and Grad-CAM parity.

**Recovery procedure:** Restore uncorrupted backup checkpoint if hash fails; if irrecoverably corrupted, mark `EXP####` `G10 FAIL`, log lost work in `T16`, and launch a clean replacement `EXP####` via `STEP-027`.

**Definition of Done:** `EXP####` audited completely with verified checkpoints/efficiency and signed `G10` eligibility verdict (`PASS` with registered `MODEL####`, or documented `FAIL` preserved). Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-030](#step-030)

---

<a id="step-030"></a>
## STEP-030 — Execute controlled multi-architecture transfer learning benchmark matrix

**Objective:** Execute and audit the full `UD13`-approved multi-architecture CNN transfer learning benchmark (all Objective 3 architectures plus any approved modern Q1 reference baseline) under strictly matched data releases, patient splits, budgets, and seeds.

**Why this step exists:** Objective 3 (`RF06`, `RF12`) and RQ1 require an unbiased, head-to-head comparison across pre-trained CNN families (VGG16, ResNet50, DenseNet121, EfficientNetB0, InceptionV3, MobileNetV2, etc.) before deciding which architecture best balances accuracy, calibration, efficiency, and XAI faithfulness.

**Governing section references:** [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §7](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §12](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-12); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** Baseline `STEP-029` achieved `G10 PASS`; `experiment_plan.md` architecture matrix approved; `G08–G09` current `PASS`.

**Estimated difficulty and time (provisional):** Hard; 2–3 hours planning/audit per architecture plus measured GPU training time across all approved architectures.

**Parallelizable:** Independent architectures may train in parallel across available GPUs; serialize `EXP`/`MODEL` ID registration and validation comparison compilation.

**Inputs:** Baseline `MODEL####` validation results, approved `UD13` architecture roster (`06_Models/candidates.csv`), matched `REL####`/`SPLIT####`, and `experiment_plan.md`.

**Expected outputs:** Individual `EXP####`, `CKPT####`, `MODEL####`, and `G10` audits for every approved architecture in the benchmark roster, plus a unified validation-only multi-architecture comparison table (discrimination, validation calibration, params, GFLOPs, latency, and any architecture-specific failures/divergences).

**Repository/file changes:** Repeat `STEP-027–029` under unique `EXP####`/`MODEL####` IDs for every `UD13` architecture; save `07_Experiments/reports/val_architecture_benchmark.md` and update registries + `gates.csv`.

**Execution procedure:**

1. Verify every remaining `UD13` architecture row in `experiment_plan.md` shares the exact baseline `REL####`/`SPLIT####` (or explicitly documented native-resolution `REL####` if InceptionV3 uses 299×299, flagged clearly as a resolution caveat!), identical two-stage schedule, imbalance rule, and primary seed(s).
2. Execute `STEP-027 → STEP-028 → STEP-029` cleanly for each architecture, issuing separate `EXP####`, `CKPT####`, `MODEL####`, and per-experiment `G10` assessments.
3. Preserve every underperforming, overfit, or diverged architecture honestly (e.g., if VGG16 saturates or MobileNetV2 underfits dense breasts, retain complete evidence rather than dropping it).
4. Compile `07_Experiments/reports/val_architecture_benchmark.md` comparing all `G10 PASS` architectures strictly on the **validation partition** across Accuracy, Precision, Recall, Specificity, F1, AUC-ROC, PR-AUC, validation ECE, parameters, GFLOPs, and inference + Grad-CAM latency. Zero test-set access!

**Planning/review prompt:**

> Audit the completed multi-architecture benchmark matrix (`val_architecture_benchmark.md`) for fair-comparison invariants. Check whether any architecture used different splits, extra epochs, altered augmentations, or omitted failures, and confirm zero held-out test leakage.

**Implementation prompt:**

> Execute the approved `UD13` benchmark matrix by iterating `STEP-027–029` with unique `EXP####` configs, aggregate validation-only metrics and efficiency profiles via script into `07_Experiments/reports/val_architecture_benchmark.md`, and run `validate_registries.py`.

**Human-only actions and decisions:** Researchers execute matrix; supervisor reviews validation comparison and approves any justified prospective amendment (e.g., if an architecture requires a documented LR adjustment, recorded transparently as an explicit new `EXP####`).

**Version-control/artifact expectations:** Keep immutable per-`EXP####` bundles and `G10` records; commit aggregation script and `val_architecture_benchmark.md`; store checkpoints in Tier-3 storage.

**Documentation updates:** `experiment_registry.csv`, `model_registry.csv`, `gates.csv` (`G10` per `EXP####`), `val_architecture_benchmark.md`, and `dashboard.md`.

**Verification checklist:**

- [ ] Every `UD13`-approved architecture has either `G10 PASS` + `MODEL####` or a documented failure/disposition.
- [ ] Matched `SPLIT####`, budgets, and imbalance rules verified (any native-resolution exception explicitly flagged).
- [ ] Validation-only comparison includes discrimination, calibration, parameters, GFLOPs, and latency.
- [ ] Zero held-out internal test or external validation images accessed.

**Common mistakes:** Giving one favored CNN extra hyperparameter tuning while running competitors on untuned defaults; dropping an architecture from the table because its validation AUC lagged; peeking at test AUC to decide which CNNs to advance to multi-seed runs.

**Recovery procedure:** Tag any inadvertently confounded run as exploratory, re-run under matched controls with a fresh `EXP####`, and re-aggregate `val_architecture_benchmark.md`.

**Definition of Done:** Full `UD13` multi-architecture transfer learning benchmark completed with per-experiment `G10` audits and a clean validation-only comparison table. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-031](#step-031)

---

<a id="step-031"></a>
## STEP-031 — Execute controlled methodological ablations and multi-seed reproducibility runs

**Objective:** Execute all pre-registered single-factor ablations (e.g., CLAHE vs minimal baseline preprocessing, focal/class-weighted loss, two-stage fine-tuning vs frozen backbone, or approved architectural refinement) and multi-seed repeats (`UD15`) strictly on train/val.

**Why this step exists:** Q1 reviewers demand controlled ablation proof showing *why* each preprocessing, imbalance, or fine-tuning design choice helps (or does not help) and multi-seed variance proving rankings are not single-seed luck.

**Governing section references:** [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §7](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §12](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-12); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-030` multi-architecture benchmark complete (`G10 PASS` across qualifying architectures); remaining GPU budget confirmed; `experiment_plan.md` ablation & seed rows approved.

**Estimated difficulty and time (provisional):** Hard; 2–3 hours audit per ablation/seed batch plus measured GPU compute duration.

**Parallelizable:** Independent single-factor ablations and distinct random seeds may train concurrently; serialize registry updates and statistical summaries.

**Inputs:** `val_architecture_benchmark.md`, pre-registered ablation & multi-seed rows in `experiment_plan.md`, `PP####` ablation release(s) (`G08`), and `UD15` seed schedule.

**Expected outputs:** Unique `EXP####`/`CKPT####`/`MODEL####` and `G10` records for every ablation and seed repeat, validation multi-seed mean ± SD report, controlled single-factor ablation report (including null/negative outcomes!), and matrix closure audit.

**Repository/file changes:** Repeat `STEP-027–029` under unique `EXP####`/`MODEL####` IDs; write `07_Experiments/reports/val_ablation_and_multiseed_report.md`; update `experiment_plan.md` row statuses, registries, and `gates.csv`.

**Execution procedure:**

1. Confirm each planned single-factor ablation varies **strictly one factor** relative to its parent `EXP####` (e.g., CLAHE `REL0002` vs minimal baseline `REL0001`; focal loss vs weighted BCE; Stage-1 frozen vs Stage-1+2 unfrozen; or approved attention/head variant) while holding seed, split, and architecture constant.
2. Execute all pre-declared random seeds (`UD15`, e.g., 3 or 5 seeds) across the approved benchmark/top architectures via `STEP-027–029`, recording `G10` for every qualifying `EXP####`.
3. Retain 100% of seeds and negative/null ablations (e.g., if CLAHE reduces validation AUC or worsens calibration, document that crucial mammography finding explicitly!).
4. Compute validation-only multi-seed mean ± SD (and min–max range) for all planned metrics and verify every row in `experiment_plan.md` is closed with an outcome or supervisor-approved disposition prior to `STEP-032`.

**Planning/review prompt:**

> Audit `val_ablation_and_multiseed_report.md` against `experiment_plan.md`. Verify strict single-factor control per ablation, confirm zero omitted unfavorable seeds, and verify readiness for validation-only final selection at `STEP-032`.

**Implementation prompt:**

> Execute all approved ablation and multi-seed configs via `STEP-027–029`, aggregate all qualifying validation runs (mean ± SD across every planned seed) into `val_ablation_and_multiseed_report.md`, and run `validate_registries.py`.

**Human-only actions and decisions:** Supervisor approves any prospective budget-driven matrix amendment and confirms development tuning is formally closed prior to `STEP-032` (`G11`).

**Version-control/artifact expectations:** Commit immutable configs, aggregation scripts, `val_ablation_and_multiseed_report.md`, and `G10` records; preserve all checkpoints in Tier-3 storage.

**Documentation updates:** `experiment_plan.md`, `experiment_registry.csv`, `model_registry.csv`, `gates.csv`, `val_ablation_and_multiseed_report.md`, and `dashboard.md`.

**Verification checklist:**

- [ ] Every ablation changes exactly one documented factor with matched `SPLIT####` and seed.
- [ ] All planned random seeds executed and aggregated (zero dropped worst seeds).
- [ ] Null and negative ablation findings retained explicitly.
- [ ] Zero held-out internal test or external cohort access occurred throughout Stage S11.

**Common mistakes:** Changing CLAHE, image resolution, and learning rate simultaneously while claiming a "CLAHE gain"; running extra seeds until one beats a rival architecture; discarding failed ablations.

**Recovery procedure:** Reclassify any accidentally confounded experiment as exploratory, run a clean single-factor `EXP####` if compute allows, or withdraw the confounded claim before `G11`.

**Definition of Done:** Approved multi-architecture, controlled ablation, and multi-seed experimental matrix fully completed and audited (`G10 PASS` for all eligible models), closing development tuning cleanly. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-032](#step-032)

---

<a id="step-032"></a>
## STEP-032 — Select on validation, fit threshold & calibration, and freeze final-test / XAI protocol (G11)

**Objective:** Apply the pre-declared validation-only selection rule, lock decision threshold(s) and post-hoc probability calibration parameters exclusively from validation predictions, freeze all test/external/XAI/statistical artifacts, audit prior test custody, and pass `G11`.

**Why this step exists:** Selecting models, tuning binary cutoffs, fitting Temperature Scaling, or picking XAI target layers after looking at held-out test outputs introduces subtle leakage that invalidates Q1 claims.

**Governing section references:** [OS §5](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-031` complete; `G10 PASS` for every candidate `MODEL####` considered; `G07–G09` current `PASS`; zero prior test-set predictions generated.

**Estimated difficulty and time (provisional):** Hard; 3–5 hours plus supervisor and evaluation-reviewer freeze sign-off.

**Parallelizable:** No for final selection and freeze lock; background literature/methods drafting may continue independently.

**Inputs:** `val_architecture_benchmark.md`, `val_ablation_and_multiseed_report.md`, validation logits of every `G10 PASS` model, `09_Evaluation/protocol.md`, `XAIP####`, and test-access audit log.

**Expected outputs:** Selected winning `MODEL####` (and full frozen benchmark roster for head-to-head paired test comparisons!), frozen validation-only scalar decision threshold(s) (e.g., Youden's J + 90%/95% validation-sensitivity thresholds), serialized validation-fitted post-hoc calibrator(s) (e.g., Temperature Scaling `T` per model with SHA-256), immutable `09_Evaluation/freeze.md` + `freeze_manifest.json`, finalized `UD16–UD20` parameters, and `G11` assessment.

**Repository/file changes:** Create `09_Evaluation/freeze.md`, `09_Evaluation/freeze_manifest.json`, serialized calibrator files in Tier-3 storage (with SHA-256 in `model_registry.csv`), and `01_Project_Management/reviews/G11_assessment_<date>.md`; update `model_registry.csv`, `decisions.csv`, and `gates.csv`.

**Execution procedure:**

1. Apply the pre-declared validation selection criterion (`UD15`) strictly on validation results to designate the **single winning final best `MODEL####`** (plus exact multi-seed aggregation policy and comparator `MODEL####` list scheduled for paired DeLong/McNemar test comparisons). Document all tradeoffs transparently.
2. Derive binary operating-point threshold(s) strictly on the **validation set** per `UD19` (e.g., primary Youden's J threshold plus clinical high-sensitivity screening threshold targeting 90%/95% validation Sensitivity). Record exact scalar values.
3. Fit any adopted post-hoc probability calibrator (e.g., Temperature Scaling / Platt Scaling per `UD19`) strictly on **validation logits**, serialize parameters with SHA-256, and bind `CalibratorHash` and `FrozenThreshold` into `model_registry.csv`.
4. Lock SHA-256 hashes of: every frozen `MODEL####`/`CKPT####`, `REL####` (internal test + external validation cohort if adopted), `LBL####` (labels + ROI masks), `PP####` (fitted state), `XAIP####` (exact target layers, perturbation schedules, sanity/localization/stability rules), `09_Evaluation/protocol.md`, and `src/bc_xai/` Git commit inside `freeze_manifest.json` and `freeze.md`.
5. Audit test-set custody logs verifying zero prior test-set leakage, obtain supervisor and evaluation-reviewer sign-off, and record dated `G11 PASS` **strictly before** any test inference timestamp.

**Planning/review prompt:**

> Audit `freeze.md` and `freeze_manifest.json` against `G11`. Confirm that the winning model, thresholds, and calibration parameters were derived 100% from validation outputs, every comparator model holds `G10 PASS`, all XAI/statistical settings are frozen, and zero prior test exposure occurred.

**Implementation prompt:**

> Fit validation-only threshold(s) and calibrator(s) inside `environment/model/`, write SHA-256-locked `09_Evaluation/freeze_manifest.json` and `freeze.md`, update `model_registry.csv` (`CalibratorHash`, `FrozenThreshold`), and configure `eval` scripts to refuse execution on any freeze-hash mismatch.

**Human-only actions and decisions:** Supervisor and evaluation reviewer audit test custody, approve winning selection/thresholds/calibrators (`UD16–UD20` final freeze), and sign `G11` authorizing test unsealing.

**Version-control/artifact expectations:** Commit `freeze.md`, `freeze_manifest.json`, updated `model_registry.csv`, and `G11` audit prior to running `STEP-033`; archive calibrator files in Tier-3 storage.

**Documentation updates:** `09_Evaluation/freeze.md`, `model_registry.csv`, `decisions.csv`, `gates.csv` (`G11`), and `dashboard.md`.

**Verification checklist:**

- [ ] Winning `MODEL####` and all paired benchmark comparators hold current `G10 PASS`.
- [ ] Operating threshold(s) and post-hoc calibration fitted 100% on validation predictions.
- [ ] Complete SHA-256 lock covers models, releases (internal + external), ROI masks, `XAIP####`, protocol, and code commit.
- [ ] Test custody audited clean and `G11 PASS` timestamp strictly precedes `STEP-033` test inference.

**Common mistakes:** Fitting Temperature Scaling on the test set; tuning the binary decision cutoff on test ROC curves; freezing only the winning model while forgetting to freeze comparator models needed for paired DeLong/McNemar tests.

**Recovery procedure:** Halt immediately if any unfrozen setting or test exposure is detected; resolve missing locks before `G11`, or disclose exposure honestly and redesign with untouched external data or exploratory framing.

**Definition of Done:** `G11 PASS` sealing a tamper-evident freeze bundle authorizing locked internal held-out test and external validation execution. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-033](#step-033)

---

<a id="step-033"></a>
## STEP-033 — Execute frozen inference on locked internal test set and independent external cohort

**Objective:** Run one-shot frozen inference across the locked internal held-out test partition and independent external validation cohort (if adopted under `UD05`) for all `G11`-frozen models, generating complete validated prediction and coverage artifacts.

**Why this step exists:** Separating immutable prediction generation from downstream metrics, statistical testing, and XAI evaluation guarantees 100% image coverage, zero dropped failures, and exact shared denominators across every paired comparison.

**Governing section references:** [OS §7](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §8](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-032` complete; `G11 PASS`; frozen `freeze_manifest.json` and sealed internal/external test releases accessible.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours plus deterministic inference runtime across frozen models and cohorts.

**Parallelizable:** Deterministic inference across distinct frozen `MODEL####` artifacts or cohorts may run concurrently without modifying any shared state.

**Inputs:** `09_Evaluation/freeze_manifest.json`, frozen `MODEL####`/`CKPT####`/calibrators/thresholds, locked internal test `REL####`, and locked independent external `REL####` (if adopted).

**Expected outputs:** Unique `EVAL####` bundle per `(MODEL####, CohortType)` containing immutable per-image raw logits, raw probabilities, calibrated probabilities, frozen-threshold binary predictions, 100% evaluated-image coverage ledger (including any inference/decode errors), prediction SHA-256 hashes, and initialized `evaluation_registry.csv` rows.

**Repository/file changes:** Create `09_Evaluation/EVAL####/` (`predictions.parquet`/`.csv` in Tier-3 storage, safe `coverage_report.md`, `inference_manifest.json`); update `09_Evaluation/evaluation_registry.csv`.

**Execution procedure:**

1. Verify every `MODEL`, `CKPT`, `REL`, `LBL`, `PP`, calibrator, protocol, and code commit hash strictly against `freeze_manifest.json`; abort immediately on any mismatch.
2. Execute deterministic inference (zero augmentation, zero batch-norm stat updates, zero threshold/calibrator re-fitting!) on 100% of scheduled internal test images and 100% of scheduled independent external cohort images (zero-shot transfer).
3. Emit one row per scheduled `ImageID` capturing `PatientGroupID`, ground-truth `y_true`, raw logit, raw probability, calibrated probability, binary predictions at every frozen validation threshold, subgroup metadata tags, and processing status (`ok | error_code`).
4. Validate exact 100% image count reconciliation against `SPLIT####`/`REL####`, check for NaN/Inf logits, verify zero duplicate `ImageID` rows, and lock prediction file SHA-256 digests in `evaluation_registry.csv`.

**Planning/review prompt:**

> Audit `EVAL####` inference manifests and coverage ledgers against `freeze_manifest.json`. Confirm 100% image coverage across internal and external cohorts, exact freeze-hash agreement, zero re-fitting on external data, and intact failure accounting.

**Implementation prompt:**

> Execute `13_Automation/run_eval_inference.py --freeze 09_Evaluation/freeze_manifest.json` inside `environment/model/`. Fail hard on any hash mismatch or missing image; persist per-image predictions in Tier-3 storage with SHA-256 hashes and write safe `coverage_report.md` and `evaluation_registry.csv` rows.

**Human-only actions and decisions:** Evaluation lead authorizes test unsealing under `G11` and reviews any unexpected decode/runtime failure under the pre-approved protocol.

**Version-control/artifact expectations:** Store full per-image prediction files in Tier-3 storage with SHA-256 checksums; commit `inference_manifest.json`, `coverage_report.md`, and `evaluation_registry.csv` updates to Git.

**Documentation updates:** `09_Evaluation/evaluation_registry.csv`, `EVAL####/coverage_report.md`, and test-access custody log.

**Verification checklist:**

- [ ] Every executed hash matches `09_Evaluation/freeze_manifest.json` verbatim.
- [ ] 100% of scheduled internal test and external validation images accounted for with zero silent drops.
- [ ] Zero NaN/Inf logits or post-freeze threshold/calibrator adjustments.
- [ ] Prediction SHA-256 digests recorded in `evaluation_registry.csv` and backed up in Tier-3 storage.

**Common mistakes:** Leaving Dropout or BatchNorm in `.train()` mode during inference; forgetting to apply the primary training-fitted `PP####` state to the external dataset; re-tuning thresholds separately on the external validation cohort.

**Recovery procedure:** Mark defective `EVAL####` `INVALID`, preserve original files untouched, fix verified inference bug under a new `EVAL####` with disclosure, and never alter models or thresholds based on observed test predictions.

**Definition of Done:** Validated, hash-locked internal and external test predictions with 100% coverage exist for all frozen models, ready for quantitative classification, statistical, and XAI evaluation. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-034](#step-034)

---

<a id="step-034"></a>
## STEP-034 — Compute classification metrics, calibration, paired statistical tests, and efficiency profiles

**Objective:** Compute all 6 report-required metrics plus the full Q1 classification, probability calibration, patient-clustered 95% confidence intervals, paired DeLong/McNemar (Holm-Bonferroni) tests, and efficiency profiles from locked `EVAL####` predictions.

**Why this step exists:** Q1 publication demands statistically rigorous uncertainty estimation respecting patient clustering, explicit false-negative/false-positive clinical tradeoffs, probability calibration proof, and honest paired significance testing across architectures.

**Governing section references:** [OS §7](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-033` validated `EVAL####` prediction files locked; `09_Evaluation/protocol.md` and `freeze_manifest.json` intact; `tests/test_{metrics,stats}.py` passing.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours including clustered bootstrap resampling compute.

**Parallelizable:** Runs cleanly in parallel with `STEP-035` (Quantitative XAI Evaluation) since both read immutable `STEP-033`/`G11` artifacts independently.

**Inputs:** Immutable `EVAL####` prediction files (internal test + external cohort), `freeze_manifest.json`, `09_Evaluation/protocol.md` (`UD19–UD20`), and `T21` statistical comparison template.

**Expected outputs:** Complete `metrics.csv`, `confusion_matrices.json`, ROC/PR curve source arrays, `calibration.csv` + reliability diagram source data (raw vs validation-calibrated ECE & Brier), efficiency comparison table (params, GFLOPs, disk MB, single-image classification & Grad-CAM latency), paired `STAT####` reports (`T21`), and populated `09_Evaluation/statistical_comparisons.csv`.

**Repository/file changes:** Write `09_Evaluation/EVAL####/{metrics.csv,calibration.csv,efficiency.csv,stat_STAT####.md}` and curve source arrays; populate `09_Evaluation/statistical_comparisons.csv` and update `evaluation_registry.csv`.

**Execution procedure:**

1. Compute all **6 mandatory report metrics** (`RF09`: Accuracy, Precision, Recall/Sensitivity, F1-score, AUC-ROC, 2×2 Confusion Matrix) PLUS **Q1 medical-AI metrics** (`UD19`: Specificity, PR-AUC, Balanced Accuracy, MCC, Specificity at fixed 90%/95% Sensitivity and Sensitivity at fixed 90% Specificity) for every frozen architecture on internal test and zero-shot external cohort (and aggregate multi-seed mean ± SD across planned seeds!).
2. Compute probability calibration metrics (`ECE`, `Brier Score`, reliability bin frequencies) for both raw probabilities and validation-fitted post-hoc calibrated probabilities (if adopted under `UD19`).
3. Run **patient-level clustered bootstrap** resampling (`PatientGroupID` clusters, pre-declared $B$ replicates & seed from `UD20`) to produce 95% CIs for every metric; never treat multiple views of the same patient as independent draws.
4. Execute paired statistical comparisons (`STAT####`, `T21`) between the validation-selected winning `MODEL####` and every other frozen benchmark architecture: two-sided **DeLong's test** (or patient-clustered equivalent) on AUC-ROC, **McNemar's test** on paired frozen-threshold predictions, exact effect sizes ($\Delta\text{AUC}$, $\Delta\text{Sens}$, $\Delta\text{Spec}$), and **Holm-Bonferroni** adjusted p-values (`UD20`).
5. Consolidate standardized hardware efficiency measurements (total params, GFLOPs, memory footprint, warmed-up repeated single-image latency for classification-only and classification+Grad-CAM under documented hardware/batch=1).

**Planning/review prompt:**

> Audit `metrics.csv`, `calibration.csv`, and `statistical_comparisons.csv` against `09_Evaluation/protocol.md`. Verify all 6 report metrics + Q1 extensions are present, patient clustering was respected in bootstrap CIs, Holm-Bonferroni correction covers all planned pairwise tests, and raw vs calibrated ECE are reported without test re-fitting.

**Implementation prompt:**

> Run `13_Automation/run_eval_metrics_stats.py --freeze 09_Evaluation/freeze_manifest.json` inside `environment/model/` over immutable `EVAL####` predictions. Emit full-precision CSVs, curve arrays, `STAT####` reports (`T21`), and `statistical_comparisons.csv` rows; fail on any NaN or missing comparator.

**Human-only actions and decisions:** Evaluation reviewer audits mathematical definitions, clustered bootstrap logs, Holm-Bonferroni family size, and raw vs adjusted p-values.

**Version-control/artifact expectations:** Commit safe aggregate CSVs, `STAT####` reports, `statistical_comparisons.csv`, and curve data; store large per-replicate bootstrap arrays in Tier-3 storage with SHA-256 hashes.

**Documentation updates:** `evaluation_registry.csv`, `statistical_comparisons.csv`, and metric/calibration/stat artifacts under `09_Evaluation/EVAL####/`.

**Verification checklist:**

- [ ] All 6 required report metrics (`RF09`) plus Specificity, PR-AUC, Balanced Accuracy, MCC, and clinical operating points computed for every model & cohort.
- [ ] Raw and validation-calibrated ECE, Brier score, and reliability data recorded.
- [ ] Patient-clustered bootstrap 95% CIs, DeLong p-values, McNemar p-values, and Holm-Bonferroni adjusted p-values recorded in `statistical_comparisons.csv`.
- [ ] Multi-seed mean ± SD and hardware-documented efficiency profiles complete; zero omitted unfavorable models.

**Common mistakes:** Reporting p-values without multiple-comparison adjustment; forgetting to cluster bootstrap resamples by `PatientGroupID`; claiming statistical superiority when 95% CIs overlap and DeLong $p_{\text{adj}} > 0.05$.

**Recovery procedure:** Mark erroneous `EVAL`/`STAT` records `INVALID`, fix verified computation bugs under new IDs with full disclosure, preserve original files, and re-run cleanly.

**Definition of Done:** Complete, reproducible classification, calibration, paired statistical inference, and efficiency evidence package computed for all frozen models and cohorts. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-035](#step-035)

---

<a id="step-035"></a>
## STEP-035 — Execute quantitative XAI evaluation (faithfulness, Adebayo sanity checks, ROI localization, and stability)

**Objective:** Run the complete `G11`-frozen quantitative XAI evaluation suite (`XAIP####`) across Grad-CAM and all approved XAI comparators on internal and external test cohorts, registering `XAIA####` audits (`T20`).

**Why this step exists:** Quantitative proof of faithfulness, weight sensitivity (sanity), anatomical lesion alignment, and explanation stability is the defining methodological differentiator between a routine class project and a publishable Q1 medical XAI paper.

**Governing section references:** [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-033` locked predictions & `G11` `freeze_manifest.json`; bound `XAIP####` & `target_layer_map.yaml`; verified `LBL####` co-transformed ROI masks; `tests/test_xai.py` passing.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours active setup/audit plus GPU attribution & perturbation compute time.

**Parallelizable:** Runs in parallel with `STEP-034`; distinct architectures or XAI methods may run concurrently under identical frozen `XAIP####` settings.

**Inputs:** Frozen `MODEL####`/`CKPT####`, locked internal & external test `REL####` images, verified co-transformed ROI masks (`LBL####`), frozen `XAIP####` protocol (`UD16–UD17`), and `T20` XAI audit template.

**Expected outputs:** Raw normalized attribution maps in Tier-3 storage, quantitative faithfulness curves & scores (Deletion AUC, Insertion AUC, ROAD vs random baseline), Adebayo cascading/independent parameter & data randomization correlation decay curves + pass/fail flags, ROI-mask localization metrics (Pointing Game, EBPG, thresholded IoU/Dice on verified mask subsets), input-perturbation & multi-seed stability scores, inter-XAI concordance matrix, completed `xai_audit_XAIA####.md` (`T20`), and populated `09_Evaluation/xai_audit_registry.csv`.

**Repository/file changes:** Write `09_Evaluation/EVAL####/xai/` aggregate CSVs & `xai_audit_XAIA####.md`; store large raw saliency arrays in Tier-3 storage with SHA-256 manifests; populate `09_Evaluation/xai_audit_registry.csv`.

**Execution procedure:**

1. Generate standardized saliency maps using frozen `XAIP####` target layers and Malignant pre-sigmoid/pre-softmax logits for **Grad-CAM** (mandatory baseline) and all `UD16`-approved comparators (e.g., Grad-CAM++, Score-CAM, LayerCAM, Integrated Gradients, Guided Backpropagation, LIME/SHAP on approved scope); log count of any zero/collapsed maps explicitly.
2. **Faithfulness pillar (`UD17`):** Compute Deletion AUC, Insertion AUC, and ROAD (linear imputation debiased removal) across the frozen perturbation schedule for every model × XAI method, alongside a random-saliency baseline control and patient-clustered bootstrap 95% CIs.
3. **Sanity-check pillar (`UD17`):** Execute Adebayo et al. cascading (top-to-bottom layer re-initialization) and independent layer randomization tests (plus label-randomization sanity test if adopted), measuring Spearman rank correlation, SSIM, and HOG similarity vs original trained heatmaps; flag any method showing invariant edge-detector behavior explicitly as `SANITY_FAILED`!
4. **ROI-mask localization pillar (`UD17`):** Across all test images possessing verified co-transformed lesion ROI masks in `LBL####` (reporting exact $n$ and mask granularity), compute Pointing Game accuracy, Energy-Based Pointing Game (EBPG), and thresholded Heatmap-to-ROI IoU/Dice (separately for Malignant TP, Malignant FN, and Benign cases where masks exist).
5. **Stability & cross-method consistency pillar (`UD17`):** Measure heatmap SSIM/Spearman stability under minor radiographically valid input perturbations AND across multi-seed checkpoints of the same architecture, plus pairwise correlation across XAI methods; assemble `xai_audit_XAIA####.md` (`T20`) and register `XAIA####`.

**Planning/review prompt:**

> Audit `xai_audit_XAIA####.md` against `XAIP####` and Q1 XAI validity standards. Verify whether any XAI method failed Adebayo sanity checks (e.g., Guided Backpropagation), whether Grad-CAM outperforms the random-mask faithfulness baseline, whether ROI localization separates true lesion attention from shortcut artifacts, and whether patient-clustered 95% CIs are reported.

**Implementation prompt:**

> Execute `13_Automation/run_xai_audit.py --freeze 09_Evaluation/freeze_manifest.json` inside `environment/model/`. Persist raw saliency arrays in Tier-3 storage with SHA-256 checksums, emit full-precision CSVs for faithfulness/sanity/localization/stability, write `xai_audit_XAIA####.md` (`T20`), and register `XAIA####` in `xai_audit_registry.csv`.

**Human-only actions and decisions:** XAI lead and evaluation reviewer inspect sanity-check decay plots, faithfulness vs random controls, and ROI localization distributions; never suppress an inconvenient sanity failure or low-EBPG architecture!

**Version-control/artifact expectations:** Commit safe aggregate CSVs, `xai_audit_XAIA####.md`, and `xai_audit_registry.csv`; store raw saliency numpy/HDF5 arrays in Tier-3 storage with SHA-256 digests.

**Documentation updates:** `09_Evaluation/xai_audit_registry.csv`, `xai_audit_XAIA####.md`, and `claims.csv` evidence links.

**Verification checklist:**

- [ ] Grad-CAM (and every `UD16`-approved comparator) evaluated strictly using `G11`-frozen target layers and logit convention.
- [ ] Deletion AUC, Insertion AUC, and ROAD computed alongside random-mask control with patient-clustered 95% CIs.
- [ ] Adebayo model-parameter randomization sanity checks executed and any failing method flagged explicitly.
- [ ] ROI Pointing Game, EBPG, and IoU/Dice computed over verified co-transformed `LBL####` masks (exact $n$ disclosed).
- [ ] Input-perturbation stability and multi-seed heatmap consistency logged in `xai_audit_registry.csv`.

**Common mistakes:** Evaluating Grad-CAM faithfulness only with black-pixel (zero) masking without ROAD/blur debiased control; hiding a failed Adebayo sanity check; evaluating ROI localization on mismatched un-transformed masks; cherry-picking a prettier intermediate layer after seeing low EBPG.

**Recovery procedure:** Mark defective `XAIA####` `INVALID`, repair verified computation bugs under a new `XAIA####` linked to the unchanged frozen model, preserve original outputs, and disclose the correction.

**Definition of Done:** Complete, reproducible quantitative XAI faithfulness, sanity, ROI-localization, and stability audit registered under `XAIA####`. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-036](#step-036)

---

<a id="step-036"></a>
## STEP-036 — Consolidate final quantitative evaluation, external generalization, and XAI faithfulness report (G12)

**Objective:** Synthesize `STEP-033–035` outputs into one auditable final quantitative evaluation report (`T19`) reconciling internal test, zero-shot external validation, calibration, paired statistical tests, quantitative XAI, and efficiency, and pass `G12`.

**Why this step exists:** Fragmented CSVs invite selective reporting across checkpoints; one unified, hash-linked quantitative report locks every empirical number before downstream error analysis, prototype packaging, and manuscript drafting.

**Governing section references:** [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-034` (`EVAL`/`STAT`) and `STEP-035` (`XAIA`) complete; `G11` freeze lineage intact; all planned analyses completed or deviations explicitly documented.

**Estimated difficulty and time (provisional):** Hard; 3–5 hours plus evaluation-reviewer & XAI-lead sign-off.

**Parallelizable:** Drafting narrative tables and running automated reconciliation scripts can run in parallel; `G12` sign-off requires full convergence.

**Inputs:** `EVAL####` metrics/calibration/efficiency files, `STAT####` paired tests, `XAIA####` quantitative XAI audits, `freeze_manifest.json`, and `T19`/`T24` templates.

**Expected outputs:** Consolidated final evaluation report (`09_Evaluation/EVAL####/report.md`), reconciled `evaluation_registry.csv`/`xai_audit_registry.csv`/`statistical_comparisons.csv`, empirical `CLAIM####` records linked to `EVAL`/`XAIA`/`STAT`, and `G12` assessment.

**Repository/file changes:** Finalize `09_Evaluation/EVAL####/report.md`, update `02_Literature/claims.csv`, `09_Evaluation/{evaluation_registry,xai_audit_registry,statistical_comparisons}.csv`, and create `01_Project_Management/reviews/G12_assessment_<date>.md`; update `gates.csv`.

**Execution procedure:**

1. Programmatically verify that every reported metric, 95% CI, p-value, ECE, efficiency stat, and XAI faithfulness/sanity/localization score in `report.md` traces directly to immutable `STEP-034`/`STEP-035` CSVs and `freeze_manifest.json` hashes.
2. Verify 100% inclusion of all 6 report-required metrics (`RF09`), all Q1 extensions (`UD19–UD20`), zero-shot external validation results (if adopted) including honest domain-shift drops, multi-seed variance, ablation outcomes (positive, null, and negative), and all XAI sanity/faithfulness results.
3. Explicitly separate **validation selection evidence** (`STEP-030–031`) from **locked held-out internal test** and **zero-shot external validation** results so readers never confuse development scores with test estimates.
4. Register verified empirical claims in `02_Literature/claims.csv` and execute itemized `G12` assessment (`PASS` certifies methodological validity and traceability, never a required high AUC score).

**Planning/review prompt:**

> Perform an adversarial Q1 reviewer audit on `09_Evaluation/EVAL####/report.md`. Hunt for omitted report metrics, missing patient-clustered CIs, unadjusted p-values, concealed Adebayo sanity failures, silent omission of weak CNNs/seeds, or blurred validation vs test boundaries.

**Implementation prompt:**

> Generate consolidated summary tables directly from immutable `EVAL`/`STAT`/`XAIA` CSVs via script (preserving full source precision and documented rounding), link empirical `CLAIM####` rows, run `validate_registries.py`, and save `09_Evaluation/EVAL####/report.md` and `G12` audit evidence.

**Human-only actions and decisions:** Evaluation reviewer and XAI lead audit reconciliation evidence and sign `G12`; supervisor reviews any consequential methodological deviation.

**Version-control/artifact expectations:** Commit consolidated `report.md`, registry updates, `claims.csv`, and `G12` review; preserve raw predictions, bootstrap arrays, and saliency dumps in Tier-3 storage.

**Documentation updates:** `evaluation_registry.csv`, `xai_audit_registry.csv`, `statistical_comparisons.csv`, `claims.csv`, `gates.csv` (`G12`), and `dashboard.md`.

**Verification checklist:**

- [ ] All 6 report metrics (`RF09`) plus Q1 calibration, clustered 95% CIs, DeLong/McNemar (Holm-Bonferroni), and quantitative XAI metrics reconciled to source CSVs.
- [ ] Internal test, zero-shot external cohort (if adopted), and multi-seed/ablation results clearly separated from validation scores.
- [ ] Zero unfavorable architectures, seeds, ablations, or failed XAI sanity checks omitted.
- [ ] `G12 PASS` evidenced on validity and traceability with named reviewer sign-off.

**Common mistakes:** Mixing the best AUC checkpoint from one architecture with the best XAI localization checkpoint from another unlabeled; reporting external-cohort performance after secret threshold re-tuning; rounding p-values inconsistently across tables.

**Recovery procedure:** Reconcile provenance mismatches, repair verified reporting or aggregation bugs under a versioned report/new `EVAL` ID with disclosure, and re-audit `G12`.

**Definition of Done:** `G12 PASS` locking one complete, traceable, Q1-grade quantitative classification, statistical, external-generalization, and XAI evaluation package. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-037](#step-037)

---

<a id="step-037"></a>
## STEP-037 — Conduct stratified subgroup analysis, FN/FP failure taxonomy, and blinded qualitative radiologist XAI review (G13)

**Objective:** Analyze stratified performance across clinical mammography subgroups, build a structured FN/FP + XAI shortcut-focus failure taxonomy, execute bounded blinded radiologist/clinical-advisor qualitative review (`UD18`), bound limitations, and pass `G13`.

**Why this step exists:** High global AUC can conceal catastrophic false-negative rates in dense breasts (BI-RADS C/D), subtle microcalcification blind spots, or "Right for the Wrong Reasons" shortcut reliance on radiopaque markers/pectoral muscles—all core Q1 reviewer checks.

**Governing section references:** [OS §6](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-036` complete; `G12 PASS`; verified subgroup metadata (`LBL####`/`DS####`), frozen predictions/saliency maps, approved blinded rubric (`UD18`, `G05`), and disclosure-cleared review setup.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours analysis plus blinded clinical-advisor review turnaround (unknown external schedule).

**Parallelizable:** Automated subgroup metric stratification and FN/FP sampling package preparation may run in parallel; qualitative rubric synthesis and `G13` sign-off consolidate both.

**Inputs:** Frozen `EVAL####` predictions, `XAIA####` heatmaps, `LBL####` ROI masks & clinical metadata (BI-RADS breast density A–D, mass vs calcification, CC vs MLO view), `qualitative_review_rubric.md` (`UD18`), and `T22` error review template.

**Expected outputs:** Stratified subgroup performance & XAI localization tables (`subgroups.csv`), systematic FN/FP + XAI failure taxonomy (`error_review.md`, `T22`), blinded clinical-advisor qualitative review results (or explicit `UD18` non-performance record if advisor unavailable), `limitations.md`, updated `xai_audit_registry.csv` (`QualitativeReviewStatus`), and `G13` assessment.

**Repository/file changes:** Create `09_Evaluation/EVAL####/{subgroups.csv,error_review.md,limitations.md,clinical_xai_review_summary.md}`; store blinded review slide decks/overlays in Tier-3 storage; update `evaluation_registry.csv`, `xai_audit_registry.csv`, `claims.csv`, `gates.csv`, and save `01_Project_Management/reviews/G13_assessment_<date>.md`.

**Execution procedure:**

1. Compute stratified classification (AUC-ROC, PR-AUC, Sensitivity, Specificity, ECE) and quantitative XAI localization (Pointing Game/EBPG where masks exist) by **BI-RADS breast density (A–D)**, **abnormality type (mass vs calcification)**, **view (CC vs MLO)**, and **cohort (internal vs external)**, explicitly reporting exact subgroup $n$ and flagging small-$n$ cells.
2. Draw the prospectively stratified qualitative review sample (TP, TN, **all or stratified high-priority FN missed cancers**, and FP false alarms, recording exact sampling seed and denominators—zero cherry-picking!).
3. Classify every sampled case into the Section 7.5 taxonomy (`aligned_success`, `right_for_wrong_reasons_shortcut`, `fn_diffuse_or_dense_masking`, `fn_threshold_calibration_miss`, `fp_benign_calc_or_artifact`, `suspected_label_ambiguity`) inspecting mammogram, Grad-CAM/comparator overlays, and ROI masks side-by-side.
4. Conduct the bounded blinded qualitative review with the qualified radiologist/clinical advisor under `qualitative_review_rubric.md` (`UD18`), recording anonymized credentials, Likert distributions, qualitative notes, and strict non-clinical-trial framing—OR if no qualified reviewer is secured, record `QualitativeReviewStatus = not_performed_unavailable` honestly without substituting student/AI ratings!
5. Draft `limitations.md` bounding retrospective public-dataset bias, single- vs multi-center generalizability, subgroup weaknesses, shortcut findings, and Section 8 exclusions (`RF15`); assess `G13`.

**Planning/review prompt:**

> Audit `subgroups.csv`, `error_review.md`, and `limitations.md` against `G13`. Check specifically for dense-breast (BI-RADS C/D) degradation, microcalcification vs mass discrepancies, "Right for the Wrong Reasons" shortcut cases, honest handling of `UD18` advisor status, and strict non-clinical wording.

**Implementation prompt:**

> Run `13_Automation/run_subgroup_error_analysis.py` inside `environment/model/` to emit `subgroups.csv` and deterministic stratified case-review bundles (storing mammogram overlays in restricted Tier-3 storage). Record actual taxonomy counts, actual blinded advisor ratings (if performed), and `limitations.md`; do not alter test labels or tune models from errors.

**Human-only actions and decisions:** Radiologist/clinical advisor performs blinded qualitative rubric scoring (`UD18`, if engaged); supervisor reviews error taxonomy, clinical wording boundaries, and signs `G13`.

**Version-control/artifact expectations:** Commit safe aggregate `subgroups.csv`, `error_review.md`, `clinical_xai_review_summary.md`, `limitations.md`, and `G13` audit; keep non-disclosure-cleared visual plates strictly in Tier-3 storage.

**Documentation updates:** `evaluation_registry.csv`, `xai_audit_registry.csv`, `claims.csv`, `gates.csv` (`G13`), and `dashboard.md`.

**Verification checklist:**

- [ ] Stratified metrics reported across available density (A–D), mass/calcification, CC/MLO, and internal/external subgroups with exact $n$.
- [ ] Prospective sampling seed, denominators, and FN/FP + shortcut-focus taxonomy counts recorded without cherry-picking.
- [ ] Blinded clinical-advisor review (`UD18`) recorded with genuine human ratings OR transparently marked `not_performed_unavailable`.
- [ ] `limitations.md` strictly respects Section 8 exclusions (no clinical validation/trial claim); `G13 PASS` signed.

**Common mistakes:** Displaying only crisp True Positive Grad-CAM overlays while hiding False Negative or pectoral-muscle shortcut failures; silently mutating frozen test labels after spotting an ambiguous case; substituting researcher opinions for radiologist evaluation.

**Recovery procedure:** Re-draw unbiased stratified review sample with recorded seed, revise overstated clinical or causal wording, route any genuine dataset label defect through versioned `LBL`/`EVAL` disclosure (never silent edits), and re-audit `G13`.

**Definition of Done:** `G13 PASS` certifying thorough subgroup analysis, honest FN/FP + XAI failure taxonomy, transparent clinical-alignment status, and bounded scientific limitations. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-038](#step-038)

---

<a id="step-038"></a>
## STEP-038 — Package and verify the local research CAD inference & Grad-CAM explanation prototype

**Objective:** Package the `G11`-frozen, `G12–G13`-evaluated winning mammogram classifier + calibration + Grad-CAM (and approved comparator) pipeline into a clean, hash-verified local research CAD entry point (`src/bc_xai/infer.py`, `UD22`).

**Why this step exists:** Objective 6 (`RF12`) requires an interpretable CAD research framework; establishing one canonical, parity-tested local entry point ensures clean reproducibility (`STEP-039`) and provides the exact single inference path that the conditional defense web demo (`STEP-048–050`) must import unchanged.

**Governing section references:** [OS §2](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §8](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-037` complete; `G12–G13 PASS`; winning `MODEL####`, frozen `PP####`, validation threshold/calibrator, and `XAIP####` hashes locked; `UD22` interface choice ratified.

**Estimated difficulty and time (provisional):** Moderate; 4–8 hours across packaging, export parity checks, error-contract tests, and guide authoring.

**Parallelizable:** Drafting `12_Documentation/prototype_guide.md` can accompany packaging; functional and parity verification wait for the finalized entry point.

**Inputs:** Frozen `MODEL####`/`CKPT####` (or verified export), deterministic `PP####` state, validation threshold & calibrator, `XAIP####` target-layer config, disclosure-reviewed sample inputs, and `UD22`.

**Expected outputs:** Stable local CAD inference & Grad-CAM entry point (`src/bc_xai/infer.py` + thin CLI `13_Automation/run_cad_prototype.py`), structured JSON + heatmap overlay output contract, export-vs-checkpoint numerical & heatmap parity test report, error-handling test suite, and `12_Documentation/prototype_guide.md`.

**Repository/file changes:** Finalize `src/bc_xai/infer.py`, `13_Automation/run_cad_prototype.py`, `tests/test_prototype.py`, `12_Documentation/prototype_guide.md`, and `DEC####` (`UD22`).

**Execution procedure:**

1. Implement `src/bc_xai/infer.py` loading `MODEL####`, `PP####`, calibrator, frozen threshold, `label_map.json`, and `XAIP####` strictly by manifest path and verifying every SHA-256 hash at startup (refusing execution on mismatch).
2. Accept authorized 2D mammogram inputs (DICOM or approved image format), validate integrity/polarity/dimensions, emit calibrated Malignant probability, binary Benign/Malignant prediction at frozen threshold, Grad-CAM (and optional comparator) overlay mapped cleanly to input geometry, provenance metadata (`MODEL`, `PP`, `XAIP`, commit hash, latency), and persistent *"Research CAD Aid Only — Not for Clinical Diagnosis"* disclaimer.
3. Verify numerical parity (raw logit, calibrated probability, binary prediction, and Grad-CAM array SSIM/max-abs-diff within `UD22` tolerance) between `infer.py` (and any ONNX/TorchScript export) and the `STEP-033`/`STEP-035` frozen evaluation outputs on permitted test samples.
4. Execute `tests/test_prototype.py` testing valid inputs, corrupted/non-image files, wrong bit-depth/empty frames, missing/tampered weight hashes, and OOM/resource errors; document usage, limitations, and exact CLI schema in `12_Documentation/prototype_guide.md`.

**Planning/review prompt:**

> Review the local CAD + Grad-CAM prototype specification (`src/bc_xai/infer.py`, `UD22`). Confirm strict startup SHA-256 checks, exact numerical & Grad-CAM parity against `EVAL####`/`XAIA####`, structured error handling, non-clinical disclaimer, and interface stability for the optional `STEP-048–050` web layer.

**Implementation prompt:**

> Finalize `src/bc_xai/infer.py`, thin `13_Automation/run_cad_prototype.py`, `tests/test_prototype.py`, and `12_Documentation/prototype_guide.md` inside `environment/model/`. Run parity and failure-contract tests on permitted fixtures and save actual check outputs; never modify preprocessing, thresholds, or Grad-CAM normalization for visual appeal.

**Human-only actions and decisions:** Researchers ratify `UD22` local interface and disclosure-reviewed sample inputs; radiologist/clinical advisor (where engaged) checks overlay legibility and disclaimer clarity.

**Version-control/artifact expectations:** Commit `src/bc_xai/infer.py`, CLI, tests, `prototype_guide.md`, and parity report; keep model weights and sample mammograms in approved Tier-2/Tier-3 storage (never committed raw).

**Documentation updates:** `12_Documentation/prototype_guide.md`, `decisions.csv` (`UD22`), `model_registry.csv` (export parity pointer), and `dashboard.md`.

**Verification checklist:**

- [ ] Startup aborts immediately on tampered `MODEL`, `PP`, calibrator, or `label_map.json` SHA-256 hash.
- [ ] Probabilities and Grad-CAM heatmaps match `EVAL####`/`XAIA####` within approved tolerance.
- [ ] Corrupt, unsupported, missing-weight, and invalid-input error paths verified via `pytest`.
- [ ] Explicit research-only CAD disclaimer included in structured JSON and rendered overlay outputs.

**Common mistakes:** Tweaking Grad-CAM color clipping or decision threshold in the prototype for prettier demos; duplicating preprocessing outside `src/bc_xai/preprocess/`; presenting calibrated Malignant probability as definitive diagnosis.

**Recovery procedure:** Remove divergent prototype logic, call frozen `src/bc_xai/` functions unchanged, register/evaluate any materially altered export as a distinct `MODEL####`, and re-run parity checks.

**Definition of Done:** Tested, hash-verified local research CAD + Grad-CAM prototype reproduces exact evaluated predictions and heatmaps with documented error handling and limitations. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-039](#step-039); if `UD25` adopts the conditional defense web demo, the parallel S16 branch may start at [STEP-048](#step-048).

---

<a id="step-039"></a>
## STEP-039 — Perform clean-environment reproducibility audit and complete CLAIM / TRIPOD+AI checklists (G14)

**Objective:** Independently verify that a fresh environment built strictly from recorded lockfiles and instructions reproduces frozen metrics, statistics, quantitative XAI scores, and representative figures, complete full CLAIM 2024 & TRIPOD+AI checklists (`T26`), and pass `G14`.

**Why this step exists:** Q1 medical imaging journals increasingly enforce CLAIM and TRIPOD+AI checklists and require verified end-to-end code/data/artifact reproducibility prior to peer review.

**Governing section references:** [OS §8](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS §14](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-038` prototype complete; `G12–G13` current `PASS`; `UD23` reproducibility level and numeric tolerances ratified; clean authorized compute environment available.

**Estimated difficulty and time (provisional):** Hard; 5–8 hours active audit plus clean-install and replay compute time (plus single-seed retrain time if adopted under `UD23`).

**Parallelizable:** Drafting CLAIM 2024 & TRIPOD+AI item mappings (`T26`) can proceed in parallel while the fresh environment installs and replays `EVAL`/`STAT`/`XAIA`.

**Inputs:** `environment/data/` & `environment/model/` lockfiles, `12_Documentation/installation.md` & `pipeline.md`, Tier-2/Tier-3 artifact manifests & SHA-256 digests, `freeze_manifest.json`, `T25` & `T26` templates, and `UD23`.

**Expected outputs:** Verified `12_Documentation/reproduce.md` (exact step-by-step replay commands), `12_Documentation/reproducibility_audit.md` (`T25`, fresh-environment logs, hash checks, predicted vs observed deltas, achieved reproducibility level), completed item-by-item `12_Documentation/claim_tripod_checklist.md` (`T26`), lawful data/code/weight availability draft, `DEC####` (`UD23`), and `G14` assessment.

**Repository/file changes:** Create `12_Documentation/{reproduce.md,reproducibility_audit.md,claim_tripod_checklist.md,data_access_instructions.md}`, `DEC####` (`UD23`), and `01_Project_Management/reviews/G14_assessment_<date>.md`; update `decisions.csv` and `gates.csv`.

**Execution procedure:**

1. Provision a genuinely clean authorized directory and virtual/conda/container environment using **only** `12_Documentation/installation.md` and `environment/{data,model}/` lockfiles (zero reliance on hidden developer paths, cached notebooks, or manual state).
2. Retrieve `REL####`, `LBL####`, frozen `MODEL####`/`CKPT####`, calibrators, and `XAIP####` strictly by recorded manifest locators and verify 100% SHA-256 hash agreement.
3. Replay locked internal + external test inference, `STEP-034` classification/calibration/DeLong/McNemar metrics, `STEP-035` Grad-CAM faithfulness/sanity/ROI-localization audits, and `STEP-038` prototype checks via documented CLI commands; compare regenerated numbers against archived `EVAL`/`STAT`/`XAIA` outputs within `UD23` predeclared tolerances. (If full single-seed retraining check was adopted in `UD23`, execute and record hardware-tolerance comparison separately.)
4. Complete every single line item of the **CLAIM 2024** and **TRIPOD+AI** checklists (`T26`) pointing each item to its concrete repository artifact/gate evidence (marking genuinely non-applicable items with explicit rationale, never blank!).
5. Write lawful external reproduction instructions (`data_access_instructions.md`, explaining exactly how an external reviewer obtains credentialed/public datasets), record honest reproducibility boundaries, and perform itemized `G14` assessment.

**Planning/review prompt:**

> Audit `reproducibility_audit.md` and `claim_tripod_checklist.md` against `G14` and Q1 journal standards. Identify any missing CLAIM/TRIPOD+AI item, hidden environment dependency, unverified artifact hash, or unexplained delta between archived and replayed metrics/XAI scores.

**Implementation prompt:**

> Execute the clean-environment reproduction strictly from `12_Documentation/reproduce.md`, capture exact CLI outputs and SHA-256 diffs into `reproducibility_audit.md`, verify registry foreign keys via `validate_registries.py`, and save completed `claim_tripod_checklist.md` without patching archived numbers.

**Human-only actions and decisions:** Reproduction reviewer independently inspects clean-run logs, tolerance compliance, and CLAIM/TRIPOD+AI checklists; supervisor ratifies `UD23` availability statements and signs `G14`.

**Version-control/artifact expectations:** Commit `reproduce.md`, `reproducibility_audit.md`, `claim_tripod_checklist.md`, `data_access_instructions.md`, and `G14` audit; store fresh-run verification artifacts in Tier-3 storage.

**Documentation updates:** `12_Documentation/`, `decisions.csv` (`UD23`), `gates.csv` (`G14`), and `dashboard.md`.

**Verification checklist:**

- [ ] Fresh environment built strictly from lockfiles and `installation.md` without manual hacks.
- [ ] All retrieved parent/model/calibrator/manifest SHA-256 checksums match archived records.
- [ ] Replayed metrics, calibration, DeLong/McNemar stats, and quantitative XAI scores match within `UD23` tolerances.
- [ ] 100% of CLAIM 2024 and TRIPOD+AI checklist items mapped to real repository evidence (`T26`).
- [ ] Declared reproduction level (replay vs retrain) and external access limits stated honestly; `G14 PASS` signed.

**Common mistakes:** Running the audit inside the dirty development conda env; claiming "100% bitwise training determinism" without running a retrain check; ticking CLAIM checklist boxes without linking exact evidence paths.

**Recovery procedure:** Fix missing dependencies, broken CLI paths, or unaddressed CLAIM items via versioned fixes, re-run affected audits cleanly, and reassess `G14` (plus `G12–G13` if any scientific calculation changed).

**Definition of Done:** `G14 PASS` proving clean-environment reproducibility and complete CLAIM/TRIPOD+AI audit readiness for writing and conditional web deployment. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-040](#step-040)

---

<a id="step-040"></a>
## STEP-040 — Build evidence-first writing map and dual-track FYDP thesis + Q1 journal submission plan

**Objective:** Construct one unified claim-to-evidence map linking verified registries to both the DIU FYDP Thesis and the target Q1 journal manuscript, finalizing formatting, authorship, and publication obligations (`UD02`).

**Why this step exists:** Mapping every planned paragraph, table, and figure to verified IDs before writing eliminates unsupported novelty claims, ensures zero divergence between thesis and journal numbers, and aligns structure with exact DIU and Q1 journal instructions.

**Governing section references:** [OS §3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §14](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-039` complete; `G03` and `G12–G14` current `PASS`; actual DIU FYDP thesis template/deadlines and candidate Q1 journal author guidelines retrieved.

**Estimated difficulty and time (provisional):** Moderate; 3–5 hours plus author/supervisor alignment.

**Parallelizable:** Collecting institutional/journal guidelines and populating `writing_registry.csv` evidence links can proceed concurrently before joint sign-off.

**Inputs:** Approved O1–O6 & RQs (`G03`), `claims.csv`, `EVAL`/`XAIA`/`STAT` reports, `claim_tripod_checklist.md`, DIU FYDP thesis guidelines, candidate Q1 journal Instructions for Authors, and `UD02`.

**Expected outputs:** Ratified `11_Writing/writing_plan.md`, populated `11_Writing/writing_registry.csv` (`WR####` for every thesis chapter and Q1 paper section), confirmed target Q1 journal selection & formatting specs (or explicit deferral pathway), written authorship/CRediT contribution agreement, and `DEC####` finalizing `UD02`.

**Repository/file changes:** Populate `11_Writing/writing_registry.csv`, create `11_Writing/writing_plan.md`, `11_Writing/thesis/format_requirements.md`, `11_Writing/paper/venue_requirements.md`, and `DEC####` (`UD02`).

**Execution procedure:**

1. Collect verbatim DIU CSE FYDP thesis formatting guidelines, cover/declaration templates, deadlines, similarity policy, and defense requirements.
2. Finalize target Q1 journal choice (`UD02`, e.g., *Computers in Biology and Medicine*, *Medical Image Analysis*, *IEEE TMI*, *Radiology: Artificial Intelligence*, *Scientific Reports*, *Expert Systems with Applications*) verifying exact Aims & Scope fit, word/figure limits, reference style, CLAIM/TRIPOD+AI supplement requirements, ethics/data/code availability mandates, and CRediT authorship order.
3. Map every thesis chapter (`WR####`, `Document = thesis`) and every concise Q1 manuscript section (`WR####`, `Document = paper`) strictly to verified `CLAIM`, `P`, `DS`/`LBL`/`SPLIT`/`PP`, `EXP`, `EVAL`, `XAIA`, `STAT`, and planned `FIG`/`TAB` IDs from the single canonical evidence base.
4. Confirm exact publication obligation pathway (`UD02`): full Q1 submission track vs approved deferral disposition—never assuming journal acceptance is required for `G16`.

**Planning/review prompt:**

> Audit `11_Writing/writing_plan.md` and `writing_registry.csv` against O1–O6, `claims.csv`, and `claim_tripod_checklist.md`. Flag any planned section lacking verified evidence, any conflicting thesis vs paper framing, or any journal requirement (e.g., blinded review, graphical abstract, highlights) overlooked.

**Implementation prompt:**

> Documentation only: save `writing_plan.md`, populated `writing_registry.csv`, actual DIU and Q1 journal requirement records, and `DEC####` (`UD02`) linked to canonical `02_Literature/references.bib`. Never fabricate section evidence or copy unverified citations.

**Human-only actions and decisions:** Researchers and supervisors ratify `UD02` (authorship order, CRediT roles, DIU thesis schedule, target Q1 journal, and paper submission obligation/disposition).

**Version-control/artifact expectations:** Commit writing plan, registries, and venue checklists; keep private authorship or editorial correspondence appropriately controlled.

**Documentation updates:** `11_Writing/writing_registry.csv`, `writing_plan.md`, `decisions.csv` (`UD02`), and `dashboard.md`.

**Verification checklist:**

- [ ] Every planned thesis chapter and Q1 paper section resolves to verified `CLAIM`/`EVAL`/`XAIA`/`STAT` IDs.
- [ ] Verbatim DIU thesis instructions and target Q1 journal guidelines saved with exact formatting/checklist rules.
- [ ] Both thesis and Q1 manuscript share canonical `02_Literature/references.bib` (zero parallel conflicting `.bib` files).
- [ ] Authorship order, CRediT roles, and paper obligation/disposition ratified under `UD02`.

**Common mistakes:** Maintaining separate conflicting `.bib` files for thesis and paper; drafting before verifying journal word/figure caps and CLAIM supplement requirements; promising clinical superiority not supported by `EVAL`/`XAIA`.

**Recovery procedure:** Reconcile discrepancies with supervisors, remove any unsupported planned section claim, and update `writing_registry.csv` before drafting.

**Definition of Done:** Approved dual-track evidence-first writing map and ratified `UD02` submission/authorship plan ready for thesis drafting. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-041](#step-041)

---

<a id="step-041"></a>
## STEP-041 — Draft complete FYDP thesis chapters from realized evidence

**Objective:** Author the complete, evidence-grounded DIU FYDP thesis covering introduction, verified literature/gap assessment, mammography datasets/labels/splits, preprocessing/transfer learning/XAI methods, complete results, error/clinical-alignment analysis, local CAD prototype (plus conditional web demo system description if adopted), limitations, and conclusions.

**Why this step exists:** The submitted thesis must accurately report realized methods, audited counts, negative/ablation findings, quantitative XAI outcomes, and honest clinical boundaries rather than recycling preliminary proposal prose.

**Governing section references:** [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-040` approved `writing_plan.md` and `writing_registry.csv`; `G03`, `G12–G14` current `PASS`; DIU formatting template ready.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours per chapter session, repeated across all chapters (total provisional).

**Parallelizable:** Independent chapters (e.g., Literature Review, Dataset/Methodology, Results/XAI, Prototype/Discussion) may be drafted concurrently by Alzubair Ahamed and Md Riyadul Hasan against one shared glossary, `claims.csv`, and `references.bib`, followed by unified editorial harmonization.

**Inputs:** `writing_plan.md`, `writing_registry.csv`, `T27` writing-unit template, `02_Literature/synthesis.md`, `DS`/`LBL`/`SPLIT`/`PP`/`REL` cards, `EXP`/`MODEL` cards, `EVAL`/`XAIA`/`STAT` reports, `error_review.md`/`limitations.md`, `prototype_guide.md`, `claim_tripod_checklist.md`, and `DEPLOY####` (if S16 adopted).

**Expected outputs:** Complete chapter drafts in `11_Writing/thesis/` (including front matter matching `RF01–RF04`, structured abstract from realized results, chapters 1–N, appendices with CLAIM/TRIPOD+AI & reproducibility commands, and canonical bibliography links), plus updated `writing_registry.csv`.

**Repository/file changes:** Create `11_Writing/thesis/` chapter files (`WR####`); update `11_Writing/writing_registry.csv` (`ReviewState = drafted`, `MissingEvidence` explicit).

**Execution procedure:**

1. Draft Front Matter & Chapter 1 (Introduction/Objectives/Scope): preserve verbatim approved title (`RF01`), CO/PO context (`RF04`), O1–O6 (`RF12`), Section 8 exclusions (`RF15`), and bounded motivation from verified epidemiology (`UD04`) without repeating refuted novelty exaggerations.
2. Draft Literature Review & Gap Verification: present PRISMA screening flow, verified direct mammography + XAI comparators (clearly segregated from quarantined histopathology/tabular studies per `UD04`), and transparent `G03` Q1 contribution framing.
3. Draft Materials & Methods from **realized** configs (never proposal future tense!): dataset provenance & DUA/ethics (`G04`), FFDM vs ROI & pathology/BI-RADS label + ROI-mask audit (`G05–G06`), connected-component patient splitting (`G07`), training-only preprocessing/augmentation (`G08`), resolved `UD13` transfer learning roster & two-stage schedule (`G09`), prospective `XAIP####` target layers & quantitative XAI metrics, validation-only threshold/calibration, and clustered bootstrap/DeLong/McNemar methodology.
4. Draft Results, Error Analysis & Prototype Chapters directly from `G12–G13` outputs: all 6 required report metrics + Q1 suite with 95% CIs, paired DeLong/McNemar p-values, raw vs calibrated ECE, internal vs zero-shot external performance, multi-seed variance, controlled ablations (including negative/null outcomes), quantitative XAI faithfulness/Adebayo sanity/ROI localization/stability tables, density/view/abnormality subgroups, FN/FP + shortcut taxonomy, blinded clinical-advisor review status (`UD18`), local CAD prototype (`STEP-038`), and conditional web showcase screenshots labeled strictly as illustrative system output (if S16 adopted).
5. Draft Discussion, Limitations, Conclusion, Abstract & Appendices: separate observed evidence from hypotheses, bind conclusions strictly to O1–O6 and non-clinical research-aid boundaries, and attach CLAIM/TRIPOD+AI checklist and reproduction instructions.

**Planning/review prompt:**

> Draft or review `WR####` strictly from its linked `CLAIM`/`P`/`EVAL`/`XAIA`/`STAT` artifacts. Convert any leftover proposal future tense to realized past tense matching actual configs, verify every clinical/novelty caveat, and mark any ungenerated figure/table cleanly as `[Asset pending: FIG####/TAB####]` rather than guessing numbers.

**Implementation prompt:**

> Documentation authoring: save source-grounded chapter files under `11_Writing/thesis/` referencing canonical `02_Literature/references.bib` citation keys and update `writing_registry.csv` with revision numbers and remaining asset dependencies.

**Human-only actions and decisions:** Researchers author and jointly harmonize all chapters; supervisor reviews scientific interpretation and contribution claims.

**Version-control/artifact expectations:** Commit coherent chapter milestones (`writing: draft thesis chapter X from verified EVAL/XAIA`); preserve version history cleanly.

**Documentation updates:** `11_Writing/writing_registry.csv`, `11_Writing/thesis/`, and `dashboard.md`.

**Verification checklist:**

- [ ] Every required DIU thesis chapter and appendix drafted at full academic depth.
- [ ] Realized methods match exact frozen configs, `DS`/`LBL`/`SPLIT`/`PP` counts, and `XAIP####` rules.
- [ ] All 6 required metrics, Q1 statistical/calibration/XAI findings, and negative/null results included honestly.
- [ ] Zero fabricated placeholder metrics, unverified citations, or unwarranted clinical-trial/deployment claims.

**Common mistakes:** Leaving future-tense title-proposal wording ("we will compare 5 CNNs") inside realized methods; forgetting to report a CNN architecture or ablation that underperformed; presenting demo screenshots as held-out evaluation proof.

**Recovery procedure:** Replace any unverified prose directly from canonical `EVAL`/`XAIA`/`STAT`/`P` records or trim unsupported claims cleanly; propagate terminology fixes consistently across all chapters.

**Definition of Done:** Complete, evidence-grounded FYDP thesis draft exists in `11_Writing/thesis/`, ready for reproducible asset generation and full citation/claim auditing. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-042](#step-042)

---

<a id="step-042"></a>
## STEP-042 — Generate reproducible figures/tables and verify every citation, number, and claim

**Objective:** Programmatically render all thesis and Q1 manuscript figures/tables (`FIG####`/`TAB####`) from frozen data, clear all visual mammogram plates for PHI/license compliance, and audit 100% of citations, numbers, and claims for cross-document consistency.

**Why this step exists:** Even flawless experiments fail Q1 peer review when plotted curves mismatch text tables, captions omit CI/p-value definitions, citations retain report anomalies (`RF18`), or mammogram plates leak unreviewed patient markers.

**Governing section references:** [OS §3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §14](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-041` complete thesis draft; frozen `EVAL`/`XAIA`/`STAT`/`P` source data; `UD06` figure-disclosure rights verified; `environment/model/` plotting tools ready.

**Estimated difficulty and time (provisional):** Hard; 5–8 hours across script generation, visual inspection, disclosure review, and citation/number audit.

**Parallelizable:** Automated figure/table rendering, bibliographic audit, and text-vs-table numeric cross-checking may run concurrently into one consolidated issue log.

**Inputs:** `11_Writing/thesis/` drafts, `02_Literature/references.bib`, `claims.csv`, immutable `EVAL`/`XAIA`/`STAT` CSVs & curve arrays, disclosure-reviewed sample mammograms + Grad-CAM maps, and `T23` asset template.

**Expected outputs:** High-resolution publication-grade figures (300+ DPI vector/PNG) and LaTeX/Markdown tables (`FIG####`/`TAB####` covering PRISMA flow, patient-split CONSORT flow, internal & external ROC/PR/calibration curves, confusion matrices, quantitative XAI faithfulness/Adebayo sanity/ROI localization plots, density/view/subtype subgroup heatmap, and disclosure-cleared qualitative Grad-CAM + ROI contour plate), populated `10_Figures_Tables/assets.csv` + `specs/`, and a zero-mismatch citation/numeric audit report.

**Repository/file changes:** Populate `10_Figures_Tables/{specs,data,rendered}/` and `assets.csv`; add plotting scripts in `13_Automation/generate_figures.py`; update `11_Writing/thesis/`, `claims.csv`, `writing_registry.csv`, and save `11_Writing/reviews/citation_claim_audit.md`.

**Execution procedure:**

1. Write versioned scripts (`13_Automation/generate_figures.py`) generating every `FIG####` and `TAB####` directly from immutable `EVAL`/`XAIA`/`STAT`/PRISMA/split source files (zero manual spreadsheet editing or hand-tweaking plot curves!), logging exact CLI commands, data SHA-256 hashes, and code commit in `specs/FIG####.md` (`T23`) and `assets.csv`.
2. Inspect every rendered asset visually for legible typography, colorblind-safe palettes (critical for Grad-CAM overlays!), labeled axes/units, exact CI/p-value/Holm-Bonferroni annotations, sample sizes ($n$), and publication DPI.
3. Conduct mandatory **PHI & License Disclosure Review** (`UD06`, §1.5) on every qualitative mammogram + Grad-CAM + ROI-contour visual plate (confirming zero burned-in patient names/dates/institution stamps and verified dataset permission to publish visual examples!).
4. Audit 100% of in-text citations against canonical publisher-verified `02_Literature/references.bib` (confirming zero residual Table 1.1 / `RF18` anomalies such as "Hassan et al. [10]" survive) and reconcile every single number, percentage, architecture name, split count, and p-value identically across abstract, text, tables, figures, and captions.

**Planning/review prompt:**

> Audit every rendered `FIG####`/`TAB####`, caption, and in-text citation in `11_Writing/thesis/`. Flag any numeric discrepancy between prose and tables, any missing 95% CI or sample denominator, any unverified reference key, any unreviewed mammogram image, or any Grad-CAM plate showing only cherry-picked successes.

**Implementation prompt:**

> Execute `13_Automation/generate_figures.py` inside `environment/model/` to build all `FIG####`/`TAB####` assets directly from archived CSVs/arrays, populate `10_Figures_Tables/assets.csv` + `T23` specs, run an automated citation/number consistency check, and save `11_Writing/reviews/citation_claim_audit.md`.

**Human-only actions and decisions:** Authors approve visual clarity and captions; data steward/clinical advisor signs off PHI/license disclosure on all qualitative mammogram plates; supervisor reviews claim boundaries.

**Version-control/artifact expectations:** Commit `generate_figures.py`, `T23` specs, `assets.csv`, safe aggregated plot CSVs, and disclosure-cleared rendered figures; keep unapproved raw visual plates strictly in Tier-3 storage.

**Documentation updates:** `10_Figures_Tables/assets.csv`, `02_Literature/claims.csv`, `11_Writing/writing_registry.csv`, and `citation_claim_audit.md`.

**Verification checklist:**

- [ ] Every `FIG####` and `TAB####` traces by SHA-256 and exact CLI command to frozen source data.
- [ ] Every qualitative mammogram + Grad-CAM plate includes balanced failure/success cases and passes PHI/license disclosure review.
- [ ] 100% of cited references verified against primary publisher records (`UD04` anomalies absent).
- [ ] Zero numeric, rounding, architecture-name, or p-value conflicts across abstract, text, tables, and figures.

**Common mistakes:** Manually editing a plotted bar or table digit in Illustrator/Word; omitting colorbars/scales on Grad-CAM overlays; publishing a dataset mammogram without verifying DUA image-reproduction rights; leaving `[Asset pending]` tags in captions.

**Recovery procedure:** Fix plotting script bugs, regenerate affected assets cleanly from frozen source data, repair mismatched numbers/citations everywhere, and re-run `citation_claim_audit.md`.

**Definition of Done:** All publication-grade figures, tables, citations, and empirical claims are programmatically generated, disclosure-cleared, and 100% internally consistent. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-043](#step-043)

---

<a id="step-043"></a>
## STEP-043 — Complete supervisor review, format/CLAIM audit, and pass G15 / thesis

**Objective:** Resolve all substantive supervisor and internal reviews on the complete FYDP thesis, verify DIU format/declaration compliance, confirm zero remaining `[Evidence pending]` placeholders, and pass the document-scoped **`G15 / thesis`** gate.

**Why this step exists:** Separating `G15 / thesis` cleanly from `G15 / paper` guarantees institutional thesis submission proceeds on schedule once verified without being blocked by external Q1 journal formatting or peer-review timelines.

**Governing section references:** [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-042` verified thesis & assets complete; `G03`, `G12–G14` current `PASS`; actual DIU thesis guidelines & similarity/declaration rules available.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours per revision round plus supervisor review turnaround (unknown).

**Parallelizable:** Editorial formatting, pagination, and cross-reference checks may run while awaiting supervisor feedback; final `G15 / thesis` sign-off is serialized.

**Inputs:** Complete compiled FYDP thesis draft + figures/tables, actual supervisor/co-supervisor review comments, `T28` review-response template, `claim_tripod_checklist.md`, and DIU submission checklist.

**Expected outputs:** Complete `11_Writing/reviews/thesis_review_responses.md` (`T28`), revised & fully compiled submission-ready thesis PDF with SHA-256 hash, DIU formatting/declaration/similarity compliance verification, and document-scoped **`G15 / thesis`** assessment (`EntityVersions = thesis_vX.Y.Z`). *(Q1 paper readiness is assessed independently in `STEP-045`.)*

**Repository/file changes:** Update `11_Writing/thesis/` final source & compiled PDF record, `11_Writing/reviews/thesis_review_responses.md`, `writing_registry.csv`, `gates.csv`, and `01_Project_Management/reviews/G15_thesis_assessment_<date>.md`.

**Execution procedure:**

1. Submit the verified `STEP-042` complete thesis draft to Supervisor (Israt Jahan) and Co-Supervisor (Ms Faiza Feroz); log every actual comment verbatim in `thesis_review_responses.md` (`T28`) with owner, action, changed section, and evidence ID (never fabricate comments from Page 11's blank lines!).
2. Apply all editorial and analytical revisions; if any supervisor critique requires new experiments or re-analysis, re-enter the gated workflow (`STEP-027–036`) under fresh IDs and re-verify `G12–G14` before continuing.
3. Compile the complete thesis document and inspect every rendered page: DIU cover page (`RF01–RF02`), certificates/declarations, TOC/List of Figures/List of Tables, rendered high-DPI figures & tables, bibliography formatting, appendices (CLAIM/TRIPOD+AI & reproducibility guide), and zero `[Evidence pending]` markers.
4. Perform institutional similarity/plagiarism check if required by DIU and verify compliance; obtain explicit co-author and supervisor authorization and record document-scoped **`G15 / thesis`** assessment in `gates.csv`.

**Planning/review prompt:**

> Audit the compiled FYDP thesis PDF and `thesis_review_responses.md` against `G15 / thesis` and DIU requirements. Confirm zero remaining `[Evidence pending]` markers, closed supervisor comments, intact `G03/G12–G14` lineage, and clear separation from `G15 / paper`.

**Implementation prompt:**

> Apply approved revisions, compile final submission-ready FYDP thesis PDF, compute its SHA-256 digest, update `writing_registry.csv`, and save `thesis_review_responses.md` and the un-signed-until-approved `G15_thesis_assessment_<date>.md`.

**Human-only actions and decisions:** Supervisor, co-supervisor, and both researchers review final compiled thesis and sign **`G15 / thesis`** authorization.

**Version-control/artifact expectations:** Commit final thesis text sources, review-response ledger, SHA-256 digest of compiled PDF, and `G15 / thesis` audit; preserve compiled PDF immutably in Tier-4 storage.

**Documentation updates:** `11_Writing/writing_registry.csv`, `thesis_review_responses.md`, `gates.csv` (`G15 / thesis`), and `dashboard.md`.

**Verification checklist:**

- [ ] 100% of actual supervisor/co-supervisor comments logged and resolved or formally accepted.
- [ ] Zero `[Evidence pending]` or `[Asset pending]` markers remain anywhere in compiled PDF.
- [ ] Every page, figure, table, equation, and reference rendered cleanly per DIU CSE format.
- [ ] Document-scoped `G15 / thesis PASS` signed by supervisor and authors (independent of `G15 / paper`).

**Common mistakes:** Marking `G15` generically without scoping `EntityVersions` to `thesis`; rushing submission before inspecting rendered PDF figures and page breaks; editing numbers during final formatting without re-verifying `EVAL`/`XAIA` alignment.

**Recovery procedure:** Keep `G15 / thesis FAIL`, fix failing formatting/evidence items at the owning step, recompile fresh PDF hash, and re-audit `G15 / thesis`.

**Definition of Done:** Document-scoped `G15 / thesis PASS` authorizing official DIU FYDP thesis submission. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-044](#step-044)

---

<a id="step-044"></a>
## STEP-044 — Submit the approved FYDP thesis and archive immutable submission files and receipt

**Objective:** Execute official DIU FYDP thesis submission using the exact `G15 / thesis`-approved file bundle and archive its immutable SHA-256 snapshot and institutional confirmation receipt.

**Why this step exists:** Generating a local PDF is not confirmed submission; preserving exact submitted bytes alongside institutional receipt prevents version confusion before defense and archival.

**Governing section references:** [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-043` complete; document-scoped `G15 / thesis PASS`; actual DIU CSE submission portal/process and signed declarations ready.

**Estimated difficulty and time (provisional):** Moderate; 1–3 hours plus institutional administrative confirmation.

**Parallelizable:** No for final submission upload; `STEP-045` Q1 manuscript adaptation and `STEP-046` archive preparation may begin on the locked evidence base.

**Inputs:** `G15 / thesis`-approved final thesis PDF & supplements, SHA-256 checksums, signed declarations, and `T30` submission template.

**Expected outputs:** Completed `11_Writing/thesis/submission.md` (`T30`), immutable submitted thesis snapshot in Tier-4 storage, exact submitted file SHA-256 hashes, and institutional receipt/acknowledgment evidence.

**Repository/file changes:** Create `11_Writing/thesis/submission.md`; store immutable submitted thesis bundle & receipt copy in Tier-4 storage; update `writing_registry.csv` and `dashboard.md`.

**Execution procedure:**

1. Verify SHA-256 hashes of the exact files staged for submission match the `G15 / thesis`-approved manifest verbatim; attach all required DIU forms, similarity report (if required), and supplementary appendices.
2. Have the authorized researcher submit through the official DIU CSE submission channel.
3. Capture and verify exact institutional receipt, submission timestamp, portal ID/confirmation email, and any pending defense/administrative items in `11_Writing/thesis/submission.md` (`T30`).
4. Mark the submitted thesis bundle strictly read-only; any post-defense thesis corrections create a new version (`thesis_v2_post_defense`) without overwriting the original submitted snapshot.

**Planning/review prompt:**

> Verify the thesis submission bundle against DIU CSE instructions and `G15 / thesis` hashes. Confirm exact separation between *ready*, *uploaded*, and *receipt-confirmed submitted* states.

**Implementation prompt:**

> Compute final submission SHA-256 manifests and save `11_Writing/thesis/submission.md` recording only actual submission confirmation supplied by the authorized submitter. Never fabricate a portal receipt or perform unauthorized external uploads.

**Human-only actions and decisions:** Authorized researchers perform institutional submission and execute any required physical/digital signatures alongside supervisors.

**Version-control/artifact expectations:** Commit safe `submission.md` metadata and SHA-256 manifest; archive exact immutable PDF and receipt in Tier-4 storage; tag verified Git commit (`thesis-submitted-v1.0`) only after receipt confirmation.

**Documentation updates:** `11_Writing/thesis/submission.md`, `writing_registry.csv`, `dashboard.md`, and pending post-defense notes.

**Verification checklist:**

- [ ] Submitted file SHA-256 hashes match `G15 / thesis PASS` artifact verbatim.
- [ ] Actual DIU receipt or written confirmation archived and referenced in `submission.md`.
- [ ] Submission date, destination, and exact status accurately distinguish submitted vs defended/accepted.
- [ ] Submitted bundle locked immutable; prior drafts preserved intact.

**Common mistakes:** Marking thesis submitted upon local PDF compilation; editing the submitted file silently after catching a typo instead of versioning a post-defense revision.

**Recovery procedure:** Resolve any institutional portal rejection cleanly, re-verify hashes, resubmit only as authorized, retain both submission records/receipts, and correct status immediately.

**Definition of Done:** Official FYDP thesis submission confirmed with immutable file hashes and verifiable institutional receipt. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-045](#step-045)

---

<a id="step-045"></a>
## STEP-045 — Prepare Q1 journal manuscript, pass G15 / paper, submit (or record disposition), and manage peer-review rebuttal

**Objective:** Adapt the frozen verified evidence base into a publication-grade Q1 journal manuscript complete with cover letter, highlights, CLAIM/TRIPOD+AI supplements, assess document-scoped **`G15 / paper`**, execute submission (or record a supervisor-approved deferral disposition), and govern structured peer-review revisions/rebuttals (`T29`).

**Why this step exists:** Elevating an FYDP to a Q1 journal requires tight scientific framing, strict compliance with journal formatting/reporting checklists, independent `G15 / paper` sign-off, and disciplined gated peer-review handling—while never making FYDP closure (`G16`) hostage to uncertain journal acceptance timelines.

**Governing section references:** [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS §14](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-044` thesis submission record (or concurrent after `STEP-042` verified assets); ratified `UD02` target Q1 journal & authorship plan; `G03`, `G12–G14` current `PASS`.

**Estimated difficulty and time (provisional):** Hard; 5–10 hours across manuscript condensing, cover-letter/supplement assembly, and `G15 / paper` audit, plus external peer-review revision cycles (unknown duration).

**Parallelizable:** Drafting concise manuscript sections, formatting high-DPI journal figures, and preparing cover letter/CLAIM supplements may run in parallel; co-author approval, `G15 / paper`, and portal submission are serialized.

**Inputs:** Verified thesis evidence & `FIG####`/`TAB####` assets, `02_Literature/references.bib`, `12_Documentation/claim_tripod_checklist.md`, `11_Writing/paper/venue_requirements.md` (`UD02`), `T29` Q1 cover/rebuttal template, and `T30` submission template.

**Expected outputs:** If submitting: concise Q1 manuscript conforming strictly to target journal format, structured cover letter & research highlights (`T29`), completed CLAIM & TRIPOD+AI submission supplements, ethics/data/code/CRediT declarations, independent **`G15 / paper`** assessment (`EntityVersions = paper_vX.Y.Z`), portal submission receipt (`11_Writing/paper/submission.md`), and initialized peer-review rebuttal tracker (`T29`). If deferred/not required at FYDP closure: supervisor-approved disposition `DEC####` preserving the manuscript package honestly without a fabricated `G15 / paper PASS`.

**Repository/file changes:** Create `11_Writing/paper/` (manuscript source, cover letter, highlights, supplements, `submission.md` or `disposition.md`, `reviews/rebuttal_R#.md`), `01_Project_Management/reviews/G15_paper_assessment_<date>.md` (when submitting), and update `writing_registry.csv`, `decisions.csv`, and `gates.csv`.

**Execution procedure:**

1. **Manuscript condensation:** Distill the verified evidence base into a tight Q1 journal structure (Structured Abstract, Introduction with verified Q1 gap, Methods covering datasets/labels/connected-component splitting/transfer learning/prospective XAI/calibration/DeLong-McNemar stats, Results with CIs/p-values/external validation/quantitative XAI/subgroups, Discussion & bounded Limitations, Conclusion, Declarations) without inflating novelty or adding unverified claims.
2. **Q1 submission package (`T29`):** Assemble target-journal-formatted figures/tables (exact DPI/font/file-type specs), completed **CLAIM 2024** and **TRIPOD+AI** checklists mapped to manuscript page/line numbers, structured **Cover Letter** (articulating Q1 novelty, scope fit, non-overlap, ethical/data compliance), research highlights / graphical abstract (if required), CRediT author contributions, competing-interest statement, and lawful code/data/weight availability statements.
3. **Independent `G15 / paper` gate:** Execute itemized **`G15 / paper`** assessment (`T24`) under a distinct `GATE####` AssessmentID in `gates.csv` verifying manuscript accuracy, 100% citation/number parity with `EVAL`/`XAIA`/`STAT`, checklist completion, journal compliance, and explicit sign-off from every co-author and supervisor. **Block journal submission until `G15 / paper PASS`.**
4. **Submission OR approved disposition:** Have the authorized corresponding author submit via the journal portal and archive exact submitted files, hashes, and manuscript tracking receipt in `11_Writing/paper/submission.md` (`T30`). *(Alternatively, if `UD02` defers journal submission post-FYDP, record a signed supervisor disposition `DEC####`—never label a deferral as `G15 / paper PASS` or "submitted"!)*
5. **Peer-review & rebuttal workflow (ongoing):** Upon receiving editor/reviewer decisions (`Major Revision`, `Minor Revision`, or `Reject & Resubmit`), log every comment verbatim in `11_Writing/paper/reviews/rebuttal_R#.md` (`T29`), route any reviewer-requested new experiment, ablation, XAI comparator, or external dataset strictly back through gated steps (`STEP-027–036` under fresh `EXP`/`EVAL`/`XAIA` IDs!), prepare tracked-changes manuscript + polite point-by-point rebuttal letter, re-verify `G15 / paper` for `R1`/`R2`, and archive every round immutably.

**Planning/review prompt:**

> Conduct a mock Q1 peer review (*IEEE TMI* / *Medical Image Analysis* / *Computers in Biology and Medicine* standard) of `11_Writing/paper/` alongside its cover letter and CLAIM/TRIPOD+AI supplements. Flag any residual novelty overstatement, missing statistical/calibration detail, XAI sanity caveat, formatting violation, or claim-to-evidence drift before `G15 / paper`.

**Implementation prompt:**

> Save journal-formatted manuscript sources, cover letter/highlights (`T29`), updated CLAIM/TRIPOD+AI page-mapped supplements, and citation/number consistency logs. Record real `G15 / paper` evidence and actual portal receipt (or signed deferral disposition) in `11_Writing/paper/submission.md`; never fabricate submission IDs or acceptance states.

**Human-only actions and decisions:** All co-authors and supervisors review and approve the Q1 manuscript, cover letter, CRediT roles, `G15 / paper`, and actual journal submission (or deferral disposition); corresponding author manages journal portal submissions and rebuttal correspondence.

**Version-control/artifact expectations:** Commit manuscript sources, cover letter, supplements, rebuttal logs, and safe submission metadata; store exact submitted PDFs, tracked-changes files, and confidential editorial decision letters appropriately in Tier-4 storage.

**Documentation updates:** `11_Writing/writing_registry.csv`, `11_Writing/paper/submission.md`, `gates.csv` (distinct `G15 / paper` AssessmentID), `decisions.csv` (if deferred), and `dashboard.md`.

**Verification checklist:**

- [ ] 100% of manuscript metrics, 95% CIs, p-values, XAI scores, and citations match frozen `EVAL`/`XAIA`/`STAT`/`references.bib`.
- [ ] CLAIM 2024 & TRIPOD+AI checklists, cover letter, declarations, and journal format rules satisfied.
- [ ] Independent `G15 / paper PASS` signed by all co-authors/supervisors prior to portal submission (OR signed deferral disposition recorded without fictitious PASS).
- [ ] Submission receipt clearly distinguished from journal acceptance; `T29` rebuttal workflow ready for peer review.

**Common mistakes:** Making FYDP completion (`G16`) wait on journal acceptance; submitting before every co-author approves the final PDF; running hasty unlogged "reviewer experiments" on the test set during R1 revision without re-entering gated `EXP`/`EVAL` discipline.

**Recovery procedure:** Repair rejected/flagged compliance gaps, re-verify `G15 / paper`, and for desk-rejections or revisions preserve complete version history and adapt cleanly to the next target journal under a new `DEC####` (`UD02`) and versioned manuscript.

**Definition of Done:** Approved Q1 publication obligation fulfilled via `G15 / paper PASS` + verified journal submission receipt (with active `T29` rebuttal readiness), OR via documented supervisor-approved deferral disposition without a fabricated PASS. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-046](#step-046)

---

<a id="step-046"></a>
## STEP-046 — Create tiered immutable release archives and verify restoration

**Objective:** Assemble the complete, license-compliant tiered archival release (`ARCH####`) preserving source code, environment locks, registries, verified models, evaluation/XAI/statistical evidence, thesis/paper submissions, and conditional web-demo records, and prove restoration via actual recovery tests (`UD24`, `UD28`).

**Why this step exists:** Research longevity and Q1 reviewer/audit requests years later require immutable, hash-indexed archives whose backups have actually been restored and verified rather than merely assumed intact.

**Governing section references:** [OS §8](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-044` thesis submission receipt and `STEP-045` Q1 paper receipt/disposition complete; `STEP-050` `G17` & `DEPLOY####` records (or `UD25` non-adoption disposition) complete; `UD24` (and `UD28` if applicable) release/license/retention decisions ratified; all scientific gates `G01–G15` current `PASS`.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours plus archive transfer and restoration verification time.

**Parallelizable:** Tier-1 (public/code subset), Tier-2 (restricted data/mask manifest), Tier-3 (model/checkpoint/prediction/XAI), and Tier-4 (submissions/receipts) inventories may be compiled concurrently before unified `ARCH####` packaging and restore testing.

**Inputs:** Full Git repository & tagged release commit, `environment/{data,model}/` locks, `DS`/`LBL`/`SPLIT`/`PP`/`REL` manifests, frozen `MODEL`/`CKPT`/calibrators, `EVAL`/`XAIA`/`STAT` outputs, `claim_tripod_checklist.md`, `11_Writing/` submission bundles & receipts, `16_Web_Demo/` `DEPLOY####` records (if S16 adopted), `T31` archive template, and `UD24`/`UD28`.

**Expected outputs:** Complete `15_Archive/archive_manifest.csv` (`ArchiveItemID`), `15_Archive/ARCH0001.md` (`T31`), verified Git release tag (`v1.0-fydp-q1-release`), segregated lawful public release package (e.g., code/configs/locks/scripts/CLAIM checklist — zero restricted mammograms or PHI!) vs restricted institutional archive, documented retention & ownership policy, and **actual restoration test log** proving recovery.

**Repository/file changes:** Populate `15_Archive/archive_manifest.csv` and `15_Archive/ARCH0001.md`; add approved root `LICENSE` only if ratified under `UD24`; write immutable archive bundles in Tier-4 storage.

**Execution procedure:**

1. Inventory 100% of final deliverables and parent dependencies across Tiers 1–4 with exact versions, SHA-256 digests, byte sizes, sensitivity classification, and verified license/DUA restrictions (`UD06`, `UD24`).
2. Strictly segregate **Public-Releasable Artifacts** (e.g., `src/bc_xai/`, `tests/`, `environment/`, YAML configs, aggregate non-PHI CSVs, plotting scripts, CLAIM/TRIPOD+AI checklist, `data_access_instructions.md`, and licensed model weights only if `UD06`/`UD24` permit!) from **Restricted Archival Artifacts** (raw/processed mammograms, ROI masks, patient linkage tables, private review overlays, signed DUAs). Never leak restricted data into public GitHub or Zenodo uploads!
3. Create immutable Tier-4 archival snapshots (`ARCH0001`), verify stable non-expiring storage locators, record any `UD28` post-defense web-demo takedown/freeze status, and tag the verified Git commit.
4. Execute an **actual end-to-end restoration test** into a clean temporary directory: pull source snapshot, verify checksums across representative manifests (`DS`/`LBL`/`SPLIT`/`REL`), restore frozen `MODEL####`/calibrator/predictions/metrics/XAI audit files and thesis/paper submission PDFs + receipts, and record exact restore outputs in `ARCH0001.md`.

**Planning/review prompt:**

> Audit `15_Archive/archive_manifest.csv` and `ARCH0001.md` against `UD06`, `UD24`, and `UD28`. Verify zero restricted mammograms, PHI, or credentials enter any public release package, zero expiring links serve as sole artifact pointers, and every restoration check was actually executed.

**Implementation prompt:**

> Generate `15_Archive/archive_manifest.csv` and `ARCH0001.md` with computed SHA-256 checksums and byte counts, execute the clean-directory restoration check across all four storage tiers, save restoration logs, and run `validate_registries.py`. Never overwrite an existing `ARCH####` snapshot.

**Human-only actions and decisions:** Researchers, data steward, and supervisor ratify `UD24` code license, public-vs-restricted archival boundaries, retention period, post-project custodian ownership, and `UD28` web-demo handover.

**Version-control/artifact expectations:** Commit `archive_manifest.csv`, `ARCH0001.md`, approved `LICENSE` (if adopted), and restoration summary; tag release commit; store large/restricted archives solely in Tier-4 durable storage.

**Documentation updates:** `15_Archive/archive_manifest.csv`, `ARCH0001.md`, `decisions.csv` (`UD24`, `UD28`), `CHANGELOG.md`, and `dashboard.md`.

**Verification checklist:**

- [ ] 100% of final source, environment, data/label/split/model/evaluation/XAI/writing/web deliverables hashed and indexed.
- [ ] Strict firewall verified between lawful public release subset and restricted medical-data archive.
- [ ] Actual restoration test executed across source, model, evaluation/XAI, and submission receipts with matching SHA-256 hashes.
- [ ] Post-project retention owner, storage locations, and any open Q1 peer-review tracking documented cleanly.

**Common mistakes:** Archiving only the final thesis PDF while losing training configs, `SPLIT####` manifests, calibrators, or XAI scripts; uploading raw public mammogram datasets to GitHub/Zenodo in violation of non-redistribution DUAs; assuming cloud links remain valid without testing restoration.

**Recovery procedure:** Retrieve missing artifacts from Tier-2/Tier-3 backups, replace unstable links with immutable versioned storage, re-run restoration test, append superseding archive record (`ARCH0002`), and retain full history.

**Definition of Done:** Complete, license-compliant, immutable tiered `ARCH####` release archived with verified restoration proof. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-047](#step-047)

---

<a id="step-047"></a>
## STEP-047 — Perform final project-completion audit and pass G16

**Objective:** Verify that every approved scientific, documentation, reporting, submission, archival, and conditional web-demo obligation holds current evidence, hand over ongoing stewardship, and pass `G16`.

**Why this step exists:** Closing a research project rigorously prevents unverified claims of completion and clearly distinguishes completed FYDP/Q1 submission obligations from non-blocking future work (such as pending journal peer review or future multi-center clinical trials).

**Governing section references:** [OS §1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §9](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-046` verified `ARCH####` complete; all prior gates `G01–G14` and `G15 / thesis` current `PASS`; `STEP-044` thesis submission receipt present; `STEP-045` Q1 paper submission receipt (`G15 / paper PASS`) OR approved deferral disposition present; `G17 PASS` (when `UD25` adopted) OR approved `UD25` non-adoption disposition present.

**Estimated difficulty and time (provisional):** Moderate to hard; 3–5 hours plus final supervisor sign-off.

**Parallelizable:** Automated registry foreign-key checks and deliverable inventory verification may run concurrently; final `G16` decision is serialized.

**Inputs:** Full `01_Project_Management/gates.csv` ledger, all 24 canonical CSV registries, `ARCH0001.md` & restoration proof, thesis/paper receipts or dispositions, `DEPLOY####`/`G17` or `UD25` disposition, and `T24` gate audit template.

**Expected outputs:** Final `01_Project_Management/reviews/project_completion_audit.md`, finalized `dashboard.md`, handover & stewardship memo (including any active Q1 peer-review tracking), and signed `G16` assessment.

**Repository/file changes:** Create `01_Project_Management/reviews/project_completion_audit.md` and `G16_assessment_<date>.md`; update `gates.csv`, `dashboard.md`, and append final audit pointer to `15_Archive/archive_manifest.csv`.

**Execution procedure:**

1. Run `13_Automation/validate_registries.py` across all 24 canonical CSV registries confirming zero broken foreign keys, zero unresolved blocking `UD` items, and zero `STALE` gates along the final artifact lineage.
2. Verify every required OS Section 13.2–13.3 deliverable against actual hashed files: `G01–G14` current `PASS` (including `G10 PASS` for every reported `EXP`), `G15 / thesis PASS` + `STEP-044` institutional receipt, `STEP-045` Q1 paper receipt (`G15 / paper PASS`) OR approved deferral disposition, `G17 PASS` + `UD28` lifecycle action (if `UD25` adopted) OR `UD25` non-adoption disposition, and `STEP-046` verified `ARCH####` restoration proof.
3. Confirm all conclusions honor `RF01`, O1–O6, and Section 8 exclusions (`RF15`), preserving failed/negative runs intact and never falsely asserting clinical validation or journal acceptance.
4. Record signed `G16` assessment with researchers and supervisor; log non-blocking post-closure responsibilities (e.g., Q1 peer-review rebuttal stewardship, post-defense demo takedown date under `UD28`).

**Planning/review prompt:**

> Conduct the final `G16` project-completion audit against OS §13. Verify every gate (`G01–G15`, plus `G17` if `UD25` adopted), every registry foreign key, submission receipts/dispositions, restoration proof, and epistemic honesty without treating high accuracy or journal acceptance as prerequisites.

**Implementation prompt:**

> Run full registry/hash cross-checks, compile `01_Project_Management/reviews/project_completion_audit.md` strictly from verified evidence paths, bind its hash into `15_Archive/archive_manifest.csv`, and record actual signed `G16` status in `gates.csv` and `dashboard.md`.

**Human-only actions and decisions:** Researchers (Alzubair Ahamed, Md Riyadul Hasan) and Supervisors (Israt Jahan, Ms Faiza Feroz) review completion evidence, accept handover, and sign `G16`.

**Version-control/artifact expectations:** Commit final completion audit, `gates.csv`, and `dashboard.md`; archive immutable final audit pointer into Tier-4 storage; never delete failed or negative experiment records.

**Documentation updates:** `project_completion_audit.md`, `gates.csv` (`G16`), `dashboard.md`, and `15_Archive/archive_manifest.csv`.

**Verification checklist:**

- [ ] All 24 canonical CSV registries pass foreign-key and hash integrity checks cleanly.
- [ ] All applicable prior gates (`G01–G15`, and `G17` if `UD25` adopted) hold current non-`STALE` `PASS`.
- [ ] Actual thesis submission receipt, Q1 paper receipt/disposition, web-demo record/disposition, and `ARCH####` restoration proof verified.
- [ ] `G16 PASS` signed by researchers and supervisor; zero clinical-trial or journal-acceptance fabrications.

**Common mistakes:** Treating completed planning documents as proof of project completion; ignoring a `STALE` gate after a late thesis revision; sweeping open blocking omissions under "Future Work."

**Recovery procedure:** Keep `G16 FAIL`, return to the owning step to close missing evidence or re-verify stale gates, update `ARCH####`, and repeat the completion audit.

**Definition of Done:** `G16 PASS` certifying complete, reproducible, lawfully archived fulfillment of all approved FYDP and Q1 research obligations. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** None for the main sequential chain. If `UD25` adopted the conditional defense web demo and Stage S16 is not yet finished, complete [STEP-048](#step-048)–[STEP-050](#step-050) (`G17`) prior to `STEP-046` archival and `G16`. Close the approved project cleanly; future clinical or multi-modal extensions require a new approved protocol.

---

<a id="step-048"></a>
## STEP-048 — [Conditional S16] Confirm defense web-demo scope, frozen best model, hosting platform, and privacy policy

**Objective:** Confirm whether the conditional FYDP defense hosted web showcase is adopted (`UD25`), lock the `G11`-frozen winning `MODEL####` + Grad-CAM config to host, compare hosting platforms (`UD26`), and approve privacy, sample-disclosure, and non-clinical disclaimer rules (`UD27–UD28`).

**Why this step exists:** `Title_defence_evaluation_report.pdf` excludes hospital/PACS deployment (`RF15`) while noting a future foundation for web clinical decision support (`RF13`). If the team and supervisor request a live defense web showcase (`UD25`), strict early governance ensures the exact evaluated model is served safely without PHI exposure or scope violations. *(If `UD25` declines hosting, record an approved non-adoption `DEC####` here and skip `STEP-049–050` cleanly.)*

**Governing section references:** [OS §1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §8.3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-08-3); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §11](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-038` local CAD + Grad-CAM prototype (`src/bc_xai/infer.py`) complete and parity-tested; `G11` freeze identifying final best `MODEL####`; `G12–G13 PASS`; optional non-medical hosting spike (synthetic image + generic CNN, zero research evidence) permitted any time after `G02`.

**Estimated difficulty and time (provisional):** Moderate; 3–5 hours plus supervisor/custodian approvals (plus 2–4 hours if running an optional hosting spike).

**Parallelizable:** Runs in parallel with `STEP-039–044` (reproducibility and thesis writing) once `STEP-038` exists.

**Inputs:** `G11` `freeze_manifest.json`, winning `MODEL####` card & export size/CPU latency from `EVAL####`/`XAIA####`, `STEP-038` `prototype_guide.md`, disclosure-cleared sample mammograms (`UD06`), defense date/window, budget, and `UD25–UD28`.

**Expected outputs:** Ratified `DEC####` records resolving `UD25–UD28` (or signed non-adoption disposition closing S16), `16_Web_Demo/hosted_model.md` binding exact `MODEL`/`EVAL`/`XAIA`/`PP`/`XAIP` hashes, `platform_decision.md` (`UD26`), `web_policy.md` (`UD27`), disclosure-cleared `samples_manifest.csv`, initialized header-only `deployment_registry.csv`, and defense-date back-planned schedule.

**Repository/file changes:** Create `16_Web_Demo/` (`README.md`, `deployment_registry.csv`, `hosted_model.md`, `platform_decision.md`, `web_policy.md`, `samples_manifest.csv`) and `DEC####` records (`UD25–UD28`) under `01_Project_Management/decision_log/`; update `decisions.csv`.

**Execution procedure:**

1. **Ratify `UD25` conditionality:** Obtain written supervisor confirmation of whether a hosted web showcase is required for the FYDP defense, defense date, availability window, and live-vs-fallback expectations. *(If declined, save signed non-adoption `DEC####` and exit S16 cleanly—feeding directly into `STEP-046` & `G16`.)*
2. **Bind the exact `G11`-frozen best model:** Copy winning `MODEL####`, export SHA-256, `PP####`, calibrator/threshold hashes, `XAIP####` Grad-CAM config, and locked `EVAL####`/`XAIA####` test metrics (Accuracy, Sensitivity, Specificity, F1, AUC-ROC, PR-AUC, ECE, faithfulness/EBPG) into `hosted_model.md`. Never re-rank by test score or prettier demo heatmaps; if a lighter CNN (e.g., MobileNetV2/EfficientNetB0) is required by CPU RAM limits, it MUST be a registered `G12`-evaluated `MODEL####` labeled honestly with its own metrics!
3. **Compare hosting platforms (`UD26`):** Evaluate candidate hosts (e.g., Hugging Face Spaces with Gradio/Streamlit, Render/Railway/Fly.io container host, university server, or VPS) on RAM/CPU latency for CNN forward + Grad-CAM backward pass, cold-start sleep behavior, HTTPS, secret storage, team-owned accounts, cost, and Docker container support (enabling offline fallback).
4. **Lock privacy, input policy & non-clinical disclaimer (`UD27`):** Recommend curated, license-permitted, PHI-screened sample mammograms only, plus optional in-memory-only uploads that are **never persisted to disk or logged**; set strict MIME/file-size/dimension caps, timeouts, scrubbed logs, and mandatory non-dismissible disclaimer (*"Research CAD Prototype Only — Not Approved for Clinical Diagnosis, Screening, or Hospital/PACS Use"*).
5. **Lock lifecycle & weight hosting rights (`UD28`):** Confirm pretrained/fine-tuned weight license permits host placement, designate post-defense action (keep/freeze/take down), owner, and defense-date freeze timeline.

**Planning/review prompt:**

> Using `freeze_manifest.json`, `MODEL####` card, `EVAL####`/`XAIA####` reports, and `prototype_guide.md`, draft the `UD25–UD28` decision package (`hosted_model.md`, `platform_decision.md`, `web_policy.md`). Verify strict alignment with Section 8's non-hospital/non-clinical-trial boundaries and flag any CPU memory/latency risk for running CNN + Grad-CAM live.

**Implementation prompt:**

> Documentation only: create `16_Web_Demo/` governance files and `UD25–UD28` decision records populated strictly from ratified hashes and approved choices. Leave unapproved items explicitly `Unresolved / Human Decision Required`; zero patient images in any hosting spike and zero deployment yet.

**Human-only actions and decisions:** Supervisor ratifies `UD25` (adopt vs decline) and `hosted_model.md`; researchers choose platform/budget (`UD26`); data steward and radiologist/clinical advisor approve `UD27` policy, bundled sample mammograms, and disclaimer; team/supervisor/steward settle `UD28` post-defense lifecycle.

**Version-control/artifact expectations:** Commit `16_Web_Demo/` policy/manifest records and `DEC####` files; keep sample image bytes in approved storage and never commit credentials, tokens, or model weight binaries.

**Documentation updates:** `decisions.csv` (`UD25–UD28`), `16_Web_Demo/README.md`, `risk_register.csv` (cold start, venue Wi-Fi, RAM limits), and `dashboard.md`.

**Verification checklist:**

- [ ] `UD25` formally ratified (if declined, S16 closes cleanly via disposition and skips `STEP-049–050`).
- [ ] Hosted `MODEL####` matches `G11` freeze (or registered `G12`-evaluated lighter variant labeled honestly) with exact `EVAL`/`XAIA` hashes.
- [ ] Platform choice supported by documented RAM/CPU Grad-CAM latency, HTTPS, and team-owned account terms (`UD26`).
- [ ] `UD27` privacy/no-storage policy, mandatory non-clinical disclaimer, and PHI/license clearance of every bundled sample approved.
- [ ] `UD28` weight-hosting rights, post-defense lifecycle, and defense-day freeze timeline recorded.

**Common mistakes:** Hosting an untracked model with higher test accuracy instead of the `G11`-frozen selection; choosing a free CPU tier that OOMs during Grad-CAM backpropagation; bundling public mammogram samples whose DUA prohibits web redistribution; omitting the non-clinical disclaimer.

**Recovery procedure:** If chosen tier cannot run the frozen CNN + Grad-CAM within latency/RAM limits, select a larger tier/host first before falling back to a registered, `G12`-evaluated lighter `MODEL####` labeled transparently; supersede `DEC####` cleanly on any change.

**Definition of Done:** `UD25–UD28` ratified with traceable `hosted_model.md`, approved hosting platform, disclosure-cleared samples, and strict research-only privacy policy (or approved `UD25` non-adoption disposition). Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-049](#step-049) (or skip to [STEP-046](#step-046) if `UD25` formally declined hosting).

---

<a id="step-049"></a>
## STEP-049 — [Conditional S16] Build thin containerized web app over frozen CAD + Grad-CAM path and verify parity

**Objective:** Build a thin containerized web application (`web/`) that imports the exact frozen `STEP-038` `src/bc_xai/infer.py` CAD + Grad-CAM entry point and prove numerical probability and heatmap parity within approved tolerances.

**Why this step exists:** Re-implementing mammogram resizing, polarity handling, threshold/calibration logic, or Grad-CAM inside web code silently serves a different model than the thesis reports; automated parity testing guarantees examiners see the exact evaluated system.

**Governing section references:** [OS §2](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §8.1](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §8.3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-08-3); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix A](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-048` complete with `UD25` adopted and `UD26–UD28` ratified; `STEP-038` `src/bc_xai/infer.py` and tests passing.

**Estimated difficulty and time (provisional):** Moderate to hard; 10–18 hours across UI/API, container build, security/input tests, and parity verification.

**Parallelizable:** UI layout, *"About This Model"* panel, and `Dockerfile` packaging can proceed concurrently; end-to-end containerized parity testing waits for full integration.

**Inputs:** `16_Web_Demo/{hosted_model.md,web_policy.md,samples_manifest.csv}`, frozen `MODEL####` export + calibrator + `PP####` + `XAIP####`, `src/bc_xai/infer.py`, and frozen `EVAL####`/`XAIA####` summary JSON.

**Expected outputs:** Thin `web/` app + API (curated sample selector + optional in-memory upload per `UD27`, side-by-side mammogram & interactive Grad-CAM overlay, calibrated Malignant probability & frozen-threshold label, provenance metadata, labeled **web response time**, *"About This Model"* page sourced from `EVAL`/`XAIA` JSON, persistent non-clinical disclaimer), `Dockerfile` + lockfile, web security/error tests, `16_Web_Demo/parity_checks/PARITY_<date>.md`, and `12_Documentation/web_demo_guide.md`.

**Repository/file changes:** Create `web/` (app, API, static UI, `Dockerfile`, pinned lock, `tests/`), `16_Web_Demo/parity_checks/PARITY_<date>.md`, and `12_Documentation/web_demo_guide.md`; fetch weights by pointer + SHA-256 at build/startup rather than committing binaries.

**Execution procedure:**

1. Implement `web/` using the `UD26`-approved framework (e.g., Gradio, Streamlit, or FastAPI + clean frontend) directly importing `src/bc_xai/infer.py` unchanged—prohibiting any duplicated DICOM/image preprocessing, calibration, threshold, or Grad-CAM logic.
2. Enforce startup SHA-256 verification of `MODEL####` export, calibrator, `PP####` state, and `label_map.json`; abort startup cleanly on any mismatch.
3. Build results view displaying: input mammogram alongside adjustable-opacity Grad-CAM overlay (and optional approved comparator toggle), calibrated Malignant probability & Benign/Malignant class at frozen threshold, `MODEL`/`PP`/`XAIP`/commit provenance, **web response time** (explicitly labeled as *not* the offline latency benchmark), *"About This Model"* page programmatically populated from frozen `EVAL`/`XAIA` JSON (including limitations and subgroup/sanity caveats!), and persistent non-clinical disclaimer.
4. Enforce `UD27` security & privacy guards: strict MIME/extension/byte-size/dimension caps, request timeouts, rate limits, strictly in-memory processing with zero upload persistence, scrubbed logs (no image bytes or uploaded filenames), and structured OS §8.1 error messages for corrupt/unsupported inputs.
5. Package inside a reproducible `Dockerfile`, run the **containerized parity check** comparing `web/` API probabilities, binary predictions, and raw Grad-CAM heatmap arrays against `STEP-038` CLI outputs on all disclosure-cleared samples within approved tolerance, save `PARITY_<date>.md`, and document exact offline local Docker run commands in `12_Documentation/web_demo_guide.md`.

**Planning/review prompt:**

> Review the `web/` design and parity test protocol against OS §8.3 and `UD27`. Verify zero duplicated preprocessing/Grad-CAM logic, startup SHA-256 enforcement, programmatic `EVAL`/`XAIA` About-page sourcing, zero upload storage, scrubbed logs, and exact numerical + heatmap parity tolerances.

**Implementation prompt:**

> Implement thin `web/` UI/API over `src/bc_xai/infer.py`, build `Dockerfile` with pinned dependencies, run web input-safety and containerized prediction+Grad-CAM parity tests against `STEP-038`, and save `PARITY_<date>.md` and `12_Documentation/web_demo_guide.md`. Never commit weights, secrets, or raw patient images.

**Human-only actions and decisions:** Radiologist/clinical advisor (where engaged) reviews Grad-CAM overlay readability and disclaimer wording; supervisor reviews *"About This Model"* metrics and limitations wording.

**Version-control/artifact expectations:** Commit `web/` source, `Dockerfile`, lockfiles, tests, `PARITY_<date>.md`, and `web_demo_guide.md`; keep weights/samples in approved artifact tiers and secrets exclusively in platform secret stores.

**Documentation updates:** `12_Documentation/web_demo_guide.md`, `16_Web_Demo/parity_checks/PARITY_<date>.md`, and `risk_register.csv`.

**Verification checklist:**

- [ ] Container refuses startup if model, calibrator, or `PP####` SHA-256 hash mismatches registry.
- [ ] Containerized API probabilities, labels, and Grad-CAM arrays match `STEP-038` CLI outputs within approved tolerance (`PARITY_<date>.md`).
- [ ] *"About This Model"* metrics populate directly from frozen `EVAL`/`XAIA` JSON; persistent non-clinical disclaimer always visible.
- [ ] Zero uploads written to disk; logs scrubbed of image bytes/filenames; corrupt/oversized inputs return clean errors.
- [ ] Local container runs offline cleanly using the exact command recorded in `web_demo_guide.md`.

**Common mistakes:** Copying resize/normalization code into `web/app.py`; normalizing Grad-CAM differently in the browser than in `src/bc_xai/xai/`; hardcoding metrics by hand; saving uploaded mammograms to `/tmp` without cleanup; labeling web latency as benchmark inference time.

**Recovery procedure:** Strip divergent web-side transforms immediately, re-wire directly to `src/bc_xai/infer.py`, rebuild container, and re-run parity checks until every sample clears tolerance.

**Definition of Done:** Containerized thin `web/` CAD + Grad-CAM showcase passes startup hash checks, prediction + heatmap parity against `STEP-038`, `UD27` privacy tests, and local offline container execution. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** [STEP-050](#step-050)

---

<a id="step-050"></a>
## STEP-050 — [Conditional S16] Deploy live HTTPS defense showcase, verify parity/fallback, rehearse, and pass G17

**Objective:** Deploy the parity-verified container over HTTPS on the `UD26` host, confirm live hosted parity & external-network smoke checks, verify an internet-independent offline fallback, rehearse with the supervisor, and pass `G17`.

**Why this step exists:** Cloud cold starts, container memory limits, missing platform secrets, or venue Wi-Fi drops frequently derail live thesis demos; rehearsed verification and a tested offline fallback guarantee an honest, resilient FYDP presentation.

**Governing section references:** [OS §8.3](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-08-3); [OS §10](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §13](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS §14](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix B](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-049` complete with passing local containerized parity; **`G14 PASS`** for the hosted model's reproducibility lineage; team-owned `UD26` platform account ready; `UD27–UD28` approved.

**Estimated difficulty and time (provisional):** Moderate; 4–8 hours for deployment, hosted parity/smoke checks, and fallback prep, plus 1–2 supervisor rehearsals and defense-day warm-up.

**Parallelizable:** Drafting `demo_runbook.md` (`T35`) and capturing illustrative screenshots/backup video may accompany deployment verification; final freeze and supervisor rehearsal are sequential.

**Inputs:** Parity-verified `web/` container (`STEP-049`), registered `MODEL####` export & hashes, `hosted_model.md`, `web_policy.md`, disclosure-cleared samples, defense date/venue info, and `T34`/`T35` templates.

**Expected outputs:** Live HTTPS defense showcase URL, `16_Web_Demo/DEPLOY0001.md` (`T34`) & `deployment_registry.csv` row, hosted parity & external-network smoke reports, tested internet-disabled offline container fallback, backup screen recording & screenshots (`FIG####` if cited as illustrative system output in thesis), `16_Web_Demo/demo_runbook.md` (`T35`), and signed `G17` assessment.

**Repository/file changes:** Create `16_Web_Demo/DEPLOY0001.md`, `16_Web_Demo/smoke_checks/SMOKE_<date>.md`, `16_Web_Demo/parity_checks/HOSTED_PARITY_<date>.md`, `16_Web_Demo/demo_runbook.md`, and `01_Project_Management/reviews/G17_assessment_<date>.md`; update `deployment_registry.csv`, `gates.csv`, and `10_Figures_Tables/assets.csv` (if thesis includes illustrative UI screenshots).

**Execution procedure:**

1. Deploy the `STEP-049` container to the team-owned `UD26` platform over HTTPS, configure secrets exclusively via the platform secret store, and verify container startup logs confirm SHA-256 pass on `MODEL`/`PP`/`calibrator`.
2. Execute **hosted parity** (comparing live HTTPS API probabilities and Grad-CAM outputs against `STEP-038` on all disclosure-cleared samples) and **external-network HTTPS smoke tests** (valid samples, corrupt file rejection, oversized file rejection, cold-start latency, peak RAM headroom).
3. Audit live host configuration against `UD27`: access mode, zero stored uploads, scrubbed logs, persistent non-clinical disclaimer, and exact `EVAL`/`XAIA`-sourced *"About This Model"* metrics.
4. Register immutable `DEPLOY0001` (`T34`) binding platform, HTTPS URL, Git commit, container image digest, `MODEL`/`PP`/`XAIP`/export hashes, parity/smoke paths, and freeze deployment prior to defense (any post-freeze edit requires a new `DEPLOY####` and fresh checks).
5. Test the **offline fallback** completely disconnected from Wi-Fi/internet on the presenter's laptop (local container run + short backup screen recording + static screenshots), write `demo_runbook.md` (`T35`), rehearse full defense walkthrough with Supervisor (Israt Jahan) & Co-Supervisor (Ms Faiza Feroz), and record itemized `G17` assessment.
6. On defense day, warm the live endpoint and log a pre-defense smoke check; after the defense, execute the `UD28` post-defense keep/freeze/takedown action and hand `DEPLOY####` + `G17` records to `STEP-046` archival.

**Planning/review prompt:**

> Audit live deployment readiness against every `G17` criterion: startup hash check, hosted prediction + Grad-CAM parity, external HTTPS smoke resilience, `UD27` privacy/no-storage compliance, internet-off fallback verification, `T35` runbook, and supervisor walkthrough evidence.

**Implementation prompt:**

> Deploy the `STEP-049` container, execute hosted parity and external HTTPS smoke scripts, archive actual logs into `16_Web_Demo/{parity_checks,smoke_checks}/`, register `DEPLOY0001.md` and `deployment_registry.csv`, write `demo_runbook.md`, and prepare `G17` audit evidence without marking `G17 PASS` before supervisor rehearsal sign-off.

**Human-only actions and decisions:** Deployment owner deploys via team-owned account; presenter verifies offline laptop fallback personally; supervisor attends full walkthrough rehearsal and signs `G17`; team executes post-defense `UD28` lifecycle decision.

**Version-control/artifact expectations:** Commit `DEPLOY0001.md`, `deployment_registry.csv`, parity/smoke reports, `demo_runbook.md`, and `G17` audit; tag deployed Git commit (`web-demo-v1.0`); store backup video/screenshots in Tier-3 storage; zero credentials in Git.

**Documentation updates:** `16_Web_Demo/deployment_registry.csv`, `demo_runbook.md`, `dashboard.md`, `gates.csv` (`G17`), and thesis system/prototype chapter screenshots (`FIG####` labeled strictly illustrative).

**Verification checklist:**

- [ ] Live HTTPS site serves hash-verified `G11`-frozen `MODEL####` + `PP####` + `XAIP####` (`G14 PASS` current).
- [ ] Hosted probability & Grad-CAM parity within tolerance; external HTTPS smoke, error-contract, and RAM/cold-start checks pass.
- [ ] Live privacy config verified against `UD27` (no stored uploads, scrubbed logs, persistent non-clinical disclaimer, cleared samples).
- [ ] Offline container fallback tested with Wi-Fi off; backup recording/screenshots stored.
- [ ] `T35` runbook rehearsed with supervisor; `G17 PASS` signed and ready for `STEP-046`/`G16`.

**Common mistakes:** Swapping in a different checkpoint the night before defense for prettier heatmaps; relying on a sleeping free tier without pre-defense warm-up; forgetting to test Docker fallback completely offline; claiming live demo screenshots are held-out test proof.

**Recovery procedure:** If live URL fails during defense, switch calmly to the tested offline container fallback (recording the presentation incident without touching scientific claims); for pre-defense bugs, fix under a fresh `DEPLOY0002` ID with renewed parity, smoke, and `G17` reassessment.

**Definition of Done:** `G17 PASS` certifying a live HTTPS, parity-verified, privacy-compliant, fallback-protected Grad-CAM CAD defense showcase ready for FYDP presentation and `STEP-046` archival. Universal DoD applies; this is a required future state, not a completed assessment.

**Next step:** Present at the FYDP defense; execute post-defense `UD28` action; archive `DEPLOY####` records in [STEP-046](#step-046) and confirm `G17` within [STEP-047](#step-047) (`G16`).

---

<a id="roadmap-self-review"></a>
# Final review — roadmap validation record

## Coverage and source fidelity

This 50-step blueprint implements every approved scientific commitment of `Title_defence_evaluation_report.pdf` verbatim: binary Benign vs Malignant classification of publicly available 2D mammogram images using transfer learning across pre-trained CNN architectures integrated with Explainable AI (Grad-CAM baseline and approved comparators), honoring Objectives O1–O6 (`RF12`), all 6 required metrics (`RF09`), and all 6 binding Section 8 exclusions (`RF15`).

Every source anomaly discovered through visual 11-page PDF inspection is preserved explicitly rather than silently smoothed away: the 5-vs-6-vs-7 candidate architecture discrepancy across report sections (`RF07`, resolved at `STEP-022` / `UD13`), the Table 1.1 handwritten brackets `[5]`–`[10]`, the SL 10 ("Hassan et al.") vs Reference `[10]` (Bazazeh & Shubair, 2016) mismatch, SL 5 survey mismatch, Ref `[9]` missing venue, uncited Refs `[11]`–`[12]`, non-mammogram BreakHis/histopathology/Wisconsin comparators (`RF17–RF18`, audited and quarantined at `STEP-007` / `UD04`), the unverified preliminary novelty claim (`RF16`, challenged via PRISMA review at `STEP-004–009` / `UD03`), the absence of any report-specified dataset or split ratio (`RF19`, resolved at `STEP-010–013` and `STEP-020`), and Page 11's blank comment lines bearing only a handwritten signature and `15/8/26` date (`RF20`, verified honestly at `STEP-001` / `UD01`).

## Dependency and recovery review

- **Two-phase bootstrap without circular dependencies:** `STEP-001` (`G01`) saves initial scope/decision logs before `STEP-002` creates the full tree and tests Phase-1 `environment/data/`; `STEP-003` (`G02`) validates all 24 canonical CSV registries and 35 blank templates (`T01–T35`). Phase-2 `environment/model/` locks cleanly at `STEP-023` without overwriting Phase-1 preprocessing provenance.
- **Literature before data; permissions before intake:** PRISMA novelty/anomaly testing (`G03`) precedes final dataset choice (`STEP-010`); written licenses/DUAs and institutional ethics/waiver determinations (`STEP-011`) strictly block raw intake (`STEP-012`) and mammography QC (`STEP-013` / `G04`).
- **Diagnostic label/ROI-mask verification & prospective XAI governance before splitting:** Stages S07–S08 (`G05–G06`) resolve FFDM-vs-ROI paradigm, pathology-vs-BI-RADS Benign/Malignant/Normal rules, verified ROI-mask alignment, and prospective `XAIP####` faithfulness/sanity/localization/stability protocols *before* touching splits or training.
- **Leakage prevention & sealed test custody:** Connected-component patient/laterality/view/ROI/duplicate grouping (`STEP-020` / `G07`) strictly precedes training-only preprocessing fitting (`STEP-021` / `G08`) and all training-only augmentation. Both internal held-out test and independent external validation cohorts stay sealed until `G11` (`STEP-032`), after multi-architecture benchmarking (`STEP-030`), controlled ablations & multi-seed runs (`STEP-031`), and validation-only threshold & calibration fitting (`STEP-032`).
- **Q1 quantitative + clinical + reproducibility rigor:** Locked inference (`STEP-033`) feeds parallel classification/calibration/paired-statistics (`STEP-034`: DeLong, McNemar, patient-clustered bootstrap 95% CIs, Holm-Bonferroni) and quantitative XAI (`STEP-035`: Deletion/Insertion/ROAD, Adebayo sanity checks, ROI Pointing Game/EBPG/IoU, stability) into `G12` (`STEP-036`), followed by density/view/subtype error analysis + blinded clinical-advisor review (`STEP-037` / `G13`), local CAD prototype (`STEP-038`), and clean-environment replay + CLAIM/TRIPOD+AI checklists (`STEP-039` / `G14`).
- **Document-scoped dual submission & conditional defense showcase:** `G15 / thesis` (`STEP-043`) → thesis submission (`STEP-044`) runs independently of Q1 journal submission & peer-review rebuttal (`STEP-045`, `G15 / paper`). Conditional Stage S16 (`STEP-048–050`, `G17`) runs *only* if ratified under `UD25`, wraps `STEP-038` unchanged with parity tests, enforces `G14 PASS` prior to live deployment, strictly respects Section 8 non-clinical exclusions, and feeds `STEP-046` archival and `G16` (`STEP-047`).

## Canonical cross-reference checklist

| Alignment check | Planning-document verification status |
|---|---|
| **Approved title & team identity** | Exact title (`RF01`), DIU CSE Summer 2026 metadata, Alzubair Ahamed (232-15-591), Md Riyadul Hasan (232-15-486), Israt Jahan, and Ms Faiza Feroz match `Title_defence_evaluation_report.pdf` p. 1 verbatim across both files |
| **Scope & exclusions** | 2D mammography Benign vs Malignant classification, transfer learning CNNs, Grad-CAM + quantitative XAI, Q1 statistical/calibration/external-validation rigor, CLAIM/TRIPOD+AI, conditional non-clinical S16 web showcase, and all 6 Section 8 exclusions aligned 100% |
| **Stages & steps** | 16 stages (`S01–S16`) aligned 1:1 to 50 unique contiguous steps (`STEP-001` through `STEP-050`) in OS Appendix C and Blueprint Stage Map |
| **Quality gates** | `G01–G17` share identical IDs, owning steps, PASS/FAIL criteria, and human reviewers with OS §13.2 (including document-scoped `G15 / thesis` & `G15 / paper` and conditional `G17`) |
| **Unresolved decisions** | `UD01–UD28` defined canonically in OS §1.6 and mapped to exact blocking milestones across `STEP-001`–`STEP-050` |
| **Canonical registries** | All 24 CSV registry paths and schemas reside authoritatively in OS Appendix B (including `label_registry.csv`, `xai_protocol_registry.csv`, `xai_audit_registry.csv`, and `statistical_comparisons.csv`) |
| **Templates** | `T01–T35` defined in OS §14.2, installed blank at `STEP-003`, and referenced consistently across owning steps |
| **20-field step completeness** | All 50 steps (`STEP-001`–`STEP-050`) include all 20 required labeled operational fields in exact canonical sequence with zero truncated placeholders |
| **Relative links & anchors** | Every cross-file link and internal `#anchor` verified programmatically across both planning documents |
| **Zero domain contamination** | Programmatic search confirmed zero residual unrelated reference-project concepts, detection-only metrics, or external-project team details across both documents (only the literal workspace template filenames appear inside OS Appendix F's cryptographic SHA-256 provenance block) |

## Verification scope and initial execution state

Programmatic and manual self-audits validate **planning-document completeness, structural fidelity, cross-reference integrity, and epistemic discipline only**. They do **not** certify acquired mammogram datasets, verified diagnostic labels, trained CNN checkpoints, passed XAI sanity checks, statistical significance, or passed scientific gates.

- **All execution steps (`STEP-001` through `STEP-050`):** `NOT STARTED`
- **All quality gates (`G01` through `G17`):** `NOT ASSESSED`
- **All unresolved decisions (`UD01` through `UD28`):** `Unresolved / Human Decision Required`

**Start execution:** [STEP-001](#step-001). **Governing policy authority:** [BC-XAI Research Operating System](./BC_XAI_RESEARCH_OPERATING_SYSTEM.md).

*End of BC-XAI Project Execution Blueprint — v1.0.0; 50 complete 20-field steps across 16 research stages.*

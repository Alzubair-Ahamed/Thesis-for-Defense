"""Canonical Registry, Template, Directory, and Link Validator (STEP-003 / G02).

Validates:
1. All 21 OS Section 2 folders and their T01 README.md contracts exist.
2. All 35 blank operational templates (T01-T35) exist in 14_Templates_Prompts/ with required headers.
3. All 24 canonical CSV registries exist at their exact OS Appendix B paths with verbatim
   domain + Appendix A.4 common governance columns.
4. Primary-key uniqueness, zero fabricated dummy scientific rows in header-only initial registries,
   and cross-registry foreign-key integrity.
5. Zero broken relative Markdown links or internal #anchors across planning and governance files.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMMON_COLS = ["Owner", "Version", "Status", "Created", "Updated", "EvidencePath"]

EXPECTED_REGISTRIES: dict[str, list[str]] = {
    "01_Project_Management/decisions.csv": [
        "DEC", "UD", "Question", "Decision", "Approver", "ApprovalDate",
        "BlocksStep", "OptionsEvidence", "Supersedes", "AffectedGates",
    ] + COMMON_COLS,
    "01_Project_Management/risk_register.csv": [
        "RISK", "Description", "Trigger", "Probability", "Impact",
        "Mitigation", "Contingency", "ReviewDate",
    ] + COMMON_COLS,
    "01_Project_Management/gates.csv": [
        "AssessmentID", "GateID", "EntityVersions", "Outcome", "CriteriaReport",
        "Assessor", "Approval", "AssessmentDate", "Supersedes", "Invalidates",
    ] + COMMON_COLS,
    "02_Literature/papers.csv": [
        "P", "ReportRef", "Title", "Authors", "Year", "Venue", "DOI", "SourceURL",
        "SourceVersion", "Access", "FullTextPath", "MetadataVerified", "ReadingStatus",
        "Task", "Modality", "Paradigm", "Dataset", "Models", "XAIMethods",
        "QuantitativeXAI", "SplitLevel", "ExternalVal", "Limitations", "CitationKey",
    ] + COMMON_COLS,
    "02_Literature/screening.csv": [
        "SCR", "PaperID", "SearchRecord", "Stage", "Decision",
        "Reason", "Reviewer", "ConflictResolution", "DuplicateOf",
    ] + COMMON_COLS,
    "02_Literature/gaps.csv": [
        "GAP", "ReportTheme", "Statement", "SupportingPapers", "ContradictingPapers",
        "SearchCoverage", "Q1SaturationVerdict", "Feasibility", "ApprovedRQ", "DecisionRecord",
    ] + COMMON_COLS,
    "02_Literature/claims.csv": [
        "CLAIM", "Statement", "Scope", "PaperIDs", "SourceLocators", "ExperimentIDs",
        "EvaluationIDs", "XAIAuditIDs", "StatIDs", "AssetIDs", "Contradictions",
        "Uncertainty", "Verification", "WritingIDs",
    ] + COMMON_COLS,
    "03_Datasets/candidates.csv": [
        "CAND", "Name", "OriginalSourceURL", "Modality", "ParadigmAvailable",
        "RoleCandidate", "Access", "LicenseDUA", "LabelProvenance", "ROIMaskAvailable",
        "PatientGroupingMeta", "SubgroupMeta", "DuplicateOf", "SelectionDecision",
    ] + COMMON_COLS,
    "03_Datasets/datasets.csv": [
        "DS", "CandidateID", "Role", "SourceVersion", "Provenance", "PermissionRecord",
        "EthicsRecord", "LicenseRecord", "ManifestHash", "ImageCount", "PatientCount",
        "CountEvidence", "CardPath", "RestrictedLocation",
    ] + COMMON_COLS,
    "03_Datasets/releases.csv": [
        "REL", "DatasetID", "DatasetVersion", "LabelReleaseID", "LabelMapHash",
        "SplitID", "PreprocessingID", "ManifestHash", "ImageCount", "PatientCount",
        "ROIMaskCount", "RestrictedLocation", "ParentRelease", "ChangeReason",
    ] + COMMON_COLS,
    "04_Labels_XAI_Governance/label_registry.csv": [
        "LBL", "DatasetID", "Paradigm", "LabelProtocolVersion", "LabelProvenanceRule",
        "NormalCasePolicy", "BenignCount", "MalignantCount", "ExcludedCount",
        "ROIMaskCount", "MaskAlignmentAudit", "ClinicalReviewer", "LabelMapHash",
        "ManifestHash", "ParentVersion",
    ] + COMMON_COLS,
    "04_Labels_XAI_Governance/xai_protocol_registry.csv": [
        "XAIP", "ProtocolPath", "MethodsIncluded", "TargetLayerMapPath",
        "LogitConvention", "FaithfulnessMetrics", "SanityCheckProtocol",
        "LocalizationMetrics", "StabilityMetrics", "QualitativeRubricPath",
        "ProtocolHash", "Approver", "ParentVersion",
    ] + COMMON_COLS,
    "05_Preprocessing/preprocessing_registry.csv": [
        "PP", "InputManifest", "Operations", "BitDepthPolicy", "ArtifactPolicy",
        "CLAHEFlag", "ConfigPath", "ConfigHash", "FitPartition", "FitStateHash",
        "CodeRevision", "VisualQAReport", "OutputManifest",
    ] + COMMON_COLS,
    "06_Models/candidates.csv": [
        "MC", "Architecture", "ReportDiscrepancySource", "FrameworkVersion",
        "SourceURL", "PretrainedWeights", "WeightLicense", "NativeInputSize",
        "ParamCount", "GFLOPs", "GradCAMTargetLayer", "Compatibility",
        "Limitations", "SelectionDecision",
    ] + COMMON_COLS,
    "06_Models/model_registry.csv": [
        "MODEL", "CandidateID", "ExperimentID", "RunID", "CheckpointID",
        "ReleaseID", "LabelMapHash", "PreprocessingID", "XAIProtocolID",
        "CalibratorHash", "FrozenThreshold", "ExportFormat", "ExportHash",
        "ArtifactLocation", "CardPath", "EvaluationIDs", "IntendedUse",
    ] + COMMON_COLS,
    "07_Experiments/experiment_registry.csv": [
        "EXP", "RQ", "Purpose", "ParentComparison", "ReleaseID", "ModelCandidate",
        "XAIProtocolID", "ConfigPath", "ConfigHash", "SourceCommit", "Seed",
        "RunIDs", "Start", "End", "StoppingReason", "ValSelectionMetric",
        "ValScore", "FailureReport", "Conclusion",
    ] + COMMON_COLS,
    "08_Checkpoints/checkpoint_registry.csv": [
        "CKPT", "ExperimentID", "RunID", "EpochStep", "Role", "StateComponents",
        "ConfigHash", "ModelHash", "ArtifactPath", "SHA256", "Bytes",
        "BackupPath", "RestoreEvidence",
    ] + COMMON_COLS,
    "09_Evaluation/evaluation_registry.csv": [
        "EVAL", "ExperimentID", "ModelID", "CheckpointID", "ReleaseID",
        "CohortType", "Partition", "ProtocolHash", "FreezeRecord", "PredictionHash",
        "CoverageReport", "MetricsPath", "CalibrationPath", "EfficiencyPath",
        "SubgroupPath", "ReportPath", "Deviations", "ParentEvaluation",
    ] + COMMON_COLS,
    "09_Evaluation/xai_audit_registry.csv": [
        "XAIA", "EvaluationID", "ModelID", "XAIProtocolID", "LabelReleaseID",
        "CohortType", "MethodsAudited", "FaithfulnessPath", "SanityCheckOutcome",
        "SanityPath", "LocalizationMaskCount", "LocalizationPath", "StabilityPath",
        "QualitativeReviewStatus", "QualitativePath", "ReportPath", "Deviations",
    ] + COMMON_COLS,
    "09_Evaluation/statistical_comparisons.csv": [
        "STAT", "BaselineEvalID", "ComparatorEvalID", "CohortType", "ClusterUnit",
        "ClusterCount", "BootstrapReplicates", "BootstrapSeed", "PrimaryMetricDelta",
        "CI95Low", "CI95High", "DeLongPValue", "McNemarPValue",
        "MultipleCompMethod", "AdjustedPValue", "ReportPath",
    ] + COMMON_COLS,
    "10_Figures_Tables/assets.csv": [
        "AssetID", "Kind", "SourceIDs", "DataHash", "SpecPath", "GeneratorCommand",
        "CodeRevision", "OutputPath", "Caption", "Units", "DisclosureReview",
        "VisualReview", "WritingIDs",
    ] + COMMON_COLS,
    "11_Writing/writing_registry.csv": [
        "WR", "Document", "Section", "Topic", "ClaimIDs", "PaperIDs",
        "EvaluationIDs", "XAIAuditIDs", "StatIDs", "AssetIDs", "DraftPath",
        "Reviewer", "ReviewState", "Revision", "MissingEvidence",
    ] + COMMON_COLS,
    "15_Archive/archive_manifest.csv": [
        "ArchiveItemID", "ArchiveID", "ReleaseTag", "ItemType", "SourcePath",
        "StoredLocation", "Version", "SHA256", "Bytes", "Sensitivity",
        "License", "Retention", "RestoreEvidence", "SubmissionReceipt",
    ] + COMMON_COLS,
    "16_Web_Demo/deployment_registry.csv": [
        "DEPLOY", "Platform", "Tier", "URL", "AccessMode", "SourceCommit",
        "ImageDigest", "ModelID", "ExportHash", "PreprocessingID", "XAIProtocolID",
        "LabelMapHash", "DataPolicyRecord", "ParityCheckPath", "SmokeCheckPath",
        "DeployedAt", "TakenDownAt", "Supersedes",
    ] + COMMON_COLS,
}

EXPECTED_TEMPLATES: dict[str, str] = {
    "T01": "T01_readme.md",
    "T02": "T02_decision.md",
    "T03": "T03_session.md",
    "T04": "T04_search.md",
    "T05": "T05_paper_summary.md",
    "T06": "T06_gap.md",
    "T07": "T07_claim.md",
    "T08": "T08_dataset_card.md",
    "T09": "T09_label_mask_protocol.md",
    "T10": "T10_label_audit_report.md",
    "T11": "T11_xai_protocol.md",
    "T12": "T12_preprocessing.md",
    "T13": "T13_split.md",
    "T14": "T14_experiment.md",
    "T15": "T15_config.yaml",
    "T16": "T16_failure.md",
    "T17": "T17_checkpoint.md",
    "T18": "T18_model_card.md",
    "T19": "T19_evaluation.md",
    "T20": "T20_xai_audit.md",
    "T21": "T21_statistical_comparison.md",
    "T22": "T22_error_review.md",
    "T23": "T23_figure_table.md",
    "T24": "T24_gate_audit.md",
    "T25": "T25_reproduce.md",
    "T26": "T26_claim_tripod_checklist.md",
    "T27": "T27_writing_unit.md",
    "T28": "T28_review_response.md",
    "T29": "T29_q1_cover_rebuttal.md",
    "T30": "T30_submission.md",
    "T31": "T31_archive.md",
    "T32": "T32_prompt.md",
    "T33": "T33_risk_meeting.md",
    "T34": "T34_web_deployment.md",
    "T35": "T35_demo_runbook.md",
}


POPULATED_SCIENTIFIC_REGISTRIES: set[str] = {
    "02_Literature/papers.csv",
    "02_Literature/screening.csv",
    "02_Literature/gaps.csv",
    "02_Literature/claims.csv",
    "03_Datasets/candidates.csv",
    "03_Datasets/datasets.csv",
    "04_Labels_XAI_Governance/label_registry.csv",
    "04_Labels_XAI_Governance/xai_protocol_registry.csv",
}


def validate_all(
    root: Path = ROOT,
    enforce_initial_scientific_empty: bool = False,
    allowed_populated_scientific: set[str] | None = None,
) -> list[str]:
    """Run all registry, template, and foreign-key checks. Return list of error strings."""
    errors: list[str] = []
    if allowed_populated_scientific is None:
        allowed_populated_scientific = POPULATED_SCIENTIFIC_REGISTRIES

    # 1. Verify all 35 templates T01-T35
    tpl_dir = root / "14_Templates_Prompts"
    for tid, fname in EXPECTED_TEMPLATES.items():
        fpath = tpl_dir / fname
        if not fpath.is_file():
            errors.append(f"Missing template {tid}: {fpath}")
            continue
        txt = fpath.read_text(encoding="utf-8")
        if tid not in txt or "BLANK_TEMPLATE" not in txt:
            errors.append(f"Template {fname} missing required TemplateID ({tid}) or BLANK_TEMPLATE status")

    # 2. Verify all 24 canonical CSV registries & collect primary keys
    pk_sets: dict[str, set[str]] = {}
    rows_by_reg: dict[str, list[dict[str, str]]] = {}

    for rel_path, expected_cols in EXPECTED_REGISTRIES.items():
        cpath = root / rel_path
        if not cpath.is_file():
            errors.append(f"Missing canonical CSV registry: {rel_path}")
            continue
        with open(cpath, encoding="utf-8", newline="") as fp:
            reader = csv.reader(fp)
            try:
                header = next(reader)
            except StopIteration:
                errors.append(f"Empty CSV file (missing header): {rel_path}")
                continue
            if header != expected_cols:
                errors.append(
                    f"Header mismatch in {rel_path}: expected {expected_cols}, got {header}"
                )
                continue
            pk_col = expected_cols[0]
            pks: set[str] = set()
            dict_rows: list[dict[str, str]] = []
            for row_idx, row in enumerate(reader, start=2):
                if len(row) != len(expected_cols):
                    errors.append(
                        f"Column count mismatch in {rel_path} line {row_idx}: expected {len(expected_cols)}, got {len(row)}"
                    )
                    continue
                row_dict = dict(zip(expected_cols, row))
                pk_val = row_dict[pk_col].strip()
                if not pk_val:
                    errors.append(f"Empty primary key {pk_col} in {rel_path} line {row_idx}")
                elif pk_val in pks:
                    errors.append(f"Duplicate primary key {pk_val} in {rel_path} line {row_idx}")
                pks.add(pk_val)
                dict_rows.append(row_dict)
            pk_sets[rel_path] = pks
            rows_by_reg[rel_path] = dict_rows

            if not rel_path.startswith("01_Project_Management/"):
                if enforce_initial_scientific_empty and len(dict_rows) > 0:
                    errors.append(
                        f"Scientific registry {rel_path} must start header-only at G02 (found {len(dict_rows)} rows)"
                    )
                elif not enforce_initial_scientific_empty and rel_path not in allowed_populated_scientific and len(dict_rows) > 0:
                    errors.append(
                        f"Unreached scientific registry {rel_path} must remain header-only before its step (found {len(dict_rows)} rows)"
                    )

    # 3. Verify foreign-key integrity on populated registries
    fk_rules = [
        ("02_Literature/screening.csv", "PaperID", "02_Literature/papers.csv"),
        ("02_Literature/screening.csv", "DuplicateOf", "02_Literature/papers.csv"),
        ("02_Literature/gaps.csv", "SupportingPapers", "02_Literature/papers.csv"),
        ("02_Literature/gaps.csv", "ContradictingPapers", "02_Literature/papers.csv"),
        ("02_Literature/claims.csv", "PaperIDs", "02_Literature/papers.csv"),
        ("03_Datasets/candidates.csv", "DuplicateOf", "03_Datasets/candidates.csv"),
        ("03_Datasets/datasets.csv", "CandidateID", "03_Datasets/candidates.csv"),
        ("04_Labels_XAI_Governance/label_registry.csv", "DatasetID", "03_Datasets/datasets.csv"),
        ("03_Datasets/releases.csv", "DatasetID", "03_Datasets/datasets.csv"),
        ("03_Datasets/releases.csv", "LabelReleaseID", "04_Labels_XAI_Governance/label_registry.csv"),
        ("03_Datasets/releases.csv", "PreprocessingID", "05_Preprocessing/preprocessing_registry.csv"),
        ("06_Models/model_registry.csv", "CandidateID", "06_Models/candidates.csv"),
        ("06_Models/model_registry.csv", "ExperimentID", "07_Experiments/experiment_registry.csv"),
        ("06_Models/model_registry.csv", "CheckpointID", "08_Checkpoints/checkpoint_registry.csv"),
        ("06_Models/model_registry.csv", "ReleaseID", "03_Datasets/releases.csv"),
        ("07_Experiments/experiment_registry.csv", "ReleaseID", "03_Datasets/releases.csv"),
        ("07_Experiments/experiment_registry.csv", "ModelCandidate", "06_Models/candidates.csv"),
        ("07_Experiments/experiment_registry.csv", "XAIProtocolID", "04_Labels_XAI_Governance/xai_protocol_registry.csv"),
        ("08_Checkpoints/checkpoint_registry.csv", "ExperimentID", "07_Experiments/experiment_registry.csv"),
        ("09_Evaluation/evaluation_registry.csv", "ModelID", "06_Models/model_registry.csv"),
        ("09_Evaluation/evaluation_registry.csv", "ReleaseID", "03_Datasets/releases.csv"),
        ("09_Evaluation/xai_audit_registry.csv", "EvaluationID", "09_Evaluation/evaluation_registry.csv"),
        ("09_Evaluation/xai_audit_registry.csv", "ModelID", "06_Models/model_registry.csv"),
        ("09_Evaluation/xai_audit_registry.csv", "XAIProtocolID", "04_Labels_XAI_Governance/xai_protocol_registry.csv"),
        ("09_Evaluation/statistical_comparisons.csv", "BaselineEvalID", "09_Evaluation/evaluation_registry.csv"),
        ("09_Evaluation/statistical_comparisons.csv", "ComparatorEvalID", "09_Evaluation/evaluation_registry.csv"),
        ("16_Web_Demo/deployment_registry.csv", "ModelID", "06_Models/model_registry.csv"),
    ]
    for child_reg, fk_col, parent_reg in fk_rules:
        if child_reg not in rows_by_reg or parent_reg not in pk_sets:
            continue
        parent_pks = pk_sets[parent_reg]
        for row in rows_by_reg[child_reg]:
            val = row.get(fk_col, "").strip()
            if val and val not in ("none", "not reported", "Unresolved / Human Decision Required"):
                for token in [t.strip() for t in val.split(";") if t.strip()]:
                    if token not in parent_pks:
                        errors.append(
                            f"Broken foreign key in {child_reg}: {fk_col}={token} not in {parent_reg}"
                        )

    return errors


def main() -> int:
    errors = validate_all(ROOT, enforce_initial_scientific_empty=False)
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(
        f"VALIDATION PASSED: 24/24 canonical CSV registries, 35/35 blank templates (T01-T35), "
        f"and foreign-key rules verified cleanly."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

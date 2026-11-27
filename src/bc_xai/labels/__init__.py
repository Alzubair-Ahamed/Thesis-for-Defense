"""Diagnostic label verification, provenance harmonization, and ROI-mask audit utilities (Stage S08)."""

from bc_xai.labels.verify import (
    CohortAuditSummary,
    LabelCohortSpec,
    LabelRecord,
    audit_cohort_labels,
    default_label_specs,
    extract_bmcd_gt_channels,
    extract_dmid_rgba_mask,
    parse_mias_00readme_text,
    rasterize_cdd_cesm_shapes,
    rasterize_mias_circle,
    render_pilot_overlay_sheet,
    run_label_verification,
    sample_pilot_records,
)

__all__ = [
    "CohortAuditSummary",
    "LabelCohortSpec",
    "LabelRecord",
    "audit_cohort_labels",
    "default_label_specs",
    "extract_bmcd_gt_channels",
    "extract_dmid_rgba_mask",
    "parse_mias_00readme_text",
    "rasterize_cdd_cesm_shapes",
    "rasterize_mias_circle",
    "render_pilot_overlay_sheet",
    "run_label_verification",
    "sample_pilot_records",
]

"""Unit and Integration Tests for Canonical Registries and Templates (STEP-003 / G02)."""

from __future__ import annotations

import csv
import shutil
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "validate_registries", str(ROOT / "13_Automation" / "validate_registries.py")
)
assert _spec is not None and _spec.loader is not None
validator_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validator_mod)


def test_live_workspace_registries_and_templates_pass() -> None:
    """All 24 canonical CSV registries and 35 templates T01-T35 in workspace must pass validation."""
    errors = validator_mod.validate_all(ROOT, enforce_initial_scientific_empty=False)
    assert errors == [], f"Live workspace registry/template validation failed: {errors}"
    with open(ROOT / "02_Literature" / "papers.csv", encoding="utf-8", newline="") as fp:
        papers_rows = list(csv.DictReader(fp))
    with open(ROOT / "02_Literature" / "screening.csv", encoding="utf-8", newline="") as fp:
        screening_rows = list(csv.DictReader(fp))
    assert len(papers_rows) >= 62, "Expected Google Scholar unique papers registered in papers.csv"
    assert len(screening_rows) >= 96, "Expected Google Scholar screening & deduplication rows in screening.csv"


def test_validator_rejects_dummy_scientific_row_and_broken_fk(tmp_path: Path) -> None:
    """Validator must catch fabricated dummy rows at G02 and unresolved foreign keys."""
    for rel_path, cols in validator_mod.EXPECTED_REGISTRIES.items():
        p = tmp_path / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(cols)

    tpl_dir = tmp_path / "14_Templates_Prompts"
    tpl_dir.mkdir(parents=True, exist_ok=True)
    for tid, fname in validator_mod.EXPECTED_TEMPLATES.items():
        (tpl_dir / fname).write_text(f"# {tid}\nstatus: BLANK_TEMPLATE\n", encoding="utf-8")

    # Baseline clean synthetic workspace passes
    assert validator_mod.validate_all(tmp_path, enforce_initial_scientific_empty=True) == []

    # Inject a dummy scientific row in 03_Datasets/datasets.csv pointing to nonexistent CAND9999
    ds_cols = validator_mod.EXPECTED_REGISTRIES["03_Datasets/datasets.csv"]
    dummy_row = ["DS0001", "CAND9999"] + ["dummy"] * (len(ds_cols) - 2)
    with open(tmp_path / "03_Datasets/datasets.csv", "a", encoding="utf-8", newline="") as fp:
        csv.writer(fp).writerow(dummy_row)

    errs_initial = validator_mod.validate_all(tmp_path, enforce_initial_scientific_empty=True)
    assert any("must start header-only at G02" in e for e in errs_initial)
    assert any("Broken foreign key" in e and "CAND9999" in e for e in errs_initial)

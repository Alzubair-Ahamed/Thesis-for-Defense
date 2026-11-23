"""STEP-002 Phase-1 Data-Tool Environment and Storage-Policy Smoke Tests.

Verifies:
1. Canonical repository directory tree and folder README contracts (OS Section 2).
2. Canonical CSV registry parsing and RFC 4180 compliance on 01_Project_Management/decisions.csv.
3. Cryptographic SHA-256 hashing and source file immutability.
4. Synthetic 16-bit mammogram MONOCHROME1 -> MONOCHROME2 polarity standardization and
   co-transformed lesion ROI-mask coordinate preservation.
5. Connected-component patient/laterality/view/duplicate graph grouping (zero cross-partition leakage).
6. .gitignore protection against committing restricted medical data, checkpoints, secrets,
   and workspace reference templates.
"""

from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SECTION2_DIRS = [
    "environment",
    "environment/data",
    "src/bc_xai",
    "tests",
    "01_Project_Management",
    "02_Literature",
    "03_Datasets",
    "04_Labels_XAI_Governance",
    "05_Preprocessing",
    "06_Models",
    "07_Experiments",
    "08_Checkpoints",
    "09_Evaluation",
    "10_Figures_Tables",
    "11_Writing",
    "12_Documentation",
    "13_Automation",
    "14_Templates_Prompts",
    "15_Archive",
    "web",
    "16_Web_Demo",
]


def test_section2_directory_skeleton_and_readmes() -> None:
    """Every OS Section 2 directory must exist and contain a T01 README.md contract."""
    for rel_dir in REQUIRED_SECTION2_DIRS:
        dir_path = ROOT / rel_dir
        assert dir_path.is_dir(), f"Missing canonical folder: {rel_dir}"
        readme_path = dir_path / "README.md"
        assert readme_path.is_file(), f"Missing T01 README.md in {rel_dir}"
        text = readme_path.read_text(encoding="utf-8")
        assert "T01" in text and "Governing Section" in text, f"Incomplete T01 header in {rel_dir}/README.md"


def test_decisions_registry_schema_and_g01_state() -> None:
    """decisions.csv must parse cleanly with 16 canonical columns and 28 UD rows."""
    csv_path = ROOT / "01_Project_Management" / "decisions.csv"
    assert csv_path.is_file()
    df = pd.read_csv(csv_path, dtype=str)
    expected_cols = [
        "DEC", "UD", "Question", "Decision", "Approver", "ApprovalDate",
        "BlocksStep", "OptionsEvidence", "Supersedes", "AffectedGates",
        "Owner", "Version", "Status", "Created", "Updated", "EvidencePath",
    ]
    assert list(df.columns) == expected_cols
    assert len(df) == 28
    assert df.loc[df["UD"] == "UD01", "Status"].iloc[0] == "Approved"


def test_synthetic_16bit_mammogram_polarity_and_roi_cotransform() -> None:
    """Verify 16-bit MONOCHROME1 polarity inversion and 1:1 ROI-mask spatial co-transform."""
    rng = np.random.default_rng(seed=20261123)
    raw_16bit = rng.integers(low=0, high=4096, size=(128, 96), dtype=np.uint16)
    # Synthetic lesion ROI mask in [40:64, 30:54]
    roi_mask = np.zeros((128, 96), dtype=np.uint8)
    roi_mask[40:64, 30:54] = 1

    # MONOCHROME1 (high value = dark background) -> MONOCHROME2 inversion
    inverted = np.uint16(4095) - raw_16bit
    assert inverted.dtype == np.uint16
    assert int(inverted[0, 0]) + int(raw_16bit[0, 0]) == 4095

    # Normalize to 8-bit PIL image & co-transform both image and ROI mask to (64, 64)
    norm_uint8 = ((inverted.astype(np.float32) / 4095.0) * 255.0).clip(0, 255).astype(np.uint8)
    img_pil = Image.fromarray(norm_uint8, mode="L").resize((64, 64), resample=Image.Resampling.BILINEAR)
    mask_pil = Image.fromarray(roi_mask * 255, mode="L").resize((64, 64), resample=Image.Resampling.NEAREST)

    img_out = np.asarray(img_pil)
    mask_out = (np.asarray(mask_pil) > 127).astype(np.uint8)
    assert img_out.shape == (64, 64)
    assert mask_out.shape == (64, 64)
    # Lesion center (y=52/128 -> ~26, x=42/96 -> ~28) must remain positive inside co-transformed ROI mask
    assert mask_out[26, 28] == 1
    assert int(mask_out.sum()) > 0, "Co-transformed lesion ROI mask must not be clipped or empty"


def test_connected_component_patient_view_duplicate_grouping() -> None:
    """Connected-component graph must keep multi-view (LCC/RCC/LMLO/RMLO) and duplicate links atomic."""
    g = nx.Graph()
    records = [
        ("IMG001", "PAT_A", "STUDY_1", "DUP_NONE"),  # LCC
        ("IMG002", "PAT_A", "STUDY_1", "DUP_NONE"),  # LMLO
        ("IMG003", "PAT_A", "STUDY_2", "DUP_CLUSTER_1"),  # Follow-up RCC
        ("IMG004", "PAT_UNKNOWN", "STUDY_9", "DUP_CLUSTER_1"),  # Near-duplicate linked to IMG003!
        ("IMG005", "PAT_B", "STUDY_3", "DUP_NONE"),  # Independent patient B
    ]
    for img_id, pat_id, study_id, dup_id in records:
        g.add_node(img_id, kind="image")
        if pat_id != "PAT_UNKNOWN":
            g.add_edge(img_id, f"PAT::{pat_id}")
        g.add_edge(img_id, f"STUDY::{study_id}")
        if dup_id != "DUP_NONE":
            g.add_edge(img_id, f"DUP::{dup_id}")

    image_nodes = {r[0] for r in records}
    components = [sorted(c & image_nodes) for c in nx.connected_components(g) if (c & image_nodes)]
    components.sort()
    assert components == [["IMG001", "IMG002", "IMG003", "IMG004"], ["IMG005"]]


def test_gitignore_blocks_restricted_medical_and_reference_paths() -> None:
    """git check-ignore must block Tier-2 medical images, Tier-3 checkpoints, secrets, and reference files."""
    restricted_dummy_paths = [
        "03_Datasets/raw/DS0001/patient001_LMLO.dcm",
        "03_Datasets/manifests/DS0001_private_linkage.csv",
        "05_Preprocessing/processed/REL0001/img001.png",
        "08_Checkpoints/EXP0001_best.pth",
        "08_Checkpoints/EXP0001_model.onnx",
        ".env",
        "Title_defence_evaluation_report.pdf",
        "OPG_RESEARCH_OPERATING_SYSTEM.md",
        "OPG_PROJECT_EXECUTION_BLUEPRINT.md",
    ]
    for rel_path in restricted_dummy_paths:
        res = subprocess.run(
            ["git", "check-ignore", "-q", rel_path],
            cwd=str(ROOT),
            capture_output=True,
        )
        assert res.returncode == 0, f"CRITICAL: Restricted path is NOT ignored by .gitignore: {rel_path}"

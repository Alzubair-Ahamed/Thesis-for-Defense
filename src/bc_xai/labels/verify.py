"""Read-only STEP-016/017/018 diagnostic label harmonization & ROI-mask verifier (`T09 v1.0.0`).

Audits all five G04-approved clean mammography cohorts (`DS0001` MIAS, `DS0002` DMID,
`DS0003` CMMD, `DS0005` BMCD, `DS0006` CDD-CESM LE) strictly from raw metadata tables,
`DS####_private_linkage.csv`, and `STEP-013` QC ledgers without modifying raw files.

Enforces `T09 v1.0.0` rules:
- Whole-breast `FFDM` vs `SFM` paradigm isolation (`UD07`)
- Dual `Tier-A` Biopsy vs `Non-Malignant (Benign + Normal)` sub-tracks (`UD08`)
- Malignant dominance for multi-lesion scans and strict exclusion buckets
- Multi-primitive `CDD-CESM` VIA shapes, `DMID` `Pixel-level annotation/*.tif` contour fill
  (strictly banning corrupt `ROI Masks/*.tif`), `BMCD` `*_GT.jpg` color separation,
  and `MIAS` circular annotations (`UD09`)
- Stratified Tier-2 visual ROI-mask overlay plates and Tier-1 pseudonymous reporting.
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import math
import os
import random
import re
import zlib
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

import cv2
import numpy as np
import pandas as pd
import pydicom
from PIL import Image, ImageDraw, ImageOps

from bc_xai.data.inventory import sha256_text
from bc_xai.data.qc import DICOM_EXTENSIONS

DEFAULT_PILOT_SEED = 20261128

# Explicit cross-label conflicting patient tokens discovered in STEP-013 (`DS0003`).
CMMD_CONFLICT_PATIENTS = {"D1-0808", "D1-1292"}


@dataclass(frozen=True)
class LabelCohortSpec:
    """Locations required to harmonize and verify labels + ROI masks for one cohort."""

    dataset_id: str
    raw_dir: Path
    linkage_csv: Path
    qc_details_csv: Path | None = None
    display_name: str = ""


@dataclass
class LabelRecord:
    """Canonical per-image harmonized label & mask audit record (stored in Tier-2 CSV)."""

    ImageID: str
    DatasetID: str
    PatientGroupID: str
    SourceStem: str
    DispositionQC: str
    Paradigm: str
    BinaryTarget: str
    LabelClass: str
    LabelProvenanceTier: str
    SubTrackA_BiopsyEligible: bool
    SubTrackB_ScreeningEligible: bool
    LesionTrack_BenignVsMalignant: bool
    RawLabelTokens: str
    MultiLesionConflict: bool
    ViewPosition: str
    Laterality: str
    DensityACR: str
    MorphologyType: str
    BIRADSScore: str
    ClinicalConcStatus: str
    LocalizationEligible: bool
    MaskSourceType: str
    MaskStatus: str
    MaskWidth: int | None = None
    MaskHeight: int | None = None
    ImageWidth: int | None = None
    ImageHeight: int | None = None
    MaskForegroundPixels: int = 0
    MaskCoveragePct: float = 0.0
    MaskComponentCount: int = 0
    ExtraMaskTelemetry: str = ""
    AnomalyFlags: str = ""
    RawRelativePath: str = ""
    MaskRelativePath: str = ""


@dataclass
class CohortAuditSummary:
    """Tier-1-safe aggregate summary for one cohort (`pilot` or `full` audit)."""

    dataset_id: str
    display_name: str
    mode: str
    total_primary_acquired: int
    total_qc_retained: int
    total_audited: int
    binary_target_counts: dict[str, int]
    label_class_counts: dict[str, int]
    provenance_tier_counts: dict[str, int]
    subtrack_a_count: int
    subtrack_b_count: int
    lesion_track_count: int
    multi_lesion_conflict_count: int
    localization_eligible_count: int
    mask_status_counts: dict[str, int]
    concordance_counts: dict[str, int]
    anomaly_flag_counts: dict[str, int]
    arithmetic_closure_ok: bool
    discrepancies: list[dict[str, str]] = field(default_factory=list)
    tier2_labels_csv: str = ""
    tier2_overlay_png: str = ""


def _parse_max_birads(raw_val: Any) -> str:
    """Parse scalar or `$`-delimited multi-lesion BI-RADS strings to max numeric category."""
    if raw_val is None or (isinstance(raw_val, float) and math.isnan(raw_val)):
        return "not_reported"
    s = str(raw_val).strip()
    if not s or s.lower() in {"nan", "none", "not available"}:
        return "not_reported"
    nums = [int(m) for m in re.findall(r"\d+", s)]
    if nums:
        return str(max(nums))
    return s


def _normalize_view(raw_view: str) -> str:
    """Normalize mammogram view strings while preserving CC/MLO orientation."""
    v = raw_view.strip().upper()
    if not v:
        return "unknown"
    if "MLO" in v:
        return "MLO"
    if "CC" in v:
        return "CC"
    return v


def _infer_laterality_from_view_or_side(raw_val: str) -> str:
    """Infer L/R breast laterality conservatively from view or side text."""
    s = raw_val.strip().upper()
    if s in {"L", "LEFT"} or s.endswith("LT") or "_L_" in s:
        return "L"
    if s in {"R", "RIGHT"} or s.endswith("RT") or "_R_" in s:
        return "R"
    return "unknown"


def _load_image_hw(img_path: Path) -> tuple[int, int]:
    """Read native `(Height, Width)` without loading full pixel arrays where headers suffice."""
    ext = img_path.suffix.lower()
    if ext in DICOM_EXTENSIONS:
        ds = pydicom.dcmread(img_path, stop_before_pixels=True, specific_tags=["Rows", "Columns"])
        return int(ds.Rows), int(ds.Columns)
    with Image.open(img_path) as im:
        w, h = im.size
        return int(h), int(w)


def _load_preview_uint8(img_path: Path, max_dim: int = 400) -> tuple[np.ndarray, int, int]:
    """Load read-only uint8 grayscale image resized smoothly to max_dim for pilot visual audit."""
    ext = img_path.suffix.lower()
    if ext in DICOM_EXTENSIONS:
        ds = pydicom.dcmread(img_path, force=False)
        arr = ds.pixel_array
        if str(getattr(ds, "PhotometricInterpretation", "")).upper() == "MONOCHROME1":
            max_v = float((1 << int(getattr(ds, "BitsStored", 8))) - 1)
            arr = max_v - arr.astype(np.float32)
        if arr.ndim == 3:
            gray = arr[..., :3].mean(axis=2, dtype=np.float32)
        else:
            gray = arr.astype(np.float32, copy=False)
    else:
        with Image.open(img_path) as im:
            im.load()
            arr = np.asarray(im)
            if arr.ndim == 3:
                gray = arr[..., :3].mean(axis=2, dtype=np.float32)
            else:
                gray = arr.astype(np.float32, copy=False)

    orig_h, orig_w = int(gray.shape[0]), int(gray.shape[1])
    scale = min(1.0, max_dim / max(orig_h, orig_w))
    new_w = max(1, int(round(orig_w * scale)))
    new_h = max(1, int(round(orig_h * scale)))
    small = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_AREA) if scale < 1.0 else gray
    lo, hi = float(np.percentile(small, 1.0)), float(np.percentile(small, 99.5))
    if hi <= lo:
        lo, hi = float(np.min(small)), float(np.max(small))
    if hi > lo:
        norm = ((small - lo) / (hi - lo) * 255.0).clip(0.0, 255.0).astype(np.uint8)
    else:
        norm = np.zeros(small.shape, dtype=np.uint8)
    return norm, orig_h, orig_w


# ---------------------------------------------------------------------------
# Mask Extraction Helpers (`UD09` / `T09 §5`)
# ---------------------------------------------------------------------------


def rasterize_cdd_cesm_shapes(
    shape_dicts: list[dict[str, Any]],
    height: int,
    width: int,
    point_radius: int = 5,
) -> tuple[np.ndarray, list[str], bool]:
    """Rasterize union of VIA shape primitives (`polygon/ellipse/circle/polyline/point`)."""
    mask = np.zeros((height, width), dtype=np.uint8)
    shape_names: list[str] = []
    out_of_bounds = False

    for shape in shape_dicts:
        if not shape:
            continue
        name = str(shape.get("name", "")).strip().lower()
        shape_names.append(name or "unknown")
        if name in {"polygon", "polyline"}:
            xs = shape.get("all_points_x") or []
            ys = shape.get("all_points_y") or []
            if len(xs) != len(ys) or not xs:
                continue
            pts = np.column_stack([np.asarray(xs, dtype=np.float64), np.asarray(ys, dtype=np.float64)])
            if np.any(pts[:, 0] < -2) or np.any(pts[:, 0] > width + 2) or np.any(pts[:, 1] < -2) or np.any(pts[:, 1] > height + 2):
                out_of_bounds = True
            pts_i = np.round(pts).astype(np.int32).reshape((-1, 1, 2))
            if len(pts_i) >= 3:
                cv2.fillPoly(mask, [pts_i], 1)
            else:
                cv2.polylines(mask, [pts_i], False, 1, thickness=2)
        elif name == "ellipse":
            cx = float(shape.get("cx", 0.0))
            cy = float(shape.get("cy", 0.0))
            rx = max(1, int(round(float(shape.get("rx", 1.0)))))
            ry = max(1, int(round(float(shape.get("ry", 1.0)))))
            theta_rad = float(shape.get("theta", 0.0) or 0.0)
            if cx < 0 or cx >= width or cy < 0 or cy >= height:
                out_of_bounds = True
            cv2.ellipse(
                mask,
                (int(round(cx)), int(round(cy))),
                (rx, ry),
                float(math.degrees(theta_rad)),
                0.0,
                360.0,
                1,
                thickness=-1,
            )
        elif name == "circle":
            cx = float(shape.get("cx", 0.0))
            cy = float(shape.get("cy", 0.0))
            r = max(1, int(round(float(shape.get("r", 1.0)))))
            if cx < 0 or cx >= width or cy < 0 or cy >= height:
                out_of_bounds = True
            cv2.circle(mask, (int(round(cx)), int(round(cy))), r, 1, thickness=-1)
        elif name == "point":
            cx = float(shape.get("cx", 0.0))
            cy = float(shape.get("cy", 0.0))
            if cx < 0 or cx >= width or cy < 0 or cy >= height:
                out_of_bounds = True
            cv2.circle(mask, (int(round(cx)), int(round(cy))), point_radius, 1, thickness=-1)

    return mask, shape_names, out_of_bounds


def _rgb_channel_diff_u8(rgb: np.ndarray) -> np.ndarray:
    """Compute exact per-pixel max(R,G,B) - min(R,G,B) via fast uint8 SIMD ops."""
    c0, c1, c2 = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    max_c = cv2.max(c0, cv2.max(c1, c2))
    min_c = cv2.min(c0, cv2.min(c1, c2))
    return cv2.subtract(max_c, min_c)


def extract_dmid_rgba_mask(
    tif_path: Path,
    color_diff_thresh: int = 35,
    fill_holes: bool = True,
) -> tuple[np.ndarray, dict[str, int]]:
    """Extract solid binary lesion ROI from DMID `Pixel-level annotation/*.tif` (`never ROI Masks`)."""
    norm_posix = tif_path.as_posix().lower()
    if "/roi masks/" in norm_posix:
        raise ValueError(f"Prohibited asset accessed (T09 §5 hard ban on DMID ROI Masks): {tif_path}")
    with Image.open(tif_path) as im:
        im.load()
        arr = np.asarray(im)
    if arr.ndim == 3 and arr.shape[2] >= 3:
        diff = _rgb_channel_diff_u8(np.ascontiguousarray(arr[..., :3]))
        raw_mask = (diff > color_diff_thresh).astype(np.uint8)
    else:
        raw_mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    raw_px = int(cv2.countNonZero(raw_mask))
    if fill_holes and raw_px > 0:
        cnts, _ = cv2.findContours(raw_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filled = np.zeros_like(raw_mask)
        cv2.drawContours(filled, cnts, -1, 1, thickness=-1)
        n_comp = len(cnts)
    else:
        filled = raw_mask
        n_comp = int(cv2.connectedComponents(raw_mask)[0] - 1) if raw_px > 0 else 0
    return filled, {
        "raw_outline_px": raw_px,
        "filled_px": int(cv2.countNonZero(filled)),
        "components": n_comp,
    }


def extract_bmcd_gt_channels(
    gt_path: Path,
    target_h: int | None = None,
    target_w: int | None = None,
    channel_thresh: int = 35,
    mode: str = "lesion_red_blue",
) -> tuple[np.ndarray, dict[str, Any]]:
    """Extract Red (benign calc), Blue (suspicious circle), and Green telemetry from BMCD `*_GT.jpg`."""
    with Image.open(gt_path) as im:
        im.load()
        rgb = np.asarray(im.convert("RGB"))

    gt_h, gt_w = int(rgb.shape[0]), int(rgb.shape[1])
    aspect_rel_err = 0.0
    if target_h and target_w:
        gt_ar = gt_w / max(gt_h, 1)
        tgt_ar = target_w / max(target_h, 1)
        aspect_rel_err = abs(gt_ar - tgt_ar) / max(tgt_ar, 1e-6)

    c0, c1, c2 = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    r_only = cv2.subtract(c0, cv2.max(c1, c2)) > channel_thresh
    g_only = cv2.subtract(c1, cv2.max(c0, c2)) > channel_thresh
    b_only = cv2.subtract(c2, cv2.max(c0, c1)) > channel_thresh

    if mode == "lesion_red_blue":
        lesion_raw = (r_only | b_only).astype(np.uint8)
        # Fill closed blue suspicious circles while preserving tiny red microcalc dots.
        if b_only.any():
            b_u8 = b_only.astype(np.uint8)
            cnts, _ = cv2.findContours(b_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            b_filled = np.zeros_like(b_u8)
            cv2.drawContours(b_filled, cnts, -1, 1, thickness=-1)
            lesion_raw = (r_only.astype(np.uint8) | b_filled)
    elif mode == "all_chromatic":
        lesion_raw = (_rgb_channel_diff_u8(rgb) > channel_thresh).astype(np.uint8)
    else:
        raise ValueError(f"Unsupported BMCD channel mode: {mode}")

    if target_h and target_w and (gt_h != target_h or gt_w != target_w):
        out_mask = cv2.resize(lesion_raw, (target_w, target_h), interpolation=cv2.INTER_NEAREST)
    else:
        out_mask = lesion_raw

    bottom_cut = int(0.88 * gt_h)
    bottom_red_px = int(r_only[bottom_cut:, :].sum()) if gt_h > 10 else 0
    return out_mask, {
        "gt_w": gt_w,
        "gt_h": gt_h,
        "red_px": int(r_only.sum()),
        "green_px": int(g_only.sum()),
        "blue_px": int(b_only.sum()),
        "bottom_red_px": bottom_red_px,
        "lesion_raw_px": int(lesion_raw.sum()),
        "aspect_rel_err": round(aspect_rel_err, 5),
    }


def rasterize_mias_circle(
    circles: list[tuple[float, float, float]],
    height: int,
    width: int,
    y_from_bottom: bool = True,
) -> np.ndarray:
    """Rasterize union of `(x, y, radius)` MIAS abnormality circles onto `(Height, Width)`."""
    mask = np.zeros((height, width), dtype=np.uint8)
    for x, y, r in circles:
        row_center = (height - float(y)) if y_from_bottom else float(y)
        col_center = float(x)
        rad = max(1, int(round(float(r))))
        cv2.circle(mask, (int(round(col_center)), int(round(row_center))), rad, 1, thickness=-1)
    return mask


# ---------------------------------------------------------------------------
# Metadata Parsers (`MIAS 00README.pdf` + `DMID` + `CMMD` + `BMCD` + `CDD`)
# ---------------------------------------------------------------------------


def _parse_mias_lines(lines: list[str]) -> list[dict[str, Any]]:
    """Parse canonical MIAS `mdb###` table rows, including unbounded `*** see note 2` diffuse cases."""
    pat = re.compile(
        r"^(mdb\d{3}[a-z]{0,2})\s+([FGD])\s+(NORM|CALC|CIRC|SPIC|MISC|ARCH|ASYM)"
        r"(?:\s+([BM])(?:\s+(?:\*\*\*.*|(\d+)\s+(\d+)\s+(\d+)))?)?$"
    )
    parsed: list[dict[str, Any]] = []
    for ln in lines:
        m = pat.match(ln.strip())
        if not m:
            continue
        stem = m.group(1)
        bg = m.group(2)
        abn = m.group(3)
        sev = m.group(4) or ("NORM" if abn == "NORM" else "")
        x = int(m.group(5)) if m.group(5) else None
        y = int(m.group(6)) if m.group(6) else None
        r = int(m.group(7)) if m.group(7) else None
        parsed.append(
            {
                "stem": stem,
                "ref_id": stem[:6],
                "bg": bg,
                "abn": abn,
                "sev": sev,
                "x": x,
                "y": y,
                "r": r,
                "raw": ln.strip(),
            }
        )
    return parsed


def parse_mias_00readme_text(pdf_path: Path) -> list[dict[str, Any]]:
    """Extract all MIAS `mdb###` table rows cleanly from compressed `00README.pdf` streams."""
    pdf_bytes = pdf_path.read_bytes()
    raw_streams = re.findall(rb"stream[\r\n]+(.*?)endstream", pdf_bytes, re.S)
    line_regex = re.compile(
        r"([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s+T[mdD]"
        r"|\[(?!/)([^\]]+)\]\s*TJ"
        r"|\(([^()]*)\)\s*Tj"
        r"|(T\*|ET)"
    )

    candidate_lines: list[str] = []
    for raw_stream in raw_streams:
        if len(raw_stream) > 30000:
            continue
        for chunk in (raw_stream, raw_stream.strip(b"\r\n")):
            try:
                decoded = zlib.decompress(chunk).decode("latin1", errors="ignore")
            except zlib.error:
                continue
            if "BT" not in decoded:
                break
            cur: list[str] = []
            for m in line_regex.finditer(decoded):
                if m.group(5) in ("T*", "ET"):
                    if cur:
                        line = " ".join("".join(cur).split())
                        if line:
                            candidate_lines.append(line)
                        cur = []
                elif m.group(1) is not None:
                    dy = float(m.group(2))
                    if abs(dy) > 0.5 and cur:
                        line = " ".join("".join(cur).split())
                        if line:
                            candidate_lines.append(line)
                        cur = []
                elif m.group(3) is not None:
                    cur.append("".join(re.findall(r"\(([^()]*)\)", m.group(3))))
                elif m.group(4) is not None:
                    cur.append(m.group(4))
            if cur:
                line = " ".join("".join(cur).split())
                if line:
                    candidate_lines.append(line)
            break

    return _parse_mias_lines(candidate_lines)


def _load_linkage_and_qc(spec: LabelCohortSpec) -> list[dict[str, str]]:
    """Load primary_image linkage rows merged with STEP-013 QC dispositions & dimensions."""
    if not spec.linkage_csv.is_file():
        raise FileNotFoundError(f"Missing private linkage manifest: {spec.linkage_csv}")

    qc_map: dict[str, dict[str, str]] = {}
    if spec.qc_details_csv and spec.qc_details_csv.is_file():
        with spec.qc_details_csv.open(encoding="utf-8", newline="") as fp:
            for row in csv.DictReader(fp):
                qc_map[row["ImageID"]] = row

    primary_rows: list[dict[str, str]] = []
    with spec.linkage_csv.open(encoding="utf-8", newline="") as fp:
        for row in csv.DictReader(fp):
            img_id = row["ImageID"]
            qc_row = qc_map.get(img_id)
            if qc_row is not None:
                if qc_row.get("RoleTrack") != "primary_image":
                    continue
                merged = dict(row)
                merged["Disposition"] = qc_row.get("Disposition", "Retained")
                merged["QCWidth"] = qc_row.get("Width", "")
                merged["QCHeight"] = qc_row.get("Height", "")
                merged["QCViewTag"] = qc_row.get("ViewTag", "")
                merged["QCLateralityTag"] = qc_row.get("LateralityTag", "")
                primary_rows.append(merged)
            else:
                # Fallback for clean synthetic tests when qc_details_csv isn't supplied.
                fcat = row.get("FileCategory", "")
                rel = row.get("RawRelativePath", "").replace("\\", "/").lower()
                if fcat not in {"image_dicom", "image_raster"}:
                    continue
                if spec.dataset_id == "DS0006" and ("subtracted" in rel or "_cm_" in Path(rel).stem):
                    continue
                if spec.dataset_id == "DS0005" and Path(rel).stem.endswith("_gt"):
                    continue
                merged = dict(row)
                merged["Disposition"] = "Retained"
                primary_rows.append(merged)
    return primary_rows


def _safe_int(val: str) -> int | None:
    try:
        return int(float(val)) if val else None
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Cohort Harmonizers (`DS0001`, `DS0002`, `DS0003`, `DS0005`, `DS0006`)
# ---------------------------------------------------------------------------


def _harmonize_cmmd(spec: LabelCohortSpec, primary_rows: list[dict[str, str]]) -> list[LabelRecord]:
    """Harmonize `DS0003 CMMD` via `(ID1, ImageLaterality)` join + clone/contralateral rules."""
    xlsx = spec.raw_dir / "CMMD_clinicaldata_revision.xlsx"
    if not xlsx.is_file():
        raise FileNotFoundError(f"Missing CMMD clinical table: {xlsx}")
    clin = pd.read_excel(xlsx)
    clin_by_side: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    sides_by_pid: dict[str, set[str]] = collections.defaultdict(set)
    for _, r in clin.iterrows():
        pid = str(r["ID1"]).strip()
        lr = str(r["LeftRight"]).strip().upper()
        cls_val = str(r["classification"]).strip()
        abn_val = str(r["abnormality"]).strip() if pd.notna(r["abnormality"]) else "not_reported"
        clin_by_side[(pid, lr)].append({"classification": cls_val, "abnormality": abn_val})
        sides_by_pid[pid].add(cls_val)
    discordant_pids = {pid for pid, vals in sides_by_pid.items() if len(vals) > 1}

    def _read_dcm_meta(row: dict[str, str]) -> tuple[str, str, str, int | None, int | None]:
        cached_lat = row.get("QCLateralityTag", "").strip().upper()
        cached_view = _normalize_view(row.get("QCViewTag", ""))
        cached_w = _safe_int(row.get("QCWidth", ""))
        cached_h = _safe_int(row.get("QCHeight", ""))
        src_tok = row.get("SourcePatientToken", "").strip()
        if (
            cached_lat in {"L", "R"}
            and cached_view in {"CC", "MLO"}
            and src_tok
            and src_tok != "PAT_UNRESOLVED"
            and cached_w
            and cached_h
        ):
            return src_tok, cached_lat, cached_view, cached_w, cached_h
        rel = row["RawRelativePath"]
        ds = pydicom.dcmread(
            spec.raw_dir / rel,
            stop_before_pixels=True,
            specific_tags=["PatientID", "ImageLaterality", "ViewPosition", "ViewCodeSequence", "Rows", "Columns"],
        )
        pid = str(getattr(ds, "PatientID", "") or src_tok).strip()
        lat = str(getattr(ds, "ImageLaterality", "") or "").strip().upper() or "unknown"
        view = _normalize_view(str(getattr(ds, "ViewPosition", "") or ""))
        if view == "unknown" and hasattr(ds, "ViewCodeSequence") and ds.ViewCodeSequence:
            seq0 = ds.ViewCodeSequence[0]
            code_val = str(getattr(seq0, "CodeValue", "") or "").strip()
            code_mean = str(getattr(seq0, "CodeMeaning", "") or "").strip()
            if code_val == "399162004" or "cranio-caudal" in code_mean.lower():
                view = "CC"
            elif code_val == "399368009" or "medio-lateral oblique" in code_mean.lower():
                view = "MLO"
        return pid, lat, view, int(getattr(ds, "Columns", 0) or 0) or None, int(getattr(ds, "Rows", 0) or 0) or None

    meta_list: list[tuple[str, str, str, int | None, int | None]]
    uncached = any(
        not (
            row.get("QCLateralityTag", "").strip().upper() in {"L", "R"}
            and _normalize_view(row.get("QCViewTag", "")) in {"CC", "MLO"}
            and row.get("SourcePatientToken", "").strip() not in {"", "PAT_UNRESOLVED"}
        )
        for row in primary_rows
    )
    if uncached and len(primary_rows) >= 40:
        with ThreadPoolExecutor(max_workers=min(8, max(2, os.cpu_count() or 2))) as pool:
            meta_list = list(pool.map(_read_dcm_meta, primary_rows))
    else:
        meta_list = [_read_dcm_meta(r) for r in primary_rows]

    out: list[LabelRecord] = []
    for row, (pid, lat, view, w_hdr, h_hdr) in zip(primary_rows, meta_list):
        disp = row["Disposition"]
        w = _safe_int(row.get("QCWidth", "")) or w_hdr
        h = _safe_int(row.get("QCHeight", "")) or h_hdr
        side_rows = clin_by_side.get((pid, lat), [])
        flags: list[str] = []
        if pid in discordant_pids:
            flags.append("BilateralDiscordantPatient")

        if disp != "Retained":
            out.append(
                LabelRecord(
                    ImageID=row["ImageID"],
                    DatasetID="DS0003",
                    PatientGroupID=row["PatientGroupID"],
                    SourceStem=Path(row["RawRelativePath"]).stem,
                    DispositionQC=disp,
                    Paradigm="WholeBreast_FFDM",
                    BinaryTarget="Excluded",
                    LabelClass=disp,
                    LabelProvenanceTier="Excluded",
                    SubTrackA_BiopsyEligible=False,
                    SubTrackB_ScreeningEligible=False,
                    LesionTrack_BenignVsMalignant=False,
                    RawLabelTokens=f"QC={disp}",
                    MultiLesionConflict=False,
                    ViewPosition=view,
                    Laterality=lat,
                    DensityACR="not_reported",
                    MorphologyType="not_reported",
                    BIRADSScore="not_reported",
                    ClinicalConcStatus="quarantined_step013",
                    LocalizationEligible=False,
                    MaskSourceType="None",
                    MaskStatus="not_applicable",
                    ImageWidth=w,
                    ImageHeight=h,
                    AnomalyFlags=";".join(flags),
                    RawRelativePath=row["RawRelativePath"],
                )
            )
            continue

        if pid in CMMD_CONFLICT_PATIENTS:
            flags.append("CrossLabelCloneCompanionView")
            out.append(
                LabelRecord(
                    ImageID=row["ImageID"],
                    DatasetID="DS0003",
                    PatientGroupID=row["PatientGroupID"],
                    SourceStem=Path(row["RawRelativePath"]).stem,
                    DispositionQC=disp,
                    Paradigm="WholeBreast_FFDM",
                    BinaryTarget="Excluded",
                    LabelClass="Excluded_CrossLabelClonePatient",
                    LabelProvenanceTier="Excluded",
                    SubTrackA_BiopsyEligible=False,
                    SubTrackB_ScreeningEligible=False,
                    LesionTrack_BenignVsMalignant=False,
                    RawLabelTokens=";".join(x["classification"] for x in side_rows) or "ConflictClonePatient",
                    MultiLesionConflict=True,
                    ViewPosition=view,
                    Laterality=lat,
                    DensityACR="not_reported",
                    MorphologyType="not_reported",
                    BIRADSScore="not_reported",
                    ClinicalConcStatus="excluded_clone_patient",
                    LocalizationEligible=False,
                    MaskSourceType="None",
                    MaskStatus="not_applicable",
                    ImageWidth=w,
                    ImageHeight=h,
                    AnomalyFlags=";".join(flags),
                    RawRelativePath=row["RawRelativePath"],
                )
            )
            continue

        if not side_rows:
            out.append(
                LabelRecord(
                    ImageID=row["ImageID"],
                    DatasetID="DS0003",
                    PatientGroupID=row["PatientGroupID"],
                    SourceStem=Path(row["RawRelativePath"]).stem,
                    DispositionQC=disp,
                    Paradigm="WholeBreast_FFDM",
                    BinaryTarget="Excluded",
                    LabelClass="Excluded_UnlabeledContralateral",
                    LabelProvenanceTier="Excluded",
                    SubTrackA_BiopsyEligible=False,
                    SubTrackB_ScreeningEligible=False,
                    LesionTrack_BenignVsMalignant=False,
                    RawLabelTokens="ContralateralUnannotated",
                    MultiLesionConflict=False,
                    ViewPosition=view,
                    Laterality=lat,
                    DensityACR="not_reported",
                    MorphologyType="not_reported",
                    BIRADSScore="not_reported",
                    ClinicalConcStatus="unlabeled_contralateral",
                    LocalizationEligible=False,
                    MaskSourceType="None",
                    MaskStatus="not_applicable",
                    ImageWidth=w,
                    ImageHeight=h,
                    AnomalyFlags=";".join(flags),
                    RawRelativePath=row["RawRelativePath"],
                )
            )
            continue

        cls_set = {x["classification"] for x in side_rows}
        if "Malignant" in cls_set and "Benign" in cls_set:
            btarget, lclass, conflict = "1", "Malignant", True
            flags.append("SameSideMultiLesionMalignantDominance")
        elif cls_set == {"Malignant"}:
            btarget, lclass, conflict = "1", "Malignant", False
        elif cls_set == {"Benign"}:
            btarget, lclass, conflict = "0", "Benign_Biopsy", False
        else:
            raise ValueError(f"Unmapped CMMD classification token(s): {cls_set} for {row['ImageID']}")

        morphs = sorted({x["abnormality"] for x in side_rows})
        morph_str = morphs[0] if len(morphs) == 1 else "both"
        out.append(
            LabelRecord(
                ImageID=row["ImageID"],
                DatasetID="DS0003",
                PatientGroupID=row["PatientGroupID"],
                SourceStem=Path(row["RawRelativePath"]).stem,
                DispositionQC=disp,
                Paradigm="WholeBreast_FFDM",
                BinaryTarget=btarget,
                LabelClass=lclass,
                LabelProvenanceTier="TierA_Biopsy",
                SubTrackA_BiopsyEligible=True,
                SubTrackB_ScreeningEligible=True,
                LesionTrack_BenignVsMalignant=True,
                RawLabelTokens=";".join(sorted(cls_set)),
                MultiLesionConflict=conflict,
                ViewPosition=view,
                Laterality=lat,
                DensityACR="not_reported",
                MorphologyType=morph_str,
                BIRADSScore="not_reported",
                ClinicalConcStatus="ok_biopsy_side_match",
                LocalizationEligible=False,
                MaskSourceType="None",
                MaskStatus="not_applicable",
                ImageWidth=w,
                ImageHeight=h,
                AnomalyFlags=";".join(flags),
                RawRelativePath=row["RawRelativePath"],
            )
        )
    return out


def _harmonize_cdd_cesm(
    spec: LabelCohortSpec,
    primary_rows: list[dict[str, str]],
    verify_mask_ids: set[str] | None = None,
) -> list[LabelRecord]:
    """Harmonize `DS0006 CDD-CESM LE` labels, postop/NAC exclusions & multi-primitive VIA masks."""
    meta_dir = spec.raw_dir / "metadata"
    if not meta_dir.is_dir():
        meta_dir = spec.raw_dir
    xlsx = meta_dir / "Radiology-manual-annotations.xlsx"
    seg_csv = meta_dir / "Radiology_hand_drawn_segmentations_v2.csv"
    if not xlsx.is_file() or not seg_csv.is_file():
        raise FileNotFoundError(f"Missing CDD-CESM metadata/segmentations in {meta_dir}")

    xl = pd.ExcelFile(xlsx)
    all_df = pd.read_excel(xl, sheet_name="all")
    postop_names = set(pd.read_excel(xl, sheet_name="postoperative")["Image_name"].astype(str).str.strip())
    nac_names = set(pd.read_excel(xl, sheet_name="postneoajuvant chemotherapy")["Image_name"].astype(str).str.strip())

    ann_by_stem: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for _, r in all_df.iterrows():
        ann_by_stem[str(r["Image_name"]).strip()].append(r.to_dict())

    seg_df = pd.read_csv(seg_csv)
    seg_by_file: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for _, r in seg_df.iterrows():
        fname = str(r["#filename"]).strip()
        raw_shape = str(r.get("region_shape_attributes", "{}") or "{}").strip()
        try:
            shape = json.loads(raw_shape)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed VIA JSON for {fname}: {raw_shape}") from exc
        if shape:
            seg_by_file[fname].append(shape)

    out: list[LabelRecord] = []
    for row in primary_rows:
        img_id = row["ImageID"]
        rel_path = row["RawRelativePath"]
        stem = Path(rel_path).stem.strip()
        fname = Path(rel_path).name.strip()
        disp = row["Disposition"]
        w = _safe_int(row.get("QCWidth", ""))
        h = _safe_int(row.get("QCHeight", ""))
        if w is None or h is None:
            h, w = _load_image_hw(spec.raw_dir / rel_path)

        ann_rows = ann_by_stem.get(stem, [])
        if not ann_rows:
            raise ValueError(f"CDD-CESM image missing in Radiology-manual-annotations.xlsx: {stem} ({img_id})")

        r0 = ann_rows[0]
        view = _normalize_view(str(r0.get("View", "") or stem.split("_")[-1]))
        lat = _infer_laterality_from_view_or_side(str(r0.get("Side", "") or stem))
        density = str(r0.get("Breast density (ACR)", "") or "not_reported").strip() or "not_reported"
        birads = _parse_max_birads(r0.get("BIRADS"))
        findings_raw = ";".join(str(x.get("Findings", "") or "").strip() for x in ann_rows if pd.notna(x.get("Findings")))
        path_tokens = sorted({str(x.get("Pathology Classification/ Follow up", "")).strip() for x in ann_rows})
        flags: list[str] = []

        # Morphology summary from Findings text
        f_lower = findings_raw.lower()
        has_mass = "mass" in f_lower
        has_calc = "calc" in f_lower
        morph = "both" if (has_mass and has_calc) else ("mass" if has_mass else ("calcification" if has_calc else "other"))

        shapes = seg_by_file.get(fname, [])
        should_verify_mask = verify_mask_ids is None or img_id in verify_mask_ids

        if disp != "Retained":
            btarget, lclass, ptier, sub_a, sub_b, les_t = "Excluded", disp, "Excluded", False, False, False
            conc = "quarantined_step013"
            conflict = False
        elif stem in nac_names:
            btarget, lclass, ptier, sub_a, sub_b, les_t = "Excluded", "Excluded_PostNAC_BIRADS6", "Excluded", False, False, False
            conc = "excluded_post_nac"
            conflict = False
        elif stem in postop_names:
            btarget, lclass, ptier, sub_a, sub_b, les_t = "Excluded", "Excluded_PostOperative", "Excluded", False, False, False
            conc = "excluded_postop"
            conflict = False
        else:
            conflict = len(path_tokens) > 1
            if "Malignant" in path_tokens:
                btarget, lclass, ptier, sub_a, sub_b, les_t = "1", "Malignant", "TierA_Biopsy", True, True, True
                conc = "ok_pathology_birads"
                if birads in {"1", "2"}:
                    flags.append(f"OccultOnDM_BIRADS_{birads}")
                    conc = f"occult_dm_birads_{birads}_malignant"
            elif "Benign" in path_tokens:
                btarget, lclass, ptier, sub_a, sub_b, les_t = "0", "Benign_Biopsy", "TierA_Biopsy", True, True, True
                conc = "ok_pathology_birads"
                if birads in {"5", "6"}:
                    flags.append(f"FalsePositiveDM_BIRADS_{birads}_BiopsyBenign")
            elif "Normal" in path_tokens:
                if birads == "6":
                    raise ValueError(f"Normal pathology paired with BIRADS 6 outside NAC on {stem} ({img_id})")
                btarget, lclass, ptier, sub_a, sub_b, les_t = "0", "Normal_Control", "TierA_Biopsy_NormalControl", False, True, False
                morph = "none"
                conc = "ok_pathology_birads"
                if birads in {"3", "4", "5"}:
                    flags.append(f"DM_BIRADS_{birads}_ClearedNormal")
                    conc = f"dm_birads_{birads}_cleared_normal"
            else:
                raise ValueError(f"Unmapped CDD-CESM pathology token(s): {path_tokens} on {stem}")
            if birads == "6":
                flags.append("UnexpectedBIRADS6OutsideNAC")

        # Rasterize VIA polygons/ellipses/circles/polylines/points on retained or requested audit items
        mask_status = "excluded_by_protocol" if btarget == "Excluded" else "ok_expected_empty"
        mask_fg, mask_cov, mask_comp = 0, 0.0, 0
        loc_eligible = False
        extra_mask = ""
        if shapes:
            if should_verify_mask:
                mask_arr, s_names, oob = rasterize_cdd_cesm_shapes(shapes, h, w)
                mask_fg = int(mask_arr.sum())
                mask_cov = round(100.0 * mask_fg / max(h * w, 1), 4)
                mask_comp = len(s_names)
                if oob:
                    flags.append("MaskCoordsClippedAtBorder")
                if mask_fg > 0:
                    mask_status = "ok_nonempty" if btarget != "Excluded" else "excluded_by_protocol"
                    loc_eligible = btarget != "Excluded"
                else:
                    mask_status = "empty_unexpected"
                    flags.append("UnexpectedEmptyVIAMask")
                extra_mask = "shapes=" + ",".join(sorted(set(s_names)))
            else:
                mask_comp = len(shapes)
                mask_status = "present_unrasterized" if btarget != "Excluded" else "excluded_by_protocol"
                loc_eligible = btarget != "Excluded"
        elif btarget != "Excluded" and lclass in {"Malignant", "Benign_Biopsy"}:
            # Abnormal CDD-CESM scans without VIA segmentation (flagged transparently, never invented)
            mask_status = "ok_expected_empty"
            flags.append("AbnormalWithoutVIASegmentation")

        out.append(
            LabelRecord(
                ImageID=img_id,
                DatasetID="DS0006",
                PatientGroupID=row["PatientGroupID"],
                SourceStem=stem,
                DispositionQC=disp,
                Paradigm="WholeBreast_FFDM",
                BinaryTarget=btarget,
                LabelClass=lclass,
                LabelProvenanceTier=ptier,
                SubTrackA_BiopsyEligible=sub_a,
                SubTrackB_ScreeningEligible=sub_b,
                LesionTrack_BenignVsMalignant=les_t,
                RawLabelTokens=";".join(path_tokens),
                MultiLesionConflict=conflict,
                ViewPosition=view,
                Laterality=lat,
                DensityACR=density,
                MorphologyType=morph,
                BIRADSScore=birads,
                ClinicalConcStatus=conc,
                LocalizationEligible=loc_eligible,
                MaskSourceType="VIA_MultiPrimitive" if shapes else "None",
                MaskStatus=mask_status,
                MaskWidth=w if shapes else None,
                MaskHeight=h if shapes else None,
                ImageWidth=w,
                ImageHeight=h,
                MaskForegroundPixels=mask_fg,
                MaskCoveragePct=mask_cov,
                MaskComponentCount=mask_comp,
                ExtraMaskTelemetry=extra_mask,
                AnomalyFlags=";".join(flags),
                RawRelativePath=rel_path,
                MaskRelativePath="metadata/Radiology_hand_drawn_segmentations_v2.csv" if shapes else "",
            )
        )
    return out


def _parse_bmcd_sheet(df: pd.DataFrame) -> dict[int, dict[str, Any]]:
    """Locate 'Folder #' header row dynamically in BMCD Excel sheet and return folder dict."""
    header_idx: int | None = None
    for idx in range(len(df)):
        row_vals = [str(v).strip().lower() for v in df.iloc[idx].tolist() if pd.notna(v)]
        if any("folder #" in v or v == "folder" for v in row_vals):
            header_idx = idx
            break
    if header_idx is None:
        raise ValueError("Unable to locate 'Folder #' header row in BMCD sheet")

    cols = [str(c).strip() if pd.notna(c) else f"col_{i}" for i, c in enumerate(df.iloc[header_idx].tolist())]
    by_folder: dict[int, dict[str, Any]] = {}
    for idx in range(header_idx + 1, len(df)):
        row = df.iloc[idx].tolist()
        mapped = dict(zip(cols, row))
        fval = mapped.get("Folder #")
        if fval is None or (isinstance(fval, float) and math.isnan(fval)):
            continue
        try:
            fnum = int(float(str(fval).strip()))
        except ValueError:
            continue
        by_folder[fnum] = {
            "side": str(mapped.get("Breast (Right/Left)", "")).strip(),
            "age": mapped.get("Age"),
            "density": str(mapped.get("BI-RADS categories for breast density", "")).strip() or "not_reported",
            "birads": str(mapped.get("BI-RADS categories for classification", "")).strip(),
            "biopsy": str(mapped.get("Biopsy Results", mapped.get("Follow-up Results", "NOT AVAILABLE"))).strip(),
        }
    return by_folder


def _harmonize_bmcd(
    spec: LabelCohortSpec,
    primary_rows: list[dict[str, str]],
    verify_mask_ids: set[str] | None = None,
) -> list[LabelRecord]:
    """Harmonize `DS0005 BMCD` temporal prior/recent pairs, biopsy status, & *_GT.jpg overlays."""
    xlsx = spec.raw_dir / "Description.xlsx"
    if not xlsx.is_file():
        raise FileNotFoundError(f"Missing BMCD Description.xlsx: {xlsx}")
    xl = pd.ExcelFile(xlsx)
    norm_meta = _parse_bmcd_sheet(pd.read_excel(xl, sheet_name="Normal_cases"))
    susp_meta = _parse_bmcd_sheet(pd.read_excel(xl, sheet_name="Suspicious_cases"))

    out: list[LabelRecord] = []
    for row in primary_rows:
        img_id = row["ImageID"]
        rel_path = row["RawRelativePath"]
        norm_rel = rel_path.replace("\\", "/")
        parts = norm_rel.split("/")
        # Expected structure: Dataset/{Normal_cases|Suspicious_cases}/{folder}/{CC|MLO}_{prior|recent}.dcm
        grp = next((p for p in parts if p in {"Normal_cases", "Suspicious_cases"}), "")
        folder_num = next((int(p) for p in parts if p.isdigit()), None)
        stem = Path(rel_path).stem
        stem_low = stem.lower()
        typo_flag = ""
        if "prior" in stem_low:
            round_tag = "prior"
        elif "recent" in stem_low:
            round_tag = "recent"
        elif any(tok in stem_low for tok in ("recemt", "reent")):
            round_tag = "recent"
            typo_flag = f"UpstreamFilenameTypo_{stem}"
        else:
            round_tag = "unknown"
        view = _normalize_view(stem)
        disp = row["Disposition"]

        if grp not in {"Normal_cases", "Suspicious_cases"} or folder_num is None:
            raise ValueError(f"Unexpected BMCD relative path structure: {rel_path}")

        meta = norm_meta.get(folder_num) if grp == "Normal_cases" else susp_meta.get(folder_num)
        if not meta:
            raise ValueError(f"Missing BMCD metadata row for {grp}/{folder_num}")

        lat = _infer_laterality_from_view_or_side(meta["side"])
        density = meta["density"]
        birads = meta["birads"] or "not_reported"
        biopsy = meta["biopsy"].upper()
        w = _safe_int(row.get("QCWidth", ""))
        h = _safe_int(row.get("QCHeight", ""))
        if w is None or h is None:
            h, w = _load_image_hw(spec.raw_dir / rel_path)

        flags: list[str] = [typo_flag] if typo_flag else []
        if disp != "Retained":
            btarget, lclass, ptier, sub_a, sub_b, les_t = "Excluded", disp, "Excluded", False, False, False
            conc = "quarantined_step013"
        elif grp == "Suspicious_cases" and round_tag == "prior":
            btarget, lclass, ptier, sub_a, sub_b, les_t = "Excluded", "Excluded_PriorScreeningRound", "Excluded", False, False, False
            conc = "excluded_prior_baseline"
        elif grp == "Suspicious_cases" and round_tag == "recent":
            if biopsy in {"MALIGNANT", "DCIS"}:
                btarget, lclass, ptier, sub_a, sub_b, les_t = "1", f"Malignant_{biopsy}", "TierA_Biopsy", True, True, True
                conc = "ok_biopsy_recent"
            elif biopsy == "BENIGN":
                btarget, lclass, ptier, sub_a, sub_b, les_t = "0", "Benign_Biopsy", "TierA_Biopsy", True, True, True
                conc = "ok_biopsy_recent"
            elif biopsy == "NOT AVAILABLE":
                btarget, lclass, ptier, sub_a, sub_b, les_t = "Excluded", "Excluded_UnconfirmedBiopsy", "Excluded", False, False, False
                conc = "unconfirmed_biopsy_birads_triage"
            else:
                raise ValueError(f"Unmapped BMCD biopsy value '{biopsy}' for {grp}/{folder_num}")
        elif grp == "Normal_cases":
            btarget = "0"
            lclass = "Normal_Control"
            ptier = "TierA_Biopsy_NormalControl"
            sub_a, sub_b, les_t = False, True, False
            conc = f"ok_normal_{round_tag}_birads_{birads}"
            flags.append(f"NormalRound_{round_tag}")
        else:
            raise ValueError(f"Unrecognized BMCD round '{round_tag}' in {rel_path}")

        # Resolve paired *_GT.jpg tolerating upstream recemt/reent typos & .Jpg casing
        dcm_folder = (spec.raw_dir / rel_path).parent
        expected_gt_names = {f"{view.lower()}_{round_tag}_gt.jpg"}
        if round_tag == "recent":
            expected_gt_names.update({f"{view.lower()}_recemt_gt.jpg", f"{view.lower()}_reent_gt.jpg"})
        gt_candidates = [p for p in sorted(dcm_folder.iterdir()) if p.is_file() and p.name.lower() in expected_gt_names]
        gt_path = gt_candidates[0] if gt_candidates else (dcm_folder / f"{stem}_GT.jpg")
        gt_rel = gt_path.relative_to(spec.raw_dir).as_posix() if gt_candidates else ""
        has_gt = gt_path.is_file()
        if has_gt and gt_path.name.lower() != f"{view.lower()}_{round_tag}_gt.jpg":
            flags.append(f"UpstreamGTTypo_{gt_path.stem}")
        should_verify = verify_mask_ids is None or img_id in verify_mask_ids

        mask_status = "not_applicable"
        mask_w, mask_h, mask_fg, mask_cov, mask_comp = None, None, 0, 0.0, 0
        loc_eligible = False
        extra_mask = ""

        if has_gt:
            if should_verify:
                m_arr, gt_meta = extract_bmcd_gt_channels(gt_path, target_h=h, target_w=w, mode="lesion_red_blue")
                mask_w, mask_h = w, h
                mask_fg = int(m_arr.sum())
                mask_cov = round(100.0 * mask_fg / max(h * w, 1), 4)
                mask_comp = int(cv2.connectedComponents(m_arr)[0] - 1) if mask_fg > 0 else 0
                extra_mask = (
                    f"gt={gt_meta['gt_w']}x{gt_meta['gt_h']},R={gt_meta['red_px']},"
                    f"B={gt_meta['blue_px']},G_ignored={gt_meta['green_px']},"
                    f"botR={gt_meta['bottom_red_px']},ar_err={gt_meta['aspect_rel_err']}"
                )
                has_bot_red_bar = gt_meta["bottom_red_px"] > 50 and gt_meta["bottom_red_px"] > 0.5 * max(gt_meta["lesion_raw_px"], 1)
                if has_bot_red_bar:
                    flags.append("BMCD_GT_BottomMarginRedBar")
                if gt_meta["aspect_rel_err"] >= 0.01:
                    mask_status = "dimension_mismatch"
                    flags.append("BMCD_GT_AspectMismatch")
                elif btarget == "Excluded":
                    mask_status = "excluded_by_protocol"
                elif has_bot_red_bar:
                    mask_status = "flagged_border_red_bar"
                    loc_eligible = False
                elif grp == "Suspicious_cases" and mask_fg == 0:
                    mask_status = "empty_unexpected"
                    flags.append("SuspiciousRecentEmptyRedBlueGT")
                elif mask_fg > 0:
                    mask_status = "ok_nonempty"
                    # Suspicious recent calcifications (and optionally BI-RADS 2 red benign calcifications)
                    loc_eligible = btarget != "Excluded" and (grp == "Suspicious_cases" or gt_meta["red_px"] > 0)
                else:
                    mask_status = "ok_expected_empty"
            else:
                mask_status = "present_unrasterized" if btarget != "Excluded" else "excluded_by_protocol"
                loc_eligible = btarget == "1"
        elif btarget != "Excluded":
            mask_status = "missing"
            flags.append("MissingBMCD_GT")

        out.append(
            LabelRecord(
                ImageID=img_id,
                DatasetID="DS0005",
                PatientGroupID=row["PatientGroupID"],
                SourceStem=f"{grp}/{folder_num}/{stem}",
                DispositionQC=disp,
                Paradigm="WholeBreast_FFDM",
                BinaryTarget=btarget,
                LabelClass=lclass,
                LabelProvenanceTier=ptier,
                SubTrackA_BiopsyEligible=sub_a,
                SubTrackB_ScreeningEligible=sub_b,
                LesionTrack_BenignVsMalignant=les_t,
                RawLabelTokens=f"grp={grp};round={round_tag};birads={birads};biopsy={biopsy}",
                MultiLesionConflict=False,
                ViewPosition=view,
                Laterality=lat,
                DensityACR=density,
                MorphologyType="calcification" if grp == "Suspicious_cases" or birads == "2" else "none",
                BIRADSScore=birads,
                ClinicalConcStatus=conc,
                LocalizationEligible=loc_eligible,
                MaskSourceType="BMCD_GT_Chromatic" if has_gt else "None",
                MaskStatus=mask_status,
                MaskWidth=mask_w,
                MaskHeight=mask_h,
                ImageWidth=w,
                ImageHeight=h,
                MaskForegroundPixels=mask_fg,
                MaskCoveragePct=mask_cov,
                MaskComponentCount=mask_comp,
                ExtraMaskTelemetry=extra_mask,
                AnomalyFlags=";".join(flags),
                RawRelativePath=rel_path,
                MaskRelativePath=gt_rel if has_gt else "",
            )
        )
    return out


def _parse_dmid_report(txt_path: Path) -> tuple[str, list[int], str]:
    """Extract ACR density, numeric BI-RADS list, and full lower text from DMID Reports/Img*.txt."""
    if not txt_path.is_file():
        return "not_reported", [], ""
    txt = txt_path.read_text(encoding="utf-8", errors="replace")
    m_acr = re.search(r"ACR\s*[-:\s]*([A-D])\b", txt, re.I)
    acr = m_acr.group(1).upper() if m_acr else "not_reported"
    birads_nums: list[int] = []
    for m_b in re.finditer(r"BIRADS\s*[:-]?\s*([0-6][a-c]?(?:\s*(?:,|and|\+)\s*[0-6][a-c]?)*)", txt, re.I):
        for d in re.findall(r"([0-6])", m_b.group(1)):
            birads_nums.append(int(d))
    return acr, birads_nums, txt.lower()


def _harmonize_dmid(
    spec: LabelCohortSpec,
    primary_rows: list[dict[str, str]],
    verify_mask_ids: set[str] | None = None,
) -> list[LabelRecord]:
    """Harmonize `DS0002 DMID` Metadata.xlsx + Reports/Img*.txt + RGBA contours."""
    xlsx = spec.raw_dir / "Metadata.xlsx"
    if not xlsx.is_file():
        raise FileNotFoundError(f"Missing DMID Metadata.xlsx: {xlsx}")
    raw_df = pd.read_excel(xlsx, header=None)
    by_img: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    for idx in range(len(raw_df)):
        v0 = raw_df.iloc[idx, 0]
        if pd.isna(v0):
            continue
        stem = str(v0).strip().upper()
        if not stem.startswith("IMG"):
            continue
        row_vals = [str(x).strip() if pd.notna(x) else "" for x in raw_df.iloc[idx, :8].tolist()]
        by_img[stem].append(
            {
                "view": row_vals[1],
                "bg": row_vals[2],
                "abn": row_vals[3],
                "cls": row_vals[4].upper(),
                "x": row_vals[5],
                "y": row_vals[6],
                "r": row_vals[7],
            }
        )

    pix_dir = spec.raw_dir / "Pixel-level annotation"
    reports_dir = spec.raw_dir / "Reports"

    out: list[LabelRecord] = []
    for row in primary_rows:
        img_id = row["ImageID"]
        rel_path = row["RawRelativePath"]
        stem = Path(rel_path).stem.strip().upper()
        disp = row["Disposition"]
        w = _safe_int(row.get("QCWidth", ""))
        h = _safe_int(row.get("QCHeight", ""))
        if w is None or h is None:
            h, w = _load_image_hw(spec.raw_dir / rel_path)

        m_rows = by_img.get(stem, [])
        if not m_rows:
            raise ValueError(f"DMID DICOM stem missing in Metadata.xlsx: {stem}")

        raw_view = m_rows[0]["view"]
        view = _normalize_view(raw_view)
        lat = _infer_laterality_from_view_or_side(raw_view)
        bg = m_rows[0]["bg"] or "not_reported"

        # Match Reports/Img###.txt cleanly (`IMG001` -> `Img001.txt`)
        num_suffix = re.sub(r"^IMG", "", stem, flags=re.I)
        rep_path = reports_dir / f"Img{num_suffix}.txt"
        acr_rep, rep_birads, rep_low = _parse_dmid_report(rep_path)
        density = acr_rep if acr_rep != "not_reported" else bg
        birads_str = str(max(rep_birads)) if rep_birads else "not_reported"

        cls_tokens = {r["cls"] if r["cls"] else ("NORM" if r["abn"].upper() == "NORM" else "") for r in m_rows}
        if "" in cls_tokens:
            raise ValueError(f"Empty DMID class token on {stem}: {m_rows}")

        abn_tokens = sorted({r["abn"] for r in m_rows if r["abn"]})
        morph = (
            "none"
            if abn_tokens == ["NORM"]
            else ("calcification" if all("CALC" in a for a in abn_tokens) else ("both" if any("CALC" in a for a in abn_tokens) and any(a != "CALC" for a in abn_tokens) else "mass_or_other"))
        )

        flags: list[str] = []
        if "CCLRT" in raw_view.upper():
            flags.append("UpstreamViewTypo_CCLRT")

        conflict = False
        conc = "ok"
        if disp != "Retained":
            btarget, lclass, ptier, sub_a, sub_b, les_t = "Excluded", disp, "Excluded", False, False, False
            conc = "quarantined_step013"
        elif "N" in cls_tokens:
            conflict = len(cls_tokens) > 1
            btarget, lclass, ptier = "Excluded", "Excluded_AmbiguousClassToken_N", "Excluded"
            sub_a, sub_b, les_t = False, False, False
            conc = f"excluded_token_N_rep_birads_{birads_str}"
            if conflict:
                flags.append(f"MixedAmbiguousTokens_{'+'.join(sorted(cls_tokens))}")
        elif cls_tokens == {"NORM"}:
            if any(b >= 3 for b in rep_birads):
                flags.append(f"Discordant_NORM_vs_RepBIRADS_{birads_str}")
                conc = "discordant_norm_vs_report"
            else:
                conc = "ok_norm_concordant"
            btarget, lclass, ptier = "0", "Normal_Control", "TierB_Radiology_BIRADS"
            sub_a, sub_b, les_t = False, True, False
        elif "M" in cls_tokens:
            conflict = "B" in cls_tokens
            if conflict:
                flags.append("MultiLesionBM_MalignantDominance")
            if rep_birads and max(rep_birads) <= 2:
                flags.append(f"Discordant_M_vs_LowBIRADS_{birads_str}")
                conc = "discordant_malignant_vs_report"
            else:
                conc = "ok_malignant_concordant"
            btarget, lclass, ptier = "1", "Malignant", "TierB_Radiology_BIRADS"
            sub_a, sub_b, les_t = False, True, True
        elif cls_tokens == {"B"}:
            if (rep_birads and max(rep_birads) >= 5) or "suggestive of malignancy" in rep_low:
                flags.append(f"Discordant_B_vs_HighBIRADS_{birads_str}")
                conc = "discordant_benign_vs_report"
            else:
                conc = "ok_benign_concordant"
            btarget, lclass, ptier = "0", "Benign_Lesion", "TierB_Radiology_BIRADS"
            sub_a, sub_b, les_t = False, True, True
        else:
            raise ValueError(f"Unmapped DMID class token(s): {cls_tokens} on {stem}")

        # ADJ-017-02 Option B: exclude scans with sheet-vs-report clinical discordance cleanly
        if conc.startswith("discordant_"):
            btarget, lclass, ptier = "Excluded", "Excluded_ReportMetadataDiscordance", "Excluded"
            sub_a, sub_b, les_t = False, False, False

        pix_tif = pix_dir / f"{stem}.tif"
        has_tif = pix_tif.is_file()
        should_verify = verify_mask_ids is None or img_id in verify_mask_ids
        mask_status = "not_applicable"
        mask_w, mask_h, mask_fg, mask_cov, mask_comp = None, None, 0, 0.0, 0
        loc_eligible = False
        extra_mask = ""

        if has_tif:
            if should_verify:
                m_arr, m_info = extract_dmid_rgba_mask(pix_tif)
                mask_h, mask_w = int(m_arr.shape[0]), int(m_arr.shape[1])
                mask_fg = m_info["filled_px"]
                mask_cov = round(100.0 * mask_fg / max(mask_h * mask_w, 1), 4)
                mask_comp = m_info["components"]
                extra_mask = f"outline={m_info['raw_outline_px']},filled={m_info['filled_px']}"
                if (mask_w, mask_h) != (w, h):
                    mask_status = "dimension_mismatch"
                    flags.append("DMID_AnnotationDimMismatch")
                elif btarget == "Excluded":
                    mask_status = "excluded_by_protocol"
                elif mask_fg == 0:
                    mask_status = "empty_unexpected"
                    flags.append("DMID_EmptyAnnotationTIF")
                else:
                    mask_status = "ok_nonempty"
                    loc_eligible = True
            else:
                mask_status = "present_unrasterized" if btarget != "Excluded" else "excluded_by_protocol"
                loc_eligible = btarget != "Excluded"
        elif btarget != "Excluded" and lclass in {"Malignant", "Benign_Lesion"}:
            mask_status = "ok_expected_empty"
            flags.append("AbnormalWithoutPixelAnnotationTIF")
        elif lclass == "Normal_Control":
            mask_status = "ok_expected_empty"

        out.append(
            LabelRecord(
                ImageID=img_id,
                DatasetID="DS0002",
                PatientGroupID=row["PatientGroupID"],
                SourceStem=stem,
                DispositionQC=disp,
                Paradigm="WholeBreast_FFDM",
                BinaryTarget=btarget,
                LabelClass=lclass,
                LabelProvenanceTier=ptier,
                SubTrackA_BiopsyEligible=sub_a,
                SubTrackB_ScreeningEligible=sub_b,
                LesionTrack_BenignVsMalignant=les_t,
                RawLabelTokens=f"cls={','.join(sorted(cls_tokens))};abn={','.join(abn_tokens)};rep_birads={birads_str}",
                MultiLesionConflict=conflict,
                ViewPosition=view,
                Laterality=lat,
                DensityACR=density,
                MorphologyType=morph,
                BIRADSScore=birads_str,
                ClinicalConcStatus=conc,
                LocalizationEligible=loc_eligible,
                MaskSourceType="DMID_RGBA_ContourFill" if has_tif else "None",
                MaskStatus=mask_status,
                MaskWidth=mask_w,
                MaskHeight=mask_h,
                ImageWidth=w,
                ImageHeight=h,
                MaskForegroundPixels=mask_fg,
                MaskCoveragePct=mask_cov,
                MaskComponentCount=mask_comp,
                ExtraMaskTelemetry=extra_mask,
                AnomalyFlags=";".join(flags),
                RawRelativePath=rel_path,
                MaskRelativePath=f"Pixel-level annotation/{stem}.tif" if has_tif else "",
            )
        )
    return out


def _harmonize_mias(
    spec: LabelCohortSpec,
    primary_rows: list[dict[str, str]],
    verify_mask_ids: set[str] | None = None,
) -> list[LabelRecord]:
    """Harmonize `DS0001 MIAS v1.21` historical labels and (x, y, radius) coarse circles."""
    pdf_candidates = list(spec.raw_dir.rglob("00README.pdf"))
    txt_candidates = list(spec.raw_dir.rglob("00README.txt"))
    rows_parsed: list[dict[str, Any]] = []
    if txt_candidates:
        rows_parsed = _parse_mias_lines(txt_candidates[0].read_text(encoding="utf-8", errors="replace").splitlines())
    elif pdf_candidates:
        rows_parsed = parse_mias_00readme_text(pdf_candidates[0])
    else:
        raise FileNotFoundError(f"Missing MIAS 00README.pdf / 00README.txt inside {spec.raw_dir}")

    by_stem: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    by_ref: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for r in rows_parsed:
        by_stem[r["stem"]].append(r)
        by_ref[r["ref_id"]].append(r)

    out: list[LabelRecord] = []
    for row in primary_rows:
        img_id = row["ImageID"]
        rel_path = row["RawRelativePath"]
        stem = Path(rel_path).stem.strip()
        ref = stem[:6]
        disp = row["Disposition"]
        w = _safe_int(row.get("QCWidth", ""))
        h = _safe_int(row.get("QCHeight", ""))
        if w is None or h is None:
            h, w = _load_image_hw(spec.raw_dir / rel_path)

        m_rows = by_stem.get(stem) or by_ref.get(ref, [])
        if not m_rows:
            raise ValueError(f"MIAS image missing in 00README metadata: {stem}")

        sevs = {r["sev"] for r in m_rows}
        abns = sorted({r["abn"] for r in m_rows})
        bg = m_rows[0]["bg"]
        lat = "L" if (len(stem) > 6 and stem[6] == "l") else ("R" if (len(stem) > 6 and stem[6] == "r") else "unknown")
        morph = "none" if abns == ["NORM"] else ("calcification" if abns == ["CALC"] else "mass_or_other")

        flags: list[str] = []
        conflict = False
        if disp != "Retained":
            btarget, lclass, ptier, sub_a, sub_b, les_t = "Excluded", disp, "Excluded", False, False, False
            conc = "quarantined_step013"
        elif sevs == {"NORM"}:
            btarget, lclass, ptier = "0", "Normal_Control", "TierB_Historical_SFM"
            sub_a, sub_b, les_t = False, True, False
            conc = "ok_sfm_normal"
        elif "M" in sevs:
            conflict = "B" in sevs
            if conflict:
                flags.append("MultiLesionBM_MalignantDominance")
            btarget, lclass, ptier = "1", "Malignant", "TierB_Historical_SFM"
            sub_a, sub_b, les_t = False, True, True
            conc = "ok_sfm_malignant"
        elif sevs == {"B"}:
            btarget, lclass, ptier = "0", "Benign_Lesion", "TierB_Historical_SFM"
            sub_a, sub_b, les_t = False, True, True
            conc = "ok_sfm_benign"
        else:
            raise ValueError(f"Unmapped MIAS severity tokens {sevs} for {stem}")

        circles = [(float(r["x"]), float(r["y"]), float(r["r"])) for r in m_rows if r["x"] is not None and r["y"] is not None and r["r"] is not None]
        should_verify = verify_mask_ids is None or img_id in verify_mask_ids
        mask_status = "ok_expected_empty"
        mask_w, mask_h, mask_fg, mask_cov, mask_comp = None, None, 0, 0.0, 0
        loc_eligible = False
        extra_mask = ""

        if circles and btarget != "Excluded":
            if any(x >= w or y >= h for x, y, _ in circles):
                flags.append("MIAS_CircleCenterOutsideImage")
            if should_verify:
                m_arr = rasterize_mias_circle(circles, h, w, y_from_bottom=True)
                mask_w, mask_h = w, h
                mask_fg = int(m_arr.sum())
                mask_cov = round(100.0 * mask_fg / max(h * w, 1), 4)
                mask_comp = len(circles)
                mask_status = "ok_nonempty" if mask_fg > 0 else "empty_unexpected"
                loc_eligible = mask_fg > 0
                extra_mask = f"circles={circles}"
            else:
                mask_status = "present_unrasterized"
                mask_comp = len(circles)
                loc_eligible = True
        elif btarget != "Excluded" and lclass in {"Malignant", "Benign_Lesion"}:
            mask_status = "excluded_by_protocol"
            flags.append("Excluded_NoRadiusForROI")

        out.append(
            LabelRecord(
                ImageID=img_id,
                DatasetID="DS0001",
                PatientGroupID=row["PatientGroupID"],
                SourceStem=stem,
                DispositionQC=disp,
                Paradigm="WholeBreast_SFM",
                BinaryTarget=btarget,
                LabelClass=lclass,
                LabelProvenanceTier=ptier,
                SubTrackA_BiopsyEligible=sub_a,
                SubTrackB_ScreeningEligible=sub_b,
                LesionTrack_BenignVsMalignant=les_t,
                RawLabelTokens=f"bg={bg};abn={','.join(abns)};sev={','.join(sorted(sevs))}",
                MultiLesionConflict=conflict,
                ViewPosition="MLO",
                Laterality=lat,
                DensityACR=bg,
                MorphologyType=morph,
                BIRADSScore="not_reported",
                ClinicalConcStatus=conc,
                LocalizationEligible=loc_eligible,
                MaskSourceType="MIAS_Circle_YFlip" if circles else "None",
                MaskStatus=mask_status,
                MaskWidth=mask_w,
                MaskHeight=mask_h,
                ImageWidth=w,
                ImageHeight=h,
                MaskForegroundPixels=mask_fg,
                MaskCoveragePct=mask_cov,
                MaskComponentCount=mask_comp,
                ExtraMaskTelemetry=extra_mask,
                AnomalyFlags=";".join(flags),
                RawRelativePath=rel_path,
                MaskRelativePath="00README.pdf" if circles else "",
            )
        )
    return out


# ---------------------------------------------------------------------------
# Stratified Pilot Sampler (`T09 §7`, seed=20261128, N=170) & Visual Overlays
# ---------------------------------------------------------------------------


def _pick_deterministic(
    pool: list[LabelRecord],
    k: int,
    rng: random.Random,
    seen: set[str],
) -> list[LabelRecord]:
    avail = [r for r in pool if r.ImageID not in seen]
    if len(avail) <= k:
        picked = list(avail)
    else:
        picked = rng.sample(avail, k)
    for p in picked:
        seen.add(p.ImageID)
    return picked


def sample_pilot_records(
    dataset_id: str,
    records: list[LabelRecord],
    seed: int = DEFAULT_PILOT_SEED,
) -> list[LabelRecord]:
    """Deterministically draw the STEP-016 stratified pilot sample per T09 §7."""
    rng = random.Random(f"{seed}::{dataset_id}")
    seen: set[str] = set()
    picked: list[LabelRecord] = []

    if dataset_id == "DS0003":
        # Mandatory inclusion of the 2x 16-bit CMMD DICOMs (`IMG00003519`, `IMG00003520`).
        for r in records:
            if r.ImageID in {"IMG00003519", "IMG00003520"} and r.ImageID not in seen:
                picked.append(r)
                seen.add(r.ImageID)
        picked.extend(_pick_deterministic([r for r in records if "BilateralDiscordantPatient" in r.AnomalyFlags], 10, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Excluded_UnlabeledContralateral"], 10, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Malignant"], max(0, 20 - sum(1 for x in picked if x.LabelClass == "Malignant")), rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Benign_Biopsy"], max(0, 20 - sum(1 for x in picked if x.LabelClass == "Benign_Biopsy")), rng, seen))
        if len(picked) < 60:
            picked.extend(_pick_deterministic(records, 60 - len(picked), rng, seen))
    elif dataset_id == "DS0006":
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Malignant" and r.LocalizationEligible], 15, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Benign_Biopsy" and r.LocalizationEligible], 15, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Normal_Control"], 5, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass.startswith(("Excluded_PostOperative", "Excluded_PostNAC"))], 5, rng, seen))
        if len(picked) < 40:
            picked.extend(_pick_deterministic(records, 40 - len(picked), rng, seen))
    elif dataset_id == "DS0005":
        picked.extend(_pick_deterministic([r for r in records if r.BinaryTarget == "1"], 8, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Benign_Biopsy"], 8, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Normal_Control"], 4, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Excluded_PriorScreeningRound"], 4, rng, seen))
        if len(picked) < 24:
            picked.extend(_pick_deterministic(records, 24 - len(picked), rng, seen))
    elif dataset_id == "DS0002":
        picked.extend(_pick_deterministic([r for r in records if r.BinaryTarget == "1" and r.LocalizationEligible], 10, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Benign_Lesion" and r.LocalizationEligible], 10, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Normal_Control"], 5, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Excluded_AmbiguousClassToken_N"], 5, rng, seen))
        if len(picked) < 30:
            picked.extend(_pick_deterministic(records, 30 - len(picked), rng, seen))
    elif dataset_id == "DS0001":
        picked.extend(_pick_deterministic([r for r in records if r.BinaryTarget == "1" and r.LocalizationEligible], 6, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Benign_Lesion" and r.LocalizationEligible], 6, rng, seen))
        picked.extend(_pick_deterministic([r for r in records if r.LabelClass == "Normal_Control"], 4, rng, seen))
        if len(picked) < 16:
            picked.extend(_pick_deterministic(records, 16 - len(picked), rng, seen))
    else:
        picked = list(records[:20])

    return picked


def _build_record_overlay_mask(spec: LabelCohortSpec, rec: LabelRecord, orig_h: int, orig_w: int) -> np.ndarray | None:
    """Recompute binary/colored overlay mask at native resolution ONLY for sampled overlay plates."""
    if spec.dataset_id == "DS0006" and rec.MaskRelativePath:
        seg_csv = spec.raw_dir / "metadata" / "Radiology_hand_drawn_segmentations_v2.csv"
        if not seg_csv.is_file():
            seg_csv = spec.raw_dir / "Radiology_hand_drawn_segmentations_v2.csv"
        fname = Path(rec.RawRelativePath).name
        seg_df = pd.read_csv(seg_csv)
        shapes = [json.loads(str(r["region_shape_attributes"])) for _, r in seg_df[seg_df["#filename"].str.strip() == fname].iterrows()]
        if shapes:
            m, _, _ = rasterize_cdd_cesm_shapes(shapes, orig_h, orig_w)
            return m
    elif spec.dataset_id == "DS0002" and rec.MaskRelativePath:
        m, _ = extract_dmid_rgba_mask(spec.raw_dir / rec.MaskRelativePath)
        return m
    elif spec.dataset_id == "DS0005" and rec.MaskRelativePath:
        m, _ = extract_bmcd_gt_channels(spec.raw_dir / rec.MaskRelativePath, target_h=orig_h, target_w=orig_w, mode="lesion_red_blue")
        return m
    elif spec.dataset_id == "DS0001" and rec.MaskRelativePath:
        m_list = re.findall(r"\(([^()]+)\)", rec.ExtraMaskTelemetry)
        if m_list:
            circles = []
            for tup in re.findall(r"\(([\d.]+),\s*([\d.]+),\s*([\d.]+)\)", rec.ExtraMaskTelemetry):
                circles.append((float(tup[0]), float(tup[1]), float(tup[2])))
            if circles:
                return rasterize_mias_circle(circles, orig_h, orig_w, y_from_bottom=True)
    return None


def render_pilot_overlay_sheet(
    spec: LabelCohortSpec,
    pilot_records: list[LabelRecord],
    out_png: Path,
    max_panels: int = 16,
    grid_cols: int = 4,
) -> Path | None:
    """Render Tier-2 visual mammogram + ROI mask overlay plate using strictly pseudonymous tags."""
    if not pilot_records:
        return None
    # Prioritize mask-positive cases alongside representative Normal/Excluded controls.
    with_mask = [r for r in pilot_records if r.MaskForegroundPixels > 0]
    others = [r for r in pilot_records if r.MaskForegroundPixels == 0]
    shown: list[LabelRecord] = (with_mask[:12] + others[: max(0, max_panels - len(with_mask[:12]))])[:max_panels]
    if not shown:
        shown = pilot_records[:max_panels]

    n_rows = max(1, math.ceil(len(shown) / grid_cols))
    cell_w, cell_h, header_h = 270, 305, 38
    canvas = Image.new("RGB", (grid_cols * cell_w, header_h + n_rows * cell_h), (20, 22, 26))
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (12, 10),
        f"{spec.dataset_id} ({spec.display_name}) Pilot Label & ROI-Mask Overlay Check | N={len(pilot_records)} (shown={len(shown)})",
        fill=(235, 242, 250),
    )

    for idx, rec in enumerate(shown):
        r_i, c_i = divmod(idx, grid_cols)
        x0 = c_i * cell_w + 10
        y0 = header_h + r_i * cell_h + 6
        gray_u8, orig_h, orig_w = _load_preview_uint8(spec.raw_dir / rec.RawRelativePath, max_dim=246)
        rgb_panel = cv2.cvtColor(gray_u8, cv2.COLOR_GRAY2RGB)

        mask_full = _build_record_overlay_mask(spec, rec, orig_h, orig_w)
        if mask_full is not None and mask_full.shape == (orig_h, orig_w) and mask_full.any():
            m_small = cv2.resize(mask_full, (gray_u8.shape[1], gray_u8.shape[0]), interpolation=cv2.INTER_NEAREST)
            # Overlay filled ROI softly in cyan and trace bright yellow/red outline
            hit = m_small > 0
            rgb_panel[hit, 1] = np.clip(rgb_panel[hit, 1].astype(int) + 70, 0, 255).astype(np.uint8)
            rgb_panel[hit, 2] = np.clip(rgb_panel[hit, 2].astype(int) + 110, 0, 255).astype(np.uint8)
            cnts, _ = cv2.findContours(m_small.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(rgb_panel, cnts, -1, (255, 65, 65), 2)

        # For BMCD, overlay GT Green contours faintly in yellow so green border vs red/blue lesion distinction is visually audited
        if spec.dataset_id == "DS0005" and rec.MaskRelativePath:
            with Image.open(spec.raw_dir / rec.MaskRelativePath) as im_gt:
                gt_rgb = np.asarray(im_gt.convert("RGB")).astype(np.int16)
            g_mask = ((gt_rgb[..., 1] - np.maximum(gt_rgb[..., 0], gt_rgb[..., 2])) > 35).astype(np.uint8)
            if g_mask.any():
                g_small = cv2.resize(g_mask, (gray_u8.shape[1], gray_u8.shape[0]), interpolation=cv2.INTER_NEAREST) > 0
                rgb_panel[g_small] = np.array([220, 210, 40], dtype=np.uint8)

        # For MIAS, also draw non-flipped reference circle in yellow dashed/thin so flip orientation is visually verifiable
        if spec.dataset_id == "DS0001" and rec.ExtraMaskTelemetry:
            for tup in re.findall(r"\(([\d.]+),\s*([\d.]+),\s*([\d.]+)\)", rec.ExtraMaskTelemetry):
                cx_s = int(round(float(tup[0]) * gray_u8.shape[1] / max(orig_w, 1)))
                cy_top = int(round(float(tup[1]) * gray_u8.shape[0] / max(orig_h, 1)))
                rad_s = max(2, int(round(float(tup[2]) * gray_u8.shape[1] / max(orig_w, 1))))
                cv2.circle(rgb_panel, (cx_s, cy_top), rad_s, (240, 220, 40), 1)

        padded = ImageOps.pad(Image.fromarray(rgb_panel, mode="RGB"), (246, 246), color=(14, 14, 16))
        canvas.paste(padded, (x0, y0))
        c1 = f"{rec.ImageID} | {rec.ViewPosition}/{rec.Laterality} | T={rec.BinaryTarget}"
        c2 = f"{rec.LabelClass[:26]} | cov={rec.MaskCoveragePct:.1f}%"
        draw.text((x0, y0 + 250), c1, fill=(215, 232, 255))
        draw.text((x0, y0 + 266), c2, fill=(175, 225, 195) if rec.MaskForegroundPixels > 0 else (195, 195, 200))

    out_png.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_png)
    return out_png


# ---------------------------------------------------------------------------
# Public Orchestration Entrypoints (`STEP-016` Pilot & `STEP-017` Full)
# ---------------------------------------------------------------------------


_HARMONIZERS: dict[str, Callable[..., list[LabelRecord]]] = {
    "DS0001": _harmonize_mias,
    "DS0002": _harmonize_dmid,
    "DS0003": _harmonize_cmmd,
    "DS0005": _harmonize_bmcd,
    "DS0006": _harmonize_cdd_cesm,
}


def _collect_discrepancies(records: list[LabelRecord]) -> list[dict[str, str]]:
    """Build Tier-1-safe discrepancy/flag summary keyed strictly by pseudonymous ImageID."""
    out: list[dict[str, str]] = []
    for r in records:
        if r.MultiLesionConflict or r.AnomalyFlags or r.MaskStatus in {"missing", "unreadable_or_corrupt", "dimension_mismatch", "empty_unexpected"}:
            out.append(
                {
                    "DatasetID": r.DatasetID,
                    "ImageID": r.ImageID,
                    "PatientGroupID": r.PatientGroupID,
                    "BinaryTarget": r.BinaryTarget,
                    "LabelClass": r.LabelClass,
                    "MaskStatus": r.MaskStatus,
                    "AnomalyFlags": r.AnomalyFlags,
                }
            )
    return out


def audit_cohort_labels(
    spec: LabelCohortSpec,
    tier2_native_dir: Path,
    tier2_overlays_dir: Path,
    mode: str = "pilot",
    seed: int = DEFAULT_PILOT_SEED,
) -> tuple[CohortAuditSummary, list[LabelRecord]]:
    """Run T09 label & ROI-mask verification on one cohort in `pilot` or `full` mode."""
    primary_rows = _load_linkage_and_qc(spec)
    if spec.dataset_id not in _HARMONIZERS:
        raise ValueError(f"Unsupported dataset_id for label verification: {spec.dataset_id}")

    harmonizer = _HARMONIZERS[spec.dataset_id]
    # Fast metadata pass first so `pilot` knows strata before touching full image/mask pixel buffers
    if spec.dataset_id == "DS0003":
        all_records = _harmonize_cmmd(spec, primary_rows)
        audited = sample_pilot_records(spec.dataset_id, all_records, seed=seed) if mode == "pilot" else all_records
    else:
        meta_only = harmonizer(spec, primary_rows, verify_mask_ids=set())
        if mode == "pilot":
            pilot_ids = {r.ImageID for r in sample_pilot_records(spec.dataset_id, meta_only, seed=seed)}
            sub_rows = [row for row in primary_rows if row["ImageID"] in pilot_ids]
            audited = harmonizer(spec, sub_rows, verify_mask_ids=pilot_ids)
        else:
            all_ids = {row["ImageID"] for row in primary_rows}
            audited = harmonizer(spec, primary_rows, verify_mask_ids=all_ids)

    tier2_native_dir.mkdir(parents=True, exist_ok=True)
    out_csv = tier2_native_dir / f"{spec.dataset_id}_{mode}_labels.csv"
    fieldnames = list(LabelRecord.__dataclass_fields__.keys())
    with out_csv.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        for r in audited:
            writer.writerow(asdict(r))

    overlay_path = render_pilot_overlay_sheet(
        spec,
        audited,
        tier2_overlays_dir / f"{spec.dataset_id}_{mode}_overlays.png",
    )

    retained_qc = sum(1 for row in primary_rows if row["Disposition"] == "Retained")
    bt_counts = dict(sorted(collections.Counter(r.BinaryTarget for r in audited).items()))
    lc_counts = dict(sorted(collections.Counter(r.LabelClass for r in audited).items()))
    pt_counts = dict(sorted(collections.Counter(r.LabelProvenanceTier for r in audited).items()))
    ms_counts = dict(sorted(collections.Counter(r.MaskStatus for r in audited).items()))
    cc_counts = dict(sorted(collections.Counter(r.ClinicalConcStatus for r in audited).items()))
    af_counts: collections.Counter[str] = collections.Counter()
    for r in audited:
        if r.AnomalyFlags:
            for tok in r.AnomalyFlags.split(";"):
                if tok:
                    af_counts[tok] += 1

    closure_ok = (bt_counts.get("0", 0) + bt_counts.get("1", 0) + bt_counts.get("Excluded", 0)) == len(audited)
    discrepancies = _collect_discrepancies(audited)

    summary = CohortAuditSummary(
        dataset_id=spec.dataset_id,
        display_name=spec.display_name or spec.dataset_id,
        mode=mode,
        total_primary_acquired=len(primary_rows),
        total_qc_retained=retained_qc,
        total_audited=len(audited),
        binary_target_counts=bt_counts,
        label_class_counts=lc_counts,
        provenance_tier_counts=pt_counts,
        subtrack_a_count=sum(1 for r in audited if r.SubTrackA_BiopsyEligible),
        subtrack_b_count=sum(1 for r in audited if r.SubTrackB_ScreeningEligible),
        lesion_track_count=sum(1 for r in audited if r.LesionTrack_BenignVsMalignant),
        multi_lesion_conflict_count=sum(1 for r in audited if r.MultiLesionConflict),
        localization_eligible_count=sum(1 for r in audited if r.LocalizationEligible),
        mask_status_counts=ms_counts,
        concordance_counts=cc_counts,
        anomaly_flag_counts=dict(sorted(af_counts.items())),
        arithmetic_closure_ok=closure_ok,
        discrepancies=discrepancies,
        tier2_labels_csv=str(out_csv.as_posix()),
        tier2_overlay_png=str(overlay_path.as_posix()) if overlay_path else "",
    )
    return summary, audited


def default_label_specs(root: Path) -> list[LabelCohortSpec]:
    """Return canonical G04-approved 5-cohort specs for S08 (`DS0004_CBIS_DDSM` untouched)."""
    manifests = root / "03_Datasets" / "manifests"
    qc_dir = root / "03_Datasets" / "cache" / "qc"
    raw = root / "03_Datasets" / "raw"
    return [
        LabelCohortSpec("DS0001", raw / "DS0001_MIAS", manifests / "DS0001_private_linkage.csv", qc_dir / "DS0001_qc_details.csv", "MIAS v1.21"),
        LabelCohortSpec("DS0002", raw / "DS0002_DMID", manifests / "DS0002_private_linkage.csv", qc_dir / "DS0002_qc_details.csv", "DMID"),
        LabelCohortSpec("DS0003", raw / "DS0003_CMMD", manifests / "DS0003_private_linkage.csv", qc_dir / "DS0003_qc_details.csv", "CMMD"),
        LabelCohortSpec("DS0005", raw / "DS0005_BMCD", manifests / "DS0005_private_linkage.csv", qc_dir / "DS0005_qc_details.csv", "BMCD"),
        LabelCohortSpec("DS0006", raw / "DS0006_CDD_CESM", manifests / "DS0006_private_linkage.csv", qc_dir / "DS0006_qc_details.csv", "CDD-CESM (LE)"),
    ]


def run_label_verification(
    specs: list[LabelCohortSpec],
    tier2_native_dir: Path,
    tier2_overlays_dir: Path,
    mode: str = "pilot",
    seed: int = DEFAULT_PILOT_SEED,
) -> dict[str, Any]:
    """Execute S08 label & ROI-mask verification across supplied cohorts and persist Tier-2 JSON."""
    generated_at = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summaries: list[dict[str, Any]] = []
    for spec in specs:
        print(f"[LABEL-VERIFY:{mode}] Processing {spec.dataset_id} ({spec.display_name})...", flush=True)
        summary, _ = audit_cohort_labels(
            spec,
            tier2_native_dir=tier2_native_dir,
            tier2_overlays_dir=tier2_overlays_dir,
            mode=mode,
            seed=seed,
        )
        summaries.append(asdict(summary))

    payload = {
        "generated_at": generated_at,
        "mode": mode,
        "seed": seed,
        "cohorts": summaries,
    }
    tier2_native_dir.mkdir(parents=True, exist_ok=True)
    summary_json = tier2_native_dir / f"{mode}_verification_summary.json"
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    payload["summary_json_path"] = str(summary_json.as_posix())
    return payload


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for STEP-016 (`--mode pilot`) and STEP-017 (`--mode full`) execution."""
    parser = argparse.ArgumentParser(description="S08 T09 Diagnostic Label & ROI-Mask Verifier")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--mode", choices=["pilot", "full"], default="pilot")
    parser.add_argument("--seed", type=int, default=DEFAULT_PILOT_SEED)
    args = parser.parse_args(argv)

    root = args.root.resolve()
    payload = run_label_verification(
        specs=default_label_specs(root),
        tier2_native_dir=root / "04_Labels_XAI_Governance" / "native",
        tier2_overlays_dir=root / "04_Labels_XAI_Governance" / "restricted_masks" / "pilot_overlays",
        mode=args.mode,
        seed=args.seed,
    )
    for c in payload["cohorts"]:
        print(
            f"[DONE] {c['dataset_id']} ({c['mode']}): audited={c['total_audited']}/{c['total_primary_acquired']} | "
            f"targets={c['binary_target_counts']} | masks={c['mask_status_counts']} | "
            f"closure={c['arithmetic_closure_ok']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

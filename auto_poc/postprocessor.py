from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from auto_poc.context import PROJECTS_DIR
from auto_poc.cwe_data import validate_cwe_id
from auto_poc.schemas import PocReport


def validate_and_build_report(raw_report: dict) -> PocReport:
    if not validate_cwe_id(raw_report.get("weakness", {}).get("cwe_id", "")):
        raw_report.setdefault("weakness", {})["cwe_id"] = None
        raw_report["weakness"]["cwe_name"] = None

    chaining = raw_report.get("description", {}).get("chaining_analysis")
    if chaining is not None:
        chaining["status"] = "suggested"

    return PocReport.model_validate(raw_report)


def save_report(project_id: str, report: PocReport) -> Path:
    reports_dir = PROJECTS_DIR / project_id / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.json"
    filepath = reports_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report.model_dump(), f, indent=2, ensure_ascii=False)

    return filepath

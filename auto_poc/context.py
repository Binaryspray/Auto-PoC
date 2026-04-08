from __future__ import annotations

import json
from pathlib import Path


PROJECTS_DIR = Path("projects")


def load_existing_reports(project_id: str) -> list[dict]:
    reports_dir = PROJECTS_DIR / project_id / "reports"

    if not reports_dir.exists():
        return []

    reports = []
    for report_file in sorted(reports_dir.glob("report_*.json")):
        with open(report_file, encoding="utf-8") as f:
            data = json.load(f)
            data["_filename"] = report_file.name
            reports.append(data)

    return reports

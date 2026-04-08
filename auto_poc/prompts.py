from __future__ import annotations

import json

from auto_poc.schemas import PocInput


SYSTEM_PROMPT = """\
You are an expert bug bounty report writer for HackerOne.
Your task is to generate a professional vulnerability report in JSON format.

Requirements:
- Focus on Root Cause and Impact
- Map to a real, existing CWE ID (do NOT hallucinate CWE numbers)
- Include MITRE ATT&CK TTPs mapping (Tactic / Technique ID)
- Write at a level immediately actionable by security engineers
- Severity must be one of: none, low, medium, high, critical (based on CVSS criteria)
- All CWE IDs must follow the format CWE-XXX with real numbers

Output ONLY valid JSON matching this schema (no markdown, no explanation):
{
  "title": "string",
  "asset": "string",
  "weakness": {"cwe_id": "CWE-XXX", "cwe_name": "string"},
  "severity": "none|low|medium|high|critical",
  "description": {
    "summary": "string",
    "steps_to_reproduce": ["string"],
    "recommendations": ["string"],
    "references": ["string"]
  },
  "impact": "string",
  "attachments": []
}"""


def build_user_prompt(
    poc_input: PocInput,
    asset: str,
    report_template: str,
    existing_reports: list[dict],
) -> str:
    sections = []

    sections.append("## Vulnerability Data")
    sections.append(json.dumps(poc_input.model_dump(), indent=2, ensure_ascii=False))

    sections.append(f"\n## Resolved Asset\n{asset}")

    sections.append(f"\n## Report Template\n{report_template}")

    if existing_reports:
        sections.append("\n## Existing Reports (for chaining analysis)")
        for i, report in enumerate(existing_reports, 1):
            sections.append(f"\n### Report {i}")
            sections.append(json.dumps(report, indent=2, ensure_ascii=False))
        sections.append(
            "\nAnalyze if the current vulnerability can be chained with any "
            "existing vulnerabilities above. If chaining is possible, add a "
            "dedicated section in the summary explaining: which vulnerability "
            "it chains with, how, and the escalated risk level."
        )

    return "\n".join(sections)

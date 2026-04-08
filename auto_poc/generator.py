from __future__ import annotations

import json

from litellm import completion

from auto_poc.prompts import SYSTEM_PROMPT, build_user_prompt
from auto_poc.schemas import PocInput


DEFAULT_MODEL = "claude-sonnet-4-20250514"


def generate_report_via_llm(
    poc_input: PocInput,
    asset: str,
    report_template: str,
    existing_reports: list[dict],
    model: str = DEFAULT_MODEL,
) -> dict:
    user_prompt = build_user_prompt(poc_input, asset, report_template, existing_reports)

    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    raw_content = response.choices[0].message.content
    return json.loads(raw_content)

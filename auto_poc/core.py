from __future__ import annotations

from auto_poc.context import load_existing_reports
from auto_poc.generator import (
    DEFAULT_BACKEND,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    generate_report_via_llm,
)
from auto_poc.postprocessor import save_report, validate_and_build_report
from auto_poc.preprocessor import get_report_template, resolve_asset, validate_input


def generate_report(
    input_data: dict,
    backend: str = DEFAULT_BACKEND,
    provider: str = DEFAULT_PROVIDER,
    model: str = DEFAULT_MODEL,
    save: bool = True,
) -> dict:
    # 1. 입력 전처리
    poc_input = validate_input(input_data)
    asset = resolve_asset(poc_input)
    template = get_report_template(poc_input)

    # 2. 체이닝 컨텍스트 조회
    existing_reports = load_existing_reports(poc_input.project_id)

    # 3. LLM 보고서 생성
    raw_report = generate_report_via_llm(
        poc_input=poc_input,
        asset=asset,
        report_template=template,
        existing_reports=existing_reports,
        backend=backend,
        provider=provider,
        model=model,
    )

    # 4. 후처리
    raw_report["asset"] = asset
    report = validate_and_build_report(raw_report)

    if save:
        filepath = save_report(poc_input.project_id, report)
        result = report.model_dump()
        result["_saved_to"] = str(filepath)
        return result

    return report.model_dump()

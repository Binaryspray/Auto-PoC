from __future__ import annotations

from auto_poc.schemas import PocInput


H1_DEFAULT_TEMPLATE = """\
## Summary:
{summary}

## Steps To Reproduce:
{steps}

## Recommendations:
{recommendations}

## Supporting Material/References:
{references}"""


def validate_input(raw: dict) -> PocInput:
    return PocInput.model_validate(raw)


def resolve_asset(poc_input: PocInput) -> str:
    subdomain = poc_input.target.subdomain
    attack_point = poc_input.target.attack_point
    scope = poc_input.program_info.scope

    for entry in scope:
        if subdomain in entry or attack_point in entry:
            return entry

    return subdomain


def get_report_template(poc_input: PocInput) -> str:
    if poc_input.program_info.report_template:
        return poc_input.program_info.report_template
    return H1_DEFAULT_TEMPLATE

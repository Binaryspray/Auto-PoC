from __future__ import annotations

import json
import os
import re
import shutil
import subprocess

from auto_poc.prompts import SYSTEM_PROMPT, build_user_prompt
from auto_poc.schemas import PocInput

# ── 기본값 ──
# backend: "cli" 또는 "api"
DEFAULT_BACKEND = os.getenv("LLM_BACKEND", "cli")
# cli provider: "claude" 또는 "codex"
DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "claude")
# api model (LiteLLM 포맷)
DEFAULT_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-4-20250514")


def generate_report_via_llm(
    poc_input: PocInput,
    asset: str,
    report_template: str,
    existing_reports: list[dict],
    backend: str | None = None,
    provider: str | None = None,
    model: str | None = None,
) -> dict:
    backend = backend or DEFAULT_BACKEND
    provider = provider or DEFAULT_PROVIDER
    model = model or DEFAULT_MODEL

    user_prompt = build_user_prompt(poc_input, asset, report_template, existing_reports)
    full_prompt = f"{SYSTEM_PROMPT}\n\n{user_prompt}"

    if backend == "cli":
        raw = _query_cli(full_prompt, provider)
    elif backend == "api":
        raw = _query_api(user_prompt, model)
    else:
        raise ValueError(f"Unknown backend: {backend}. Use 'cli' or 'api'.")

    return _extract_json(raw)


# ── CLI 백엔드 ──

def _query_cli(prompt: str, provider: str) -> str:
    if provider == "claude":
        return _query_claude(prompt)
    elif provider == "codex":
        return _query_codex(prompt)

    # 자동 감지
    if shutil.which("claude"):
        return _query_claude(prompt)
    if shutil.which("codex"):
        return _query_codex(prompt)

    raise RuntimeError(
        "LLM CLI를 찾을 수 없습니다. claude 또는 codex를 설치해주세요.\n"
        "또는 --backend api 로 API 모드를 사용하세요."
    )


def _query_claude(prompt: str) -> str:
    if not shutil.which("claude"):
        raise RuntimeError("claude CLI가 설치되어있지 않습니다.")

    result = subprocess.run(
        ["claude", "--print", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude 호출 실패: {result.stderr}")
    return result.stdout.strip()


def _query_codex(prompt: str) -> str:
    if not shutil.which("codex"):
        raise RuntimeError("codex CLI가 설치되어있지 않습니다.")

    result = subprocess.run(
        ["codex", "exec", "--full-auto", "--skip-git-repo-check", "-q", prompt],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"codex 호출 실패: {result.stderr}")
    return result.stdout.strip()


# ── API 백엔드 ──

def _query_api(user_prompt: str, model: str) -> str:
    from litellm import completion

    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


# ── JSON 추출 ──

def _extract_json(raw: str) -> dict:
    # 먼저 그대로 파싱 시도
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # markdown 코드블록에서 JSON 추출
    match = re.search(r"```(?:json)?\s*\n(.*?)\n```", raw, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    # 첫 번째 { ... 마지막 } 추출
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1:
        return json.loads(raw[start:end + 1])

    raise ValueError(f"LLM 응답에서 JSON을 추출할 수 없습니다:\n{raw[:500]}")

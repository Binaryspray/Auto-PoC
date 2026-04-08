# Auto-PoC

HackerOne 버그바운티 취약점 분석 보고서 자동 생성 도구.

Solve 단계의 취약점 테스트 결과를 입력받아, LLM 기반으로 HackerOne 제출용 보고서를 자동 생성합니다.

## 주요 기능

- HackerOne 보고서 포맷 자동 생성 (title, asset, weakness, severity, description, impact)
- CWE 및 MITRE ATT&CK TTPs 자동 매핑
- 기존 보고서 기반 취약점 체이닝 분석
- CWE ID 유효성 검증 (할루시네이션 방지)
- 다중 LLM 지원: CLI 백엔드 (Claude Code, Codex) + API 백엔드 (LiteLLM)

## 설치

```bash
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## 환경 설정

`.env.example`을 복사하여 `.env` 파일을 생성합니다.

```bash
cp .env.example .env
```

```env
# ── 백엔드 설정 ──
LLM_BACKEND=cli          # cli (기본값) 또는 api

# ── CLI 모드 설정 ──
LLM_PROVIDER=claude       # claude (기본값) 또는 codex

# ── API 모드 설정 ──
LLM_MODEL=claude-sonnet-4-20250514
# ANTHROPIC_API_KEY=sk-ant-...
# GEMINI_API_KEY=AIzaSy...
# OPENAI_API_KEY=sk-...
```

## 사용법

두 가지 백엔드를 지원합니다:
- **CLI 백엔드** (기본값) — `claude` 또는 `codex` CLI를 직접 호출. API 키 불필요, 기존 구독 활용.
- **API 백엔드** — LiteLLM을 통해 Claude, Gemini, GPT 등 호출. API 키 필요.

### CLI 백엔드 (기본값)

```bash
# Claude Code CLI 사용 (기본값)
python -m auto_poc -i input.json

# Codex CLI 사용
python -m auto_poc -i input.json -p codex

# 출력 파일 지정
python -m auto_poc -i input.json -o report.json

# 프로젝트 폴더에 저장하지 않기
python -m auto_poc -i input.json --no-save
```

### API 백엔드

```bash
# Gemini API 사용
python -m auto_poc -i input.json -b api -m gemini/gemini-2.5-flash

# Claude API 사용
python -m auto_poc -i input.json -b api -m claude-sonnet-4-20250514

# OpenAI API 사용
python -m auto_poc -i input.json -b api -m gpt-4o
```

### 라이브러리

```python
from auto_poc import generate_report

# CLI 백엔드 (기본값)
report = generate_report(input_data)

# API 백엔드
report = generate_report(input_data, backend="api", model="gemini/gemini-2.5-flash")
```

## 입력 JSON 형식

```json
{
  "project_id": "example_project",
  "target": {
    "subdomain": "api.example.com",
    "attack_point": "/api/v1/users"
  },
  "vulnerability": {
    "type": "IDOR",
    "payload": "GET /api/v1/users/1337 with another user's token",
    "test_result": "200 OK - returned victim's PII",
    "reproduction_steps": [
      "Login as user A and capture Bearer token",
      "Send GET /api/v1/users/{victim_id} with user A's token",
      "Observe unauthorized access to victim's PII"
    ]
  },
  "program_info": {
    "platform": "hackerone",
    "program_name": "Example Corp",
    "scope": ["*.example.com"],
    "report_template": null
  }
}
```

## 출력 JSON 형식

```json
{
  "title": "IDOR on /api/v1/users endpoint",
  "asset": "api.example.com",
  "weakness": { "cwe_id": "CWE-639", "cwe_name": "Authorization Bypass Through User-Controlled Key" },
  "severity": "high",
  "description": {
    "summary": "...",
    "steps_to_reproduce": ["..."],
    "recommendations": ["..."],
    "references": ["..."],
    "chaining_analysis": {
      "status": "suggested",
      "related_reports": ["report_20260408_031758.json"],
      "scenario": "브루트포스로 계정 탈취 → IDOR로 전체 PII 열람",
      "chained_severity": "critical"
    }
  },
  "impact": "...",
  "attachments": []
}
```

### 체이닝 분석 상태

| status | 의미 |
|---|---|
| `suggested` | LLM이 추론한 체이닝 가능성 (Auto-PoC 단계) |
| `unverified` | 사람이 검토했지만 아직 테스트 안 함 |
| `verified` | Solve에서 실제 체이닝 테스트 완료 |
```

## 프로젝트 구조

```
auto_poc/
├── __init__.py          # 공개 API
├── __main__.py          # python -m auto_poc 진입점
├── cli.py               # CLI 인터페이스
├── core.py              # 파이프라인 오케스트레이션
├── preprocessor.py      # 입력 전처리 및 유효성 검증
├── context.py           # 체이닝 컨텍스트 로드
├── generator.py         # LLM 보고서 생성
├── postprocessor.py     # 후처리, CWE 검증, 저장
├── prompts.py           # LLM 프롬프트 템플릿
├── cwe_data.py          # CWE ID 검증 데이터
├── schemas.py           # Pydantic 입출력 스키마
examples/
└── sample_input.json    # 테스트용 입력 예시
```

## 파이프라인

1. **입력 전처리** — JSON 파싱, 유효성 검증, asset 매칭
2. **체이닝 컨텍스트 조회** — 기존 보고서 로드 (있으면)
3. **LLM 보고서 생성** — Root Cause/Impact 중심, CWE + MITRE ATT&CK 매핑
4. **후처리** — CWE 검증, 스키마 정리, 보고서 저장

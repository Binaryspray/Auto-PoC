---
name: auto-poc
description: HackerOne 버그바운티 자동화 파이프라인의 PoC 단계. 취약점 테스트 결과와 Payload를 입력받아 HackerOne 보고서를 자동 생성한다. Root Cause / Impact 분석, CWE 및 MITRE ATT&CK TTPs 매핑, 기존 취약점과의 체이닝 가능성 검토를 포함한다. 보고서 작성 자동화, PoC 생성, 취약점 분석 보고서, HackerOne 제출 포맷 작업 시 반드시 이 스킬을 사용할 것.
---

# Auto-PoC Skill

HackerOne 버그바운티 보고서 자동 생성 모듈.

## 역할
- 입력: project_id + Solve output (취약점 테스트 결과/Payload) + program_info
- 출력: HackerOne 포맷의 취약점 분석 보고서 JSON

---

## 입력 스키마

```json
{
  "project_id": "string",
  "target": {
    "subdomain": "string",
    "attack_point": "string"
  },
  "vulnerability": {
    "type": "string",
    "payload": "string",
    "test_result": "string",
    "reproduction_steps": ["string"]
  },
  "program_info": {
    "platform": "hackerone",
    "program_name": "string",
    "scope": ["string"],
    "report_template": "string | null"
  }
}
```

**주의사항**
- `vulnerability` 내부 필드는 Solve 모듈이 채워서 넘겨줌
- `program_info`는 Recon 모듈이 H1 API로 수집해서 넘겨줌
- `report_template`이 null이면 H1 디폴트 양식 사용

---

## 출력 스키마 (HackerOne 보고서 포맷)

```json
{
  "title": "string",
  "asset": "string",
  "weakness": {
    "cwe_id": "CWE-XXX",
    "cwe_name": "string"
  },
  "severity": "none | low | medium | high | critical",
  "description": {
    "summary": "string",
    "steps_to_reproduce": ["string"],
    "recommendations": ["string"],
    "references": ["string"]
  },
  "impact": "string",
  "attachments": []
}
```

---

## 내부 프로세스

### 1단계 — 입력 전처리
- 입력 JSON 파싱 및 필수 필드 유효성 검증
- `report_template != null` → 해당 양식 사용
- `report_template == null` → H1 디폴트 양식 폴백
- `program_info.scope` 리스트에서 `target.subdomain` / `attack_point` 매칭 → `asset` 결정
  - 매칭 안 되면 `subdomain` 값을 그대로 사용

### 2단계 — 체이닝 컨텍스트 조회
- `/projects/{project_id}/reports/` 경로 확인
- 존재하면 폴더 내 모든 보고서 JSON 로드
- 없거나 비어있으면 스킵 (체이닝 섹션 생략)

### 3단계 — LLM 보고서 생성
프롬프트 구성 순서:
1. 보고서 양식 (template or H1 디폴트)
2. 현재 취약점 데이터 (입력 전체)
3. 기존 보고서 컨텍스트 (2단계에서 로드한 것들)

생성 항목:
- `title` — 취약점 유형 + 대상 기반으로 명확하게
- `weakness.cwe_id` / `weakness.cwe_name` — CWE DB 기반 매핑
- `severity` — CVSS 기준 판단
- `description.summary` — Root Cause 중심 요약
- `description.steps_to_reproduce` — `reproduction_steps` 기반으로 재구성
- `description.recommendations` — 완화/패치 방안
- `description.references` — CWE 링크, MITRE ATT&CK TTPs 링크 포함
- `impact` — 실제 비즈니스/보안 영향도 중심
- 체이닝 가능성 있으면 `description` 내 별도 섹션 추가

**LLM 작성 지침**
- Root Cause와 Impact에 집중
- CWE 번호는 반드시 실존하는 번호만 사용 (후처리에서 검증)
- MITRE ATT&CK TTPs 매핑 포함 (Tactic / Technique ID)
- 보안 담당자가 즉시 식별 가능한 수준으로 작성
- 체이닝 추천 시: 어떤 기존 취약점과 어떻게 체이닝되는지, 체이닝 시 위험도 상승 정도 명시

### 4단계 — 후처리
- 출력 스키마 포맷 검증 및 정리
- CWE ID 유효성 검증 — 잘못된 ID 감지 시 LLM 재호출 or 필드 null 처리
- `/projects/{project_id}/reports/report_{timestamp}.json`으로 저장
- 최종 JSON 반환

---

## 파일 저장 규칙
```
/projects/{project_id}/reports/report_{YYYYMMDD_HHMMSS}.json
```

---

## H1 디폴트 보고서 양식 참고

```
## Summary:
[취약점 요약]

## Steps To Reproduce:
1. [단계]
2. [단계]

## Recommendations:
* [완화 방안]

## Supporting Material/References:
* [참고 자료 / 첨부]
```

필드 매핑:
- Title → `title`
- Asset (Scope) → `asset`
- Weakness → `weakness` (CWE 선택)
- Severity → `severity` (선택 아님)
- Description → `description` (Summary + Steps + Recommendations + References)
- Impact → `impact`
- Attachments → `attachments`

---

## 관련 모듈
- **Recon** — `project_id`, `program_info` 생성 및 폴더 구조 초기화
- **Solve** — `vulnerability` 필드 (type, payload, test_result, reproduction_steps) 생성

# Bug Bounty Automation Pipeline

## 프로젝트 개요
HackerOne 버그바운티 자동화 파이프라인. Recon → Solve → PoC 3단계로 구성.

## 개발 순서
1. **Auto-PoC** (현재) — 취약점 분석 보고서 자동 생성
2. **Auto-Recon** — 대상 수집 및 스코어링
3. **Solve** — 취약점 발굴 (LLM 퍼징)

## 전체 파이프라인

### ① Recon
- **Input**: 버그바운티 대상 목록, `rule.csv`
- **Process**: 대상 Scoring → 서브도메인 수집 → 단계별 가능성 판별
- **Output**: SubDomain / AP 쌍 JSON 리스트, Project ID, 폴더 구조 생성

### ② Solve (Web)
- **Input**: SubDomain / AP 단일 쌍
- **Process**: 전문 도구 매칭 → 취약점 가능성 판별 → LLM 퍼징 → 취약점 발현 테스트
- **Output**: 테스트 결과, 취약한 Payload, 재현 단계

### ③ PoC
- **Input**: project_id + Solve output + program_info
- **Process**: 입력 전처리 → 체이닝 컨텍스트 조회 → LLM 보고서 생성 → 후처리
- **Output**: HackerOne 보고서 JSON

## 프로젝트 폴더 구조
```
/projects
  /{project_id}/           # Recon에서 생성, 도메인/기업 단위
    program_info.json      # H1 scope, template 등
    /reports/
      report_001.json
      report_002.json
      ...
```

## 기술 스택 고려사항
- 네트워크 I/O 집약적 작업 (Recon, Solve): **Go** 우선 고려
- LLM 연동 / 오케스트레이션: **Python**
- 퍼징 엔진 코어: **Rust** or **Go**

## 현재 작업: Auto-PoC

### 입력 스키마
```json
{
  "project_id": "",
  "target": {
    "subdomain": "",
    "attack_point": ""
  },
  "vulnerability": {
    "type": "",
    "payload": "",
    "test_result": "",
    "reproduction_steps": []
  },
  "program_info": {
    "platform": "hackerone",
    "program_name": "",
    "scope": [],
    "report_template": null
  }
}
```

### 출력 스키마 (HackerOne 보고서 포맷)
```json
{
  "title": "",
  "asset": "",
  "weakness": { "cwe_id": "", "cwe_name": "" },
  "severity": "",
  "description": {
    "summary": "",
    "steps_to_reproduce": [],
    "recommendations": [],
    "references": []
  },
  "impact": "",
  "attachments": []
}
```

### 내부 프로세스
1. **입력 전처리**
   - 입력 JSON 파싱 및 유효성 검증
   - `report_template` 있으면 사용, 없으면 H1 디폴트 양식 폴백
   - `scope`에서 `subdomain` / `attack_point` 매칭 → `asset` 결정

2. **체이닝 컨텍스트 조회**
   - `/projects/{project_id}/reports/` 내 기존 보고서 전부 로드
   - 없으면 스킵

3. **LLM 보고서 생성**
   - 프롬프트: `[보고서 양식 + 입력 데이터 + 기존 보고서 컨텍스트]`
   - 생성 항목: title, weakness(CWE), severity, summary, steps_to_reproduce, recommendations, references, impact
   - 체이닝 가능성 있으면 별도 섹션 추가
   - LLM 보고서 작성 시 Root Cause / Impact 중심, CWE + MITRE ATT&CK TTPs 매핑

4. **후처리**
   - 출력 스키마 포맷 정리
   - CWE ID 유효성 검증 (할루시네이션 방지)
   - `/projects/{project_id}/reports/`에 보고서 저장
   - 최종 JSON 반환

## 주요 설계 결정
- RAG 대신 프로젝트 폴더 기반 컨텍스트 관리 (취약점 수가 많지 않을 것으로 예상)
- Solve output 내부 스키마는 미정 — JSON 포맷만 확정, 필드는 추후 결정
- `program_info`는 Recon에서 H1 API로 수집 후 넘겨줌
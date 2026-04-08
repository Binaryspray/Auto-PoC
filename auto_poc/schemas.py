from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── 입력 스키마 ──

class Target(BaseModel):
    subdomain: str
    attack_point: str


class Vulnerability(BaseModel):
    type: str
    payload: str
    test_result: str
    reproduction_steps: list[str]


class ProgramInfo(BaseModel):
    platform: str = "hackerone"
    program_name: str
    scope: list[str] = Field(default_factory=list)
    report_template: Optional[str] = None


class PocInput(BaseModel):
    project_id: str
    target: Target
    vulnerability: Vulnerability
    program_info: ProgramInfo


# ── 출력 스키마 ──

class Severity(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Weakness(BaseModel):
    cwe_id: Optional[str] = None
    cwe_name: Optional[str] = None


class Description(BaseModel):
    summary: str
    steps_to_reproduce: list[str]
    recommendations: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)


class PocReport(BaseModel):
    title: str
    asset: str
    weakness: Weakness
    severity: Severity
    description: Description
    impact: str
    attachments: list[str] = Field(default_factory=list)

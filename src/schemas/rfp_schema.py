"""
RFP 분석 결과 스키마
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EvaluationCriterion(BaseModel):
    """평가 기준"""

    category: str
    item: str
    weight: Optional[float] = None
    description: Optional[str] = None


class Requirement(BaseModel):
    """요구사항"""

    category: str  # 기능, 비기능, 기술, 관리 등
    requirement: str
    priority: str = "필수"  # 필수, 선택, 권장
    notes: Optional[str] = None


class Deliverable(BaseModel):
    """산출물"""

    name: str
    phase: Optional[str] = None
    description: Optional[str] = None


class TimelineInfo(BaseModel):
    """일정 정보"""

    total_duration: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    milestones: Optional[List[Dict[str, str]]] = None
    phases: Optional[List[Dict[str, Any]]] = None


class BudgetInfo(BaseModel):
    """예산 정보"""

    total_budget: Optional[str] = None
    budget_breakdown: Optional[Dict[str, Any]] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None


class RFPAnalysis(BaseModel):
    """RFP 분석 결과"""

    # 기본 정보
    project_name: str = Field(description="프로젝트명")
    client_name: str = Field(description="발주처명")
    project_overview: str = Field(description="프로젝트 개요")

    # 요구사항
    key_requirements: List[Requirement] = Field(
        default_factory=list, description="핵심 요구사항"
    )
    technical_requirements: List[Requirement] = Field(
        default_factory=list, description="기술 요구사항"
    )
    functional_requirements: List[Requirement] = Field(
        default_factory=list, description="기능 요구사항"
    )

    # 평가 기준
    evaluation_criteria: List[EvaluationCriterion] = Field(
        default_factory=list, description="평가 기준"
    )

    # 산출물
    deliverables: List[Deliverable] = Field(
        default_factory=list, description="산출물 목록"
    )

    # 일정
    timeline: Optional[TimelineInfo] = Field(default=None, description="일정 정보")

    # 예산
    budget: Optional[BudgetInfo] = Field(default=None, description="예산 정보")

    # 분석 인사이트
    key_success_factors: List[str] = Field(
        default_factory=list, description="핵심 성공 요인"
    )
    potential_risks: List[str] = Field(
        default_factory=list, description="잠재적 리스크"
    )
    winning_strategy: Optional[str] = Field(
        default=None, description="수주 전략 제안"
    )
    differentiation_points: List[str] = Field(
        default_factory=list, description="차별화 포인트"
    )

    # v3.6 추가: 설득 구조 강화 필드
    project_type: str = Field(
        default="general",
        description="프로젝트 유형 (marketing_pr, event, it_system, public, consulting, general)"
    )
    pain_points: List[str] = Field(
        default_factory=list,
        description="발주처 핵심 고민/문제점 (RFP 행간에서 추출, 3~5개)"
    )
    hidden_needs: List[str] = Field(
        default_factory=list,
        description="RFP에 명시되지 않은 숨겨진 니즈"
    )
    evaluation_strategy: Optional[Dict[str, Any]] = Field(
        default=None,
        description="평가 기준 전략 (high_weight_items, emphasis_mapping)"
    )
    win_theme_candidates: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Win Theme 후보 3개 (name, rationale, rfp_alignment)"
    )
    competitive_landscape: Optional[str] = Field(
        default=None,
        description="예상 경쟁 환경 분석"
    )

    # 원본 데이터
    raw_sections: Optional[Dict[str, Any]] = Field(
        default=None, description="원본 섹션 데이터"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "스마트시티 통합 플랫폼 구축",
                "client_name": "서울특별시",
                "project_overview": "도시 데이터 통합 관리 및 시민 서비스 제공",
                "key_requirements": [
                    {
                        "category": "기능",
                        "requirement": "실시간 데이터 수집",
                        "priority": "필수",
                    }
                ],
                "evaluation_criteria": [
                    {
                        "category": "기술",
                        "item": "시스템 아키텍처",
                        "weight": 20,
                    }
                ],
            }
        }

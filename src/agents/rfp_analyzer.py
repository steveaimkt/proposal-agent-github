"""RFP 분석 에이전트"""

import json
from typing import Any, Callable, Dict, Optional

from .base_agent import BaseAgent
from ..schemas.rfp_schema import RFPAnalysis
from ..utils.logger import get_logger

logger = get_logger("rfp_analyzer")


class RFPAnalyzer(BaseAgent):
    """RFP 문서 분석 에이전트"""

    async def execute(
        self,
        input_data: Dict[str, Any],
        progress_callback: Optional[Callable] = None,
    ) -> RFPAnalysis:
        """
        RFP 문서를 분석하여 핵심 정보 추출

        Args:
            input_data: {
                "raw_text": str,
                "tables": List[Dict],
                "sections": List[Dict]
            }
            progress_callback: 진행 상황 콜백

        Returns:
            RFPAnalysis: 분석된 RFP 정보
        """
        if progress_callback:
            progress_callback(
                {"step": 1, "total": 3, "message": "RFP 텍스트 준비 중..."}
            )

        # 프롬프트 로드
        system_prompt = self._load_prompt("rfp_analysis")
        if not system_prompt:
            system_prompt = self._get_default_system_prompt()

        # 입력 데이터 준비
        raw_text = self._truncate_text(input_data.get("raw_text", ""), 25000)
        tables_json = json.dumps(
            input_data.get("tables", [])[:10], ensure_ascii=False, indent=2
        )[:5000]

        user_message = f"""
다음 RFP(제안요청서) 문서를 분석해주세요.

## 문서 텍스트
{raw_text}

## 테이블 데이터
{tables_json}

위 내용을 분석하여 다음 JSON 형식으로 응답해주세요:

```json
{{
    "project_name": "프로젝트명",
    "client_name": "발주처명",
    "project_overview": "프로젝트 개요 (2-3문장)",
    "project_type": "marketing_pr / event / it_system / public / consulting / general 중 택1",
    "key_requirements": [
        {{"category": "기능/비기능/기술/관리", "requirement": "요구사항", "priority": "필수/선택"}}
    ],
    "technical_requirements": [
        {{"category": "기술", "requirement": "기술 요구사항", "priority": "필수/선택"}}
    ],
    "evaluation_criteria": [
        {{"category": "분야", "item": "평가 항목", "weight": 배점}}
    ],
    "deliverables": [
        {{"name": "산출물명", "phase": "단계", "description": "설명"}}
    ],
    "timeline": {{
        "total_duration": "전체 기간",
        "phases": [{{"name": "단계명", "duration": "기간"}}]
    }},
    "budget": {{
        "total_budget": "예산 (있는 경우)",
        "notes": "예산 관련 참고사항"
    }},
    "key_success_factors": ["핵심 성공 요인 1", "핵심 성공 요인 2"],
    "potential_risks": ["리스크 1", "리스크 2"],
    "winning_strategy": "수주를 위한 전략 제안",
    "differentiation_points": ["차별화 포인트 1", "차별화 포인트 2"],
    "pain_points": [
        "발주처 핵심 고민 1 (RFP 행간에서 추출)",
        "발주처 핵심 고민 2",
        "발주처 핵심 고민 3"
    ],
    "hidden_needs": [
        "RFP에 명시되지 않은 숨겨진 니즈 1",
        "RFP에 명시되지 않은 숨겨진 니즈 2"
    ],
    "evaluation_strategy": {{
        "high_weight_items": [
            {{"item": "배점 높은 평가 항목", "weight": 30, "proposal_emphasis": "이 항목에 대응하기 위해 제안서에서 강조할 내용"}}
        ],
        "emphasis_mapping": {{
            "Phase 2 (INSIGHT)": "이 Phase에서 강조할 평가 항목",
            "Phase 4 (ACTION)": "이 Phase에서 강조할 평가 항목",
            "Phase 6 (WHY US)": "이 Phase에서 강조할 평가 항목"
        }}
    }},
    "win_theme_candidates": [
        {{
            "name": "Win Theme 이름 (짧은 키워드)",
            "rationale": "이 Win Theme이 효과적인 이유",
            "rfp_alignment": "연결되는 RFP 요구사항/평가 기준"
        }},
        {{
            "name": "Win Theme 2",
            "rationale": "이유",
            "rfp_alignment": "연결 요구사항"
        }},
        {{
            "name": "Win Theme 3",
            "rationale": "이유",
            "rfp_alignment": "연결 요구사항"
        }}
    ],
    "competitive_landscape": "예상 경쟁 환경 분석 (어떤 유형의 회사가 경쟁할지, 차별화 가능 영역)"
}}
```
"""

        if progress_callback:
            progress_callback(
                {"step": 2, "total": 3, "message": "Claude 분석 수행 중..."}
            )

        # Claude API 호출
        response = self._call_claude(system_prompt, user_message, max_tokens=8192)

        if progress_callback:
            progress_callback(
                {"step": 3, "total": 3, "message": "분석 결과 정리 중..."}
            )

        # JSON 파싱
        analysis_data = self._extract_json(response)

        # 기본값 설정
        analysis_data.setdefault("project_name", "프로젝트명 미확인")
        analysis_data.setdefault("client_name", "발주처 미확인")
        analysis_data.setdefault("project_overview", "")

        logger.info(f"RFP 분석 완료: {analysis_data.get('project_name')}")

        return RFPAnalysis(**analysis_data)

    def _get_default_system_prompt(self) -> str:
        """기본 시스템 프롬프트"""
        return """당신은 경쟁 입찰에서 승리하는 제안서를 위한 RFP 분석 전문가입니다.
단순 정보 추출을 넘어, 수주를 위한 전략적 분석을 수행합니다.

## 분석 영역

### 기본 정보 추출
1. 프로젝트 기본 정보 (이름, 발주처, 개요)
2. 요구사항 (기능, 비기능, 기술)
3. 평가 기준 및 배점
4. 산출물 목록
5. 일정 및 예산 정보

### 전략적 분석 (★핵심)
6. **프로젝트 유형 분류**: marketing_pr, event, it_system, public, consulting, general
7. **Pain Point 추출**: 발주처가 겪고 있는 핵심 고민 3~5개
8. **평가 기준 전략화**: 배점 높은 항목 → 제안서 강조 포인트 변환
9. **Win Theme 후보 도출**: RFP에 직접 대응하는 핵심 수주 전략 메시지 3개
10. **숨겨진 니즈**: RFP에 명시되지 않았지만 발주처가 원하는 것

## Pain Point 추출 원칙
- RFP의 "배경", "목적", "필요성" 섹션에서 발주처가 겪고 있는 문제를 읽어냄
- 평가 기준 배점이 높은 항목 = 발주처가 가장 중요하게 여기는 것
- "~해야 한다", "~이 필요하다", "~이 미흡하다" 표현에서 Pain Point 추출
- 예: "효과적인 홍보 체계 구축이 필요하다" → Pain Point: "현재 홍보 체계의 효과성 부족"

## Win Theme 후보 도출 원칙
- 각 후보는 RFP의 Pain Point에 직접 대응해야 함
- 경쟁사가 쉽게 모방할 수 없는 차별점이어야 함
- 3개를 제안하되, 서로 다른 축으로 분산:
  - 축 1: 데이터/분석/기술 역량
  - 축 2: 실행력/전문성/실적
  - 축 3: 통합/시너지/혁신

## 평가 기준 전략화 원칙
- 배점 25% 이상: 최고 우선순위 → 해당 영역에 제안서 비중 집중
- 배점 15~24%: 높은 우선순위 → 충분한 분량 배정
- 배점 15% 미만: 기본 대응
- 각 고배점 항목에 대해 "어떤 Phase에서 어떻게 대응할지" 매핑

## 분석 원칙
- 명시적 정보 추출 + 행간 해석 병행
- 불확실한 정보는 "미확인" 표시
- 모든 분석에 근거 제시

응답은 반드시 유효한 JSON 형식으로 제공해주세요."""

"""
제안서 콘텐츠 스키마 (v3.0 - Impact-8 Framework)

Claude가 생성하고 [회사명]가 소비하는 중간 데이터 포맷
수주 제안서 분석 기반 개선된 구조
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProposalType(str, Enum):
    """제안서 유형"""

    MARKETING_PR = "marketing_pr"  # 마케팅/PR/소셜미디어
    EVENT = "event"                # 이벤트/행사
    PUBLIC = "public"              # 공공/입찰
    IT_SYSTEM = "it_system"        # IT/시스템
    CONSULTING = "consulting"      # 컨설팅
    GENERAL = "general"            # 일반


class SlideType(str, Enum):
    """슬라이드 유형"""

    TITLE = "title"
    SECTION_DIVIDER = "section_divider"  # Phase 구분자
    CONTENT = "content"
    TWO_COLUMN = "two_column"
    THREE_COLUMN = "three_column"  # 3단 레이아웃 추가
    TABLE = "table"
    CHART = "chart"
    TIMELINE = "timeline"
    ORG_CHART = "org_chart"
    IMAGE = "image"
    COMPARISON = "comparison"
    KEY_MESSAGE = "key_message"    # 핵심 메시지 강조
    INDEX = "index"                # 목차
    PROCESS = "process"            # 프로세스 플로우
    TEASER = "teaser"              # 티저/임팩트 슬라이드
    CASE_STUDY = "case_study"      # 사례 연구
    CONTENT_EXAMPLE = "content_example"  # 콘텐츠 예시
    CHANNEL_STRATEGY = "channel_strategy"  # 채널별 전략
    CAMPAIGN = "campaign"          # 캠페인 소개
    BUDGET = "budget"              # 예산 테이블
    # v3.1 추가 슬라이드 유형
    EXECUTIVE_SUMMARY = "executive_summary"  # Executive Summary
    NEXT_STEP = "next_step"        # Next Step / Call to Action
    DIFFERENTIATION = "differentiation"  # 차별화 포인트


class BulletPoint(BaseModel):
    """불릿 포인트"""

    text: str
    level: int = 0  # 0: 메인, 1: 서브, 2: 서브서브
    emphasis: bool = False
    icon: Optional[str] = None  # 아이콘 힌트 (예: "check", "star", "warning")


class TableData(BaseModel):
    """테이블 데이터"""

    headers: List[str]
    rows: List[List[str]]
    highlight_rows: Optional[List[int]] = None
    highlight_cols: Optional[List[int]] = None
    column_widths: Optional[List[float]] = None
    caption: Optional[str] = None
    style: Optional[str] = "default"  # "default", "dark", "accent", "minimal"


class ChartData(BaseModel):
    """차트 데이터"""

    chart_type: str  # "bar", "line", "pie", "gantt", "donut", "comparison", "funnel"
    title: str
    data: Dict[str, Any]
    colors: Optional[List[str]] = None
    show_values: bool = True
    show_legend: bool = True


class TimelineItem(BaseModel):
    """타임라인 항목"""

    phase: str
    title: str
    duration: str
    description: Optional[str] = None
    milestones: Optional[List[str]] = None
    deliverables: Optional[List[str]] = None
    color: Optional[str] = None


class OrgChartNode(BaseModel):
    """조직도 노드"""

    name: str
    role: str
    expertise: Optional[str] = None
    children: Optional[List["OrgChartNode"]] = None


class KPIItem(BaseModel):
    """KPI 항목 (정량적 약속)"""

    metric: str        # 지표명 (예: "고객 만족도")
    target: str        # 목표값 (예: "95%")
    baseline: Optional[str] = None  # 현재값 (예: "80%")
    improvement: Optional[str] = None  # 개선폭 (예: "+15%p")


class CompetitorComparison(BaseModel):
    """경쟁사 비교"""

    criteria: str      # 비교 기준
    our_strength: str  # 우리의 강점
    competitor: str    # 경쟁사 대비


class ComparisonItem(BaseModel):
    """비교 항목 (Before/After)"""

    label: str         # 항목명
    left: str          # 왼쪽 값 (Before/AS-IS)
    right: str         # 오른쪽 값 (After/TO-BE)


class ComparisonData(BaseModel):
    """비교 데이터 (Before/After)"""

    left_title: str = "AS-IS"
    right_title: str = "TO-BE"
    items: List[ComparisonItem]


class MilestoneItem(BaseModel):
    """마일스톤 항목"""

    name: str
    date: str
    deliverable: Optional[str] = None


class ContentExample(BaseModel):
    """콘텐츠 예시 (마케팅/PR용)"""

    platform: str          # "instagram", "youtube", "facebook", "blog" 등
    content_type: str      # "feed", "story", "reel", "shorts", "long_form" 등
    title: str
    description: str
    visual_description: Optional[str] = None  # 비주얼 설명
    copy_example: Optional[str] = None        # 카피 예시
    hashtags: Optional[List[str]] = None
    kpi_target: Optional[str] = None


class ChannelStrategy(BaseModel):
    """채널별 전략"""

    channel_name: str
    role: str              # 채널 역할
    target_audience: str
    content_pillars: List[str]
    posting_frequency: str
    kpis: List[KPIItem]


class CampaignPlan(BaseModel):
    """캠페인 계획"""

    campaign_name: str
    concept: str
    period: str
    objectives: List[str]
    target: str
    channels: List[str]
    key_activities: List[str]
    expected_results: List[str]


# ============================================================
# v3.1 신규 스키마 - Win Theme, Executive Summary, Next Step
# ============================================================

class WinTheme(BaseModel):
    """Win Theme (핵심 수주 전략 메시지)

    Win Theme은 제안서 전체에 반복적으로 등장하여
    핵심 차별화 메시지를 각인시키는 전략적 키워드/문장
    """

    name: str = Field(description="Win Theme 이름 (짧은 키워드)")
    description: str = Field(description="Win Theme 상세 설명")
    evidence: List[str] = Field(
        default_factory=list,
        description="Win Theme을 뒷받침하는 근거/증거"
    )
    related_phases: List[int] = Field(
        default_factory=list,
        description="이 Win Theme이 주로 등장하는 Phase 번호"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "데이터 기반 타겟 마케팅",
                "description": "MZ세대 SNS 이용 패턴 분석을 통한 최적화된 콘텐츠 전략",
                "evidence": [
                    "와이즈앱 인스타그램 MAU 2,644만명 데이터 활용",
                    "릴스 도달률 피드 대비 1.8배 (Social Insider 2025)"
                ],
                "related_phases": [1, 2, 3]
            }
        }


class KPIWithBasis(BaseModel):
    """KPI 항목 (산출 근거 포함)

    기존 KPIItem을 확장하여 산출 근거를 명시
    """

    metric: str = Field(description="지표명")
    target: str = Field(description="목표값")
    baseline: Optional[str] = Field(None, description="현재값/기준값")
    improvement: Optional[str] = Field(None, description="개선폭")
    calculation_basis: str = Field(
        description="KPI 산출 근거 (어떻게 이 목표를 도출했는지)"
    )
    data_source: Optional[str] = Field(
        None, description="데이터 출처 (예: 와이즈앱, Social Insider 등)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "metric": "팔로워 성장률",
                "target": "+30%",
                "baseline": "3,500명",
                "improvement": "+1,050명",
                "calculation_basis": "인플루언서 협업 +10%, 릴스 확대 +12%, 이벤트 +8%",
                "data_source": "유사 프로젝트 평균 성장률 참고"
            }
        }


class ExecutiveSummary(BaseModel):
    """Executive Summary (의사결정권자용 1페이지 핵심 요약)

    바쁜 의사결정권자가 5분 내에 제안의 핵심을 파악할 수 있도록
    프로젝트 목표, Win Theme, KPI, 차별점을 압축
    """

    project_objective: str = Field(
        description="프로젝트 핵심 목표 (1문장)"
    )
    win_themes: List[WinTheme] = Field(
        description="3대 핵심 전략 (Win Themes)",
        min_length=2,
        max_length=4
    )
    key_kpis: List[KPIWithBasis] = Field(
        description="핵심 KPI (산출 근거 포함)",
        min_length=3,
        max_length=5
    )
    why_us_points: List[str] = Field(
        description="왜 우리인가 핵심 포인트 (3-4개)",
        min_length=2,
        max_length=5
    )

    class Config:
        json_schema_extra = {
            "example": {
                "project_objective": "10개월간 [프로젝트명] 브랜드 인지도 +20%p 상승, SNS 팔로워 +30% 성장",
                "win_themes": [
                    {"name": "데이터 기반 타겟 마케팅", "description": "MZ세대 SNS 분석 기반 콘텐츠 최적화"},
                    {"name": "시민 참여형 브랜드 빌딩", "description": "러닝/요가/시네마 커뮤니티로 지속가능 브랜드 구축"},
                    {"name": "온-오프라인 통합 시너지", "description": "SNS-행사-홍보물 연계 선순환"}
                ],
                "why_us_points": [
                    "인천 지역 인플루언서 47명 네트워크",
                    "유사 프로젝트 5건 수행 (평균 130% 목표 초과)",
                    "시민참여 프로그램 8,000명+ 운영 경험"
                ]
            }
        }


class NextStepItem(BaseModel):
    """Next Step 항목"""

    step_number: int
    title: str
    date: str
    description: str


class NextStep(BaseModel):
    """Next Step (다음 단계 안내 / Call to Action)

    제안서 마무리 전 구체적인 다음 단계를 제시하여
    의사결정을 유도
    """

    headline: str = Field(
        default="다음 단계를 준비하고 있습니다",
        description="Next Step 슬라이드 헤드라인"
    )
    steps: List[NextStepItem] = Field(
        description="다음 단계 목록 (3-5개)",
        min_length=2,
        max_length=5
    )
    call_to_action: List[str] = Field(
        description="제안하는 것 (명확한 성과 약속)",
        min_length=2,
        max_length=5
    )
    contact_info: Optional[Dict[str, str]] = Field(
        None, description="담당자 연락처"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "headline": "[프로젝트명]과 함께할 준비가 되어 있습니다",
                "steps": [
                    {"step_number": 1, "title": "계약 체결", "date": "2026.03", "description": "계약 조건 협의"},
                    {"step_number": 2, "title": "착수 보고", "date": "2026.03", "description": "상세 실행계획 확정"},
                    {"step_number": 3, "title": "실행 개시", "date": "2026.04", "description": "SNS 채널 운영 시작"}
                ],
                "call_to_action": [
                    "10개월간 브랜드 인지도 +20%p 달성",
                    "SNS 팔로워 +30% 성장 및 연간 도달 100만+ 확보"
                ]
            }
        }


class ActionTitle(BaseModel):
    """Action Title (인사이트 기반 슬라이드 제목)

    Topic Title(주제 제목) 대신 Action Title(행동/인사이트 제목)을 사용하여
    슬라이드를 읽지 않고도 핵심 메시지를 전달

    예시:
    - Topic Title: "시장 환경 분석"
    - Action Title: "숏폼·로컬 트렌드가 [프로젝트명] 성장 기회"
    """

    topic_title: str = Field(description="기존 주제 제목")
    action_title: str = Field(description="개선된 인사이트 제목")

    class Config:
        json_schema_extra = {
            "example": {
                "topic_title": "타겟 분석",
                "action_title": "MZ세대 2030이 핵심, 하루 SNS 55분 사용"
            }
        }


# Action Title 변환 가이드라인
ACTION_TITLE_GUIDELINES = {
    "principles": [
        "슬라이드 내용의 결론/인사이트를 제목에 담기",
        "숫자나 구체적 데이터 포함 권장",
        "동사 또는 명사형 결론문으로 구성",
        "15-30자 내외로 간결하게"
    ],
    "examples": [
        {"before": "사업 개요 및 목표", "after": "10개월간 브랜드 인지도 +20%p 달성이 핵심 과제"},
        {"before": "홍보 환경 분석", "after": "숏폼·로컬 트렌드가 [프로젝트명] 성장 기회"},
        {"before": "타겟 분석", "after": "MZ세대 2030이 핵심, 하루 SNS 55분 사용"},
        {"before": "SNS 운영 전략", "after": "인스타그램 집중 운영으로 팔로워 5,000+ 달성"},
        {"before": "차별화 포인트", "after": "유사 사업 130% 목표 초과 달성, 검증된 실행력 보유"},
    ],
    "bad_examples": [
        "~~에 대하여",
        "~~의 현황",
        "~~의 방안",
        "~~의 필요성"
    ]
}


# 플레이스홀더 포맷 가이드라인
PLACEHOLDER_FORMAT = {
    "description": "제안서 내 플레이스홀더는 [대괄호] 형식으로 통일",
    "categories": {
        "company_info": {
            "description": "회사 정보 관련",
            "placeholders": [
                "[회사명]",
                "[대표이사명]",
                "[설립연도]",
                "[직원수]",
                "[회사 주소]",
                "[사업자번호]",
            ]
        },
        "contact_info": {
            "description": "연락처 관련",
            "placeholders": [
                "[대표전화]",
                "[대표이메일]",
                "[홈페이지]",
                "[담당자명]",
                "[전화번호]",
                "[이메일]",
            ]
        },
        "project_team": {
            "description": "프로젝트 팀 관련",
            "placeholders": [
                "[PM 성명]",
                "[PM 연락처]",
                "[PM 이메일]",
                "[담당자명]",
                "[담당자 연락처]",
                "[담당자 이메일]",
            ]
        },
        "portfolio": {
            "description": "포트폴리오/실적 관련",
            "placeholders": [
                "[유사실적 발주처]",
                "[프로젝트명]",
                "[수행기간]",
                "[성과]",
            ]
        }
    }
}


class SlideContent(BaseModel):
    """슬라이드 콘텐츠"""

    slide_type: SlideType
    title: str
    subtitle: Optional[str] = None
    bullets: Optional[List[BulletPoint]] = None
    table: Optional[TableData] = None
    chart: Optional[ChartData] = None
    timeline: Optional[List[TimelineItem]] = None
    org_chart: Optional[OrgChartNode] = None
    image_placeholder: Optional[str] = None
    left_content: Optional[List[BulletPoint]] = None  # two_column용
    right_content: Optional[List[BulletPoint]] = None  # two_column용
    center_content: Optional[List[BulletPoint]] = None  # three_column용
    left_title: Optional[str] = None  # column 제목
    right_title: Optional[str] = None
    center_title: Optional[str] = None
    notes: Optional[str] = None  # 발표자 노트
    key_message: Optional[str] = None  # 핵심 메시지 (슬라이드 하단)
    kpis: Optional[List[KPIItem]] = None  # KPI 목록
    competitor_comparison: Optional[List[CompetitorComparison]] = None  # 경쟁사 비교
    comparison: Optional[ComparisonData] = None  # Before/After 비교
    milestones: Optional[List[MilestoneItem]] = None  # 마일스톤

    # 마케팅/PR 특화 필드
    content_examples: Optional[List[ContentExample]] = None
    channel_strategy: Optional[ChannelStrategy] = None
    campaign: Optional[CampaignPlan] = None

    # 디자인 힌트
    layout_hint: Optional[str] = None  # "full_bleed", "centered", "left_heavy"
    visual_style: Optional[str] = None  # "dark", "light", "gradient", "image_bg"
    accent_color: Optional[str] = None


class PhaseContent(BaseModel):
    """Phase 콘텐츠 (기존 PartContent 대체)"""

    phase_number: int
    phase_title: str
    phase_subtitle: Optional[str] = None  # Phase 부제목/설명
    phase_icon: Optional[str] = None      # Phase 아이콘 힌트
    story_title: Optional[str] = None     # 스토리텔링 타이틀 (예: "상상을 이해하다")
    win_theme: Optional[str] = None       # 이 Phase와 연결된 Win Theme
    slides: List[SlideContent]


class TOCItem(BaseModel):
    """목차 항목"""

    phase_number: int
    title: str
    page_start: Optional[int] = None


class TeaserContent(BaseModel):
    """티저/훅 콘텐츠 (Phase 0)"""

    main_slogan: str
    sub_message: Optional[str] = None
    visual_concept: str  # 비주얼 컨셉 설명
    key_visuals: Optional[List[str]] = None  # 주요 비주얼 설명
    slides: List[SlideContent]


class ProposalContent(BaseModel):
    """제안서 전체 콘텐츠 (v3.1 - Impact-8 Framework + Win Theme)"""

    # 기본 정보
    project_name: str
    client_name: str
    submission_date: str
    company_name: str = "[회사명]"

    # 제안서 유형
    proposal_type: ProposalType = ProposalType.GENERAL

    # 핵심 메시지 (Executive Summary용)
    one_sentence_pitch: Optional[str] = None  # 한 문장 제안
    key_differentiators: Optional[List[str]] = None  # 3가지 차별점
    slogan: Optional[str] = None  # 슬로건

    # v3.1 추가: Win Themes (제안서 전체에 반복되는 핵심 메시지)
    win_themes: Optional[List[WinTheme]] = Field(
        None,
        description="3-4개의 Win Theme (제안서 전체에 반복되는 핵심 수주 전략)"
    )

    # v3.1 추가: Executive Summary (의사결정권자용 요약)
    executive_summary: Optional[ExecutiveSummary] = Field(
        None,
        description="Executive Summary - 의사결정권자용 1페이지 핵심 요약"
    )

    # v3.1 추가: Next Step (Call to Action)
    next_step: Optional[NextStep] = Field(
        None,
        description="Next Step - 다음 단계 안내 및 Call to Action"
    )

    # RFP 분석 결과
    rfp_summary: Dict[str, Any] = Field(default_factory=dict)

    # 목차
    table_of_contents: Optional[List[TOCItem]] = None

    # Phase 0: HOOK (티저)
    teaser: Optional[TeaserContent] = None

    # Phase 콘텐츠 (Impact-8 구조: Phase 1-7)
    phases: List[PhaseContent] = Field(
        description="Phase 1~7 콘텐츠 (Impact-8 Framework)",
        min_length=6,
        max_length=8,
    )

    # 디자인 설정
    design_style: Optional[str] = "modern"  # 디자인 스타일 프리셋
    design_preferences: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "[예시] 소셜미디어 채널 운영 프로젝트",
                "client_name": "[발주처명]",
                "submission_date": "2024-03-15",
                "proposal_type": "marketing_pr",
                "one_sentence_pitch": "모빌리티 리더십 채널로의 포지셔닝을 통해 EV/SDV 시대 브랜드 팬덤 구축",
                "key_differentiators": [
                    "AI 콘텐츠 협업 캠페인으로 MZ세대 자발적 참여 유도",
                    "숏폼-롱폼 연계 전략으로 조회수 300% 향상",
                    "데이터 기반 퍼포먼스 리포팅 체계"
                ],
                "slogan": "Positioning as a Leading Mobility Channel",
            }
        }


# Impact-8 Phase 정의 상수
PHASE_DEFINITIONS = {
    0: {
        "title": "HOOK",
        "subtitle": "임팩트 있는 오프닝",
        "purpose": "몰입감 형성, 핵심 비전 전달",
        "recommended_slides": (3, 10),
        "weight_by_type": {
            "marketing_pr": 0.08,
            "event": 0.06,
            "it_system": 0.03,
            "public": 0.03,
            "consulting": 0.05,
            "general": 0.05,
        }
    },
    1: {
        "title": "SUMMARY",
        "subtitle": "Executive Summary",
        "purpose": "의사결정자용 5분 핵심 요약",
        "recommended_slides": (3, 5),
        "weight_by_type": {
            "marketing_pr": 0.05,
            "event": 0.05,
            "it_system": 0.08,
            "public": 0.08,
            "consulting": 0.08,
            "general": 0.06,
        }
    },
    2: {
        "title": "INSIGHT",
        "subtitle": "시장 환경 & 문제 정의",
        "purpose": "트렌드 분석, 문제 이해, 숨겨진 니즈 발굴",
        "recommended_slides": (8, 15),
        "weight_by_type": {
            "marketing_pr": 0.12,
            "event": 0.08,
            "it_system": 0.12,
            "public": 0.15,
            "consulting": 0.15,
            "general": 0.10,
        }
    },
    3: {
        "title": "CONCEPT & STRATEGY",
        "subtitle": "핵심 컨셉 & 차별화 전략",
        "purpose": "우리만의 해결책과 경쟁 우위 제시",
        "recommended_slides": (8, 15),
        "weight_by_type": {
            "marketing_pr": 0.12,
            "event": 0.10,
            "it_system": 0.10,
            "public": 0.10,
            "consulting": 0.12,
            "general": 0.10,
        }
    },
    4: {
        "title": "ACTION PLAN",
        "subtitle": "상세 실행 계획",
        "purpose": "채널별 전략, 콘텐츠 예시, 구체적 실행안",
        "recommended_slides": (30, 60),
        "weight_by_type": {
            "marketing_pr": 0.40,
            "event": 0.45,
            "it_system": 0.35,
            "public": 0.30,
            "consulting": 0.30,
            "general": 0.35,
        }
    },
    5: {
        "title": "MANAGEMENT",
        "subtitle": "운영 & 품질 관리",
        "purpose": "조직 체계, 품질관리, 리포팅",
        "recommended_slides": (6, 12),
        "weight_by_type": {
            "marketing_pr": 0.08,
            "event": 0.10,
            "it_system": 0.12,
            "public": 0.12,
            "consulting": 0.10,
            "general": 0.10,
        }
    },
    6: {
        "title": "WHY US",
        "subtitle": "수행 역량 & 실적",
        "purpose": "회사 역량, 유사 실적, 레퍼런스",
        "recommended_slides": (8, 15),
        "weight_by_type": {
            "marketing_pr": 0.10,
            "event": 0.10,
            "it_system": 0.12,
            "public": 0.15,
            "consulting": 0.12,
            "general": 0.12,
        }
    },
    7: {
        "title": "INVESTMENT & ROI",
        "subtitle": "투자 비용 & 기대효과",
        "purpose": "예산, 정량적 효과, ROI",
        "recommended_slides": (4, 8),
        "weight_by_type": {
            "marketing_pr": 0.05,
            "event": 0.06,
            "it_system": 0.08,
            "public": 0.07,
            "consulting": 0.08,
            "general": 0.07,
        }
    },
}


# Modern 스타일 디자인 설정
DESIGN_STYLE = {
    "name": "modern",
    "description": "Modern 제안서 스타일 - 모던하고 임팩트 있는 디자인",

    # 컬러 팔레트
    "colors": {
        "primary": "#002C5F",      # 다크 블루
        "secondary": "#00AAD2",    # 스카이블루
        "accent": "#E63312",       # 액센트 레드
        "background": "#FFFFFF",
        "dark_bg": "#1A1A1A",      # 다크 배경
        "text_primary": "#333333",
        "text_secondary": "#666666",
        "text_light": "#FFFFFF",
    },

    # 타이포그래피
    "typography": {
        "title_font": "Pretendard",
        "body_font": "Pretendard",
        "title_size": 44,
        "subtitle_size": 28,
        "body_size": 18,
        "caption_size": 14,
        "line_height": 1.5,
    },

    # 레이아웃
    "layout": {
        "slide_width": 1920,
        "slide_height": 1080,
        "margin_top": 80,
        "margin_bottom": 60,
        "margin_left": 100,
        "margin_right": 100,
        "content_gap": 40,
    },

    # 섹션 디바이더 스타일
    "section_divider": {
        "style": "full_bleed_dark",  # 전체 다크 배경
        "title_position": "center",
        "show_number": True,
        "number_style": "large_outline",  # 큰 아웃라인 숫자
    },

    # 티저 슬라이드 스타일
    "teaser": {
        "style": "cinematic",
        "text_animation": "fade_in",
        "background": "gradient_dark",
    },

    # 콘텐츠 슬라이드 스타일
    "content": {
        "bullet_style": "minimal",
        "icon_style": "line",
        "card_style": "shadow_soft",
        "image_treatment": "rounded_corners",
    },

    # 차트 스타일
    "chart": {
        "style": "flat",
        "show_grid": False,
        "bar_radius": 4,
        "line_width": 3,
    },

    # 테이블 스타일
    "table": {
        "header_bg": "#002C5F",
        "header_text": "#FFFFFF",
        "row_alternate": True,
        "border_style": "minimal",
    }
}


# 프로젝트 유형별 구조 가중치 계산 함수
def get_phase_weights(proposal_type: ProposalType) -> Dict[int, float]:
    """프로젝트 유형에 따른 Phase별 권장 비중 반환"""
    weights = {}
    type_key = proposal_type.value

    for phase_num, phase_def in PHASE_DEFINITIONS.items():
        weights[phase_num] = phase_def["weight_by_type"].get(type_key, 0.1)

    return weights


def get_recommended_pages(proposal_type: ProposalType, total_pages: int = 100) -> Dict[int, tuple]:
    """프로젝트 유형과 총 페이지 수에 따른 Phase별 권장 페이지 수 반환"""
    weights = get_phase_weights(proposal_type)
    recommended = {}

    for phase_num, weight in weights.items():
        base_pages = int(total_pages * weight)
        # 최소/최대 범위 설정
        min_pages = max(3, int(base_pages * 0.7))
        max_pages = int(base_pages * 1.3)
        recommended[phase_num] = (min_pages, max_pages)

    return recommended

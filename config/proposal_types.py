"""
프로젝트 유형별 제안서 구조 설정

각 프로젝트 유형에 맞는 Phase 구성, 권장 페이지 수, 특화 콘텐츠 정의
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class ProposalType(str, Enum):
    """제안서 유형"""
    MARKETING_PR = "marketing_pr"      # 마케팅/PR/소셜미디어
    EVENT = "event"                    # 이벤트/행사
    IT_SYSTEM = "it_system"            # IT/시스템
    PUBLIC = "public"                  # 공공/입찰
    CONSULTING = "consulting"          # 컨설팅
    GENERAL = "general"                # 일반


@dataclass
class PhaseConfig:
    """Phase 구성 설정"""
    title: str
    subtitle: str
    weight: float                      # 전체 대비 비중 (0.0 ~ 1.0)
    min_slides: int
    max_slides: int
    required: bool = True
    special_focus: Optional[List[str]] = None  # 특별히 강조할 요소


@dataclass
class ProposalTypeConfig:
    """프로젝트 유형별 설정"""
    type_name: str
    description: str
    total_pages_range: tuple           # (min, max)
    phases: Dict[int, PhaseConfig]
    special_features: List[str]        # 특화 기능
    recommended_style: str = "modern"


# 마케팅/PR 프로젝트 설정
MARKETING_PR_CONFIG = ProposalTypeConfig(
    type_name="마케팅/PR",
    description="소셜미디어 운영, 브랜드 마케팅, PR 캠페인",
    total_pages_range=(100, 150),
    phases={
        0: PhaseConfig(
            title="HOOK",
            subtitle="임팩트 있는 오프닝",
            weight=0.08,
            min_slides=5,
            max_slides=10,
            special_focus=["트렌드 선언", "비전 제시", "시각적 임팩트"]
        ),
        1: PhaseConfig(
            title="SUMMARY",
            subtitle="Executive Summary",
            weight=0.05,
            min_slides=3,
            max_slides=5,
            special_focus=["KPI 약속", "차별점"]
        ),
        2: PhaseConfig(
            title="INSIGHT",
            subtitle="시장 환경 & 문제 정의",
            weight=0.12,
            min_slides=8,
            max_slides=15,
            special_focus=["소비자 트렌드", "경쟁 환경", "기술 트렌드 (AI, 숏폼)"]
        ),
        3: PhaseConfig(
            title="CONCEPT & STRATEGY",
            subtitle="핵심 컨셉 & 전략",
            weight=0.12,
            min_slides=8,
            max_slides=15,
            special_focus=["채널별 역할", "콘텐츠 필러", "차별화 전략"]
        ),
        4: PhaseConfig(
            title="ACTION PLAN",
            subtitle="상세 실행 계획",
            weight=0.40,
            min_slides=30,
            max_slides=60,
            special_focus=[
                "채널별 상세 전략 (Instagram, YouTube 등)",
                "캠페인 상세 기획",
                "실제 콘텐츠 예시",
                "인플루언서 협업",
                "광고/미디어 전략",
                "예산 계획"
            ]
        ),
        5: PhaseConfig(
            title="MANAGEMENT",
            subtitle="운영 & 품질 관리",
            weight=0.08,
            min_slides=6,
            max_slides=10,
            special_focus=["콘텐츠 검수 프로세스", "퍼포먼스 리포팅", "VOC 모니터링"]
        ),
        6: PhaseConfig(
            title="WHY US",
            subtitle="수행 역량",
            weight=0.10,
            min_slides=8,
            max_slides=15,
            special_focus=["SNS 운영 실적", "캠페인 사례", "크리에이티브 역량"]
        ),
        7: PhaseConfig(
            title="INVESTMENT & ROI",
            subtitle="투자 & 기대효과",
            weight=0.05,
            min_slides=4,
            max_slides=8,
            special_focus=["미디어 밸류", "인게이지먼트 ROI"]
        ),
    },
    special_features=[
        "콘텐츠 예시 (비주얼, 카피)",
        "채널별 전략",
        "캠페인 기획",
        "인플루언서 협업 계획",
        "숏폼/릴스 전략",
        "AI 콘텐츠 활용"
    ]
)


# 이벤트/행사 프로젝트 설정
EVENT_CONFIG = ProposalTypeConfig(
    type_name="이벤트/행사",
    description="기업 행사, 컨퍼런스, 전시회, 프로모션 이벤트",
    total_pages_range=(80, 120),
    phases={
        0: PhaseConfig(
            title="HOOK",
            subtitle="임팩트 있는 오프닝",
            weight=0.06,
            min_slides=3,
            max_slides=8,
            special_focus=["이벤트 비전", "기대 경험"]
        ),
        1: PhaseConfig(
            title="SUMMARY",
            subtitle="Executive Summary",
            weight=0.05,
            min_slides=3,
            max_slides=5
        ),
        2: PhaseConfig(
            title="INSIGHT",
            subtitle="환경 분석",
            weight=0.08,
            min_slides=5,
            max_slides=10,
            special_focus=["타겟 오디언스", "벤치마킹", "트렌드"]
        ),
        3: PhaseConfig(
            title="CONCEPT & STRATEGY",
            subtitle="이벤트 컨셉",
            weight=0.10,
            min_slides=6,
            max_slides=12,
            special_focus=["테마/컨셉", "공간 연출", "경험 설계"]
        ),
        4: PhaseConfig(
            title="ACTION PLAN",
            subtitle="실행 계획",
            weight=0.45,
            min_slides=35,
            max_slides=55,
            special_focus=[
                "세부 프로그램",
                "공간/부스 설계",
                "연출 계획",
                "참가자 동선",
                "온/오프라인 연계",
                "일정표 (타임테이블)"
            ]
        ),
        5: PhaseConfig(
            title="MANAGEMENT",
            subtitle="운영 관리",
            weight=0.10,
            min_slides=6,
            max_slides=12,
            special_focus=["현장 운영", "안전 관리", "비상 대응"]
        ),
        6: PhaseConfig(
            title="WHY US",
            subtitle="수행 역량",
            weight=0.10,
            min_slides=6,
            max_slides=12,
            special_focus=["이벤트 실적", "협력사 네트워크"]
        ),
        7: PhaseConfig(
            title="INVESTMENT & ROI",
            subtitle="투자 & 효과",
            weight=0.06,
            min_slides=4,
            max_slides=8
        ),
    },
    special_features=[
        "공간 설계도",
        "프로그램 타임테이블",
        "연출 계획",
        "안전 관리 계획",
        "참가자 경험 여정"
    ]
)


# IT/시스템 프로젝트 설정
IT_SYSTEM_CONFIG = ProposalTypeConfig(
    type_name="IT/시스템",
    description="시스템 구축, 소프트웨어 개발, 플랫폼 구축",
    total_pages_range=(60, 100),
    phases={
        0: PhaseConfig(
            title="HOOK",
            subtitle="오프닝",
            weight=0.03,
            min_slides=2,
            max_slides=4,
            special_focus=["디지털 전환 비전"]
        ),
        1: PhaseConfig(
            title="SUMMARY",
            subtitle="Executive Summary",
            weight=0.08,
            min_slides=4,
            max_slides=6,
            special_focus=["기술적 차별점", "성능 KPI"]
        ),
        2: PhaseConfig(
            title="INSIGHT",
            subtitle="현황 분석",
            weight=0.12,
            min_slides=6,
            max_slides=12,
            special_focus=["As-Is 분석", "요구사항 분석", "기술 동향"]
        ),
        3: PhaseConfig(
            title="CONCEPT & STRATEGY",
            subtitle="아키텍처 & 전략",
            weight=0.10,
            min_slides=5,
            max_slides=10,
            special_focus=["시스템 아키텍처", "기술 스택", "보안 전략"]
        ),
        4: PhaseConfig(
            title="ACTION PLAN",
            subtitle="구축 계획",
            weight=0.35,
            min_slides=20,
            max_slides=35,
            special_focus=[
                "WBS",
                "Phase별 상세 계획",
                "산출물 목록",
                "테스트 계획",
                "마이그레이션 계획"
            ]
        ),
        5: PhaseConfig(
            title="MANAGEMENT",
            subtitle="프로젝트 관리",
            weight=0.12,
            min_slides=6,
            max_slides=12,
            special_focus=["품질 관리", "형상 관리", "리스크 관리"]
        ),
        6: PhaseConfig(
            title="WHY US",
            subtitle="수행 역량",
            weight=0.12,
            min_slides=6,
            max_slides=12,
            special_focus=["기술 인력", "유사 구축 실적", "인증"]
        ),
        7: PhaseConfig(
            title="INVESTMENT & ROI",
            subtitle="투자 & 효과",
            weight=0.08,
            min_slides=4,
            max_slides=8,
            special_focus=["TCO 분석", "운영 비용 절감"]
        ),
    },
    special_features=[
        "시스템 아키텍처 다이어그램",
        "WBS",
        "간트 차트",
        "인력 투입 계획",
        "산출물 목록"
    ]
)


# 공공/입찰 프로젝트 설정
PUBLIC_CONFIG = ProposalTypeConfig(
    type_name="공공/입찰",
    description="정부/지자체 사업, 공공 입찰",
    total_pages_range=(60, 90),
    phases={
        0: PhaseConfig(
            title="HOOK",
            subtitle="오프닝",
            weight=0.03,
            min_slides=2,
            max_slides=3,
            special_focus=["정책 부합성"]
        ),
        1: PhaseConfig(
            title="SUMMARY",
            subtitle="Executive Summary",
            weight=0.08,
            min_slides=4,
            max_slides=6
        ),
        2: PhaseConfig(
            title="INSIGHT",
            subtitle="사업 이해",
            weight=0.15,
            min_slides=8,
            max_slides=15,
            special_focus=["RFP 요구사항 대응", "정책 연계", "현황 진단"]
        ),
        3: PhaseConfig(
            title="CONCEPT & STRATEGY",
            subtitle="추진 전략",
            weight=0.10,
            min_slides=5,
            max_slides=10,
            special_focus=["추진 방향", "핵심 전략"]
        ),
        4: PhaseConfig(
            title="ACTION PLAN",
            subtitle="세부 추진 계획",
            weight=0.30,
            min_slides=18,
            max_slides=30,
            special_focus=[
                "세부 과업 내용",
                "추진 일정",
                "산출물",
                "성과 지표"
            ]
        ),
        5: PhaseConfig(
            title="MANAGEMENT",
            subtitle="사업 관리",
            weight=0.12,
            min_slides=6,
            max_slides=12,
            special_focus=["조직 체계", "보고 체계", "보안 관리"]
        ),
        6: PhaseConfig(
            title="WHY US",
            subtitle="수행 역량",
            weight=0.15,
            min_slides=8,
            max_slides=15,
            special_focus=["유사 사업 실적", "인력 보유 현황", "재무 안정성"]
        ),
        7: PhaseConfig(
            title="INVESTMENT & ROI",
            subtitle="사업비 & 기대효과",
            weight=0.07,
            min_slides=4,
            max_slides=8
        ),
    },
    special_features=[
        "RFP 요구사항 대응표",
        "정책 연계표",
        "인력 투입 계획",
        "유사 실적 증빙"
    ]
)


# 컨설팅 프로젝트 설정
CONSULTING_CONFIG = ProposalTypeConfig(
    type_name="컨설팅",
    description="경영 컨설팅, 전략 컨설팅, 디지털 전환 컨설팅",
    total_pages_range=(50, 80),
    phases={
        0: PhaseConfig(
            title="HOOK",
            subtitle="오프닝",
            weight=0.05,
            min_slides=2,
            max_slides=5,
            special_focus=["인사이트 제시"]
        ),
        1: PhaseConfig(
            title="SUMMARY",
            subtitle="Executive Summary",
            weight=0.08,
            min_slides=3,
            max_slides=6
        ),
        2: PhaseConfig(
            title="INSIGHT",
            subtitle="진단 & 분석",
            weight=0.15,
            min_slides=8,
            max_slides=15,
            special_focus=["현황 진단", "벤치마킹", "Gap 분석"]
        ),
        3: PhaseConfig(
            title="CONCEPT & STRATEGY",
            subtitle="전략 방향",
            weight=0.12,
            min_slides=6,
            max_slides=12,
            special_focus=["전략 프레임워크", "핵심 이니셔티브"]
        ),
        4: PhaseConfig(
            title="ACTION PLAN",
            subtitle="실행 로드맵",
            weight=0.30,
            min_slides=15,
            max_slides=25,
            special_focus=[
                "단계별 추진 계획",
                "Quick Win",
                "장기 과제"
            ]
        ),
        5: PhaseConfig(
            title="MANAGEMENT",
            subtitle="추진 체계",
            weight=0.10,
            min_slides=5,
            max_slides=10,
            special_focus=["거버넌스", "변화 관리"]
        ),
        6: PhaseConfig(
            title="WHY US",
            subtitle="수행 역량",
            weight=0.12,
            min_slides=6,
            max_slides=12,
            special_focus=["컨설턴트 프로필", "유사 프로젝트"]
        ),
        7: PhaseConfig(
            title="INVESTMENT & ROI",
            subtitle="투자 & 효과",
            weight=0.08,
            min_slides=4,
            max_slides=8
        ),
    },
    special_features=[
        "전략 프레임워크",
        "벤치마킹 분석",
        "로드맵",
        "Quick Win 과제"
    ]
)


# 일반 프로젝트 설정
GENERAL_CONFIG = ProposalTypeConfig(
    type_name="일반",
    description="기타 일반 프로젝트",
    total_pages_range=(50, 80),
    phases={
        0: PhaseConfig(
            title="HOOK",
            subtitle="오프닝",
            weight=0.05,
            min_slides=2,
            max_slides=5
        ),
        1: PhaseConfig(
            title="SUMMARY",
            subtitle="Executive Summary",
            weight=0.06,
            min_slides=3,
            max_slides=5
        ),
        2: PhaseConfig(
            title="INSIGHT",
            subtitle="현황 분석",
            weight=0.10,
            min_slides=5,
            max_slides=10
        ),
        3: PhaseConfig(
            title="CONCEPT & STRATEGY",
            subtitle="전략 방향",
            weight=0.10,
            min_slides=5,
            max_slides=10
        ),
        4: PhaseConfig(
            title="ACTION PLAN",
            subtitle="실행 계획",
            weight=0.35,
            min_slides=18,
            max_slides=30
        ),
        5: PhaseConfig(
            title="MANAGEMENT",
            subtitle="운영 관리",
            weight=0.10,
            min_slides=5,
            max_slides=10
        ),
        6: PhaseConfig(
            title="WHY US",
            subtitle="수행 역량",
            weight=0.12,
            min_slides=6,
            max_slides=12
        ),
        7: PhaseConfig(
            title="INVESTMENT & ROI",
            subtitle="투자 & 효과",
            weight=0.07,
            min_slides=4,
            max_slides=8
        ),
    },
    special_features=[]
)


# 유형별 설정 매핑
PROPOSAL_TYPE_CONFIGS: Dict[ProposalType, ProposalTypeConfig] = {
    ProposalType.MARKETING_PR: MARKETING_PR_CONFIG,
    ProposalType.EVENT: EVENT_CONFIG,
    ProposalType.IT_SYSTEM: IT_SYSTEM_CONFIG,
    ProposalType.PUBLIC: PUBLIC_CONFIG,
    ProposalType.CONSULTING: CONSULTING_CONFIG,
    ProposalType.GENERAL: GENERAL_CONFIG,
}


def get_config(proposal_type: ProposalType) -> ProposalTypeConfig:
    """프로젝트 유형에 맞는 설정 반환"""
    return PROPOSAL_TYPE_CONFIGS.get(proposal_type, GENERAL_CONFIG)


def get_phase_config(proposal_type: ProposalType, phase_number: int) -> PhaseConfig:
    """특정 Phase 설정 반환"""
    config = get_config(proposal_type)
    return config.phases.get(phase_number)


def calculate_pages(proposal_type: ProposalType, total_pages: int = 100) -> Dict[int, tuple]:
    """유형과 총 페이지에 따른 Phase별 페이지 수 계산"""
    config = get_config(proposal_type)
    result = {}

    for phase_num, phase_config in config.phases.items():
        base_pages = int(total_pages * phase_config.weight)
        min_pages = max(phase_config.min_slides, int(base_pages * 0.8))
        max_pages = min(phase_config.max_slides, int(base_pages * 1.2))
        result[phase_num] = (min_pages, max_pages)

    return result


def get_prompt_file(phase_number: int) -> str:
    """Phase 번호에 해당하는 프롬프트 파일 경로 반환"""
    phase_names = {
        0: "hook",
        1: "summary",
        2: "insight",
        3: "concept",
        4: "action",
        5: "management",
        6: "whyus",
        7: "investment",
    }
    name = phase_names.get(phase_number, "general")
    return f"config/prompts/phase{phase_number}_{name}.txt"

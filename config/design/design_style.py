"""
Modern 스타일 디자인 설정 ([발주처명] 제안서 기반)

실제 수주 성공 제안서를 분석하여 추출한 디자인 시스템
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class SlideBackground(str, Enum):
    """슬라이드 배경 유형"""
    WHITE = "white"
    DARK = "dark"
    GRADIENT_DARK = "gradient_dark"
    IMAGE = "image"
    ACCENT = "accent"


class LayoutType(str, Enum):
    """레이아웃 유형"""
    FULL_BLEED = "full_bleed"      # 전체 화면
    CENTERED = "centered"          # 중앙 정렬
    LEFT_HEAVY = "left_heavy"      # 왼쪽 강조
    RIGHT_HEAVY = "right_heavy"    # 오른쪽 강조
    SPLIT = "split"                # 좌우 분할
    GRID = "grid"                  # 그리드
    CARD = "card"                  # 카드형


@dataclass
class ColorPalette:
    """컬러 팔레트"""
    primary: str = "#002C5F"           # 다크 블루
    secondary: str = "#00AAD2"         # 스카이블루
    accent: str = "#E63312"            # 액센트 레드
    accent_secondary: str = "#00A19C"  # 청록색

    background_white: str = "#FFFFFF"
    background_light: str = "#F5F5F5"
    background_dark: str = "#1A1A1A"
    background_gradient_start: str = "#1A1A1A"
    background_gradient_end: str = "#2D2D2D"

    text_primary: str = "#333333"
    text_secondary: str = "#666666"
    text_light: str = "#FFFFFF"
    text_muted: str = "#999999"

    success: str = "#00A19C"
    warning: str = "#F5A623"
    error: str = "#E63312"

    chart_colors: List[str] = field(default_factory=lambda: [
        "#002C5F", "#00AAD2", "#E63312", "#00A19C",
        "#F5A623", "#8B5CF6", "#EC4899", "#10B981"
    ])


@dataclass
class Typography:
    """타이포그래피 설정"""
    # 폰트 패밀리
    title_font: str = "Pretendard"
    body_font: str = "Pretendard"
    accent_font: str = "Pretendard"

    # 폰트 사이즈 (pt)
    title_hero: int = 72           # 티저용 대형 타이틀
    title_large: int = 48          # 섹션 타이틀
    title_medium: int = 36         # 슬라이드 타이틀
    title_small: int = 28          # 서브 타이틀

    subtitle: int = 24
    body_large: int = 20
    body: int = 18
    body_small: int = 16
    caption: int = 14
    footnote: int = 12

    # 라인 높이
    line_height_tight: float = 1.2
    line_height_normal: float = 1.5
    line_height_relaxed: float = 1.8

    # 폰트 웨이트
    weight_light: int = 300
    weight_regular: int = 400
    weight_medium: int = 500
    weight_semibold: int = 600
    weight_bold: int = 700
    weight_extrabold: int = 800


@dataclass
class Layout:
    """레이아웃 설정"""
    # 슬라이드 크기 (16:9)
    slide_width: int = 1920
    slide_height: int = 1080

    # 여백
    margin_top: int = 80
    margin_bottom: int = 60
    margin_left: int = 100
    margin_right: int = 100

    # 콘텐츠 영역
    content_width: int = 1720  # slide_width - margin_left - margin_right
    content_height: int = 940  # slide_height - margin_top - margin_bottom

    # 간격
    section_gap: int = 60
    content_gap: int = 40
    item_gap: int = 24
    card_gap: int = 32

    # 그리드
    grid_columns: int = 12
    grid_gutter: int = 24


@dataclass
class SectionDividerStyle:
    """섹션 구분자 스타일"""
    background: SlideBackground = SlideBackground.DARK
    title_position: str = "center"  # "center", "left", "bottom_left"
    show_number: bool = True
    number_style: str = "large_outline"  # "large_outline", "small_filled", "none"
    number_size: int = 200
    number_opacity: float = 0.1
    title_color: str = "#FFFFFF"
    subtitle_color: str = "#00AAD2"


@dataclass
class TeaserStyle:
    """티저 슬라이드 스타일"""
    background: SlideBackground = SlideBackground.GRADIENT_DARK
    text_position: str = "center"
    title_size: int = 72
    title_weight: int = 700
    title_color: str = "#FFFFFF"
    subtitle_color: str = "#00AAD2"
    animation_hint: str = "fade_in"


@dataclass
class ContentStyle:
    """콘텐츠 슬라이드 스타일"""
    bullet_style: str = "minimal"  # "minimal", "numbered", "icon"
    bullet_color: str = "#00AAD2"
    bullet_size: int = 8

    icon_style: str = "line"  # "line", "filled", "duotone"
    icon_size: int = 24

    card_background: str = "#FFFFFF"
    card_border_radius: int = 12
    card_shadow: str = "0 4px 12px rgba(0,0,0,0.08)"
    card_padding: int = 24

    highlight_background: str = "#002C5F"
    highlight_text_color: str = "#FFFFFF"


@dataclass
class TableStyle:
    """테이블 스타일"""
    header_background: str = "#002C5F"
    header_text_color: str = "#FFFFFF"
    header_font_weight: int = 600

    row_background: str = "#FFFFFF"
    row_alternate_background: str = "#F5F5F5"
    row_hover_background: str = "#E8F4F8"

    border_color: str = "#E0E0E0"
    border_width: int = 1
    border_style: str = "minimal"  # "minimal", "full", "horizontal"

    cell_padding: int = 16
    cell_align: str = "left"  # "left", "center", "right"


@dataclass
class ChartStyle:
    """차트 스타일"""
    style: str = "flat"  # "flat", "gradient", "3d"
    show_grid: bool = False
    grid_color: str = "#E0E0E0"

    bar_radius: int = 4
    bar_gap: float = 0.3

    line_width: int = 3
    line_style: str = "smooth"  # "smooth", "straight"
    show_dots: bool = True
    dot_size: int = 6

    pie_inner_radius: float = 0  # 0 for pie, 0.5+ for donut
    pie_label_position: str = "outside"  # "inside", "outside"

    show_values: bool = True
    show_legend: bool = True
    legend_position: str = "bottom"  # "top", "bottom", "left", "right"


@dataclass
class KPIStyle:
    """KPI 카드 스타일"""
    layout: str = "horizontal"  # "horizontal", "vertical", "grid"
    card_background: str = "#FFFFFF"
    card_border: str = "1px solid #E0E0E0"
    card_border_radius: int = 12
    card_shadow: str = "0 2px 8px rgba(0,0,0,0.06)"

    number_size: int = 48
    number_weight: int = 700
    number_color: str = "#002C5F"

    label_size: int = 16
    label_color: str = "#666666"

    trend_up_color: str = "#00A19C"
    trend_down_color: str = "#E63312"


# ============================================================
# v3.1 신규 스타일 - Win Theme, Executive Summary, Next Step
# ============================================================

@dataclass
class WinThemeBadgeStyle:
    """Win Theme 배지 스타일 (섹션 구분자 하단에 표시)"""
    background: str = "#00AAD2"     # secondary 컬러
    text_color: str = "#FFFFFF"
    font_size: int = 14
    font_weight: int = 600
    height: int = 36
    border_radius: int = 4
    icon: str = "💡"               # Win Theme 아이콘
    prefix: str = "Win Theme: "


@dataclass
class ExecutiveSummaryStyle:
    """Executive Summary 슬라이드 스타일"""
    background: str = "#FFFFFF"
    accent_bar_color: str = "#002C5F"
    accent_bar_width: int = 8

    section_title_size: int = 16
    section_title_color: str = "#333333"
    section_title_weight: int = 600

    objective_box_background: str = "#002C5F"
    objective_text_color: str = "#FFFFFF"

    win_theme_card_height: int = 100
    win_theme_gap: int = 24

    kpi_card_background: str = "#F5F5F5"
    kpi_card_height: int = 100

    why_us_icon: str = "✓"
    why_us_color: str = "#00AAD2"


@dataclass
class NextStepStyle:
    """Next Step 슬라이드 스타일"""
    background: str = "#FFFFFF"
    accent_bar_color: str = "#002C5F"
    accent_bar_width: int = 8

    headline_size: int = 28
    headline_color: str = "#333333"
    headline_weight: int = 700

    step_card_height: int = 120
    step_primary_color: str = "#002C5F"    # 첫 번째 스텝
    step_secondary_color: str = "#00AAD2"  # 나머지 스텝
    step_text_color: str = "#FFFFFF"

    cta_box_background: str = "#F5F5F5"
    cta_item_icon: str = "✓"

    contact_text_color: str = "#666666"
    contact_text_size: int = 14


@dataclass
class DifferentiationStyle:
    """차별화 포인트 슬라이드 스타일"""
    card_height: int = 220
    card_gap: int = 24

    card_colors: List[str] = field(default_factory=lambda: [
        "#002C5F",   # primary
        "#00AAD2",   # secondary
        "#00A19C",   # teal
        "#00A19C",   # teal (repeated)
    ])

    title_size: int = 16
    title_weight: int = 700
    title_color: str = "#FFFFFF"

    content_size: int = 14
    content_color: str = "#FFFFFF"

    why_us_section_title: str = "왜 저희인가?"
    why_us_badge_color: str = "#002C5F"
    why_us_badge_text_color: str = "#FFFFFF"


@dataclass
class ProposalDesignStyle:
    """Modern 전체 디자인 스타일 (v3.1)"""
    name: str = "modern"
    description: str = "Modern 제안서 스타일 - 모던하고 임팩트 있는 디자인"

    colors: ColorPalette = field(default_factory=ColorPalette)
    typography: Typography = field(default_factory=Typography)
    layout: Layout = field(default_factory=Layout)

    section_divider: SectionDividerStyle = field(default_factory=SectionDividerStyle)
    teaser: TeaserStyle = field(default_factory=TeaserStyle)
    content: ContentStyle = field(default_factory=ContentStyle)
    table: TableStyle = field(default_factory=TableStyle)
    chart: ChartStyle = field(default_factory=ChartStyle)
    kpi: KPIStyle = field(default_factory=KPIStyle)

    # v3.1 추가 스타일
    win_theme_badge: WinThemeBadgeStyle = field(default_factory=WinThemeBadgeStyle)
    executive_summary: ExecutiveSummaryStyle = field(default_factory=ExecutiveSummaryStyle)
    next_step: NextStepStyle = field(default_factory=NextStepStyle)
    differentiation: DifferentiationStyle = field(default_factory=DifferentiationStyle)


# 기본 Modern 스타일 인스턴스
DEFAULT_STYLE = ProposalDesignStyle()


# Phase별 권장 스타일 (v3.1 - Win Theme, Story Title 추가)
PHASE_STYLES = {
    0: {  # HOOK
        "background": SlideBackground.GRADIENT_DARK,
        "title_size": 72,
        "text_color": "#FFFFFF",
        "accent_color": "#00AAD2",
        "layout": LayoutType.CENTERED,
        "story_title": None,  # HOOK은 스토리 타이틀 없음
        "suggested_win_themes": [],  # HOOK은 Win Theme 없음
    },
    1: {  # SUMMARY (사업 이해)
        "background": SlideBackground.WHITE,
        "title_size": 36,
        "layout": LayoutType.LEFT_HEAVY,
        "use_charts": True,
        "story_title": "~를 이해하다",
        "suggested_win_themes": ["데이터 기반 타겟 마케팅"],
    },
    2: {  # INSIGHT (전략)
        "background": SlideBackground.WHITE,
        "title_size": 36,
        "layout": LayoutType.CENTERED,
        "accent_slides": True,
        "story_title": "~를 설계하다",
        "suggested_win_themes": ["온-오프라인 통합 시너지"],
    },
    3: {  # CONCEPT & STRATEGY (뉴미디어)
        "background": SlideBackground.WHITE,
        "title_size": 32,
        "layout": LayoutType.GRID,
        "use_examples": True,
        "story_title": "~를 말하다",
        "suggested_win_themes": ["데이터 기반 타겟 마케팅"],
    },
    4: {  # ACTION PLAN (시민참여)
        "background": SlideBackground.WHITE,
        "title_size": 32,
        "layout": LayoutType.GRID,
        "use_examples": True,
        "story_title": "~를 경험하다",
        "suggested_win_themes": ["시민 참여형 브랜드 빌딩"],
    },
    5: {  # MANAGEMENT (오프라인)
        "background": SlideBackground.WHITE,
        "title_size": 32,
        "layout": LayoutType.LEFT_HEAVY,
        "use_process": True,
        "story_title": "~를 알리다",
        "suggested_win_themes": ["온-오프라인 통합 시너지"],
    },
    6: {  # WHY US (사업관리)
        "background": SlideBackground.WHITE,
        "title_size": 32,
        "layout": LayoutType.LEFT_HEAVY,
        "use_process": True,
        "story_title": "~를 관리하다",
        "suggested_win_themes": ["데이터 기반 타겟 마케팅"],
    },
    7: {  # INVESTMENT & ROI (수행역량)
        "background": SlideBackground.WHITE,
        "title_size": 32,
        "layout": LayoutType.CARD,
        "use_case_studies": True,
        "story_title": "~를 실현하다",
        "suggested_win_themes": ["검증된 전문성과 실행력"],
    },
}


# Win Theme 예시 템플릿
WIN_THEME_TEMPLATES = {
    "marketing_pr": [
        {
            "name": "데이터 기반 타겟 마케팅",
            "description": "타겟 고객의 행동 패턴 분석을 통한 최적화된 마케팅 전략",
            "related_phases": [1, 3, 6],
        },
        {
            "name": "시민 참여형 브랜드 빌딩",
            "description": "오프라인 커뮤니티를 통한 지속가능한 브랜드 자산 구축",
            "related_phases": [4, 5],
        },
        {
            "name": "온-오프라인 통합 시너지",
            "description": "디지털-물리적 접점의 유기적 연계로 시너지 극대화",
            "related_phases": [2, 5],
        },
    ],
    "event": [
        {
            "name": "몰입형 경험 설계",
            "description": "참가자 중심의 기억에 남는 경험 창출",
            "related_phases": [2, 4],
        },
        {
            "name": "안전하고 체계적인 운영",
            "description": "리스크 제로를 위한 철저한 사전 준비와 현장 관리",
            "related_phases": [5, 6],
        },
    ],
    "general": [
        {
            "name": "검증된 전문성",
            "description": "유사 프로젝트 수행 경험을 통한 안정적 실행력",
            "related_phases": [7],
        },
        {
            "name": "고객 중심 접근",
            "description": "발주처의 니즈를 정확히 이해하고 맞춤형 솔루션 제공",
            "related_phases": [1, 2],
        },
    ],
}


# ═══════════════════════════════════════════════════════════════
#  v3.4 — 레이아웃 규칙 + 컨셉 슬라이드 패턴 (테스트 06 검증)
# ═══════════════════════════════════════════════════════════════

LAYOUT_RULES = {
    # Zone 시스템 (slide_kit.py Z 상수와 동기화)
    "zone_system": {
        "title_bar": {"top": 0, "bottom": 0.88, "desc": "타이틀 바 (TB 함수)"},
        "content":   {"top": 1.1, "bottom": 6.5, "desc": "콘텐츠 영역 (5.4\" 가용)"},
        "footer":    {"top": 6.7, "bottom": 7.5, "desc": "푸터 (PN, source)"},
    },
    # 요소 간 최소 간격 (인치) — 겹침 방지
    "spacing": {
        "highlight_to_next": 0.75,   # HIGHLIGHT → 다음 요소 (HIGHLIGHT 높이 ~0.65-0.7")
        "metric_card_gap": 0.15,     # METRIC_CARD → 다음 요소
        "cols_to_next": 0.2,         # COLS → 다음 요소
        "text_to_visual": 0.2,       # 텍스트 → 시각 요소
        "img_ph_min_height": 0.5,    # IMG_PH 최소 높이
    },
    # MT(불릿 텍스트) 높이 가이드 (body_sm + ls 1.7 기준)
    "mt_height": {
        "per_line": 0.35,            # 1줄당 적정 높이
        3: 1.1,  4: 1.4,  5: 1.7,  6: 2.0,  8: 2.8,
    },
    # 한글 텍스트 너비 (인치/글자)
    "korean_char_width": {
        44: 0.61,  36: 0.50,  28: 0.39,  24: 0.33,  18: 0.25,
    },
    # 전략적 여백 (수정 불필요 대상)
    "intentional_gaps": [
        "slide_cover", "slide_closing", "slide_section_divider",
        "slide_next_step", "concept_reveal",
    ],
}

# 컨셉 슬라이드 패턴 — Phase 3에 필수 적용
CONCEPT_PATTERNS = {
    "concept_reveal": {
        "desc": "다크 배경 + 대형 컨셉 키워드(60pt) + 4단계 순환 흐름",
        "bg": "dark",
        "elements": [
            "상단 라벨 (CORE CONCEPT, 14pt secondary)",
            "대형 컨셉 키워드 (60pt white, 중앙정렬)",
            "구분선 (secondary, 2.5\")",
            "부제 설명 (subtitle, lgray, 중앙정렬)",
            "4단계 가로 카드 (BOX + 설명 텍스트)",
            "순환 화살표 (→ 연결, ↻ 선순환 텍스트)",
        ],
        "usage": "Phase 3 섹션 구분자 직후, 핵심 컨셉 임팩트 전달",
    },
    "strategy_synergy_map": {
        "desc": "3대 Win Theme 연결 구조 시각화",
        "bg": "white",
        "elements": [
            "상단 허브 박스 (다크 배경, 통합 컨셉 설명)",
            "3개 전략 카드 (BOX 헤더 + MT 불릿)",
            "순환 연결 바 (secondary 라인 + 순환 텍스트)",
            "하단 IMG_PH (인포그래픽 영역)",
        ],
        "usage": "Phase 3 전략 연결 구조 시각화 (Concept Reveal 다음)",
    },
    "hero_statement": {
        "desc": "다크 배경 + 2줄 분리 대형 타이틀 + 수치 카드",
        "bg": "dark",
        "elements": [
            "소제목 라벨 (14pt secondary)",
            "2줄 분리 타이틀 (각각 별도 T() 호출, 44pt)",
            "구분선 + 설명 텍스트",
            "좌 IMG_PH + 우 수치 스택",
        ],
        "usage": "Phase 0 비전 슬라이드 — 긴 한글 제목은 반드시 2줄 분리",
    },
    "big_idea_reveal": {
        "desc": "대형 컨셉 텍스트(36pt) + 3-Step 카드",
        "bg": "white",
        "elements": [
            "중앙정렬 컨셉 (36pt primary bold)",
            "부제 설명 (body gray)",
            "구분선",
            "3단 카드 (BOX 헤더 + 설명 텍스트 + → 연결)",
        ],
        "usage": "핵심 아이디어 전달 (Phase 3)",
    },
    "pillar_cards": {
        "desc": "FLOW 헤더 + N분할 카드 + 하단 이미지",
        "bg": "white",
        "elements": [
            "FLOW 가로 헤더",
            "N개 BOX+텍스트 카드 (2~4분할)",
            "하단 IMG_PH 스트립",
        ],
        "usage": "전략 프레임워크, 실행 계획 (Phase 3, 4)",
    },
}

# 공백 보완 패턴 — 콘텐츠 하단 0.5\"+ 공백 발생 시
GAP_FILL_PATTERNS = {
    "img_ph": {
        "desc": "이미지 플레이스홀더 추가",
        "min_gap": 0.5,  # 적용 기준 (인치)
        "rule": "HIGHLIGHT 아래 0.75\"+ 간격 확보 후 IMG_PH(h=0.5~1.1\")",
    },
    "highlight_summary": {
        "desc": "HIGHLIGHT 요약 바 추가",
        "min_gap": 0.4,
        "rule": "텍스트 아래 0.2\" 간격 후 HIGHLIGHT(color=C['primary'])",
    },
    "metric_expand": {
        "desc": "METRIC_CARD 높이 확대",
        "min_gap": 0.3,
        "rule": "METRIC_CARD h를 0.2~0.3\" 증가 (비율 기반 배치가 자동 대응)",
    },
}


def get_phase_style(phase_number: int) -> Dict:
    """Phase별 스타일 설정 반환"""
    return PHASE_STYLES.get(phase_number, PHASE_STYLES[1])


def export_to_pptx_theme() -> Dict:
    """PPTX 테마용 설정 내보내기"""
    style = DEFAULT_STYLE
    return {
        "colors": {
            "accent1": style.colors.primary,
            "accent2": style.colors.secondary,
            "accent3": style.colors.accent,
            "accent4": style.colors.accent_secondary,
            "dark1": style.colors.text_primary,
            "dark2": style.colors.text_secondary,
            "light1": style.colors.background_white,
            "light2": style.colors.background_light,
        },
        "fonts": {
            "major": style.typography.title_font,
            "minor": style.typography.body_font,
        },
        "sizes": {
            "title": style.typography.title_medium,
            "body": style.typography.body,
        }
    }

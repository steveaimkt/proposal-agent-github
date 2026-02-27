# 입찰 제안서 자동 생성 에이전트 (v3.6 - Impact-8 + slide_kit v3.6 + Layout System + Design Quality)

## 프로젝트 개요
RFP(제안요청서) 문서를 입력받아 PPTX 형식의 입찰 제안서를 자동 생성하는 Python 에이전트 시스템

**작동 방식**: Claude Code가 RFP를 분석하고, `slide_kit.py`를 import하는 Python 생성 스크립트를 직접 작성하여 실행합니다.

**v3.6 업데이트**: v3.5 + 컬러 유틸(darken/lighten) + 21색 확장 팔레트 + 그라디언트 커버/섹션/클로징 + 그림자 프리셋(subtle/normal/elevated/card) + SemiBold/Medium 타이포 계층 + KPIS/GRID/COLS/TABLE/STAT_ROW/METRIC_CARD 시각 폴리시 + LINE_CHART smooth 버그 수정

## ★★★ 제안서 생성 워크플로우 (최우선 규칙)

사용자가 "제안요청서 폴더에 있는 테스트 XX 폴더 내 파일을 분석한 후 제안서를 제작해줘" 라고 요청하면:

### 폴더 구조
```
제안요청서/테스트 XX/    ← RFP 입력 (PDF 문서들)
output/테스트 XX/        ← PPTX 출력 (생성 스크립트 + 결과물)
```

### 실행 단계

**STEP 0: 레퍼런스 디자인 분석** (선택 — input 폴더에 PPTX 있을 때)
- `input/` 폴더에 레퍼런스 PPTX 파일이 있으면 디자인 요소 추출
- 추출 항목: 컬러 팔레트, 폰트, 레이아웃 패턴, 슬라이드 구조
- 추출된 테마를 `apply_theme()` 또는 직접 `C[]` 딕셔너리에 적용
- 사용법:
```python
from src.utils.reference_analyzer import ReferenceAnalyzer
analyzer = ReferenceAnalyzer("input/레퍼런스.pptx")
profile = analyzer.to_design_profile()  # 디자인 프로파일
theme = analyzer.to_slide_kit_theme()   # slide_kit 테마 호환 형식
# slide_kit에 적용:
from src.generators.slide_kit import C, RGBColor
for key, rgb in theme.items():
    if key in C:
        C[key] = RGBColor(*rgb)
```

**STEP 1: RFP 분석** (제안요청서 폴더 내 PDF 읽기)
- `제안요청서/테스트 XX/` 내 모든 PDF를 분석
- 추출 항목: 프로젝트명, 발주처, 과업 범위, 평가 기준, 예산, 일정, 특이사항
- 프로젝트 유형 판별: marketing_pr / event / it_system / public / consulting

**STEP 2: 콘텐츠 기획** (Impact-8 Phase 구조)
- Phase 0~7 콘텐츠를 RFP 맞춤형으로 설계
- Win Theme 3개 도출
- Action Title (인사이트 기반 문장형 제목) 작성
- KPI + 산출근거 설계

**STEP 3: 생성 스크립트 작성**
- `output/테스트 XX/generate_제안서.py` 스크립트 생성
- **반드시 slide_kit.py import** (아래 규칙 참조)
- **LAYOUTS 프리셋 활용** — `get_zones()` 으로 안전 영역 사용
- 목표 분량: 40~80장 (프로젝트 규모에 따라 조정)

**STEP 4: 실행 및 검증**
- 스크립트 실행하여 PPTX 생성
- 오류 발생 시 즉시 수정 후 재실행
- 최종 파일 경로 안내

### 레이아웃 선택 가이드 (내용에 맞게 적용)

| 콘텐츠 유형 | 권장 레이아웃 | slide_kit 함수 |
|------------|-------------|---------------|
| 시장 환경/배경 분석 | `THREE_COL` or `TWO_COL` | `COLS()` or Zone 직접 |
| 핵심 인사이트/메시지 | `HIGHLIGHT_BODY` | `HIGHLIGHT()` |
| 전략 프레임워크 | `PYRAMID_DESC` | `PYRAMID()` |
| 채널/항목 비교 | `COMPARE_LR` | `COMPARE()` |
| 실행 프로세스 | `PROCESS_DESC` | `FLOW()` |
| KPI/성과 목표 | `KPI_GRID` | `KPIS()` |
| 월별 일정 | `GANTT` | `GANTT_CHART()` |
| 조직도 | `ORG_CHART` | `ORG()` |
| 수행 실적 | `GALLERY_3x2` or `GRID` | `GRID()` |
| 리스크 관리 | `RISK_CARD` | Zone 직접 |
| 데이터 비교 | `TABLE_INSIGHT` | `TABLE()` |
| 통계/수치 강조 | `FULL_BODY` | `STAT_ROW()` |
| 타임라인 | `TIMELINE_DESC` | `TIMELINE()` |
| 차별화 포인트 | `FOUR_COL` | `ICON_CARDS()` |
| 우선순위 매트릭스 | `MATRIX_DESC` | `MATRIX()` |
| 프로그램 소개 | `PROGRAM_CARD_3` | Zone 직접 |
| 키비주얼/대표이미지 | `KEY_VISUAL` | `IMG()` + Zone |
| 인용문/핵심 메시지 | `HIGHLIGHT_BODY` | `QUOTE()` |
| 예산/비율 시각화 | `FULL_BODY` | `PIE_CHART()` or `BAR_CHART()` |
| 추세/성장 데이터 | `FULL_BODY` | `LINE_CHART()` |
| 구조화된 항목 | `FULL_BODY` | `NUMBERED_LIST()` |
| 고급 카드 (그림자) | `THREE_COL` or `FOUR_COL` | `CARD()` |

## ★ 필수 규칙: PPTX 생성 스크립트 작성 시

**모든 제안서 생성 스크립트는 반드시 `src/generators/slide_kit.py`를 import하여 사용해야 합니다.**

```python
# 스크립트 상단에 반드시 추가 (output/테스트 XX/ 에서 실행 기준)
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, PROJECT_ROOT)
from src.generators.slide_kit import *
```

**경로 규칙:**
- 생성 스크립트는 `output/테스트 XX/generate_제안서.py` 에 위치
- `../..` 로 프로젝트 루트까지 올라가서 `src/generators/slide_kit.py` import
- 절대경로 하드코딩 금지 → 반드시 `__file__` 기준 상대경로 사용

### slide_kit이 제공하는 것 (v3.6)

| 카테고리 | 함수 | 설명 |
|---------|------|------|
| **상수** | `C`, `SW`, `SH`, `ML`, `CW`, `SZ`, `FONT` | 컬러(21색), 크기, 폰트 |
| **상수 (v3.6)** | `FONT_W`, `SHADOW`, `GRAD` | 폰트 웨이트, 그림자 프리셋, 그라디언트 프리셋 |
| **컬러 유틸 (v3.6)** | `darken()`, `lighten()` | RGBColor 밝기 조절 유틸 |
| **Zone** | `Z`, `GAP`, `CGAP`, `CW_IN`, `ML_IN` | 표준 영역, 간격 |
| **레이아웃** | `LAYOUTS`, `get_zones()`, `zone_to_inches()`, `list_layouts()` | 20가지 프리셋 |
| **도형 (기본)** | `R()`, `BOX()`, `OBOX()` | 직각 사각형, 텍스트 박스, 아웃라인 |
| **도형 (v3.5)** | `RBOX()`, `ORBOX()`, `CARD()` | 라운드 박스, 라운드 아웃라인, 통합 카드 |
| **텍스트** | `T(fn=)`, `RT()`, `MT()` | 단일(fn=FONT_W 지원)/리치/멀티라인 |
| **이펙트** | `gradient_bg()`, `bg()`, `set_char_spacing()` | 그래디언트, 자간 |
| **이펙트 (v3.6)** | `gradient_shape()`, `add_shadow(preset=)`, `OVERLAY()` | 도형 그라디언트, 프리셋 그림자, 오버레이 |
| **구분/악센트** | `DIVIDER()`, `ACCENT_LINE()` | 구분선 3종, 좌측 악센트 |
| **컴포넌트** | `IMG()`, `PN()`, `TB()`, `SRC()`, `WB()` | 이미지홀더, 페이지번호, 타이틀바, 출처, Win Theme |
| **텍스트 블록** | `QUOTE()`, `NUMBERED_LIST()` | 인용문(modern/box), 번호 리스트 |
| **도식화 (기본)** | `FLOW()`, `COLS(shadow=)`, `PYRAMID()`, `MATRIX()`, `TABLE()`, `HIGHLIGHT(grad=)`, `KPIS(shadow=)`, `COMPARE()`, `TIMELINE()` | 플로우, 컬럼(그림자), 피라미드 등 |
| **도식화 (확장)** | `GRID(shadow=)`, `STAT_ROW(shadow=)`, `GANTT_CHART()`, `ORG()`, `ICON_CARDS()` | 그리드(그림자), 통계, 간트, 조직도, 아이콘카드 |
| **차트** | `BAR_CHART()`, `PIE_CHART()`, `LINE_CHART(smooth=)` | 바(세로/가로), 파이/도넛, 라인(곡선 수정) |
| **시각화 헬퍼** | `IMG_PH()`, `PROGRESS_BAR()`, `METRIC_CARD(shadow=)`, `STEP_ARROW()`, `DONUT_LABEL()` | 이미지홀더, 프로그레스, 메트릭카드(그림자), 스텝화살표, 도넛 |
| **슬라이드** | `slide_cover()`, `slide_section_divider()`, `slide_toc()`, `slide_exec_summary()`, `slide_next_step()`, `slide_closing()` | 표지(그라디언트), 구분자(그라디언트), 목차, 요약, CTA(그라디언트), 마지막(그라디언트) |
| **자동 배치** | `VStack` 클래스 | 자동 Y좌표 계산, 겹침 방지 |
| **테마** | `THEMES`, `apply_theme()`, `reset_theme()`, `list_themes()` | 5가지 테마, 동적 색상 변경 |
| **검증** | `validate_sequence()` | 레이아웃 시퀀스 단조로움 검증 |
| **유틸** | `new_presentation()`, `new_presentation_from_template()`, `new_slide()`, `save_pptx()`, `_cols()` | 생성, 템플릿, 저장, 컬럼너비 |

### ★★★ 겹침·공백 방지 규칙 (v3.4 — 테스트 06 검증 결과)

**1. 요소 간 최소 간격 (인치)**
```
HIGHLIGHT → 다음 요소:  0.75"  (HIGHLIGHT 높이 ~0.65-0.7")
COLS       → 다음 요소:  0.30"
METRIC_CARD → 다음 요소:  0.15"
MT(불릿)   → 다음 요소:  0.20"
```

**2. MT(불릿 텍스트) 높이 — 줄 수에 맞춤**
```
3줄=1.1"  4줄=1.4"  5줄=1.7"  6줄=2.0"  8줄=2.8"
❌ 절대 금지: 줄 수와 무관한 고정 높이 (예: 4줄인데 h=3.2")
```

**3. 한글 텍스트 너비 추정**
```
44pt: 0.61"/자 → CW(~11.8") 내 최대 ~18자
36pt: 0.50"/자 → CW 내 최대 ~23자
→ 44pt 제목이 18자 초과 시 반드시 2줄 분리 (별도 T() 호출)
```

**4. 공백 보완 규칙**
- 콘텐츠 하단 공백 > 0.5" → IMG_PH 또는 HIGHLIGHT 추가
- METRIC_CARD 높이 확대 (비율 기반 배치가 자동 대응)
- 섹션 구분자/표지/마지막 슬라이드의 공백은 의도적 → 수정 불필요

**5. 배경색 충돌 방지**
- slide_next_step 배경: C["dark"] (카드가 C["primary"] 등)
- 카드 색상 = 배경 색상이면 반드시 다른 색상으로 변경

**6. Phase 3 필수 컨셉 장표 (3종)**
1. **Concept Reveal** — 다크 배경, 60pt 대형 컨셉 키워드, 4단계 순환 카드
2. **Strategy Synergy Map** — 3대 Win Theme 연결 구조, 순환 흐름도
3. **Big Idea Reveal** — 36pt 중앙 컨셉 + 3-Step 카드

**7. 시각 요소 필수 포함**
```
| 슬라이드 유형 | 필수 시각 요소 |
|-------------|-------------|
| 시장 분석    | METRIC_CARD 4개 + HIGHLIGHT + IMG_PH |
| 컨셉        | Concept Reveal + Synergy Map |
| 시즌 전략    | 좌우 카드 + IMG_PH (캠페인 비주얼) |
| 이벤트 종합  | TABLE + METRIC_CARD + IMG_PH (현장 사진) |
| 운영 프로세스 | COLS + HIGHLIGHT + IMG_PH (인포그래픽) |
| 커뮤니케이션  | COLS + HIGHLIGHT + IMG_PH (흐름도) |
```

### 절대 하지 말 것
- ❌ 헬퍼 함수를 스크립트 내에 다시 정의하지 말 것
- ❌ RGBColor를 직접 하드코딩하지 말 것 → `C["primary"]` 사용
- ❌ 폰트명을 직접 쓰지 말 것 → `FONT` 상수 사용
- ❌ "맑은 고딕" 등 다른 폰트 사용 금지 → Pretendard만 사용

### 기본 사용 패턴

```python
#!/usr/bin/env python3
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, PROJECT_ROOT)
from src.generators.slide_kit import *

prs = new_presentation()
WIN = {"data": "...", "story": "...", "ugc": "..."}

# 표지
slide_cover(prs, "프로젝트명", "발주처명")

# 목차
slide_toc(prs, "목차", [("01", "HOOK", "설명"), ...], pg=2)

# 섹션 구분자
slide_section_divider(prs, "01", "사업이해", "부제", "스토리", "data", WIN)

# 일반 콘텐츠
s = new_slide(prs)
bg(s, C["white"])
TB(s, "Action Title — 인사이트 기반 제목", pg=3)
MT(s, ML, Inches(1.3), CW, Inches(3), ["항목1", "항목2"], bul=True)

# 저장
save_pptx(prs, "output/파일명.pptx")
```

**v3.1 업데이트**: Win Theme, Executive Summary, Next Step, Action Title 시스템 도입
- Win Theme: 제안서 전체에 반복되는 핵심 수주 전략 메시지
- Executive Summary: 의사결정권자용 1페이지 핵심 요약
- Next Step: 다음 단계 안내 / Call to Action
- Action Title: 인사이트 기반 슬라이드 제목 (Topic Title → Action Title)

## 역할 분리

### Claude Code (콘텐츠 생성)
- RFP 문서 분석 및 핵심 정보 추출
- Phase 0~7 제안서 콘텐츠 생성
- 수주 전략 및 차별화 포인트 도출
- 실제 콘텐츠 예시 생성 (마케팅/PR)

### [회사명] (문서화)
- PPTX 변환 및 Modern 스타일 디자인 적용
- 슬라이드 레이아웃 및 포맷팅
- 차트, 타임라인, 조직도 생성

## 디렉토리 구조

```
├── main.py                 # CLI 엔트리포인트
├── config/
│   ├── prompts/            # Phase별 프롬프트 템플릿
│   │   ├── content_guidelines.txt  # v3.1 콘텐츠 작성 가이드라인
│   │   ├── phase0_hook.txt
│   │   ├── phase1_summary.txt
│   │   ├── phase2_insight.txt
│   │   ├── phase3_concept.txt
│   │   ├── phase4_action.txt
│   │   ├── phase5_management.txt
│   │   ├── phase6_whyus.txt
│   │   └── phase7_investment.txt
│   └── design/             # 디자인 설정
│       └── design_style.py    # Modern 스타일 정의 (v3.1)
├── src/
│   ├── parsers/            # 문서 파싱 (PDF, DOCX)
│   ├── agents/             # Claude 에이전트
│   ├── generators/         # PPTX 생성 ([회사명])
│   ├── orchestrators/      # 워크플로우 조율
│   └── schemas/            # Pydantic 스키마
│       └── proposal_schema.py  # Impact-8 스키마 (v3.0)
│   └── utils/              # 유틸리티
│       ├── logger.py           # 로깅 설정
│       └── reference_analyzer.py  # 레퍼런스 PPTX 디자인 분석기
├── examples/               # 예제 생성 스크립트
│   └── example_generate.py     # slide_kit 사용 패턴 예시
├── templates/              # PPTX 템플릿
├── company_data/           # 회사 정보
├── input/                  # 레퍼런스 PPTX 파일 (디자인 참조용)
│   └── 서울배달플러스_홍보마케팅_제안서.pptx
├── 제안요청서/             # ★ RFP 입력 (PDF 문서들)
│   └── 테스트 XX/              # 테스트별 RFP 문서 폴더
├── output/                 # ★ PPTX 출력 (생성 스크립트 + 결과물)
│   └── 테스트 XX/              # 테스트별 출력 폴더
└── 제안서/                 # 레퍼런스 제안서 (PDF)
    └── reference_proposal.pdf (비공개)
```

## 사용법

### 방법 1: Claude Code로 제안서 생성 (★ 메인 방식)

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. RFP 문서를 제안요청서 폴더에 배치
mkdir -p 제안요청서/테스트\ 01
cp your_rfp.pdf 제안요청서/테스트\ 01/

# 3. Claude Code에게 요청
# "제안요청서 폴더에 있는 테스트 01 폴더 내 파일을 분석한 후 제안서를 제작해줘"

# Claude Code가 자동으로:
# → RFP 분석 → 콘텐츠 기획 → generate_제안서.py 작성 → 실행 → PPTX 생성
```

### 방법 2: CLI 자동 파이프라인 (대안)

```bash
# .env에 ANTHROPIC_API_KEY 설정 필요
cp .env.example .env

# Claude API 기반 자동 생성
python main.py generate 제안요청서/테스트\ 01/rfp.pdf -n "프로젝트명" -c "발주처" -t marketing_pr

# 레퍼런스 PPTX 디자인 분석
python main.py reference-analyze input/서울배달플러스_홍보마케팅_제안서.pptx
```

## 제안서 구조: Impact-8 Framework

실제 수주 성공 제안서 분석을 기반으로 개선된 8-Phase 구조

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 0: HOOK (티저)                         3-10p (5%)   │
│  → 임팩트 있는 오프닝, 핵심 메시지, 비전                      │
├─────────────────────────────────────────────────────────────┤
│  PHASE 1: SUMMARY                             3-5p (5%)    │
│  → Executive Summary (의사결정자용 5분 요약)                 │
├─────────────────────────────────────────────────────────────┤
│  PHASE 2: INSIGHT                             8-15p (10%)  │
│  → 시장 환경 + 문제 정의 + 숨겨진 니즈                       │
├─────────────────────────────────────────────────────────────┤
│  PHASE 3: CONCEPT & STRATEGY                  8-15p (12%)  │
│  → 핵심 컨셉 + 차별화 전략 + 경쟁 우위                       │
├─────────────────────────────────────────────────────────────┤
│  PHASE 4: ACTION PLAN (★핵심)                 30-60p (40%) │
│  → 상세 실행 계획 + 콘텐츠 예시 + 채널별 전략                 │
├─────────────────────────────────────────────────────────────┤
│  PHASE 5: MANAGEMENT                          6-12p (10%)  │
│  → 조직 + 운영 + 품질관리 + 리포팅                          │
├─────────────────────────────────────────────────────────────┤
│  PHASE 6: WHY US                              8-15p (12%)  │
│  → 수행 역량 + 유사 실적 + 레퍼런스                          │
├─────────────────────────────────────────────────────────────┤
│  PHASE 7: INVESTMENT & ROI                    4-8p (6%)    │
│  → 투자 비용 + 정량적 효과 + ROI                            │
└─────────────────────────────────────────────────────────────┘
  총 70-140p (프로젝트 규모에 따라 조정)
```

## 프로젝트 유형별 가중치

| Phase | Marketing/PR | Event | IT/System | Public | Consulting |
|-------|-------------|-------|-----------|--------|------------|
| 0. HOOK | 8% | 6% | 3% | 3% | 5% |
| 1. SUMMARY | 5% | 5% | 8% | 8% | 8% |
| 2. INSIGHT | 12% | 8% | 12% | 15% | 15% |
| 3. CONCEPT | 12% | 10% | 10% | 10% | 12% |
| 4. ACTION | **40%** | **45%** | 35% | 30% | 30% |
| 5. MANAGEMENT | 8% | 10% | 12% | 12% | 10% |
| 6. WHY US | 10% | 10% | 12% | 15% | 12% |
| 7. INVESTMENT | 5% | 6% | 8% | 7% | 8% |

## v3.1 핵심 컴포넌트

### Win Theme (수주 전략 메시지)
제안서 전체에 반복되는 3대 핵심 수주 전략 메시지

```python
WIN_THEMES = {
    "data": "데이터 기반 타겟 마케팅",
    "community": "시민 참여형 브랜드 빌딩",
    "integration": "온-오프라인 통합 시너지",
}
```

- 각 섹션 구분자에 관련 Win Theme 표시
- 슬라이드 내에서 Win Theme 뱃지로 강조
- 일관된 메시지 반복으로 수주 전략 강화

### Action Title (인사이트 기반 제목)
Topic Title에서 Action Title로 전환

| Before (Topic Title) | After (Action Title) |
|---------------------|---------------------|
| 타겟 분석 | MZ세대 2030이 핵심, 하루 SNS 55분 사용 |
| 채널 전략 | 인스타그램 중심, 릴스로 도달률 3배 확보 |
| 예산 계획 | 월 3,000만원으로 팔로워 50만 달성 |

### Executive Summary
의사결정권자용 1페이지 핵심 요약

구성요소:
- 프로젝트 목표 (One Sentence Pitch)
- 3대 Win Theme
- 핵심 KPI (산출 근거 포함)
- Why Us 핵심 차별점

### Next Step (Call to Action)
다음 단계 안내 및 행동 촉구

```
┌─────────────────────────────────────────┐
│  NEXT STEP                              │
│                                         │
│  STEP 1: 제안 설명회 (00월 00일)         │
│  STEP 2: Q&A 및 추가 협의               │
│  STEP 3: 계약 체결                      │
│                                         │
│  Contact: [담당자 정보]                 │
└─────────────────────────────────────────┘
```

### KPI 산출 근거
모든 KPI에 산출 근거 필수 포함

```
목표: 팔로워 +30%
산출 근거: 인플루언서 협업 +10% + 릴스 확대 +12% + 이벤트 +8%
데이터 출처: 유사 프로젝트 평균 성장률 참고
```

### Placeholder 표준화
미완성 콘텐츠 표기 형식 통일: `[대괄호]`

```
✅ [발주처명], [프로젝트명], [담당자 연락처]
❌ OOO, XXX, ___
```

## 디자인 스타일: Modern

실제 수주 성공 제안서를 분석하여 추출한 디자인 시스템

### 컬러 팔레트
- Primary: `#002C5F` (다크 블루)
- Secondary: `#00AAD2` (스카이 블루)
- Teal: `#00A19C` (틸 - Win Theme 뱃지용)
- Accent: `#E63312` (레드)
- Dark BG: `#1A1A1A`
- Light BG: `#F5F5F5` (밝은 배경)

### 타이포그래피
- Font: Pretendard
- 티저 타이틀: 72pt Bold
- 섹션 타이틀: 48pt Bold
- 슬라이드 타이틀: 36pt SemiBold
- 본문: 18pt Regular

### 레이아웃
- 16:9 비율 (1920 x 1080)
- 여백: 상 80px, 하 60px, 좌우 100px
- 섹션 구분자: 다크 배경, 대형 숫자 아웃라인

## 핵심 컴포넌트

### 스키마 (Claude ↔ [회사명] 인터페이스)
- `src/schemas/proposal_schema.py` - ProposalContent, PhaseContent (v3.1)
  - 새로운 모델: WinTheme, KPIWithBasis, ExecutiveSummary, NextStep, ActionTitle
  - 새로운 SlideType: EXECUTIVE_SUMMARY, NEXT_STEP, DIFFERENTIATION
- `src/schemas/rfp_schema.py` - RFPAnalysis

### 에이전트 (Claude)
- `src/agents/rfp_analyzer.py` - RFP 분석
- `src/agents/content_generator.py` - 콘텐츠 생성

### 생성기 ([회사명])
- `src/generators/pptx_generator.py` - 슬라이드 생성 (v3.1)
  - 새로운 메서드: add_executive_summary_slide(), add_next_step_slide(), add_section_divider_with_win_theme()
- `src/generators/chart_generator.py` - 차트/다이어그램

### 디자인 설정
- `config/design/design_style.py` - Modern 스타일 정의 (v3.1)
  - 새로운 스타일: WinThemeBadgeStyle, ExecutiveSummaryStyle, NextStepStyle, DifferentiationStyle
  - WIN_THEME_TEMPLATES: 프로젝트 유형별 Win Theme 템플릿

### 콘텐츠 가이드라인
- `config/prompts/content_guidelines.txt` - Action Title, Win Theme, KPI 산출 근거 작성 가이드

## 마케팅/PR 특화 기능

### 콘텐츠 예시 생성
- 실제 포스팅 예시 (비주얼 설명, 카피)
- 해시태그 전략
- 캠페인 상세 기획

### 채널별 전략
- Instagram: 피드, 스토리, 릴스
- YouTube: 롱폼, 숏폼, 커뮤니티
- Facebook, X, TikTok, Blog

### 캠페인 기획
- 캠페인 컨셉 및 목표
- 실행 계획
- 예상 성과

## 레퍼런스

- 실제 수주 성공 제안서 (200p+) — 구조 분석 레퍼런스
  - 구조: INTRO(13p) + CONCEPT(31p) + STRATEGY(14p) + ACTION PLAN(101p) + MANAGEMENT(16p) + CREDENTIALS(44p)
  - 핵심: ACTION PLAN이 전체의 46% 차지
  - 특징: 실제 콘텐츠 예시, AI 캠페인, 숏폼-롱폼 연계 전략

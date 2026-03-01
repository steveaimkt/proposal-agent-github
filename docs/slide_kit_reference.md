# slide_kit.py API Reference (for Code Generation)

이 문서는 `slide_kit.py`를 사용하여 PPTX 생성 스크립트를 작성하기 위한 레퍼런스입니다.

## 스크립트 기본 구조

```python
#!/usr/bin/env python3
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, PROJECT_ROOT)
from src.generators.slide_kit import *

WIN = {
    "data": "데이터 기반 타겟 마케팅",
    "community": "시민 참여형 브랜드 빌딩",
    "integration": "온-오프라인 통합 시너지",
}

prs = new_presentation()
pg = 1

# 표지
slide_cover(prs, "[프로젝트명]", "[발주처명]", year="2026")
pg += 1

# 목차
slide_toc(prs, "목차", [("01", "HOOK", "임팩트 오프닝"), ...], pg=pg)
pg += 1

# 섹션 구분자
slide_section_divider(prs, "01", "HOOK", "부제", "스토리", "data", WIN)
pg += 1

# 콘텐츠 슬라이드 (아래 패턴 반복)
s = new_slide(prs)
bg(s, C["white"])
TB(s, "Action Title — 인사이트 기반 제목", pg=pg)
# ... 시각화 함수 호출
PN(s, pg)
pg += 1

# 마지막
slide_closing(prs, "감사합니다", tagline="Tagline")
save_pptx(prs, os.path.join(PROJECT_ROOT, "output", "테스트 XX", "제안서.pptx"))
```

## 상수

### 컬러 (C 딕셔너리)
```python
C["primary"]        # #002C5F  다크블루 (주색)
C["secondary"]      # #00AAD2  스카이블루 (보조)
C["teal"]           # #00A19C  틸 (Win Theme 뱃지)
C["accent"]         # #E63312  레드 (강조)
C["dark"]           # #212121  본문 텍스트
C["light"]          # #F5F5F5  밝은 배경
C["white"]          # #FFFFFF
C["gray"]           # #757575  보조 텍스트
C["lgray"]          # #C8C8C8  구분선
C["green"]          # #2E7D32  성과/긍정
C["orange"]         # #F5A623  주의
C["gold"]           # #C5973E  프리미엄

# 파생 컬러 (v3.6)
C["primary_dark"]   # 진한 네이비
C["primary_light"]  # 연한 블루 배경
C["secondary_light"]# 연한 스카이 배경
C["teal_light"]     # 연한 틸 배경
C["accent_light"]   # 연한 레드 배경
C["green_light"]    # 연한 그린 배경
C["card_bg"]        # 카드 배경
C["card_border"]    # 카드 테두리
```

### 크기
```python
SW = Inches(13.333)   # 슬라이드 너비
SH = Inches(7.5)      # 슬라이드 높이
ML = Inches(0.8)      # 좌측 여백
CW = SW - ML - MR     # 콘텐츠 너비 (~11.733")
```

### 폰트
```python
FONT = "Pretendard"
FONT_W = {
    "light": "Pretendard Light",
    "regular": "Pretendard",
    "medium": "Pretendard Medium",
    "semibold": "Pretendard SemiBold",
    "bold": "Pretendard Bold",
    "black": "Pretendard Black",
}
SZ = {"hero": 60, "divider": 40, "action": 20, "subtitle": 16, "body": 13, "body_sm": 11, "caption": 10, "source": 8}
```

## 슬라이드 생성/관리

```python
prs = new_presentation()                    # 16:9 빈 프레젠테이션
s = new_slide(prs)                          # 빈 슬라이드 추가
save_pptx(prs, "output/file.pptx")         # 저장
```

## 배경/스타일

```python
bg(s, C["white"])                           # 단색 배경
gradient_bg(s, C["primary"], C["dark"])     # 그라디언트 배경
```

## 상단바 / 페이지번호 / 출처

```python
TB(s, "Action Title 제목", pg=3)            # 상단 타이틀바 + 페이지 번호
PN(s, 3)                                    # 우하단 페이지 번호
SRC(s, "출처: 한국관광공사, 2024")           # 좌하단 출처
WB(s, "data", WIN)                          # Win Theme 뱃지
```

## 텍스트

```python
T(s, ML, Inches(1.3), CW, Inches(0.5), "텍스트", sz=13, c=C["dark"], b=False, al=PP_ALIGN.LEFT)
RT(s, ML, Inches(1.3), CW, Inches(0.5), [("굵게", 14, C["primary"], True), (" 일반", 13, C["dark"], False)])
MT(s, ML, Inches(1.3), CW, Inches(1.4), ["항목1", "항목2", "항목3", "항목4"], sz=13, bul=True)
```

**MT 높이 규칙**: 3줄=Inches(1.1), 4줄=Inches(1.4), 5줄=Inches(1.7), 6줄=Inches(2.0), 8줄=Inches(2.8)

## 도형

```python
R(s, ML, Inches(1.3), CW, Inches(3), f=C["light"])          # 직각 사각형
BOX(s, ML, Inches(1.3), Inches(3), Inches(1), C["primary"], "텍스트", sz=14, tc=C["white"])
OBOX(s, ML, Inches(1.3), Inches(3), Inches(1), "텍스트", lc=C["primary"])
RBOX(s, ML, Inches(1.3), Inches(3), Inches(1), C["primary"], "텍스트", tc=C["white"])  # 라운드
CARD(s, ML, Inches(1.3), Inches(3), Inches(2), "제목", body="본문", color=C["primary"])
```

## ★ 핵심 시각화 함수

### COLS — N-컬럼 카드 레이아웃
```python
COLS(s, [
    {"title": "전략 1", "body": ["데이터 분석", "타겟 설정", "콘텐츠 기획"]},
    {"title": "전략 2", "body": ["채널 최적화", "A/B 테스트", "성과 측정"]},
    {"title": "전략 3", "body": ["커뮤니티 운영", "UGC 캠페인", "브랜드 앰배서더"]},
], y=Inches(1.5), h=Inches(4.5))
```

### KPIS — KPI 카드 그리드
```python
KPIS(s, [
    {"label": "팔로워", "value": "+30%", "sub": "12만 → 15.6만"},
    {"label": "도달률", "value": "3.5%", "sub": "업계 평균 2.1%"},
    {"label": "전환율", "value": "2.8%", "sub": "전년 대비 +40%"},
    {"label": "ROI", "value": "320%", "sub": "투자 대비 수익률"},
], y=Inches(1.5), h=Inches(2.0))
```

### HIGHLIGHT — 핵심 메시지 강조 박스
```python
HIGHLIGHT(s, "핵심 메시지 텍스트", sub="보조 설명", y=Inches(1.3), grad=True)
```

### TABLE — 데이터 테이블
```python
TABLE(s, ["구분", "현재", "목표", "비고"],
    [["팔로워", "12만", "15.6만", "+30%"],
     ["도달률", "2.1%", "3.5%", "+67%"],
     ["전환율", "2.0%", "2.8%", "+40%"]],
    y=Inches(1.5))
```

### FLOW — 프로세스 플로우
```python
FLOW(s, ["환경 분석", "전략 수립", "콘텐츠 제작", "실행/운영", "성과 측정"], y=Inches(1.5))
```

### PYRAMID — 피라미드 구조
```python
PYRAMID(s, [
    {"title": "비전", "desc": "대한민국 대표 관광 브랜드"},
    {"title": "전략", "desc": "데이터 기반 + 커뮤니티 중심"},
    {"title": "실행", "desc": "채널별 맞춤 콘텐츠 + 캠페인"},
], y=Inches(1.5))
```

### MATRIX — 2x2 매트릭스
```python
MATRIX(s, [
    {"label": "High Impact\nLow Effort", "items": ["SNS 콘텐츠", "이벤트"]},
    {"label": "High Impact\nHigh Effort", "items": ["브랜드 캠페인"]},
    {"label": "Low Impact\nLow Effort", "items": ["블로그 포스팅"]},
    {"label": "Low Impact\nHigh Effort", "items": ["TV 광고"]},
], x_label="Effort →", y_label="Impact →")
```

### COMPARE — 좌우 비교
```python
COMPARE(s, "AS-IS", ["현재 상태 항목1", "현재 상태 항목2"],
           "TO-BE", ["개선 후 항목1", "개선 후 항목2"],
    y=Inches(1.5))
```

### TIMELINE — 타임라인
```python
TIMELINE(s, [
    ("1~3월", "기반 구축\n채널 셋업"),
    ("4~6월", "콘텐츠 강화\n팔로워 확보"),
    ("7~9월", "캠페인 실행\n인플루언서 협업"),
    ("10~12월", "성과 극대화\nROI 분석"),
], y=Inches(1.5))
```

### GRID — N×M 카드 그리드
```python
GRID(s, [
    {"title": "항목1", "body": "설명1"},
    {"title": "항목2", "body": "설명2"},
    {"title": "항목3", "body": "설명3"},
    {"title": "항목4", "body": "설명4"},
    {"title": "항목5", "body": "설명5"},
    {"title": "항목6", "body": "설명6"},
], cols=3, y=Inches(1.5))
```

### STAT_ROW — 통계/수치 강조 행
```python
STAT_ROW(s, [
    {"value": "150만", "label": "월평균 도달"},
    {"value": "4.2%", "label": "참여율"},
    {"value": "320%", "label": "ROI"},
], y=Inches(1.5))
```

### GANTT_CHART — 간트 차트
```python
GANTT_CHART(s,
    categories=["전략 수립", "콘텐츠 제작", "캠페인 실행", "성과 분석"],
    months=["1월", "2월", "3월", "4월", "5월", "6월"],
    data=[
        [1, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1],
    ],
    y=Inches(1.5))
```

### ORG — 조직도
```python
ORG(s,
    pm={"name": "PM 홍길동", "role": "프로젝트 총괄"},
    directors=[
        {"name": "김전략", "role": "전략 디렉터"},
        {"name": "이크리", "role": "크리에이티브 디렉터"},
        {"name": "박미디어", "role": "미디어 디렉터"},
    ],
    teams=[
        ["전략팀 3명", "리서치팀 2명"],
        ["디자인팀 3명", "영상팀 2명"],
        ["운영팀 3명", "분석팀 2명"],
    ])
```

### ICON_CARDS — 아이콘 카드
```python
ICON_CARDS(s, [
    {"icon": "🎯", "tag": "POINT 01", "title": "데이터 기반", "body": "AI 분석으로 타겟 정밀화"},
    {"icon": "🤝", "tag": "POINT 02", "title": "커뮤니티", "body": "팬 기반 자발적 확산"},
    {"icon": "🔄", "tag": "POINT 03", "title": "통합 운영", "body": "온오프라인 시너지"},
], y=Inches(1.5))
```

### STEP_ARROW — 화살표 스텝
```python
STEP_ARROW(s, [
    {"title": "분석", "body": "환경 분석 및 목표 설정"},
    {"title": "전략", "body": "채널별 전략 수립"},
    {"title": "실행", "body": "콘텐츠 제작 및 배포"},
    {"title": "측정", "body": "성과 분석 및 개선"},
], y=Inches(1.5))
```

## 차트

### BAR_CHART
```python
BAR_CHART(s, ML, Inches(1.5), CW, Inches(4.5),
    categories=["Instagram", "YouTube", "Facebook", "TikTok"],
    series_data=[("팔로워(만)", [15, 8, 12, 5])],
    title="채널별 팔로워")
```

### PIE_CHART
```python
PIE_CHART(s, ML, Inches(1.5), Inches(5), Inches(4.5),
    categories=["콘텐츠", "광고", "인플루언서", "이벤트"],
    values=[35, 25, 25, 15],
    title="예산 배분", donut=True)
```

### LINE_CHART
```python
LINE_CHART(s, ML, Inches(1.5), CW, Inches(4.5),
    categories=["1월", "2월", "3월", "4월", "5월", "6월"],
    series_data=[("팔로워", [10, 11, 12.5, 14, 15, 15.6])],
    title="팔로워 성장 추이", smooth=True)
```

## 헬퍼

```python
IMG_PH(s, ML, Inches(4.5), CW, Inches(2.5), label="캠페인 비주얼")
METRIC_CARD(s, ML, Inches(1.5), Inches(2.5), Inches(1.5), "150만", "월평균 도달", sub="전년 대비 +35%")
PROGRESS_BAR(s, ML, Inches(5.0), CW, "목표 달성률", 75)
NUMBERED_LIST(s, ML, Inches(1.5), CW, [
    {"title": "분석", "body": "시장 환경 분석"},
    {"title": "전략", "body": "채널별 전략 수립"},
])
QUOTE(s, "핵심 인용문 텍스트", author="출처", style="modern")
DIVIDER(s, Inches(4.0), style="line")
ACCENT_LINE(s, ML, Inches(1.5), Inches(2.0))
```

## 특수 슬라이드

```python
slide_cover(prs, "프로젝트명", "발주처명", year="2026", tagline="태그라인")
slide_section_divider(prs, "01", "HOOK", "부제", "스토리", "data", WIN)
slide_toc(prs, "목차", [("01", "HOOK", "설명"), ("02", "INSIGHT", "설명"), ...], pg=2)
slide_exec_summary(prs, "Executive Summary", "원라이너", WIN, [{"label": "KPI", "value": "수치", "sub": "설명"}, ...], ["차별점1", "차별점2"])
slide_next_step(prs, "Next Step", [{"step": "STEP 1", "title": "제안설명회", "desc": "일시: [날짜]"}, ...], contact="[담당자]")
slide_closing(prs, "감사합니다", tagline="태그라인", project_title="프로젝트명")
```

## VStack (자동 Y좌표 관리)

```python
vs = VStack(y_start=Inches(1.3))
HIGHLIGHT(s, "핵심 메시지", y=vs.next(Inches(0.7)))
COLS(s, [...], y=vs.next(Inches(4.0)))
MT(s, ML, vs.next(Inches(1.4)), CW, Inches(1.4), ["항목1", "항목2", "항목3", "항목4"], bul=True)
```

## 슬라이드 패턴 (매 슬라이드 필수)

```python
s = new_slide(prs)
bg(s, C["white"])                          # 1. 배경
TB(s, "Action Title — 인사이트 제목", pg=pg)  # 2. 상단바
# ... 시각화 함수들 ...                       # 3. 콘텐츠
PN(s, pg)                                   # 4. 페이지번호
pg += 1
```

## slide_type → slide_kit 매핑

| slide_type | slide_kit 함수 |
|------------|---------------|
| section_divider | slide_section_divider() |
| content | COLS(), MT(), HIGHLIGHT() 조합 |
| two_column | COLS() (2개 아이템) |
| three_column | COLS() (3개 아이템) |
| table | TABLE() |
| chart (bar) | BAR_CHART() |
| chart (pie) | PIE_CHART() |
| chart (line) | LINE_CHART() |
| timeline | TIMELINE() |
| org_chart | ORG() |
| comparison | COMPARE() |
| key_message | HIGHLIGHT() + STAT_ROW() |
| kpi | KPIS() |
| process | FLOW() |
| pyramid | PYRAMID() |
| matrix | MATRIX() |
| grid | GRID() |
| budget | PIE_CHART() + TABLE() |

## 디자인 규칙

1. **배경색 충돌 방지**: 카드 색상 ≠ 배경 색상
2. **요소 간 최소 간격**: HIGHLIGHT→다음: 0.75", COLS→다음: 0.30"
3. **44pt 제목 18자 초과 시 2줄로 분리**
4. **하단 공백 > 0.5" → IMG_PH 또는 HIGHLIGHT 추가**
5. **Pretendard 폰트만 사용** (FONT, FONT_W 상수 사용)
6. **RGBColor 직접 하드코딩 금지** → C["primary"] 등 사용

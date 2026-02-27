#!/usr/bin/env python3
"""
예제 생성 스크립트 — slide_kit.py 사용 패턴

이 스크립트는 slide_kit.py를 활용한 제안서 생성의 최소 동작 예시입니다.
실행: python3 examples/example_generate.py
출력: output/example_제안서.pptx
"""

import sys
import os

# ─── 프로젝트 루트 자동 감지 (examples/ 에서 한 단계 위) ────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
from src.generators.slide_kit import *

# ─── Win Theme 정의 ───────────────────────────────────────────────
WIN = {
    "data": "데이터 기반 타겟 마케팅",
    "community": "시민 참여형 브랜드 빌딩",
    "integration": "온-오프라인 통합 시너지",
}

# ─── 프레젠테이션 생성 ────────────────────────────────────────────
prs = new_presentation()
pg = 1

# ── 1. 표지 ──────────────────────────────────────────────────────
slide_cover(prs, "[프로젝트명] 제안서", "[발주처명]", year="2026")
pg += 1

# ── 2. 목차 ──────────────────────────────────────────────────────
slide_toc(prs, "목차", [
    ("01", "HOOK", "임팩트 있는 오프닝"),
    ("02", "INSIGHT", "시장 환경 분석"),
    ("03", "CONCEPT", "핵심 전략 제안"),
    ("04", "ACTION PLAN", "실행 계획"),
    ("05", "WHY US", "수행 역량"),
], pg=pg)
pg += 1

# ── 3. 섹션 구분자 ───────────────────────────────────────────────
slide_section_divider(prs, "01", "HOOK", "우리가 함께할 미래",
                      "비전을 그리다", "data", WIN)
pg += 1

# ── 4. 콘텐츠 슬라이드 — 3컬럼 레이아웃 ──────────────────────────
s = new_slide(prs)
bg(s, C["white"])
TB(s, "MZ세대 2030이 핵심, 하루 SNS 55분 사용", pg=pg)
COLS(s, [
    {"title": "인스타그램", "body": ["릴스 중심 콘텐츠", "도달률 3배 확보", "해시태그 전략"]},
    {"title": "유튜브", "body": ["숏폼-롱폼 연계", "브랜드 스토리텔링", "커뮤니티 운영"]},
    {"title": "틱톡", "body": ["트렌드 챌린지", "UGC 콘텐츠 확산", "바이럴 마케팅"]},
])
PN(s, pg)
pg += 1

# ── 5. 콘텐츠 슬라이드 — KPI 카드 ────────────────────────────────
s = new_slide(prs)
bg(s, C["white"])
TB(s, "월 3,000만원으로 팔로워 50만 달성", pg=pg)
KPIS(s, [
    {"label": "팔로워 증가", "value": "+30%", "sub": "인플루언서 협업 +10%\n릴스 확대 +12%\n이벤트 +8%"},
    {"label": "참여율 목표", "value": "4.5%", "sub": "업계 평균 2.1% 대비\n2배 이상 달성"},
    {"label": "도달 수", "value": "500만", "sub": "월 기준\n전년 대비 200% 성장"},
    {"label": "전환율", "value": "2.8%", "sub": "광고 → 구매 전환\n업계 평균 1.2%"},
])
PN(s, pg)
pg += 1

# ── 6. 콘텐츠 슬라이드 — HIGHLIGHT + 불릿 ────────────────────────
s = new_slide(prs)
bg(s, C["white"])
TB(s, "콘텐츠 전략: 진정성 있는 스토리텔링이 핵심", pg=pg)
HIGHLIGHT(s, "고품질 콘텐츠 × 데이터 기반 최적화 = 지속 가능한 성장")
MT(s, ML, Inches(2.3), CW, Inches(3.5), [
    "주 3회 이상 정기 콘텐츠 발행 (피드 + 릴스 + 스토리)",
    "A/B 테스트를 통한 최적 게시 시간대 도출",
    "UGC(사용자 생성 콘텐츠) 활용으로 진정성 확보",
    "월간 콘텐츠 캘린더 사전 기획 및 승인 프로세스",
    "실시간 트렌드 모니터링 → 즉시 반영 체계",
], bul=True)
PN(s, pg)
pg += 1

# ── 7. 콘텐츠 슬라이드 — 타임라인 ────────────────────────────────
s = new_slide(prs)
bg(s, C["white"])
TB(s, "6개월 단계별 성장 로드맵", pg=pg)
TIMELINE(s, [
    ("1~2월", "기반 구축\n채널 셋업, 콘텐츠 가이드"),
    ("3~4월", "성장 가속\n인플루언서 협업, 광고 집행"),
    ("5~6월", "성과 확산\nUGC 캠페인, 성과 리포팅"),
])
PN(s, pg)
pg += 1

# ── 8. 클로징 ────────────────────────────────────────────────────
slide_closing(prs, "[프로젝트명]", "[발주처명]과 함께 성장하겠습니다")

# ─── 저장 ─────────────────────────────────────────────────────────
output_dir = os.path.join(PROJECT_ROOT, "output")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "example_제안서.pptx")
save_pptx(prs, output_path)

print(f"생성 완료: {output_path} ({pg + 1}장)")

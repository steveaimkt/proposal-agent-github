# Proposal Agent — AI 입찰 제안서 자동 생성 에이전트

RFP(제안요청서) PDF를 입력하면 **40~80장 PPTX 입찰 제안서**를 자동 생성하는 AI 에이전트 시스템

## 핵심 특징

- **Impact-8 Framework**: 실제 수주 성공 제안서 분석을 기반으로 도출한 8-Phase 구조
- **Win Theme 전달 체인**: Phase 1에서 확정한 3대 Win Theme이 전체 제안서에 일관 반복
- **C-E-I 설득 구조**: Claim(주장) → Evidence(근거) → Impact(영향) 3단계 설득 로직
- **Action Title**: 모든 슬라이드에 인사이트 기반 제목 자동 적용
- **slide_kit.py 엔진**: 2,270줄 PPTX 렌더링 엔진 (20가지 레이아웃, 네이티브 차트, VStack 자동 배치)

## 빠른 시작

### 설치

```bash
git clone https://github.com/steveaimkt/proposal-agent-github.git
cd proposal-agent-github
pip install -r requirements.txt
```

### 제안서 생성 (Claude Code 방식)

```bash
# 1. RFP 문서를 제안요청서 폴더에 배치
mkdir -p 제안요청서/테스트\ 01
cp your_rfp.pdf 제안요청서/테스트\ 01/

# 2. Claude Code에게 요청
# "제안요청서 폴더에 있는 테스트 01 폴더 내 파일을 분석한 후 제안서를 제작해줘"
```

Claude Code가 자동으로 수행하는 작업:
1. **RFP 분석** — PDF 문서에서 프로젝트명, 과업 범위, 평가 기준 추출
2. **콘텐츠 기획** — Impact-8 Phase 구조로 40~80장 콘텐츠 설계
3. **생성 스크립트 작성** — `output/테스트 01/generate_제안서.py` 자동 작성
4. **실행 및 검증** — 스크립트 실행하여 PPTX 파일 생성

### 생성 스크립트 구조

Claude Code가 작성하는 생성 스크립트 예시:

```python
#!/usr/bin/env python3
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, PROJECT_ROOT)
from src.generators.slide_kit import *

# Win Theme 정의
WIN = {
    "data": "데이터 기반 타겟 마케팅",
    "community": "시민 참여형 브랜드 빌딩",
    "integration": "온-오프라인 통합 시너지",
}

# 프레젠테이션 생성
prs = new_presentation()

# 표지
slide_cover(prs, "프로젝트명", "발주처명", year="2026")

# 목차
slide_toc(prs, "목차", [("01", "HOOK", "설명"), ...], pg=2)

# 콘텐츠 슬라이드 (40~80장)
s = new_slide(prs)
bg(s, C["white"])
TB(s, "Action Title — 인사이트 기반 제목", pg=3)
COLS(s, ML, Inches(1.3), CW, [
    {"head": "항목 1", "body": "설명..."},
    {"head": "항목 2", "body": "설명..."},
    {"head": "항목 3", "body": "설명..."},
])

# 저장
save_pptx(prs, "output/테스트 01/제안서.pptx")
```

### CLI 자동 파이프라인 (대안)

Claude API를 직접 호출하여 자동 생성하는 방식:

```bash
# .env에 API 키 설정 필요
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 자동 생성
python main.py generate 제안요청서/테스트\ 01/rfp.pdf -n "프로젝트명" -c "발주처"

# 레퍼런스 PPTX 디자인 분석
python main.py reference-analyze input/서울배달플러스_홍보마케팅_제안서.pptx
```

## 파이프라인

```
제안요청서/테스트 XX/*.pdf   ← RFP 입력
    │
    ▼
Claude Code가 PDF 분석
    ├─ Pain Point 추출
    ├─ Win Theme 3개 도출
    └─ 평가 기준 → 강조 포인트
    │
    ▼
Claude Code가 콘텐츠 설계 (Impact-8 × 8 Phase)
    ├─ Win Theme 전달 체인
    ├─ Action Title + C-E-I 설득 구조
    └─ KPI + 산출 근거
    │
    ▼
Claude Code가 generate_제안서.py 작성
    └─ slide_kit.py import하여 PPTX 렌더링
    │
    ▼
output/테스트 XX/제안서.pptx  ← 40~80장 PPTX 출력
```

## Impact-8 Framework

| Phase | 이름 | 비중 | 설명 |
|-------|------|------|------|
| 0 | HOOK | 5% | 임팩트 있는 오프닝 |
| 1 | EXECUTIVE SUMMARY | 5% | 의사결정자용 요약 + Win Theme 정의 |
| 2 | INSIGHT | 12% | 시장 환경 + Pain Point |
| 3 | CONCEPT & STRATEGY | 12% | 핵심 컨셉 + 차별화 전략 |
| 4 | ACTION PLAN | **40%** | 상세 실행 계획 (핵심) |
| 5 | MANAGEMENT | 8% | 조직 + 운영 + 품질관리 |
| 6 | WHY US | 12% | 수행 역량 + 실적 |
| 7 | INVESTMENT & ROI | 6% | 비용 + 기대효과 |

## 프로젝트 유형별 자동 적응

| 유형 | Phase 4 비중 | 특화 콘텐츠 |
|------|-------------|-------------|
| 마케팅/PR | 40% | 채널별 전략, 콘텐츠 예시, 인플루언서 |
| 이벤트 | 45% | 공간 설계, 프로그램표, 참가자 여정 |
| IT/시스템 | 35% | 시스템 아키텍처, WBS, 간트 |
| 공공 | 30% | RFP 대응표, 정책 연계 |
| 컨설팅 | 30% | 전략 프레임워크, 벤치마킹 |

## 디렉토리 구조

```
├── main.py                        # CLI 엔트리포인트 (대안 방식)
├── CLAUDE.md                      # ★ Claude Code 워크플로우 규칙
├── requirements.txt
├── config/
│   ├── proposal_types.py          # 제안서 유형별 설정
│   ├── design/
│   │   └── design_style.py        # 디자인 시스템
│   └── prompts/                   # Phase별 프롬프트 (9개)
├── src/
│   ├── parsers/                   # PDF/DOCX 파싱
│   ├── agents/                    # Claude AI 에이전트
│   │   ├── rfp_analyzer.py        # RFP 전략 분석
│   │   └── content_generator.py   # 8-Phase 콘텐츠 생성
│   ├── schemas/                   # Pydantic 데이터 모델
│   ├── generators/
│   │   ├── slide_kit.py           # ★ PPTX 렌더링 엔진 (2,270줄)
│   │   └── pptx_generator.py      # 스키마 → PPTX 변환
│   ├── orchestrators/             # 워크플로우 조율
│   └── utils/
│       ├── logger.py              # 로깅
│       └── reference_analyzer.py  # 레퍼런스 PPTX 디자인 분석기
├── examples/                      # 예제 생성 스크립트
├── input/                         # 레퍼런스 PPTX (디자인 참조)
├── 제안요청서/                     # ★ RFP 입력 (PDF)
├── output/                        # ★ 생성 스크립트 + PPTX 출력
└── docs/                          # 가이드 문서
```

## 기술 스택

| 카테고리 | 기술 |
|---------|------|
| AI | Claude Code (메인) 또는 Anthropic API (대안) |
| 문서 처리 | pypdf, pdfplumber, python-pptx |
| 데이터 | Pydantic v2, JSON |
| CLI | Typer, Rich |

## 가이드 문서

- [설치 및 사용 가이드](docs/INSTALL_AND_USAGE.md) — 설치부터 실행까지 단계별 안내
- [에이전트 구축 방식 · 시스템 구조](docs/입찰제안서_에이전트_가이드.md) — 아키텍처 및 설계 원리
- [상세 사용 가이드](docs/제안서_에이전트_사용_가이드.md) — 고급 사용법 및 커스터마이징
- [기술 문서](docs/PROPOSAL_AGENT_GUIDE.md) — API 및 스키마 레퍼런스

## 버전

- **v3.6**: Win Theme 전달 체인 + Action Title 강제 + C-E-I 설득 구조 + KPIWithBasis
- **v3.5**: VStack 자동 배치 + 네이티브 차트 + 테마 시스템 + 20가지 레이아웃

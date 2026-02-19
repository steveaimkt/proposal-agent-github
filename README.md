# Proposal Agent — AI 입찰 제안서 자동 생성 에이전트

RFP(제안요청서) PDF를 입력하면 **40~80장 PPTX 입찰 제안서**를 자동 생성하는 AI 에이전트 시스템

## 핵심 특징

- **Impact-8 Framework**: 실제 수주 성공 제안서 분석을 기반으로 도출한 8-Phase 구조
- **Win Theme 전달 체인**: Phase 1에서 확정한 3대 Win Theme이 전체 제안서에 일관 반복
- **C-E-I 설득 구조**: Claim(주장) → Evidence(근거) → Impact(영향) 3단계 설득 로직
- **Action Title**: 모든 슬라이드에 인사이트 기반 제목 자동 적용
- **slide_kit.py 엔진**: 2,270줄 PPTX 렌더링 엔진 (20가지 레이아웃, 네이티브 차트, VStack 자동 배치)

## 빠른 시작

### ① Claude Code 방식 (권장)

```bash
# 의존성 설치
pip install -r requirements.txt
```

Claude Code에게 자연어로 요청하면 끝:

```
"input 폴더의 RFP를 분석한 후 제안서를 제작해줘"
```

### ② CLI(API) 방식

```bash
# 의존성 설치
pip install -r requirements.txt

# .env 설정 (API 방식만 필요)
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 제안서 생성
python main.py generate input/rfp.pdf -n "프로젝트명" -c "발주처명"

# 프로젝트 유형 지정
python main.py generate input/rfp.pdf -n "프로젝트명" -c "발주처" -t marketing_pr
```

## 파이프라인

```
RFP (PDF)
    │
    ▼
STEP 1: PDF 파싱 (pypdf + pdfplumber)
    │
    ▼
STEP 2: RFP 전략 분석 (Claude AI)
    ├─ Pain Point 추출
    ├─ Win Theme 후보 3개 도출
    └─ 평가 기준 → 제안서 강조 포인트
    │
    ▼
STEP 3: 콘텐츠 생성 (Claude AI × 8 Phase)
    ├─ Win Theme 전달 체인
    ├─ Action Title + C-E-I 설득 구조
    └─ KPI + 산출 근거
    │
    ▼
STEP 4: PPTX 렌더링 (slide_kit.py)
    └─ 40~80장 PPTX 출력
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
├── main.py                        # CLI 엔트리포인트
├── requirements.txt
├── config/
│   ├── proposal_types.py          # 제안서 유형별 설정
│   ├── design/
│   │   └── design_style.py           # 디자인 시스템
│   └── prompts/                   # Phase별 프롬프트 (9개)
├── src/
│   ├── parsers/                   # PDF/DOCX 파싱
│   ├── agents/                    # Claude AI 에이전트
│   │   ├── rfp_analyzer.py        # RFP 전략 분석
│   │   └── content_generator.py   # 8-Phase 콘텐츠 생성
│   ├── schemas/                   # Pydantic 데이터 모델
│   ├── generators/
│   │   ├── slide_kit.py           # PPTX 렌더링 엔진 (2,270줄)
│   │   └── pptx_generator.py      # 스키마 → PPTX 변환
│   └── orchestrators/             # 워크플로우 조율
└── docs/                          # 가이드 문서
```

## 기술 스택

| 카테고리 | 기술 |
|---------|------|
| AI | Claude (Claude Code 또는 Anthropic API) |
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

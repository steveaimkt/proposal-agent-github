# Proposal Agent — AI 입찰 제안서 자동 생성 에이전트

RFP(제안요청서) PDF를 입력하면 **40~80장 PPTX 입찰 제안서**를 자동 생성하는 AI 에이전트 시스템

## 핵심 특징

- **2-LLM 분업 구조**: Claude(기획) + Gemini(디자인 코드) 역할 분리
- **Impact-8 Framework**: 실제 수주 성공 제안서 기반 8-Phase 구조
- **디자인 레퍼런스 반영**: 사용자가 원하는 디자인 PPTX를 추가하면 스타일 자동 적용
- **slide_kit.py 엔진**: 2,270줄 PPTX 렌더링 엔진 (20가지 레이아웃, 네이티브 차트)

## 사전 준비

| 항목 | 설명 |
|------|------|
| **Claude 요금제** | Claude Pro 이상 (Pro / Max / Team) |
| **Claude Code** | `npm install -g @anthropic-ai/claude-code` |
| **Gemini API 키** | [Google AI Studio](https://aistudio.google.com/)에서 발급 |
| **Python 3.9+** | PPTX 생성 스크립트 실행용 |

## 파이프라인

```
제안요청서/테스트 XX/*.pdf     ← RFP 입력
    │
    ▼  [STEP 1-2] Claude Code (기획)
    │  RFP 분석 → 콘텐츠 설계 (Impact-8)
    │  Win Theme 도출 + Action Title + KPI
    │
    ▼  proposal_content.json 저장
    │
    │  [STEP 3] 사용자가 디자인 레퍼런스 추가
    │  input/design_reference.pptx
    │
    ▼  [STEP 4] Gemini (디자인 코드 생성)
    │  JSON + 레퍼런스 + slide_kit API → Python 코드
    │
    ▼  generate_제안서.py 실행
    │
output/테스트 XX/제안서.pptx   ← 40~80장 PPTX 출력
```

## 빠른 시작

### 1. 설치

```bash
git clone https://github.com/steveaimkt/proposal-agent-github.git
cd proposal-agent-github
pip install -r requirements.txt
export GEMINI_API_KEY=your-gemini-api-key
```

### 2. 제안서 생성

```bash
# STEP 1-2: Claude Code가 RFP 분석 + 콘텐츠 기획
mkdir -p 제안요청서/테스트\ 01
cp your_rfp.pdf 제안요청서/테스트\ 01/
claude
# → "제안요청서 폴더에 있는 테스트 01 폴더 내 파일을 분석한 후 콘텐츠를 기획해줘"
# → output/테스트 01/proposal_content.json 저장됨

# STEP 3: 디자인 레퍼런스 추가 (선택)
cp design_reference.pptx input/

# STEP 4: Gemini가 디자인 코드 생성 + 자동 실행
python3 src/gemini_codegen.py output/테스트\ 01/proposal_content.json \
    --reference input/design_reference.pptx \
    --execute
```

### gemini_codegen.py 옵션

```bash
python3 src/gemini_codegen.py <content_json> [옵션]

옵션:
  --reference, -r    디자인 레퍼런스 PPTX 경로
  --design-note, -d  디자인 요청 사항 (텍스트, 예: "미니멀 블루톤")
  --output, -o       생성 스크립트 저장 경로
  --model, -m        Gemini 모델 (기본: gemini-2.0-flash)
  --execute, -x      생성 후 자동 실행
  --api-key          Gemini API 키 (또는 GEMINI_API_KEY 환경변수)
```

## 역할 분리

| 역할 | 담당 | 입력 | 출력 |
|------|------|------|------|
| **기획** | Claude Code (Claude Pro) | RFP PDF | proposal_content.json |
| **디자인 코드** | Gemini (API) | JSON + 레퍼런스 + slide_kit API | generate_제안서.py |
| **렌더링** | Python (slide_kit.py) | generate_제안서.py | 제안서.pptx |

## Impact-8 Framework

| Phase | 이름 | 비중 | 설명 |
|-------|------|------|------|
| 0 | HOOK | 5% | 임팩트 있는 오프닝 |
| 1 | EXECUTIVE SUMMARY | 5% | 의사결정자용 요약 + Win Theme |
| 2 | INSIGHT | 12% | 시장 환경 + Pain Point |
| 3 | CONCEPT & STRATEGY | 12% | 핵심 컨셉 + 차별화 전략 |
| 4 | ACTION PLAN | **40%** | 상세 실행 계획 (핵심) |
| 5 | MANAGEMENT | 8% | 조직 + 운영 + 품질관리 |
| 6 | WHY US | 12% | 수행 역량 + 실적 |
| 7 | INVESTMENT & ROI | 6% | 비용 + 기대효과 |

## 디렉토리 구조

```
├── CLAUDE.md                      # ★ Claude Code 워크플로우 규칙
├── src/
│   ├── gemini_codegen.py          # ★ Gemini 디자인 코드 생성기
│   ├── generators/
│   │   └── slide_kit.py           # ★ PPTX 렌더링 엔진 (2,270줄)
│   ├── utils/
│   │   └── reference_analyzer.py  # 레퍼런스 PPTX 디자인 분석
│   ├── parsers/                   # PDF/DOCX 파싱
│   ├── agents/                    # Claude AI 에이전트
│   ├── schemas/                   # Pydantic 데이터 모델
│   └── orchestrators/             # 워크플로우 조율
├── docs/
│   └── slide_kit_reference.md     # ★ Gemini용 slide_kit API 가이드
├── examples/                      # 예제 + 레퍼런스 PPTX
├── input/                         # ★ 사용자 디자인 레퍼런스
├── 제안요청서/                     # ★ RFP 입력 (PDF)
├── output/                        # ★ 생성 결과물
│   └── 테스트 XX/
│       ├── proposal_content.json  # Claude 기획
│       ├── generate_제안서.py     # Gemini 코드
│       └── 제안서.pptx            # 최종 출력
└── docs/                          # 가이드 문서
```

## 기술 스택

| 카테고리 | 기술 |
|---------|------|
| 기획 AI | Claude Code (Claude Pro 이상 구독) |
| 코드 생성 AI | Gemini API (gemini-2.0-flash) |
| PPTX 렌더링 | python-pptx + slide_kit.py |
| 문서 처리 | pypdf, pdfplumber |

## 가이드 문서

- [slide_kit API 레퍼런스](docs/slide_kit_reference.md) — Gemini 코드 생성용 API 가이드
- [설치 및 사용 가이드](docs/INSTALL_AND_USAGE.md) — 단계별 안내
- [에이전트 구축 방식](docs/입찰제안서_에이전트_가이드.md) — 아키텍처 및 설계 원리
- [상세 사용 가이드](docs/제안서_에이전트_사용_가이드.md) — 고급 사용법

## 버전

- **v4.0**: 2-LLM 분업 구조 (Claude 기획 + Gemini 디자인 코드) + 디자인 레퍼런스 반영
- **v3.6**: Win Theme 전달 체인 + Action Title + C-E-I 설득 구조 + KPIWithBasis
- **v3.5**: VStack 자동 배치 + 네이티브 차트 + 테마 시스템 + 20가지 레이아웃

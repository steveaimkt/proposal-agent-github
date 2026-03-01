#!/usr/bin/env python3
"""
gemini_codegen.py — Gemini 기반 제안서 디자인 코드 생성기

워크플로우:
  1. Claude Code가 RFP 분석 → proposal_content.json 저장
  2. 사용자가 디자인 레퍼런스 추가 (PPTX 또는 텍스트)
  3. 이 스크립트가 Gemini API로 slide_kit.py 코드 생성
  4. 생성된 스크립트 실행 → PPTX 출력

사용법:
  python3 src/gemini_codegen.py output/테스트01/proposal_content.json
  python3 src/gemini_codegen.py output/테스트01/proposal_content.json --reference examples/레퍼런스.pptx
  python3 src/gemini_codegen.py output/테스트01/proposal_content.json --reference "https://www.behance.net/gallery/..."
  python3 src/gemini_codegen.py output/테스트01/proposal_content.json --design-note "미니멀 블루톤, 여백 많이"
"""

import argparse
import json
import os
import subprocess
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)


def load_slide_kit_reference():
    """slide_kit API 레퍼런스 문서 로드"""
    ref_path = os.path.join(PROJECT_ROOT, "docs", "slide_kit_reference.md")
    if not os.path.exists(ref_path):
        print(f"[ERROR] slide_kit_reference.md not found: {ref_path}")
        sys.exit(1)
    with open(ref_path, "r", encoding="utf-8") as f:
        return f.read()


def load_proposal_content(json_path):
    """Claude가 생성한 proposal_content.json 로드"""
    if not os.path.exists(json_path):
        print(f"[ERROR] proposal_content.json not found: {json_path}")
        sys.exit(1)
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_url(path):
    """URL인지 로컬 파일인지 판별"""
    return path.startswith("http://") or path.startswith("https://")


def analyze_url_reference(url, api_key, model="gemini-2.0-flash"):
    """URL 링크의 디자인 레퍼런스를 Gemini Vision으로 분석"""
    try:
        import google.generativeai as genai
    except ImportError:
        print("[ERROR] google-generativeai 패키지가 필요합니다.")
        return None

    try:
        import urllib.request
        from pathlib import Path
        import tempfile

        print(f"[INFO] URL 페이지 다운로드 중: {url}")

        # HTML 페이지 가져오기
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get("Content-Type", "")
            data = resp.read()

        # 이미지 URL인 경우 직접 Gemini Vision으로 분석
        if any(ext in url.lower() for ext in [".png", ".jpg", ".jpeg", ".webp", ".gif"]):
            print("[INFO] 이미지 파일 → Gemini Vision 분석")
            tmp = tempfile.NamedTemporaryFile(suffix=Path(url).suffix, delete=False)
            tmp.write(data)
            tmp.close()

            genai.configure(api_key=api_key)
            model_instance = genai.GenerativeModel(model)
            img_file = genai.upload_file(tmp.name)
            response = model_instance.generate_content([
                img_file,
                "이 디자인 이미지를 분석해주세요. 다음 항목을 추출하세요:\n"
                "1. 주요 컬러 팔레트 (HEX 코드)\n"
                "2. 레이아웃 스타일 (여백, 정렬, 그리드)\n"
                "3. 타이포그래피 스타일 (제목/본문 크기 비율, 굵기)\n"
                "4. 시각 요소 스타일 (카드, 아이콘, 차트, 이미지 처리)\n"
                "5. 전체적인 디자인 톤앤매너 (미니멀/화려/기업/캐주얼 등)\n"
                "한국어로 응답해주세요."
            ])
            os.unlink(tmp.name)
            return response.text

        # HTML 페이지인 경우 텍스트 추출 후 Gemini로 분석
        if "html" in content_type.lower() or data[:100].decode("utf-8", errors="ignore").strip().startswith("<!"):
            print("[INFO] HTML 페이지 → 텍스트 추출 + Gemini 분석")
            html_text = data.decode("utf-8", errors="ignore")

            # 간단한 태그 제거
            import re
            text = re.sub(r"<script[^>]*>.*?</script>", "", html_text, flags=re.DOTALL)
            text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            # 최대 5000자
            text = text[:5000]

            genai.configure(api_key=api_key)
            model_instance = genai.GenerativeModel(model)
            response = model_instance.generate_content(
                f"아래는 디자인 레퍼런스 웹페이지의 텍스트입니다. "
                f"이 페이지의 디자인 스타일을 분석해주세요:\n"
                f"1. 주요 컬러 팔레트\n"
                f"2. 레이아웃 스타일\n"
                f"3. 타이포그래피\n"
                f"4. 시각 요소 스타일\n"
                f"5. 전체 톤앤매너\n\n"
                f"URL: {url}\n"
                f"페이지 내용:\n{text}\n\n"
                f"한국어로 응답해주세요."
            )
            return response.text

        # PDF 등 기타 바이너리
        print(f"[WARN] 지원하지 않는 콘텐츠 타입: {content_type}")
        return f"디자인 레퍼런스 URL: {url} (자동 분석 불가 — 수동 디자인 지시 사용 권장)"

    except Exception as e:
        print(f"[WARN] URL 분석 실패: {e}")
        return f"디자인 레퍼런스 URL: {url} (접근 실패 — 수동 디자인 지시 사용 권장)"


def analyze_design_reference(pptx_path):
    """레퍼런스 PPTX에서 디자인 요소 추출"""
    try:
        from src.utils.reference_analyzer import ReferenceAnalyzer
        analyzer = ReferenceAnalyzer(pptx_path)
        profile = analyzer.to_design_profile()
        return json.dumps(profile, indent=2, ensure_ascii=False, default=str)
    except Exception as e:
        print(f"[WARN] 레퍼런스 분석 실패: {e}")
        return None


def build_prompt(proposal_content, slide_kit_ref, design_ref=None, design_note=None):
    """Gemini에게 보낼 프롬프트 구성"""

    prompt = f"""당신은 입찰 제안서 PPTX 생성 코드를 작성하는 전문가입니다.

## 작업
아래 제안서 콘텐츠 JSON을 기반으로, slide_kit.py API를 사용하는 Python 생성 스크립트를 작성하세요.

## 출력 규칙
1. 완전한 Python 스크립트를 출력하세요 (```python ... ``` 코드블록으로)
2. 스크립트 상단에 반드시 아래 import 패턴을 사용하세요:
   ```python
   import sys, os
   PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
   sys.path.insert(0, PROJECT_ROOT)
   from src.generators.slide_kit import *
   ```
3. 모든 슬라이드에 Action Title (인사이트 기반 문장형 제목)을 사용하세요
4. 매 슬라이드 패턴: bg(s, C["white"]) → TB(s, title, pg=pg) → 시각화 → PN(s, pg)
5. Win Theme 뱃지를 섹션 구분자에 포함하세요
6. 목표 분량: 40~80장
7. RGBColor 직접 하드코딩 금지 → C["primary"] 등 상수 사용
8. FONT, FONT_W 상수 사용 (폰트명 직접 입력 금지)

## slide_kit.py API 레퍼런스
{slide_kit_ref}
"""

    if design_ref:
        prompt += f"""
## 디자인 레퍼런스 분석 결과
아래 디자인 요소를 참고하여 컬러, 레이아웃 스타일을 맞추세요:
{design_ref}
"""

    if design_note:
        prompt += f"""
## 사용자 디자인 요청
{design_note}
"""

    prompt += f"""
## 제안서 콘텐츠 (JSON)
```json
{json.dumps(proposal_content, indent=2, ensure_ascii=False)}
```

위 JSON의 각 phase → slides를 순서대로 slide_kit 함수로 변환하세요.
slide_type에 따라 적절한 시각화 함수를 선택하고, 콘텐츠를 정확히 반영하세요.

Python 코드만 출력하세요.
"""
    return prompt


def call_gemini(prompt, api_key, model="gemini-2.0-flash"):
    """Gemini API 호출"""
    try:
        import google.generativeai as genai
    except ImportError:
        print("[ERROR] google-generativeai 패키지가 필요합니다.")
        print("  pip install google-generativeai")
        sys.exit(1)

    genai.configure(api_key=api_key)
    model_instance = genai.GenerativeModel(model)

    print(f"[INFO] Gemini ({model}) 호출 중...")
    response = model_instance.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.2,
            max_output_tokens=65536,
        ),
    )

    return response.text


def extract_code(response_text):
    """Gemini 응답에서 Python 코드 블록 추출"""
    # ```python ... ``` 블록 추출
    if "```python" in response_text:
        start = response_text.index("```python") + len("```python")
        end = response_text.index("```", start)
        return response_text[start:end].strip()
    elif "```" in response_text:
        start = response_text.index("```") + 3
        # 첫 줄이 언어 지정이면 스킵
        if response_text[start:start+10].strip().startswith(("python", "py")):
            start = response_text.index("\n", start) + 1
        end = response_text.index("```", start)
        return response_text[start:end].strip()
    else:
        return response_text.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Gemini 기반 제안서 디자인 코드 생성기"
    )
    parser.add_argument(
        "content_json",
        help="Claude가 생성한 proposal_content.json 경로",
    )
    parser.add_argument(
        "--reference", "-r",
        help="디자인 레퍼런스 (PPTX 파일 경로 또는 URL 링크)",
        default=None,
    )
    parser.add_argument(
        "--design-note", "-d",
        help="디자인 요청 사항 (텍스트)",
        default=None,
    )
    parser.add_argument(
        "--output", "-o",
        help="생성 스크립트 저장 경로 (기본: content_json과 같은 폴더)",
        default=None,
    )
    parser.add_argument(
        "--model", "-m",
        help="Gemini 모델 (기본: gemini-2.0-flash)",
        default="gemini-2.0-flash",
    )
    parser.add_argument(
        "--execute", "-x",
        help="생성 후 자동 실행",
        action="store_true",
    )
    parser.add_argument(
        "--api-key",
        help="Gemini API 키 (또는 GEMINI_API_KEY 환경변수)",
        default=None,
    )

    args = parser.parse_args()

    # API 키 확인
    api_key = args.api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] Gemini API 키가 필요합니다.")
        print("  export GEMINI_API_KEY=your-api-key")
        print("  또는: --api-key your-api-key")
        sys.exit(1)

    # 1. 콘텐츠 JSON 로드
    print(f"[STEP 1] 콘텐츠 로드: {args.content_json}")
    proposal_content = load_proposal_content(args.content_json)

    # 2. slide_kit 레퍼런스 로드
    print("[STEP 2] slide_kit 레퍼런스 로드")
    slide_kit_ref = load_slide_kit_reference()

    # 3. 디자인 레퍼런스 분석 (선택)
    design_ref = None
    if args.reference:
        if is_url(args.reference):
            # URL 링크 → Gemini로 분석
            print(f"[STEP 3] 디자인 레퍼런스 URL 분석: {args.reference}")
            design_ref = analyze_url_reference(args.reference, api_key, model=args.model)
        elif args.reference.lower().endswith(".pptx"):
            # 로컬 PPTX 파일 → reference_analyzer로 분석
            print(f"[STEP 3] 디자인 레퍼런스 PPTX 분석: {args.reference}")
            design_ref = analyze_design_reference(args.reference)
        else:
            # 기타 파일 (이미지 등)
            print(f"[STEP 3] 디자인 레퍼런스: {args.reference}")
            design_ref = f"디자인 레퍼런스 파일: {args.reference}"
    else:
        # examples/ 폴더에서 자동 탐색
        examples_dir = os.path.join(PROJECT_ROOT, "examples")
        if os.path.exists(examples_dir):
            pptx_files = [f for f in os.listdir(examples_dir) if f.endswith(".pptx")]
            if pptx_files:
                ref_path = os.path.join(examples_dir, pptx_files[0])
                print(f"[STEP 3] 디자인 레퍼런스 자동 탐색: {ref_path}")
                design_ref = analyze_design_reference(ref_path)

    # 4. 프롬프트 구성 + Gemini 호출
    print("[STEP 4] Gemini 코드 생성 중...")
    prompt = build_prompt(proposal_content, slide_kit_ref, design_ref, args.design_note)
    response = call_gemini(prompt, api_key, model=args.model)

    # 5. 코드 추출 및 저장
    code = extract_code(response)

    if args.output:
        output_path = args.output
    else:
        output_dir = os.path.dirname(args.content_json)
        output_path = os.path.join(output_dir, "generate_제안서.py")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[STEP 5] 생성 스크립트 저장: {output_path}")

    # 6. 자동 실행 (선택)
    if args.execute:
        print(f"[STEP 6] 스크립트 실행: python3 {output_path}")
        result = subprocess.run(
            [sys.executable, output_path],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print("[SUCCESS] PPTX 생성 완료!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"[ERROR] 스크립트 실행 실패:")
            print(result.stderr)
            sys.exit(1)
    else:
        print(f"\n실행하려면:")
        print(f"  python3 {output_path}")


if __name__ == "__main__":
    main()

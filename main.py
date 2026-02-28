#!/usr/bin/env python3
"""
입찰 제안서 자동 생성 에이전트 (v3.0 - Impact-8 Framework)

RFP 문서를 입력받아 PPTX 제안서를 자동 생성합니다.
실제 수주 성공 제안서 분석을 기반으로 개선된 구조 적용.

역할 분리:
- Claude Code: RFP 분석, 콘텐츠 생성 (Impact-8 Framework)
- [회사명]: PPTX 변환, Modern 스타일 디자인 적용
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from src.orchestrators.proposal_orchestrator import ProposalOrchestrator
from src.orchestrators.pptx_orchestrator import PPTXOrchestrator

load_dotenv()

app = typer.Typer(
    name="proposal-agent",
    help="입찰 제안서 자동 생성 에이전트 (v3.0 - Impact-8 Framework)",
    add_completion=False,
)
console = Console()

# 제안서 유형 상수
PROPOSAL_TYPES = {
    "marketing_pr": "마케팅/PR/소셜미디어",
    "event": "이벤트/행사",
    "it_system": "IT/시스템",
    "public": "공공/입찰",
    "consulting": "컨설팅",
    "general": "일반",
}


@app.command()
def generate(
    rfp_path: Path = typer.Argument(
        ...,
        help="RFP 문서 경로 (PDF/DOCX)",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    project_name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="프로젝트명 (미입력시 RFP에서 추출)",
    ),
    client_name: Optional[str] = typer.Option(
        None,
        "--client",
        "-c",
        help="발주처명 (미입력시 RFP에서 추출)",
    ),
    proposal_type: Optional[str] = typer.Option(
        None,
        "--type",
        "-t",
        help="제안서 유형 (marketing_pr, event, it_system, public, consulting, general)",
    ),
    company_data: Path = typer.Option(
        Path("company_data/company_profile.json"),
        "--company",
        "-d",
        help="회사 정보 JSON 경로",
    ),
    output_dir: Path = typer.Option(
        Path("output"),
        "--output",
        "-o",
        help="출력 디렉토리",
    ),
    reference: Optional[Path] = typer.Option(
        None,
        "--reference",
        "-r",
        help="레퍼런스 PPTX 경로 (디자인 참조용, 미지정시 examples/ 폴더 자동 탐색)",
    ),
    template: str = typer.Option(
        "modern",
        "--template",
        help="PPTX 템플릿/스타일명",
    ),
    save_json: bool = typer.Option(
        False,
        "--save-json",
        help="중간 JSON 파일 저장",
    ),
):
    """
    RFP 문서로부터 입찰 제안서(PPTX) 자동 생성 (Impact-8 Framework)

    예시:
        python main.py generate input/rfp.pdf -n "[프로젝트명]" -c "[발주처명]" -t marketing_pr
    """
    # API 키 확인
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print(
            Panel(
                "[red]ANTHROPIC_API_KEY가 설정되지 않았습니다.[/red]\n\n"
                ".env 파일에 API 키를 설정하거나 환경 변수로 설정해주세요.\n"
                "예: export ANTHROPIC_API_KEY=your-api-key",
                title="Error",
            )
        )
        raise typer.Exit(1)

    # 유형 검증
    if proposal_type and proposal_type not in PROPOSAL_TYPES:
        console.print(f"[red]지원하지 않는 제안서 유형: {proposal_type}[/red]")
        console.print(f"사용 가능한 유형: {', '.join(PROPOSAL_TYPES.keys())}")
        raise typer.Exit(1)

    # 헤더 출력
    console.print(
        Panel(
            "[bold cyan]입찰 제안서 자동 생성 에이전트[/bold cyan]\n"
            "[bold]v3.0 - Impact-8 Framework[/bold]\n\n"
            "[dim]Claude Code: 콘텐츠 생성 | [회사명]: Modern 스타일 PPTX[/dim]",
            title="Proposal Agent",
            border_style="cyan",
        )
    )

    console.print(f"\n[bold]입력 파일:[/bold] {rfp_path}")
    if project_name:
        console.print(f"[bold]프로젝트명:[/bold] {project_name}")
    if client_name:
        console.print(f"[bold]발주처:[/bold] {client_name}")
    if proposal_type:
        console.print(f"[bold]제안서 유형:[/bold] {PROPOSAL_TYPES.get(proposal_type, proposal_type)}")
    console.print()

    # 출력 디렉토리 생성
    output_dir.mkdir(parents=True, exist_ok=True)

    # 레퍼런스 파일 탐색
    reference_path = reference
    if not reference_path:
        input_dir = Path("examples")
        if input_dir.exists():
            pptx_files = list(input_dir.glob("*.pptx"))
            if pptx_files:
                reference_path = pptx_files[0]
                console.print(f"[bold]레퍼런스:[/bold] {reference_path} (자동 탐색)")

    # 비동기 실행
    asyncio.run(
        _generate_async(
            rfp_path=rfp_path,
            project_name=project_name or "",
            client_name=client_name or "",
            proposal_type=proposal_type,
            company_data=company_data,
            output_dir=output_dir,
            template=template,
            save_json=save_json,
            api_key=api_key,
            reference_path=reference_path,
        )
    )


async def _generate_async(
    rfp_path: Path,
    project_name: str,
    client_name: str,
    proposal_type: Optional[str],
    company_data: Path,
    output_dir: Path,
    template: str,
    save_json: bool,
    api_key: str,
    reference_path: Optional[Path] = None,
):
    """비동기 제안서 생성 (Impact-8 Framework)"""

    # Phase 0: 레퍼런스 디자인 분석 (선택)
    design_profile = None
    if reference_path and reference_path.exists():
        console.print("\n[bold cyan]Phase 0: 레퍼런스 디자인 분석[/bold cyan]")
        try:
            from src.utils.reference_analyzer import ReferenceAnalyzer
            analyzer = ReferenceAnalyzer(reference_path)
            design_profile = analyzer.to_design_profile()

            # 분석 결과 JSON 저장
            analysis_path = output_dir / "reference_analysis.json"
            analyzer.save_analysis(analysis_path)

            console.print(
                f"  [green]분석 완료[/green]: {design_profile['slide_count']}장, "
                f"주요 테마 {design_profile['theme_hex'].get('primary', 'N/A')}"
            )
            console.print(f"  [dim]분석 결과: {analysis_path}[/dim]")
        except Exception as e:
            console.print(f"  [yellow]레퍼런스 분석 실패 (기본 스타일 사용): {e}[/yellow]")

    # Phase 1: 콘텐츠 생성 (Claude Code)
    console.print("\n[bold cyan]Phase 1: 콘텐츠 생성 (Claude Code - Impact-8)[/bold cyan]")

    proposal_orchestrator = ProposalOrchestrator(api_key=api_key)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("분석 및 콘텐츠 생성 중...", total=None)

        def update_progress(p):
            msg = p.get("message", "처리 중...")
            progress.update(task, description=msg)

        submission_date = datetime.now().strftime("%Y-%m-%d")

        content = await proposal_orchestrator.execute(
            rfp_path=rfp_path,
            company_data_path=company_data if company_data.exists() else None,
            project_name=project_name,
            client_name=client_name,
            submission_date=submission_date,
            proposal_type=proposal_type,
            progress_callback=update_progress,
        )

    console.print("[green]Phase 1 완료[/green]")

    # 콘텐츠 요약 출력
    summary = proposal_orchestrator.get_proposal_summary(content)
    _print_content_summary(summary)

    # 최종 프로젝트명 확정
    final_project_name = content.project_name
    safe_filename = final_project_name.replace(" ", "_").replace("/", "-")

    # 중간 JSON 저장 (옵션)
    if save_json:
        json_path = output_dir / f"{safe_filename}_content.json"
        proposal_orchestrator.save_content_json(content, json_path)
        console.print(f"[dim]JSON 저장: {json_path}[/dim]")

    # Phase 2: PPTX 생성 ([회사명])
    style_label = "Modern 스타일"
    if design_profile:
        style_label = f"레퍼런스 기반 스타일 ({design_profile['theme_hex'].get('primary', '#002C5F')})"
    console.print(f"\n[bold cyan]Phase 2: PPTX 생성 ({style_label})[/bold cyan]")

    # 레퍼런스 테마 적용
    if design_profile and design_profile.get("theme"):
        try:
            from src.generators.slide_kit import C as SK_C
            from pptx.dml.color import RGBColor as _RGB
            for key, rgb in design_profile["theme"].items():
                if key in SK_C:
                    SK_C[key] = _RGB(*rgb)
            console.print("  [green]레퍼런스 테마 적용 완료[/green]")
        except Exception as e:
            console.print(f"  [yellow]테마 적용 실패: {e}[/yellow]")

    pptx_orchestrator = PPTXOrchestrator()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("PPTX 생성 중...", total=None)

        def update_progress(p):
            msg = p.get("message", "처리 중...")
            progress.update(task, description=msg)

        output_path = output_dir / f"{safe_filename}_제안서.pptx"

        pptx_orchestrator.execute(
            content=content,
            output_path=output_path,
            template_name=template,
            progress_callback=update_progress,
        )

    console.print("[green]Phase 2 완료[/green]")

    # 결과 출력
    total_slides = summary["total_slides"]
    console.print(
        Panel(
            f"[bold green]제안서가 생성되었습니다![/bold green]\n\n"
            f"[bold]파일:[/bold] {output_path}\n"
            f"[bold]프로젝트:[/bold] {content.project_name}\n"
            f"[bold]발주처:[/bold] {content.client_name}\n"
            f"[bold]유형:[/bold] {PROPOSAL_TYPES.get(content.proposal_type.value, content.proposal_type.value)}\n"
            f"[bold]슬라이드 수:[/bold] {total_slides}장\n"
            f"[bold]디자인 스타일:[/bold] {content.design_style or 'modern'}",
            title="Complete",
            border_style="green",
        )
    )


def _print_content_summary(summary: dict):
    """콘텐츠 요약 출력"""
    console.print("\n[bold]생성된 콘텐츠 요약:[/bold]")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Phase", style="dim")
    table.add_column("슬라이드 수", justify="right")

    if summary.get("teaser_slides", 0) > 0:
        table.add_row("Phase 0: HOOK", str(summary["teaser_slides"]))

    for phase_name, count in summary.get("phase_slides", {}).items():
        table.add_row(phase_name, str(count))

    table.add_row("[bold]총계[/bold]", f"[bold]{summary['total_slides']}[/bold]")

    console.print(table)

    if summary.get("slogan"):
        console.print(f"\n[bold]슬로건:[/bold] {summary['slogan']}")
    if summary.get("one_sentence_pitch"):
        console.print(f"[bold]핵심 제안:[/bold] {summary['one_sentence_pitch']}")


@app.command()
def analyze(
    rfp_path: Path = typer.Argument(
        ...,
        help="RFP 문서 경로 (PDF/DOCX)",
        exists=True,
    ),
):
    """
    RFP 문서 분석만 수행 (PPTX 생성 없이)
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY가 설정되지 않았습니다.[/red]")
        raise typer.Exit(1)

    console.print(f"\n[bold]RFP 분석:[/bold] {rfp_path}\n")

    from src.parsers.pdf_parser import PDFParser
    from src.parsers.docx_parser import DOCXParser
    from src.agents.rfp_analyzer import RFPAnalyzer

    # 파싱
    suffix = rfp_path.suffix.lower()
    if suffix == ".pdf":
        parser = PDFParser()
    else:
        parser = DOCXParser()

    parsed = parser.parse(rfp_path)
    console.print(f"파싱 완료: {len(parsed.get('raw_text', ''))} 문자\n")

    # 분석
    async def _analyze():
        analyzer = RFPAnalyzer(api_key=api_key)
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("RFP 분석 중...", total=None)

            def update_progress(p):
                progress.update(task, description=p.get("message", "분석 중..."))

            result = await analyzer.execute(parsed, progress_callback=update_progress)

        return result

    result = asyncio.run(_analyze())

    # 결과 출력
    console.print(
        Panel(
            f"[bold]프로젝트명:[/bold] {result.project_name}\n"
            f"[bold]발주처:[/bold] {result.client_name}\n"
            f"[bold]개요:[/bold] {result.project_overview[:200]}...\n\n"
            f"[bold]핵심 요구사항:[/bold] {len(result.key_requirements)}개\n"
            f"[bold]평가 기준:[/bold] {len(result.evaluation_criteria)}개\n"
            f"[bold]산출물:[/bold] {len(result.deliverables)}개\n\n"
            f"[bold]수주 전략:[/bold]\n{result.winning_strategy or '분석 필요'}",
            title="RFP 분석 결과",
            border_style="cyan",
        )
    )


@app.command()
def types():
    """사용 가능한 제안서 유형 목록"""
    console.print("\n[bold]사용 가능한 제안서 유형 (Impact-8 Framework):[/bold]\n")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("유형 코드", style="cyan")
    table.add_column("설명")
    table.add_column("ACTION PLAN 비중", justify="right")

    weights = {
        "marketing_pr": "40%",
        "event": "45%",
        "it_system": "35%",
        "public": "30%",
        "consulting": "30%",
        "general": "35%",
    }

    for code, desc in PROPOSAL_TYPES.items():
        table.add_row(code, desc, weights.get(code, "35%"))

    console.print(table)
    console.print("\n[dim]사용 예: python main.py generate rfp.pdf -t marketing_pr[/dim]")


@app.command()
def templates():
    """사용 가능한 PPTX 템플릿 목록"""
    templates_dir = Path("templates")

    console.print("\n[bold]디자인 스타일:[/bold]")
    console.print("  - [cyan]modern[/cyan] (기본) - Modern 제안서 스타일")

    if not templates_dir.exists():
        console.print("\n[yellow]templates 디렉토리가 없습니다.[/yellow]")
        return

    pptx_files = list(templates_dir.glob("*.pptx"))

    if pptx_files:
        console.print("\n[bold]커스텀 템플릿:[/bold]")
        for t in pptx_files:
            console.print(f"  - {t.stem}")


@app.command()
def info():
    """Impact-8 Framework 정보"""
    console.print(
        Panel(
            """[bold cyan]Impact-8 Framework[/bold cyan]

실제 수주 성공 제안서 분석을 기반으로 개선된 8-Phase 구조

[bold]Phase 구성:[/bold]
  Phase 0: HOOK (5%)      - 임팩트 있는 오프닝
  Phase 1: SUMMARY (5%)   - Executive Summary
  Phase 2: INSIGHT (10%)  - 시장 환경 & 문제 정의
  Phase 3: CONCEPT (12%)  - 핵심 컨셉 & 전략
  Phase 4: ACTION (40%)   - ★ 상세 실행 계획 (핵심!)
  Phase 5: MANAGEMENT (10%) - 운영 & 품질 관리
  Phase 6: WHY US (12%)   - 수행 역량 & 실적
  Phase 7: INVESTMENT (6%) - 투자 & ROI

[bold]핵심 특징:[/bold]
  • 티저(HOOK) 섹션으로 강력한 첫인상
  • ACTION PLAN이 전체의 40% (Modern 스타일)
  • 실제 콘텐츠 예시 포함 (마케팅/PR)
  • 프로젝트 유형별 가변 구조
  • Modern 스타일 디자인 시스템

[bold]디자인 스타일:[/bold]
  • 컬러: #002C5F (다크 블루), #00AAD2 (스카이블루)
  • 폰트: Pretendard
  • 레이아웃: 16:9 (1920x1080)
""",
            title="About Impact-8 Framework",
            border_style="cyan",
        )
    )


@app.command(name="reference-analyze")
def reference_analyze(
    pptx_path: Path = typer.Argument(
        ...,
        help="레퍼런스 PPTX 파일 경로",
        exists=True,
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="분석 결과 JSON 저장 경로 (미지정시 콘솔 출력)",
    ),
):
    """레퍼런스 PPTX 파일의 디자인 요소 분석"""
    from src.utils.reference_analyzer import ReferenceAnalyzer

    console.print(f"\n[bold]레퍼런스 분석:[/bold] {pptx_path}\n")

    analyzer = ReferenceAnalyzer(pptx_path)
    profile = analyzer.to_design_profile()

    # 결과 출력
    console.print(
        Panel(
            f"[bold]슬라이드 수:[/bold] {profile['slide_count']}장\n"
            f"[bold]주요 폰트:[/bold] {profile['primary_font']}\n"
            f"[bold]타이틀 크기:[/bold] {profile['title_sizes']}pt\n"
            f"[bold]본문 크기:[/bold] {profile['body_sizes']}pt\n\n"
            f"[bold]컬러 테마:[/bold]\n"
            f"  Primary:   {profile['theme_hex'].get('primary', 'N/A')}\n"
            f"  Secondary: {profile['theme_hex'].get('secondary', 'N/A')}\n"
            f"  Teal:      {profile['theme_hex'].get('teal', 'N/A')}\n"
            f"  Accent:    {profile['theme_hex'].get('accent', 'N/A')}\n"
            f"  Dark:      {profile['theme_hex'].get('dark', 'N/A')}\n"
            f"  Light:     {profile['theme_hex'].get('light', 'N/A')}\n\n"
            f"[bold]구조 분포:[/bold] {profile['structure_summary']}\n"
            f"[bold]레이아웃 분포:[/bold] {profile['layout_summary']}",
            title="레퍼런스 디자인 분석 결과",
            border_style="cyan",
        )
    )

    # JSON 저장
    if output:
        result_path = analyzer.save_analysis(output)
        console.print(f"\n[green]분석 결과 저장: {result_path}[/green]")

    # slide_kit 테마 호환 형식 출력
    theme = analyzer.to_slide_kit_theme()
    console.print("\n[bold]slide_kit 테마 (복사하여 사용):[/bold]")
    console.print(f'  "reference": {{')
    for k, v in theme.items():
        console.print(f'      "{k}": {v},')
    console.print(f'  }}')


if __name__ == "__main__":
    app()

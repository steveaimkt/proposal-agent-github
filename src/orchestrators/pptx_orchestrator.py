"""
PPTX 생성 오케스트레이터 (v3.0 - Impact-8 Framework)

[회사명] 레이어: ProposalContent → PPTX 변환 (Modern 스타일)
"""

from pathlib import Path
from typing import Callable, List, Optional

from ..schemas.proposal_schema import ProposalContent, PhaseContent, SlideContent, TeaserContent
from ..generators.template_manager import TemplateManager
from ..generators.pptx_generator import PPTXGenerator
from ..generators.chart_generator import ChartGenerator
from ..generators.diagram_generator import DiagramGenerator
from ..utils.logger import get_logger
from config.settings import get_settings

logger = get_logger("pptx_orchestrator")


class PPTXOrchestrator:
    """
    PPTX 생성 오케스트레이터 (v3.0 - Impact-8 Framework)

    [회사명] 레이어: Claude 콘텐츠 → Modern 스타일 PPTX
    """

    # Impact-8 Phase 제목
    PHASE_TITLES = {
        0: "HOOK",
        1: "SUMMARY",
        2: "INSIGHT",
        3: "CONCEPT & STRATEGY",
        4: "ACTION PLAN",
        5: "MANAGEMENT",
        6: "WHY US",
        7: "INVESTMENT & ROI",
    }

    def __init__(self, templates_dir: Optional[Path] = None):
        settings = get_settings()
        self.templates_dir = templates_dir or settings.templates_dir

        self.template_manager = TemplateManager(self.templates_dir)
        self.generator = PPTXGenerator(self.template_manager)
        self.chart_generator = ChartGenerator(self.template_manager)
        self.diagram_generator = DiagramGenerator(self.template_manager)

    def execute(
        self,
        content: ProposalContent,
        output_path: Path,
        template_name: str = "modern",
        progress_callback: Optional[Callable] = None,
    ) -> Path:
        """
        ProposalContent를 PPTX로 변환 (Impact-8 Framework, Modern 스타일)

        Args:
            content: Claude가 생성한 제안서 콘텐츠 (Impact-8 구조)
            output_path: 출력 PPTX 경로
            template_name: 사용할 템플릿/스타일
            progress_callback: 진행 상황 콜백

        Returns:
            생성된 PPTX 파일 경로
        """
        try:
            # 프레젠테이션 초기화 (Modern 스타일 적용)
            self.generator.create_presentation(template_name)

            # 총 단계: 티저 + Phase 1~7 + 저장
            has_teaser = content.teaser is not None
            total_steps = (1 if has_teaser else 0) + len(content.phases) + 1

            current_step = 0

            # Step 1: 티저/HOOK 슬라이드 (Phase 0)
            if has_teaser and content.teaser:
                current_step += 1
                if progress_callback:
                    progress_callback({
                        "step": current_step,
                        "total": total_steps,
                        "message": "Phase 0: HOOK (티저) 슬라이드 생성 중...",
                    })

                self._add_teaser_slides(content.teaser, content)
                logger.info(f"Phase 0: HOOK 슬라이드 생성 완료 ({len(content.teaser.slides)}장)")

            # Step 2~8: Phase 슬라이드 생성 (Impact-8 구조)
            for phase in content.phases:
                current_step += 1
                phase_title = self.PHASE_TITLES.get(phase.phase_number, phase.phase_title)

                if progress_callback:
                    progress_callback({
                        "step": current_step,
                        "total": total_steps,
                        "message": f"Phase {phase.phase_number}: {phase_title} 생성 중...",
                    })

                self._add_phase_slides(phase, content)
                logger.info(
                    f"Phase {phase.phase_number}: {phase_title} 슬라이드 생성 완료 "
                    f"({len(phase.slides)}장)"
                )

            # 마지막 단계: 저장
            current_step += 1
            if progress_callback:
                progress_callback({
                    "step": current_step,
                    "total": total_steps,
                    "message": "PPTX 파일 저장 중...",
                })

            self.generator.save(output_path)

            # 총 슬라이드 수 계산
            total_slides = len(content.teaser.slides) if content.teaser else 0
            total_slides += sum(len(p.slides) for p in content.phases)

            logger.info(f"PPTX 생성 완료: {output_path} ({total_slides}장)")
            return output_path

        except Exception as e:
            logger.error(f"PPTX 생성 실패: {e}")
            raise

    def _add_teaser_slides(self, teaser: TeaserContent, content: ProposalContent) -> None:
        """
        Phase 0: HOOK (티저) 슬라이드 추가

        Modern 스타일: 다크 배경, 임팩트 있는 오프닝
        """
        for slide in teaser.slides:
            slide_type = slide.slide_type.value if slide.slide_type else "teaser"

            if slide_type == "teaser":
                # 티저 슬라이드 (다크 배경, 큰 텍스트)
                headline = slide.key_message or slide.title
                subheadline = slide.subtitle or ""
                self.generator.add_teaser_slide(
                    headline=headline,
                    subheadline=subheadline,
                    background_color="dark_blue",
                    notes=slide.notes or "",
                )
            elif slide_type == "title":
                # 표지 슬라이드
                subtitle_parts = [content.client_name]
                if content.submission_date:
                    subtitle_parts.append(content.submission_date)
                subtitle_parts.append(content.company_name)

                self.generator.add_title_slide(
                    title=content.project_name,
                    subtitle=" | ".join(subtitle_parts),
                    slogan=teaser.main_slogan,
                    is_part_divider=False,
                )
            else:
                # 기타 슬라이드
                self._add_content_slide(slide)

    def _add_phase_slides(self, phase: PhaseContent, content: ProposalContent) -> None:
        """
        Phase 슬라이드 추가 (Impact-8 구조)
        """
        # 섹션 구분자 슬라이드 (첫 슬라이드가 section_divider가 아닌 경우)
        first_slide = phase.slides[0] if phase.slides else None
        if not first_slide or first_slide.slide_type.value != "section_divider":
            self.generator.add_section_divider(
                phase_number=phase.phase_number,
                phase_title=phase.phase_title,
                phase_subtitle=phase.phase_subtitle or "",
            )

        # Phase의 각 슬라이드 추가
        for slide in phase.slides:
            self._add_content_slide(slide, phase_number=phase.phase_number)

    def _add_content_slide(
        self,
        slide: SlideContent,
        phase_number: Optional[int] = None
    ) -> None:
        """
        개별 슬라이드 추가 (슬라이드 유형에 따라 분기)
        """
        slide_type = slide.slide_type.value if slide.slide_type else "content"

        if slide_type == "section_divider":
            self.generator.add_section_divider(
                phase_number=phase_number or 0,
                phase_title=slide.title,
                phase_subtitle=slide.subtitle or "",
                notes=slide.notes or "",
            )

        elif slide_type == "content":
            self.generator.add_content_slide(
                title=slide.title,
                subtitle=slide.subtitle,
                bullets=slide.bullets,
                key_message=slide.key_message,
                layout_hint=slide.layout_hint,
            )

        elif slide_type == "two_column":
            self.generator.add_two_column_slide(
                title=slide.title,
                left_title=slide.left_title,
                right_title=slide.right_title,
                left_content=slide.left_content,
                right_content=slide.right_content,
                key_message=slide.key_message,
            )

        elif slide_type == "three_column":
            self.generator.add_three_column_slide(
                title=slide.title,
                left_title=slide.left_title,
                center_title=slide.center_title,
                right_title=slide.right_title,
                left_content=slide.left_content,
                center_content=slide.center_content,
                right_content=slide.right_content,
                key_message=slide.key_message,
            )

        elif slide_type == "table":
            self.generator.add_table_slide(
                title=slide.title,
                table_data=slide.table,
                key_message=slide.key_message,
            )

        elif slide_type == "chart":
            self.chart_generator.add_chart_slide(
                generator=self.generator,
                title=slide.title,
                chart_data=slide.chart,
                key_message=slide.key_message,
            )

        elif slide_type == "timeline":
            self.diagram_generator.add_timeline_slide(
                generator=self.generator,
                title=slide.title,
                timeline_items=slide.timeline,
                key_message=slide.key_message,
            )

        elif slide_type == "org_chart":
            self.diagram_generator.add_org_chart_slide(
                generator=self.generator,
                title=slide.title,
                org_chart=slide.org_chart,
                key_message=slide.key_message,
            )

        elif slide_type == "comparison":
            # 비교 슬라이드 (AS-IS / TO-BE)
            as_is = {"title": "AS-IS (현재)", "items": []}
            to_be = {"title": "TO-BE (제안)", "items": []}

            if slide.comparison:
                if hasattr(slide.comparison, 'as_is'):
                    as_is["items"] = slide.comparison.as_is if isinstance(slide.comparison.as_is, list) else [slide.comparison.as_is]
                if hasattr(slide.comparison, 'to_be'):
                    to_be["items"] = slide.comparison.to_be if isinstance(slide.comparison.to_be, list) else [slide.comparison.to_be]
            elif slide.bullets:
                # bullets를 절반으로 나눠서 as_is/to_be로 처리
                mid = len(slide.bullets) // 2
                as_is["items"] = slide.bullets[:mid] if mid > 0 else []
                to_be["items"] = slide.bullets[mid:] if mid > 0 else slide.bullets

            self.generator.add_comparison_slide(
                title=slide.title,
                as_is=as_is,
                to_be=to_be,
                notes=slide.notes or "",
            )

        elif slide_type == "key_message":
            self.generator.add_key_message_slide(
                message=slide.key_message or slide.title,
                supporting_text=slide.subtitle or "",
                background_style="dark" if slide.visual_style == "dark" else "gradient",
                notes=slide.notes or "",
            )

        elif slide_type == "content_example":
            # 마케팅/PR 콘텐츠 예시 슬라이드
            examples = []
            if slide.content_examples:
                for ex in slide.content_examples:
                    if hasattr(ex, 'dict'):
                        examples.append(ex.dict())
                    elif isinstance(ex, dict):
                        examples.append(ex)
                    else:
                        examples.append({"title": str(ex), "description": ""})

            self.generator.add_content_example_slide(
                title=slide.title,
                examples=examples,
                notes=slide.notes or "",
            )

        elif slide_type == "channel_strategy":
            # 채널 전략 슬라이드
            channels = []
            if slide.channel_strategy:
                for ch in slide.channel_strategy:
                    if hasattr(ch, 'dict'):
                        channels.append(ch.dict())
                    elif isinstance(ch, dict):
                        channels.append(ch)
                    else:
                        channels.append({"name": str(ch), "role": "", "kpis": []})

            self.generator.add_channel_strategy_slide(
                title=slide.title,
                channels=channels,
                notes=slide.notes or "",
            )

        elif slide_type == "campaign":
            # 캠페인 슬라이드
            campaign_data = slide.campaign or {}
            if hasattr(campaign_data, 'dict'):
                campaign_data = campaign_data.dict()

            self.generator.add_campaign_slide(
                title=slide.title,
                campaign_name=campaign_data.get("name", slide.title),
                period=campaign_data.get("period", ""),
                objective=campaign_data.get("objective", ""),
                activities=campaign_data.get("activities", slide.bullets or []),
                notes=slide.notes or "",
            )

        elif slide_type == "budget":
            # 예산 슬라이드
            budget_items = []
            total = ""

            if slide.table:
                table_data = slide.table
                if hasattr(table_data, 'rows'):
                    for row in table_data.rows:
                        if len(row) >= 4:
                            budget_items.append({
                                "name": row[0],
                                "unit_price": row[1],
                                "quantity": row[2],
                                "amount": row[3],
                            })
                        elif len(row) >= 2:
                            budget_items.append({
                                "name": row[0],
                                "unit_price": "",
                                "quantity": "",
                                "amount": row[-1],
                            })
                    # 마지막 행이 총계인 경우
                    if table_data.rows and "총" in str(table_data.rows[-1][0]):
                        total = str(table_data.rows[-1][-1])
                        budget_items = budget_items[:-1]

            self.generator.add_budget_slide(
                title=slide.title,
                budget_items=budget_items,
                total=total,
                notes=slide.notes or "",
            )

        elif slide_type == "case_study":
            # 케이스 스터디 슬라이드
            case_data = {
                "project_name": slide.title,
                "client": "",
                "period": "",
                "description": "",
                "kpis": [],
            }

            if slide.bullets:
                case_data["description"] = " ".join(slide.bullets[:2])

            if slide.kpis:
                for kpi in slide.kpis:
                    if hasattr(kpi, 'dict'):
                        case_data["kpis"].append(kpi.dict())
                    elif isinstance(kpi, dict):
                        case_data["kpis"].append(kpi)
                    else:
                        case_data["kpis"].append({"name": str(kpi), "value": ""})

            self.generator.add_case_study_slide(
                title=slide.title,
                case=case_data,
                notes=slide.notes or "",
            )

        elif slide_type == "teaser":
            # 티저 슬라이드
            self.generator.add_teaser_slide(
                headline=slide.key_message or slide.title,
                subheadline=slide.subtitle or "",
                background_color="dark_blue",
                notes=slide.notes or "",
            )

        elif slide_type == "index":
            # 목차 슬라이드
            self.generator.add_index_slide(
                title=slide.title,
                items=slide.bullets or [],
                current_index=-1,
                notes=slide.notes or "",
            )

        elif slide_type == "process":
            # 프로세스 슬라이드
            self.diagram_generator.add_process_slide(
                generator=self.generator,
                title=slide.title,
                bullets=slide.bullets,
                key_message=slide.key_message,
            )

        else:
            # 기본 콘텐츠 슬라이드로 처리
            self.generator.add_content_slide(
                title=slide.title,
                subtitle=slide.subtitle,
                bullets=slide.bullets,
                key_message=slide.key_message,
            )

    # 레거시 호환성을 위한 별칭
    def _add_cover_slide(self, content: ProposalContent) -> None:
        """표지 슬라이드 추가 (레거시 호환)"""
        subtitle_parts = [content.client_name]
        if content.submission_date:
            subtitle_parts.append(content.submission_date)
        subtitle_parts.append(content.company_name)

        subtitle = " | ".join(subtitle_parts)

        self.generator.add_title_slide(
            title=content.project_name,
            subtitle=subtitle,
            slogan=content.slogan,
            is_part_divider=False,
        )

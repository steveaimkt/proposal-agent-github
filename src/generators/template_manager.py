"""
PPTX 템플릿 관리자 ([회사명])

템플릿 로드, 레이아웃 관리, 디자인 시스템 제공
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

from ..utils.logger import get_logger
from config.settings import get_settings

logger = get_logger("template_manager")


class TemplateManager:
    """PPTX 템플릿 관리자"""

    def __init__(self, templates_dir: Optional[Path] = None):
        settings = get_settings()
        self.templates_dir = templates_dir or settings.templates_dir
        self.layouts = self._load_layouts()
        self.design_system = self._get_design_system()

    def _load_layouts(self) -> Dict[str, Any]:
        """레이아웃 정의 로드"""
        layout_file = self.templates_dir / "slide_layouts.json"
        if layout_file.exists():
            try:
                return json.loads(layout_file.read_text(encoding="utf-8"))
            except Exception as e:
                logger.warning(f"레이아웃 파일 로드 실패: {e}")

        return self._default_layouts()

    def _default_layouts(self) -> Dict[str, Any]:
        """기본 레이아웃 정의"""
        return {
            "layouts": {
                "title": {"index": 0, "name": "Title Slide"},
                "section": {"index": 2, "name": "Section Header"},
                "content": {"index": 1, "name": "Title and Content"},
                "two_column": {"index": 3, "name": "Two Content"},
                "comparison": {"index": 4, "name": "Comparison"},
                "blank": {"index": 6, "name": "Blank"},
            }
        }

    def _get_design_system(self) -> Dict[str, Any]:
        """디자인 시스템 반환 (색상, 폰트 등)"""
        return {
            "colors": {
                "primary": RGBColor(0, 82, 147),  # 진한 파랑
                "secondary": RGBColor(0, 150, 199),  # 밝은 파랑
                "accent": RGBColor(255, 107, 0),  # 오렌지
                "success": RGBColor(40, 167, 69),  # 초록
                "warning": RGBColor(255, 193, 7),  # 노랑
                "danger": RGBColor(220, 53, 69),  # 빨강
                "text_dark": RGBColor(51, 51, 51),  # 진한 회색
                "text_light": RGBColor(128, 128, 128),  # 밝은 회색
                "background": RGBColor(255, 255, 255),  # 흰색
                "background_light": RGBColor(245, 245, 245),  # 연한 회색
            },
            "fonts": {
                "title": "맑은 고딕",
                "body": "맑은 고딕",
                "english": "Arial",
                "sizes": {
                    "cover_title": Pt(44),
                    "part_title": Pt(40),
                    "slide_title": Pt(28),
                    "subtitle": Pt(20),
                    "body": Pt(16),
                    "small": Pt(14),
                    "caption": Pt(12),
                },
            },
            "spacing": {
                "margin": Inches(0.5),
                "content_margin": Inches(0.75),
                "element_gap": Inches(0.25),
            },
            "dimensions": {
                "slide_width": Inches(13.33),
                "slide_height": Inches(7.5),
            },
        }

    def load_template(self, template_name: str = "base_template") -> Presentation:
        """
        템플릿 파일 로드

        Args:
            template_name: 템플릿 파일명 (확장자 제외)

        Returns:
            Presentation 객체
        """
        template_path = self.templates_dir / f"{template_name}.pptx"

        if template_path.exists():
            logger.info(f"템플릿 로드: {template_path}")
            return Presentation(template_path)

        logger.info("기본 빈 프레젠테이션 생성")
        return Presentation()

    def get_layout_index(self, layout_name: str) -> int:
        """
        레이아웃 인덱스 반환

        Args:
            layout_name: 레이아웃 이름

        Returns:
            레이아웃 인덱스 (기본값: 1)
        """
        layouts = self.layouts.get("layouts", {})
        layout = layouts.get(layout_name, {})
        return layout.get("index", 1)

    def get_color(self, color_name: str) -> RGBColor:
        """색상 반환"""
        return self.design_system["colors"].get(
            color_name, self.design_system["colors"]["text_dark"]
        )

    def get_font_size(self, size_name: str) -> Pt:
        """폰트 크기 반환"""
        return self.design_system["fonts"]["sizes"].get(
            size_name, self.design_system["fonts"]["sizes"]["body"]
        )

    def get_font_name(self, font_type: str = "body") -> str:
        """폰트 이름 반환"""
        return self.design_system["fonts"].get(font_type, "맑은 고딕")

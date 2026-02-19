"""디자인 설정 모듈"""

from .design_style import (
    ProposalDesignStyle,
    DEFAULT_STYLE,
    PHASE_STYLES,
    get_phase_style,
    export_to_pptx_theme,
    ColorPalette,
    Typography,
    Layout,
    SlideBackground,
    LayoutType,
)

__all__ = [
    "ProposalDesignStyle",
    "DEFAULT_STYLE",
    "PHASE_STYLES",
    "get_phase_style",
    "export_to_pptx_theme",
    "ColorPalette",
    "Typography",
    "Layout",
    "SlideBackground",
    "LayoutType",
]

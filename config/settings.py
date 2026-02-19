"""애플리케이션 설정"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    """앱 설정"""

    # API
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

    # Paths
    base_dir: Path = Path(__file__).parent.parent
    templates_dir: Path = base_dir / "templates"
    prompts_dir: Path = base_dir / "config" / "prompts"
    company_data_dir: Path = base_dir / "company_data"
    output_dir: Path = base_dir / "output"
    input_dir: Path = base_dir / "input"

    # PPTX Settings
    default_template: str = "base_template"
    slide_width_inches: float = 13.33
    slide_height_inches: float = 7.5

    class Config:
        arbitrary_types_allowed = True


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """싱글톤 설정 반환"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

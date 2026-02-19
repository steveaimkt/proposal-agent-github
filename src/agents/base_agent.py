"""Claude 기반 에이전트 추상 클래스"""

import json
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import anthropic

from ..utils.logger import get_logger
from config.settings import get_settings

logger = get_logger("agent")


class BaseAgent(ABC):
    """Claude 기반 에이전트 추상 클래스"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        settings = get_settings()
        self.api_key = api_key or settings.anthropic_api_key
        self.model = model or settings.claude_model
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.prompts_dir = settings.prompts_dir

    @abstractmethod
    async def execute(
        self,
        input_data: Dict[str, Any],
        progress_callback: Optional[Callable] = None,
    ) -> Any:
        """에이전트 실행"""
        pass

    def _call_claude(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 4096,
    ) -> str:
        """
        Claude API 호출

        Args:
            system_prompt: 시스템 프롬프트
            user_message: 사용자 메시지
            max_tokens: 최대 토큰 수

        Returns:
            Claude 응답 텍스트
        """
        logger.debug(f"Claude API 호출 (model: {self.model})")

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Claude API 호출 실패: {e}")
            raise

    def _load_prompt(self, prompt_name: str) -> str:
        """
        프롬프트 템플릿 로드

        Args:
            prompt_name: 프롬프트 파일명 (확장자 제외)

        Returns:
            프롬프트 텍스트
        """
        prompt_path = self.prompts_dir / f"{prompt_name}.txt"

        if not prompt_path.exists():
            logger.warning(f"프롬프트 파일 없음: {prompt_path}")
            return ""

        return prompt_path.read_text(encoding="utf-8")

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        텍스트에서 JSON 추출

        Args:
            text: JSON을 포함한 텍스트

        Returns:
            파싱된 JSON 딕셔너리
        """
        # JSON 블록 찾기 (```json ... ``` 또는 { ... })
        patterns = [
            r"```json\s*([\s\S]*?)\s*```",  # 코드 블록
            r"```\s*([\s\S]*?)\s*```",  # 일반 코드 블록
            r"(\{[\s\S]*\})",  # 중괄호 매칭
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                json_str = match.group(1)
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    continue

        logger.error("JSON 추출 실패")
        return {}

    def _truncate_text(self, text: str, max_chars: int = 30000) -> str:
        """텍스트 길이 제한"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n... (텍스트가 잘렸습니다)"

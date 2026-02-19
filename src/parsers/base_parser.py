"""문서 파서 추상 클래스"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class BaseParser(ABC):
    """문서 파서 추상 클래스"""

    @abstractmethod
    def parse(self, file_path: Path) -> Dict[str, Any]:
        """
        문서를 파싱하여 구조화된 데이터 반환

        Args:
            file_path: 파일 경로

        Returns:
            {
                "raw_text": str,
                "tables": List[Dict],
                "sections": List[Dict],
                "metadata": Dict
            }
        """
        pass

    @abstractmethod
    def extract_text(self, file_path: Path) -> str:
        """전체 텍스트 추출"""
        pass

    @abstractmethod
    def extract_tables(self, file_path: Path) -> List[Dict[str, Any]]:
        """테이블 데이터 추출"""
        pass

    def is_supported(self, file_path: Path) -> bool:
        """파일 형식 지원 여부"""
        return file_path.suffix.lower() in self.supported_extensions

    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """지원하는 파일 확장자"""
        pass

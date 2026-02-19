"""로깅 설정"""

import sys
from loguru import logger


def setup_logger(level: str = "INFO") -> None:
    """로거 설정"""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True,
    )


def get_logger(name: str = "proposal"):
    """로거 인스턴스 반환"""
    return logger.bind(name=name)


# 기본 설정 적용
setup_logger()

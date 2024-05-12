import os
from loguru import logger

ROOT_DIR = os.getcwd()


class CustomLogger:

    def __init__(self) -> None:
        logger.add(
            sink=f"{ROOT_DIR}/src/logs/logs{{time:YYYY-MM-DD_HH-mm}}.log",
            format="""
                <green>{time:YYYY-MM-DD HH:mm:ss UTC}</green> |
                <level>{level}</level> --
                <cyan>{message}</cyan> --
                <level>{module}:{function}</level>
            """,
            level="DEBUG",
            enqueue=True,
            rotation="500 MB"
        )
        logger.info("CustomLogger CLASS INITIALIZED")

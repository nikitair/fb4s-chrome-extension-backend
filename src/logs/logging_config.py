import os
from loguru import logger
import time

ROOT_DIR = os.getcwd()


class CustomLogger():
    def __init__(self) -> None:
        logger.add(
            sink=f"{ROOT_DIR}/src/logs/logs.log",
            format="""<green>{time:YYYY-MM-DD HH:mm:ss}</green> UTC - <level>{level}</level> - {message} || <level>{module}</level>""",
            level="DEBUG",
            rotation="500 MB",
            enqueue=True,
            catch=True 
        )

        os.environ['TZ'] = 'UTC'
        time.tzset() 

        logger.debug("CustomLogger CLASS INITIALIZED")

CustomLogger()

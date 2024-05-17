import os
import time
from datetime import datetime

from loguru import logger

ROOT_DIR = os.getcwd()

class CustomLogger():
    def __init__(self) -> None:
        log_filename = datetime.now().strftime("logs_%Y-%m-%dT%H:%M.log")

        logger.add(
            sink=f"{ROOT_DIR}/src/logs/{log_filename}",
            format="""<green>{time:YYYY-MM-DD HH:mm:ss}</green> UTC - <level>{level}</level> - {message} || <level>{module}</level>""",
            level="DEBUG",
            rotation="500 MB",
            enqueue=True,
            catch=True 
        )

        # Set the timezone to UTC
        os.environ['TZ'] = 'UTC'
        time.tzset() 

        logger.debug("CustomLogger CLASS INITIALIZED")

CustomLogger()

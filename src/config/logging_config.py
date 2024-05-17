import os
import time
from datetime import datetime
from loguru import logger

ROOT_DIR = os.getcwd()


log_config = {
    "handlers": [
        {
            "sink": f"{ROOT_DIR}/src/logs/app.log",
            "format": "{time:YYYY-MM-DD HH:mm} UTC - {level} - {name}:{function}:{line} - {message}",
            "level": "DEBUG",
            "rotation": "50 MB",
            "enqueue": True,
            "catch": True
        }
    ]
}

def configure_logger():
    # Set the timezone to UTC
    os.environ['TZ'] = 'UTC'
    time.tzset()
    logger.configure(**log_config)
    return True

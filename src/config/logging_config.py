import os
import time
from datetime import datetime

from loguru import logger

from . import ROOT_DIR

app_log_config = {
            "sink": f"{ROOT_DIR}/src/logs/app.log",
            "format": "{time:YYYY-MM-DD HH:mm} UTC - {level} - {name}:{function}:{line} - {message}",
            "level": "DEBUG",
            "rotation": "100 MB",
            "enqueue": True,
            "catch": True,
        }


server_log_config = {

            "sink": f"{ROOT_DIR}/src/logs/server.log",
            "format": "{time:YYYY-MM-DD HH:mm} UTC - {level} - {name}:{function}:{line} - {message}",
            "level": "INFO",
            "rotation": "50 MB",
            "enqueue": True,
            "catch": True
        }


def configure_logger():
    logger.remove()
    logger.add(**app_log_config)
    logger.debug("LOGGER CONFIGURED")


# def configure_server_logger():
#     logger.remove()
#     logger.add(**server_log_config)

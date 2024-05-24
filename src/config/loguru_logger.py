import os

from loguru import logger

from . import ROOT_DIR

log_file_path = os.path.join(ROOT_DIR, "src", "logs", "app.log")

app_log_config = {
    "sink": log_file_path,
    "format": "{time:YYYY-MM-DD HH:mm} UTC - {level} - {name}:{function}:{line} - {message}",
    "level": "DEBUG",
    "rotation": "100 MB",
    "enqueue": True,
    "catch": True,
}

logger = logger.bind()
logger.add(**app_log_config)

import logging
import os
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

from . import ROOT_DIR


class UTCFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, timezone.utc)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + ' UTC'


# Logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Custom UTC formatter
formatter = UTCFormatter('%(asctime)s - %(levelname)s - %(message)s')

# File output with size limit
log_file = os.path.join(ROOT_DIR, "src", "logs", "server.log")
fh = RotatingFileHandler(log_file, maxBytes=50 * 1024 * 1024, backupCount=5)  # 50MB limit, keep up to 5 old logs
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

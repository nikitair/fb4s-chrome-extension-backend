import logging

from . import ROOT_DIR

legacy_logger = logging.getLogger(__name__)
legacy_logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Terminal output
th = logging.StreamHandler()
th.setLevel(logging.INFO)
th.setFormatter(formatter)
legacy_logger.addHandler(th)

# File output
fh = logging.FileHandler(f"{ROOT_DIR}/src/logs/server.log")
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
legacy_logger.addHandler(fh)

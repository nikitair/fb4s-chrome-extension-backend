import os
import time

# set timezone to UTC
os.environ['TZ'] = 'UTC'
time.tzset()

ROOT_DIR = os.getcwd()

LOGTRAIL_API_KEY = os.getenv("LOGTRAIL_API_KEY", "")
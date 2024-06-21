import os
import time

# set timezone to UTC
os.environ['TZ'] = 'UTC'
time.tzset()

ROOT_DIR = os.getcwd()

LOGTRAIL_API_KEY = os.getenv("LOGTRAIL_API_KEY", "")


CORS_ORIGINS = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5003",
    "chrome-extension://kephamhkieifbokkbkmjpjhnkhmcpdhj",
    "https://marketing.findbusinesses4sale.com",
    "*"
]

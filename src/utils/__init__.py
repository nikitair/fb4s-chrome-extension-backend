import os

from dotenv import load_dotenv

load_dotenv()

FUB_API_KEY = os.getenv("FUB_API_KEY")
FUB_BASE_URL = os.getenv("FUB_BASE_URL")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

NINJAS_API_KEY = os.getenv("NINJAS_API_KEY", "")
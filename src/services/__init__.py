import os

from dotenv import load_dotenv

from processors.fub import FUBProcessor
from processors.retool import RetoolProcessor
from processors.twilio import TwilioProcessor

load_dotenv()

FUB_API_KEY = os.getenv("FUB_API_KEY")
FUB_BASE_URL = os.getenv("FUB_BASE_URL")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

fub = FUBProcessor(
    api_key=FUB_API_KEY,
    base_url=FUB_BASE_URL
)

twilio = TwilioProcessor(
    sid=TWILIO_SID,
    auth_token=TWILIO_AUTH_TOKEN,
    from_phone_number=TWILIO_FROM_NUMBER
)

retool = RetoolProcessor()

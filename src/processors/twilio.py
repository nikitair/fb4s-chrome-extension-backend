
from dotenv import load_dotenv
from twilio.rest import Client

from config.logging_config import logger
from utils import twilio as utils

load_dotenv()


class TwilioProcessor:

    def __init__(self, sid, auth_token, from_phone_number):
        self.sid = sid
        self.auth_token = auth_token
        self.from_phone_number = from_phone_number
        self.client = Client(self.sid, self.auth_token)
        logger.debug("(Twilio) - CLASS INITIALIZED")

    def send_sms(self, phone_number, message):
        phone_number = utils.format_phone_number(phone_number)

        logger.info(f"(Twilio) - SENDING SMS TO - {phone_number}")

        result = {
            "success": None,
            "sms_sid": None
        }

        try:
            sms = self.client.messages.create(
                body=message,
                from_=self.from_phone_number,
                to=phone_number
            )
            logger.info(f"(TWILIO) - SID - {sms.sid}; STATUS - {sms.status}")

            result["success"] = True if sms.status in ("delivered", "queued", "sending", "sent", "receiving", "received", "accepted") else False
            result["sms_id"] = sms.sid

        except Exception:
            logger.exception("(Twilio) - !!! TWILIO ERROR")

        return result

    def sms_status(self, sid):
        logger.info(f"(Twilio) - CHECKING DELIVERY STATUS OF - {sid}")
        status = None

        try:
            status = self.client.messages(sid).fetch().status
            # status = self.client.messages(sid).fetch().error_code
            logger.info(f"(Twilio) - DELIVERY STATUS - {status}")
        except Exception:
            logger.exception("(Twilio) - !!! TWILIO ERROR")

        return True if status == "delivered" else False

    def __str__(self):
        return self.__class__.__name__

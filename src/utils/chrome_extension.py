import base64
import pytz
from datetime import datetime

from config.logging_config import logger

demo_admin = "d2lsbG93QGZiNHMuY29t"
demo_buyer = "c3RscnZua0BnbWFpbC5jb20="
demo_buyer_id = "Mjc2OTY="


def decode_base64_item(encoded_item: str) -> str | int | None:
    logger.info(f"DECODE BASE64 - {encoded_item}")
    decoded_item = None
    if encoded_item:
        try:
            decoded_item = base64.b64decode(encoded_item).decode()
        except Exception:
            logger.exception(f"!!! FAILED DECODING - ({encoded_item}) OF TYPE ({type(encoded_item)})")
    return decoded_item


def get_utc_offset(timezone: str) -> int | None:
    logger.info(f"GET UTC OFFSET - {timezone}")
    if timezone:
        utc_now = datetime.now(pytz.utc)
        city_timezone = pytz.timezone(timezone)
        local_time = utc_now.astimezone(city_timezone)
        utc_offset = int(local_time.utcoffset().total_seconds() / 3600)
        return utc_offset
        

if __name__ == "__main__":
    print(get_utc_offset("Toronto"))

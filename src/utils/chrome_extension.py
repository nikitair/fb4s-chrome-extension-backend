import base64
import pytz
import httpx
from datetime import datetime
from . import NINJAS_KEY

from config.logging_config import logger

demo_admin = "d2lsbG93QGZiNHMuY29t"
demo_buyer = "c3RscnZua0BnbWFpbC5jb20="
demo_buyer_id = "Mjc2OTY="


def decode_base64_item(encoded_item: str) -> str | int | None:
    decoded_item = None
    if encoded_item:
        try:
            decoded_item = base64.b64decode(encoded_item).decode()
        except Exception:
            logger.exception(f"!!! FAILED DECODING - ({encoded_item}) OF TYPE ({type(encoded_item)})")
    return decoded_item


def get_utc_offset(city: str) -> int:
    logger.debug(f"GETTING TIMEZONE OF - {city}")
    response = httpx.get(
        url=f"https://api.api-ninjas.com/v1/timezone?city={city}&country=Canada",
        headers={"X-Api-Key": NINJAS_KEY}
    )
    status_code = response.status_code
    data = response.json()
    logger.debug(f"NINJA API RESPONSE - {status_code} - {data}")
    
    if status_code == 200:
        timezone = data["timezone"]
        utc_now = datetime.now(pytz.utc)
        city_timezone = pytz.timezone(timezone)
        local_time = utc_now.astimezone(city_timezone)
        utc_offset = int(local_time.utcoffset().total_seconds() / 3600)
        return utc_offset
        

if __name__ == "__main__":
    print(get_utc_offset("Toronto"))

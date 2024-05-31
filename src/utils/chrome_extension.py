import base64

from config.logging_config import logger

demo_admin = "d2lsbG93QGZiNHMuY29t"
demo_buyer = "c3RscnZua0BnbWFpbC5jb20="
demo_buyer_id = "Mjc2OTY="


def decode_base64_item(encoded_item: str) -> str | int | None:
    decoded_item = None
    try:
        decoded_item = base64.b64decode(encoded_item).decode()
    except Exception:
        logger.exception(f"!!! FAILED DECODING - ({encoded_item}) OF TYPE ({type(encoded_item)})")
    return decoded_item


if __name__ == "__main__":
    print(decode_base64_item(None))

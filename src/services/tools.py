import base64
from config.logging_config import logger
from schemas.tools import Base64Response


def encode_to_base64(item) -> str:
    logger.info(f"ENCODING TO BASE64 - {item}")
    
    response = Base64Response()
    response.mode = "encode"
    
    try:
        encoded_item = base64.b64encode(item.encode()).decode()
        logger.info(f"BASE64 ENCODING RESULT - {encoded_item}")
    except (TypeError, ValueError) as ex:
        response.success = False
        logger.exception(f"!!! FAILED ENCODING TO BASE64 - {ex}")
    
    # TODO: find better solution
    return response.dict()



def decode_from_base64(item) -> str:
    logger.info(f"DECODING FROM BASE64 - {item}")
    
    response = Base64Response()
    response.mode = "decode"
    
    try:
        decoded_item = base64.b64decode(item).decode()
        logger.info(f"BASE64 DECODING RESULT - {decoded_item}")
    except (TypeError, ValueError) as ex:
        response.success = False
        logger.exception(f"!!! FAILED DECODING FROM BASE64 - {ex}")
    
    # TODO: find better solution
    return response.dict()

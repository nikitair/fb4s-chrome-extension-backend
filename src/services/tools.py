import base64
from config.logging_config import logger
from schemas.tools import Base64Response


def encode_to_base64(item) -> str:
    logger.info(f"ENCODING TO BASE64 - {item}")
    
    response_dict = {
        "success": True,
        "mode": "encode",
        "data": None
    }
    
    try:
        encoded_item = base64.b64encode(item.encode()).decode()
        response_dict["data"] = encoded_item
        logger.info(f"BASE64 ENCODING RESULT - {encoded_item}")
    except (TypeError, ValueError) as ex:
        response_dict["success"] = False
        logger.exception(f"!!! FAILED ENCODING TO BASE64 - {ex}")
    
    # TODO: find better solution
    # response_dict = dict(response.model_dump())
    logger.info(f"RESPONSE - {response_dict}")
    return response_dict


def decode_from_base64(item) -> str:
    logger.info(f"DECODING FROM BASE64 - {item}")
    
    # response = Base64Response()
    response_dict = {
        "success": True,
        "mode": "decode",
        "data": None
    }
    
    try:
        decoded_item = base64.b64decode(item).decode()
        response_dict["data"] = decoded_item
        logger.info(f"BASE64 DECODING RESULT - {decoded_item}")
    except (TypeError, ValueError) as ex:
        response_dict["success"] = False
        logger.exception(f"!!! FAILED DECODING FROM BASE64 - {ex}")
    
    # TODO: find better solution
    # response_dict = dict(response.model_dump())
    logger.info(f"RESPONSE - {response_dict}")
    return response_dict

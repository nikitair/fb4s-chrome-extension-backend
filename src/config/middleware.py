from fastapi import Request, Response
from config.logging_config import logger


async def log_middleware(request: Request, call_next):
    # configure_server_logger()
    request_data = {
        'ip': request.client.host, 
        'url': request.url.__str__(),
        'method': request.method,
        'query_params': request.query_params.__str__(),
        
    }
    logger.info(f"SERVER REQUEST - {request_data}")

    response: Response = await call_next(request)
    response_data = {
        'status_code': response.status_code
    }
    logger.info(f"SERVER RESPONSE - {response_data}")

    # configure_logger()
    return response

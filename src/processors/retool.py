from config.logging_config import logger
import os
import requests


class RetoolProcessor:

    def __init__(self):
        logger.debug(f"({self.__class__.__name__}) CLASS INITIALIZED")

    def get_sms_template(self, campaign_special_id: int, campaign_day: int):
        logger.info(f"{self.get_sms_template.__name__} -- GETTING SMS TEMPLATE WITH campaign_special_id - {campaign_special_id}; campaign_day - {campaign_day}")
        response = requests.post(
            url=os.getenv("RETOOL_GET_SMS_TEMPLATE_URL", ""),
            json={"campaign_special_id": campaign_special_id, "campaign_day": campaign_day}
        )
        status_code = response.status_code
        data = response.json()
        logger.info(f"{self.get_sms_template.__name__} -- STATUS CODE - {status_code}; DATA - {data}")

        if status_code != 200:
            logger.warning(f"{self.get_sms_template.__name__} -- ! SMS TEMPLATE NOT FOUND")
        return data

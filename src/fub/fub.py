import base64

import requests

from logs.logging_config import logger


class FUB:

    def __init__(self, api_key: str, base_url: str):
        self.api_key = base64.b64encode(api_key.encode()).decode()
        self.base_url = base_url
        logger.debug(f"{self.__class__.__name__} ( {self.__init__.__name__} ) -- CLASS INITIALIZED")

    
    def get_people_list(self):
        logger.info(f"{self.__class__.__name__} ( {self.get_people_list.__name__} ) -- GETTING PEOPLE LIST")
        url = f"{self.base_url}people?sort=created&limit=10&offset=0&includeTrash=false&includeUnclaimed=false"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }

        data = None

        try:
            response = requests.get(url, headers=headers)
            logger.info(f"{self.__class__.__name__} ( {self.get_people_list.__name__} ) -- FUB API STATUS CODE - {response.status_code}")

            data = response.json()
            logger.debug(f"{self.__class__.__name__} ( {self.get_people_list.__name__} ) -- FUB API DATA - {data}")

        except Exception as ex:
            logger.exception(f"{self.__class__.__name__} ( {self.get_people_list.__name__} ) -- !!! FUB API ERROR - {ex}")

        return data
    

    def get_people(self, people_id: int):
        logger.info(f"{self.__class__.__name__} ( {self.get_people.__name__} ) -- GETTING PEOPLE WITH ID: {people_id}")
        url = f"{self.base_url}people/{people_id}"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }

        data = None

        try:
            response = requests.get(url, headers=headers)
            logger.info(f"{self.__class__.__name__} ( {self.get_people.__name__} ) -- FUB API STATUS CODE - {response.status_code}")

            data = response.json()
            logger.debug(f"{self.__class__.__name__} ( {self.get_people.__name__} ) -- FUB API DATA - {data}")

        except Exception as ex:
            logger.exception(f"{self.__class__.__name__} ( {self.get_people.__name__} ) -- !!! FUB API ERROR - {ex}")

        return data


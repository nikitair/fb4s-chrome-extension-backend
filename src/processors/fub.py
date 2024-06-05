import base64

import requests

from config.logging_config import logger


class FUBProcessor:

    def __init__(self, api_key: str, base_url: str):
        self.api_key = base64.b64encode(api_key.encode()).decode()
        self.base_url = base_url
        logger.debug(f"({self.__class__.__name__}) - CLASS INITIALIZED")

    def get_people_list(self):
        logger.info(f"({self.__class__.__name__}) - GET PEOPLE LIST")
        url = f"{self.base_url}people?sort=created&limit=10&offset=0&includeTrash=false&includeUnclaimed=false"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }

        data = None

        try:
            response = requests.get(url, headers=headers)
            logger.info(
                f"({self.__class__.__name__}) - FUB API STATUS CODE - {response.status_code}")

            data = response.json()
            logger.debug(f"({self.__class__.__name__}) - FUB API DATA - {data}")

        except Exception as ex:
            logger.exception(
                f"({self.__class__.__name__})- !!! FUB API ERROR - {ex}")

        return data

    def get_person_by_id(self, person_id: int) -> dict | None:
        logger.info(f"({self.__class__.__name__}) - GET PEOPLE WITH ID: {person_id}")
        url = f"{self.base_url}people/{person_id}"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }
        data = None

        response = requests.get(url, headers=headers)
        status_code = response.status_code
        logger.info(f"({self.__class__.__name__}) - FUB API STATUS CODE - {status_code}")

        if status_code == 200:
            data = response.json()
            logger.debug(f"({self.__class__.__name__}) - FUB API DATA - {data}")
        else:
            logger.error(f"({self.__class__.__name__}) - !!! FUB API ERROR - {response.text}")

        return data
    
    
    def get_user_by_id(self, user_id: int) -> dict | None:
        logger.info(f"({self.__class__.__name__}) - GET USER WITH ID: {user_id}")
        url = f"{self.base_url}users/{user_id}"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }
        data = None

        response = requests.get(url, headers=headers)
        status_code = response.status_code
        logger.info(f"({self.__class__.__name__}) - FUB API STATUS CODE - {status_code}")

        if status_code == 200:
            data = response.json()
            logger.debug(f"({self.__class__.__name__}) - FUB API DATA - {data}")
        else:
            logger.error(f"({self.__class__.__name__}) - !!! FUB API ERROR - {response.text}")

        return data

    
    def get_person_by_email(self, person_email: str) -> dict | None:
        logger.info(f"({self.__class__.__name__}) - GET PEOPLE WITH EMAIL: {person_email}")
        url = f"{self.base_url}people?sort=created&limit=10&offset=0&includeTrash=false&includeUnclaimed=false&email={person_email}"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }
        data = None

        response = requests.get(url, headers=headers)
        status_code = response.status_code
        logger.info(f"({self.__class__.__name__}) - FUB API STATUS CODE - {status_code}")

        if status_code == 200:
            data = response.json()["people"]
            logger.debug(f"({self.__class__.__name__}) - FUB API DATA - {data}")
        else:
            logger.error(f"({self.__class__.__name__}) - !!! FUB API ERROR - {response.text}")

        return data

    def get_note(self, note_id: int):
        logger.info(f"({self.__class__.__name__}) - GET NOTE WITH ID: {note_id}")
        url = f"{self.base_url}notes/{note_id}"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }

        data = None

        try:
            response = requests.get(url, headers=headers)
            logger.info(
                f"({self.__class__.__name__}) - FUB API STATUS CODE - {response.status_code}")

            data = response.json()
            logger.debug(f"({self.__class__.__name__}) - FUB API DATA - {data}")

        except Exception as ex:
            logger.exception(f"({self.__class__.__name__}) - !!! FUB API ERROR - {ex}")

        return data

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
    

    def get_people(self, person_id: int):
        logger.info(f"{self.__class__.__name__} ( {self.get_people.__name__} ) -- GETTING PERSON WITH ID: {person_id}")
        url = f"{self.base_url}people/{person_id}"
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
    

    def get_note(self, note_id: int):
        logger.info(f"{self.__class__.__name__} ( {self.get_note.__name__} ) -- GETTING NOTE WITH ID: {note_id}")
        url = f"{self.base_url}notes/{note_id}"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }

        data = None

        try:
            response = requests.get(url, headers=headers)
            logger.info(f"{self.__class__.__name__} ( {self.get_note.__name__} ) -- FUB API STATUS CODE - {response.status_code}")

            data = response.json()
            logger.debug(f"{self.__class__.__name__} ( {self.get_note.__name__} ) -- FUB API DATA - {data}")

        except Exception as ex:
            logger.exception(f"{self.__class__.__name__} ( {self.get_note.__name__} ) -- !!! FUB API ERROR - {ex}")

        return data
    

    def create_note(self, person_id: int, note_subject: str, note_body: str):
        logger.info(f"{self.__class__.__name__} ( {self.create_note.__name__} ) -- CREATING NOTE - PERSON_ID: {person_id}; SUBJECT: {note_subject}; BODY: {note_body}")
        url = f"{self.base_url}notes"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }
        payload = {
            "personId": {person_id},
            "subject": {note_subject},
            "body": {note_body},
            "isHtml": True
        }

        data = None

        try:
            response = requests.post(url, headers=headers, json=payload)
            logger.info(f"{self.__class__.__name__} ( {self.create_note.__name__} ) -- FUB API STATUS CODE - {response.status_code}")

            data = response.json()
            logger.debug(f"{self.__class__.__name__} ( {self.create_note.__name__} ) -- FUB API DATA - {data}")

        except Exception as ex:
            logger.exception(f"{self.__class__.__name__} ( {self.create_note.__name__} ) -- !!! FUB API ERROR - {ex}")

        return data
    

    def update_note(self, note_id: int, person_id: int, note_subject: str, note_body: str):
        logger.info(f"{self.__class__.__name__} ( {self.update_note.__name__} ) -- UPDATING NOTE WITH ID: {note_id} - PERSON_ID: {person_id}; SUBJECT: {note_subject}; BODY: {note_body}")
        url = f"{self.base_url}notes/{note_id}"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }
        payload = {
            "personId": {person_id},
            "subject": {note_subject},
            "body": {note_body},
            "isHtml": True
        }

        data = None

        try:
            response = requests.put(url, headers=headers, json=payload)
            logger.info(f"{self.__class__.__name__} ( {self.update_note.__name__} ) -- FUB API STATUS CODE - {response.status_code}")

            data = response.json()
            logger.debug(f"{self.__class__.__name__} ( {self.update_note.__name__} ) -- FUB API DATA - {data}")

        except Exception as ex:
            logger.exception(f"{self.__class__.__name__} ( {self.update_note.__name__} ) -- !!! FUB API ERROR - {ex}")

        return data


    def delete_note(self, note_id: int):
        logger.info(f"{self.__class__.__name__} ( {self.delete_note.__name__} ) -- DELETING NOTE WITH ID: {note_id}")
        url = f"{self.base_url}notes/{note_id}"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.api_key}"
        }

        data = None

        try:
            response = requests.delete(url, headers=headers)
            logger.info(f"{self.__class__.__name__} ( {self.delete_note.__name__} ) -- FUB API STATUS CODE - {response.status_code}")

            data = response.json()
            logger.debug(f"{self.__class__.__name__} ( {self.delete_note.__name__} ) -- FUB API DATA - {data}")

        except Exception as ex:
            logger.exception(f"{self.__class__.__name__} ( {self.delete_note.__name__} ) -- !!! FUB API ERROR - {ex}")

        return data

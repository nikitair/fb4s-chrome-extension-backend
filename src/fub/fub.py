from logs.logging_config import logger
import base64
import requests

# encoded_string = base64.b64encode(string_to_encode.encode()).decode()


class FUB:

    def __init__(self, api_key: str):
        self.api_key = base64.b64encode(api_key.encode()).decode()
        logger.info(f"{self.__class__.__name__} ( {self.__init__.__name__} ) -- CLASS INITIALIZED")

    
    def get_people(self, people_ids: list[str]):
        url = "https://api.followupboss.com/v1/people?sort=created&limit=10&offset=0&includeTrash=false&includeUnclaimed=false"

        headers = {
            "accept": "application/json",
            "authorization": "Basic ZmthXzA3RVh4VlhMNVhWc3lCYXU0TUVPTnNVYXVXUFFzbEJNV2Y6"
        }

        response = requests.get(url, headers=headers)

        print(response.text)
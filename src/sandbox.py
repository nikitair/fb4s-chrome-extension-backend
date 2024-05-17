import os

from dotenv import load_dotenv

from services.fub import FUB

load_dotenv()


fub = FUB(api_key=os.getenv("FUB_API_KEY"), base_url=os.getenv("https://api.followupboss.com/v1/"))

fub.get_people()
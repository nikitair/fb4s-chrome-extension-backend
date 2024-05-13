import os
from dotenv import load_dotenv
from fub.fub import FUB

load_dotenv()


fub = FUB(api_key=os.getenv("FUB_API_KEY"))

fub.get_people()
from services.fub import FUBService
import os
from dotenv import  load_dotenv

load_dotenv()

fub = FUBService(api_key=os.getenv("FUB_API_KEY", ""), base_url=os.getenv("FUB_BASE_URL", ""))


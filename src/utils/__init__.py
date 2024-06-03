import os
from dotenv import load_dotenv

load_dotenv()

NINJAS_KEY = os.getenv("NINJAS_KEY", "")

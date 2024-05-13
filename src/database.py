import os
from dotenv import load_dotenv
# from logs.logging_config import logger
from db.postgres.handler import PostgresHandler

load_dotenv()

POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 0))
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


postgres = PostgresHandler(
    database=POSTGRES_DATABASE,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)


if __name__ == "__main__":
    postgres.connect()
    postgres.select_executor(
        query="SELECT * FROM fub.fub_users LIMIT 1"
    )
    postgres.disconnect()

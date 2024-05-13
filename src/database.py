import os
from dotenv import load_dotenv
from db.postgres.handler import PostgresHandler
from db.mysql.handler import MySQLHandler 

load_dotenv()

POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 0))
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")


MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "")
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 0))
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")


postgres = PostgresHandler(
    database=POSTGRES_DATABASE,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)

mysql = MySQLHandler(
    database=MYSQL_DATABASE,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT
)


if __name__ == "__main__":
    # postgres.connect()
    # postgres.select_executor(
    #     query="SELECT * FROM fub.fub_users LIMIT 1"
    # )
    # postgres.disconnect()

    mysql.connect()
    mysql.select_executor(
        query="SELECT * FROM tbl_customers LIMIT 1"
    )
    mysql.disconnect()

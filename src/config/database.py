import os
from db.mysql.m_sql import MySQLQueries
from dotenv import load_dotenv

from db.mysql.m_handler import MySQLHandler
from db.postgres.p_handler import PostgresHandler

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

mysql_queries = MySQLQueries


if __name__ == "__main__":
    # postgres.connect()
    # postgres.select_executor(
    #     query="SELECT * FROM fub.fub_users LIMIT 1"
    # )
    # postgres.disconnect()

    # postgres.execute_with_connection(
    #     func = postgres.select_executor,
    #     query = "SELECT * FROM fub.fub_users LIMIT 1"
    # )

    mysql.execute_with_connection(
        mysql.select_executor,
        query=mysql_queries.sent_weekly_outreach_emails
    )

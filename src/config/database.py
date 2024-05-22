import os

from dotenv import load_dotenv

from database.mysql.mysql_handler import AsyncMySQLHandler
from database.mysql.mysql_sql import MySQLQueries
from database.postgres.postgres_handler import AsyncPostgresHandler

load_dotenv()

LOCAL_PORT = int(os.getenv("LOCAL_PORT", 0))

SSH_TUNNEL_MODE = bool(int(os.getenv("SSH_TUNNEL_MODE", 0)))
SSH_TUNNEL_SERVER_USERNAME = os.getenv("SSH_TUNNEL_SERVER_USERNAME", "")
SSH_TUNNEL_SERVER_HOST = os.getenv("SSH_TUNNEL_SERVER_HOST", "")
SSH_TUNNEL_SERVER_PORT = int(os.getenv("SSH_TUNNEL_SERVER_PORT", 0))
SSH_KEY_PATH = os.getenv("SSH_KEY_PATH", "")

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

postgres = AsyncPostgresHandler(
    database=POSTGRES_DATABASE,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)

mysql = AsyncMySQLHandler(
    database=MYSQL_DATABASE,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT
)

mysql_queries = MySQLQueries

if __name__ == "__main__":
    # postgres.connect(
    #     ssh_mode=SSH_TUNNEL_MODE,
    #     ssh_key_path=SSH_KEY_PATH,
    #     ssh_server_host=SSH_TUNNEL_SERVER_HOST,
    #     ssh_server_port=SSH_TUNNEL_SERVER_PORT
    # )
    #
    # postgres.select_executor(
    #     query="SELECT * FROM fub.fub_users LIMIT 1"
    # )
    # postgres.disconnect()

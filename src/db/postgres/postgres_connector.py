import os

# import psycopg2
import asyncpg
from dotenv import load_dotenv

# from sshtunnel import SSHTunnelForwarder
from logs.logging_config import logger

load_dotenv()


class PostgresConnector:

    database = os.getenv("POSTGRES_DATABASE", "")
    host = os.getenv("POSTGRES_HOST", "")
    port = int(os.getenv("POSTGRES_PORT", 0))
    local_port = int(os.getenv("POSTGRES_LOCAL_PORT", 0))
    user = os.getenv("POSTGRES_USER", "")
    password = os.getenv("POSTGRES_PASSWORD", "")

    ssh_postgres_port = os.getenv("SSH_POSTGRES_PORT", "")

    ssh_mode = bool(os.getenv("SSH_MODE", 0))
    ssh_server_port = int(os.getenv("SSH_SERVER_PORT", 0))
    ssh_server_host = os.getenv("SSH_SERVER_HOST", "")
    ssh_server_password = os.getenv("SSH_SERVER_PASSWORD", "")
    ssh_pkey_path = os.getenv("SSH_PKEY_PATH", "")

    def __init__(self, ssh_tunnel_mode: bool = False) -> None:
        self.ssh_tunnel_mode = ssh_tunnel_mode
        logger.info(f"{self.__class__.__name__} ( {self.__init__.__name__} ) -- CLASS INITIALIZED | SSH TUNNEL MODE - {self.ssh_tunnel_mode}")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    async def connector(self, func):
        logger.debug(f"{self.__class__.__name__} ( {self.connector.__name__} ) -- CONNECTING TO POSTGRES")

        async def wrapper(*args, **kwargs):
            conn = None
            try:
                conn = await asyncpg.connect(
                    dbname=self.database,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                logger.debug(f"{self.__class__.__name__} ( {self.connector.__name__} ) -- SUCCESSFULLY CONNECTED TO POSTGRES")
            except Exception:
                logger.exception(f"{self.__class__.__name__} ( {self.connector.__name__} ) -- !!! POSTGRES DIRECT CONNECTION ERROR")

            if conn:
                try:
                    return await func(conn, *args, **kwargs)
                except Exception:
                    logger.exception(f"{self.__class__.__name__} ( {self.connector.__name__} ) -- !!! POSTGRES QUERY EXECUTION ERROR")
                finally:
                    await conn.close()
                    logger.debug(f"{self.__class__.__name__} ( {self.connector.__name__} ) -- CLOSED POSTGRES CONNECTION")

        return await wrapper

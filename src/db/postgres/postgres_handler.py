import os
import psycopg2
from sshtunnel import SSHTunnelForwarder
from logs.logging_config import logger
from dotenv import load_dotenv

load_dotenv()


class PostgresHandler:

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

    def ssh_tunnel_connector(self):
        try:
            server = SSHTunnelForwarder(
                (self.ssh_server_host, self.ssh_server_port),
                ssh_username="",
                ssh_pkey=self.ssh_pkey_path,
                remote_bind_address=(self.host, self.port),
                local_bind_address=("localhost", self.local_port)
            )
            server.start()

            conn = psycopg2.connect(dbname=self.database, user=self.user,
                                    password=self.password, host="localhost", port=self.local_port)
            
            curr = conn.cursor()
            curr.execute("SELECT * FROM fub.fub_users")
            curr.execute()
            data = curr.fetchall()
            print(data)
            conn.close()

        except:
            logger.exception(f"{self.__class__.__name__} ( {self.ssh_tunnel_connector.__name__} ) -- !!! POSTGRES CONNECTION ERROR")

    def direct_connector(self):
        ...

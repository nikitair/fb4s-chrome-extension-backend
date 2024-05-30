import sys

import asyncpg
import psycopg2
from sshtunnel import SSHTunnelForwarder

# from config.loguru_logger import logger
from config.logging_config import logger


class PostgresHandler:
    """
    How to use:

    postgres = PostgresHandler(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

    --------------------------------------------------------- 

    # Use Case 1 (Manual connection / disconnection):

    postgres.connect()
    postgres.select_executor(
        query="SELECT * FROM fub.fub_users LIMIT 1"
    )
    postgres.disconnect()

    ---------------------------------------------------------

    # Use Case 2 (Automatic connection / disconnection): s

    postgres.execute_with_connection(
        func = postgres.select_executor,
        query = "SELECT * FROM fub.fub_users WHERE id = %s",
        params = [10]
    )
    """

    def __init__(self, database: str, user: str, password: str, host: str, port: int):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.connection = None
        self.tunnel = None

        logger.debug(f"({self.__class__.__name__}) - CLASS INITIALIZED")

    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.database})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.database})"

    def connect(self,
                ssh_mode=False,
                ssh_host=None,
                ssh_port=None,
                ssh_username=None,
                ssh_key_path=None,
                local_port=None):
        try:
            if ssh_mode:
                logger.info(f"({self.__class__.__name__}) - SSH TUNNEL MODE")

                self.tunnel = SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_username,
                    ssh_pkey=ssh_key_path,
                    remote_bind_address=(self.host, self.port),
                    local_bind_address=("localhost", local_port)
                )
                self.tunnel.start()
                logger.debug(
                    f"({self.__class__.__name__}) - SSH TUNNEL ESTABLISHED")

                self.connection = psycopg2.connect(dbname=self.database, user=self.user,
                                                   password=self.password, host="localhost", port=local_port)
            else:
                self.connection = psycopg2.connect(
                    dbname=self.database,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
            logger.debug(
                f"({self.__class__.__name__}) - CONNECTED TO POSTGRES")
        except Exception as ex:
            logger.exception(
                f"({self.__class__.__name__}) - !!! FAILED CONNECTING TO POSTGRES - {ex}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.debug(
                f"({self.__class__.__name__}) - CLOSED POSTGRES CONNECTION")
        if self.tunnel:
            self.tunnel.stop()
            logger.debug(f"({self.__class__.__name__}) - CLOSED SSH TUNNEL")

    def execute_with_connection(self, func, *args, **kwargs):
        try:
            self.connect()
            result = func(*args, **kwargs)
            return result
        finally:
            self.disconnect()

    def select_executor(self, query: str, params: list = []):
        logger.info(
            f"({self.__class__.__name__}) - EXECUTING SELECT QUERY: {query} - PARAMS: {params}")

        data = None

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            logger.debug(f"({self.__class__.__name__}) - SQL RESULT: {data}")

        except Exception as ex:
            logger.exception(
                f"({self.__class__.__name__}) - !!! FAILED EXECUTING SQL QUERY - {ex}")

        finally:
            return data

    def insert_executor(self, query: str, params: list[tuple]):
        logger.info(
            f"({self.__class__.__name__}) - EXECUTING INSERT QUERY: {query} - INSERT PARAMS: {params}")

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, params)
            self.connection.commit()
            logger.info(
                f"({self.__class__.__name__}) - BULK INSERT SUCCESSFUL")

        except Exception as ex:
            self.connection.rollback()
            logger.exception(
                f"({self.__class__.__name__}) - !!! FAILED INSERTION - {ex}")

        finally:
            if cursor:
                cursor.close()

    def delete_executor(self, query: str, params: list, safe: bool = True):
        logger.warning(
            f"({self.__class__.__name__}) - EXECUTING DELETE QUERY: {query} - PARAMS: {params}")

        user_answer = 'y'

        if safe:
            user_answer = input("! Confirm Deletion [y / n] >> ")

        if user_answer.strip().lower() == 'y':
            cursor = None
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                self.connection.commit()
                logger.info(f"({self.__class__.__name__}) - DELETE SUCCESSFUL")

            except Exception as ex:
                self.connection.rollback()
                logger.exception(
                    f"({self.__class__.__name__}) - !!! FAILED DELETION - {ex}")

            finally:
                cursor.close()
        else:
            sys.stdout.write("Aborted Deletion")


class AsyncPostgresHandler(PostgresHandler):
    """
    Async implementation of the original PostgresHandler
    """

    def __init__(self, database: str, user: str, password: str, host: str, port: int):
        super().__init__(database, user, password, host, port)
        self.connection = None  # asyncpg connection object

    async def connect(self):
        try:
            self.connection = await asyncpg.connect(
                user=self.user,
                password=self.password,
                database=self.database,
                host=self.host,
                port=self.port
            )
            logger.debug(
                f"({self.__class__.__name__}) - CONNECTED TO POSTGRES")
        except Exception as ex:
            logger.exception(
                f"({self.__class__.__name__}) - !!! FAILED CONNECTING TO POSTGRES - {ex}")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            logger.debug(
                f"({self.__class__.__name__}) - CLOSED POSTGRES CONNECTION")

    async def execute_with_connection(self, func, *args, **kwargs):
        try:
            await self.connect()
            result = await func(*args, **kwargs)
            return result
        finally:
            await self.disconnect()

    async def select_executor(self, query: str, params: list = []):
        logger.info(
            f"({self.__class__.__name__}) - EXECUTING SELECT QUERY: {query} - PARAMS: {params}")

        data = None

        try:
            data = await self.connection.fetch(query, *params)
            logger.debug(f"({self.__class__.__name__}) - SQL RESULT: {data}")

        except Exception as ex:
            logger.exception(
                f"({self.__class__.__name__}) - !!! FAILED EXECUTING SQL QUERY - {ex}")

        finally:
            return data

    async def insert_executor(self, query: str, params: list[tuple]):
        logger.info(
            f"({self.__class__.__name__}) - EXECUTING INSERT QUERY: {query} - INSERT PARAMS: {params}")

        try:
            await self.connection.executemany(query, params)
            logger.info(
                f"({self.__class__.__name__}) - BULK INSERT SUCCESSFUL")

        except Exception as ex:
            logger.exception(
                f"({self.__class__.__name__}) - !!! FAILED INSERTION - {ex}")

    async def delete_executor(self, query: str, params: list, safe: bool = True):
        logger.warning(
            f"({self.__class__.__name__}) - EXECUTING DELETE QUERY: {query} - PARAMS: {params}")

        user_answer = 'y'

        if safe:
            user_answer = input("! Confirm Deletion [y / n] >> ")

        if user_answer.strip().lower() == 'y':
            try:
                await self.connection.execute(query, *params)
                logger.info(f"({self.__class__.__name__}) - DELETE SUCCESSFUL")

            except Exception as ex:
                logger.exception(
                    f"({self.__class__.__name__}) - !!! FAILED DELETION - {ex}")
        else:
            sys.stdout.write("Aborted Deletion")

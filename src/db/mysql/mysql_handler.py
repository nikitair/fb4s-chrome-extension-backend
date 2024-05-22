import asyncio
import sys

import aiomysql
import pymysql

from config.logging_config import logger


class MySQLHandler:
    """
    MySQL handler.
    
    How to use:

    mysql = MySQLHandler(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

    --------------------------------------------------------- 

    # Use Case 1 (Manual connection / disconnection):

    mysql.connect()
    mysql.select_executor(
        query="SELECT * FROM your_table LIMIT 1"
    )
    mysql.disconnect()

    ---------------------------------------------------------

    # Use Case 2 (Automatic connection / disconnection):

    mysql.execute_with_connection(
        func=mysql.select_executor,
        query="SELECT * FROM your_table WHERE id = %s",
        params=[10]
    )
    """

    def __init__(self, database: str, user: str, password: str, host: str, port: int):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.connection = None  # pymysql connector object

        logger.debug(f"{self.__class__.__name__} ({self.__init__.__name__}) -- CLASS INITIALIZED")

    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.database})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.database})"

    def connect(self):
        conn = None
        try:
            conn = pymysql.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.connection = conn
            logger.debug(f"{self.__class__.__name__} ({self.connect.__name__}) -- CONNECTED TO MYSQL")
        except Exception as ex:
            logger.exception(f"{self.__class__.__name__} ({self.connect.__name__}) -- !!! FAILED CONNECTING TO MYSQL - {ex}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.debug(f"{self.__class__.__name__} ({self.disconnect.__name__}) -- CLOSED MYSQL CONNECTION")

    def execute_with_connection(self, func, *args, **kwargs):
        """
        Executes the given function with an active connection.
        Automatically opens and closes the connection.
        """
        try:
            self.connect()
            result = func(*args, **kwargs)
            return result
        finally:
            self.disconnect()

    def select_executor(self, query: str, params: list = []):
        """
        query example: SELECT * FROM table_name WHERE id IN %s AND value = %s;
        params example: [(1, 2, 3), 'a']
        """
        logger.info(f"{self.__class__.__name__} ({self.select_executor.__name__}) -- EXECUTING SELECT QUERY: {query} - PARAMS: {params}")

        data = None

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            logger.debug(f"{self.__class__.__name__} ({self.select_executor.__name__}) -- SQL RESULT: {data}")
        except Exception as ex:
            logger.exception(f"{self.__class__.__name__} ({self.select_executor.__name__}) -- !!! FAILED EXECUTING SQL QUERY - {ex}")
        finally:
            return data

    def insert_executor(self, query: str, params: list[tuple]):
        """
        query example: INSERT INTO table_name (col1, col2) VALUES (%s, %s);
        params_list example: [ ('a', 1), ('b', 2) ]
        """
        logger.info(f"{self.__class__.__name__} ({self.insert_executor.__name__}) -- EXECUTING INSERT QUERY: {query} - INSERT PARAMS: {params}")

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, params)
            self.connection.commit()
            logger.info(f"{self.__class__.__name__} ({self.insert_executor.__name__}) -- BULK INSERT SUCCESSFUL")
        except Exception as ex:
            self.connection.rollback()
            logger.exception(f"{self.__class__.__name__} ({self.insert_executor.__name__}) -- !!! FAILED INSERTION - {ex}")
        finally:
            if cursor:
                cursor.close()

    def delete_executor(self, query: str, params: list):
        """
        query example: DELETE FROM table_name WHERE id IN %s AND value = %s;
        params example: [ (1, 2, 3), 'a' ]
        """
        logger.warning(f"{self.__class__.__name__} ({self.delete_executor.__name__}) -- EXECUTING DELETE QUERY: {query} - PARAMS: {params}")

        user_answer = input("! Confirm Deletion [y / n] >> ")
        if user_answer.strip().lower() == 'y':
            cursor = None
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                self.connection.commit()
                logger.info(f"{self.__class__.__name__} ({self.delete_executor.__name__}) -- DELETE SUCCESSFUL")
            except Exception as ex:
                self.connection.rollback()
                logger.exception(f"{self.__class__.__name__} ({self.delete_executor.__name__}) -- !!! FAILED DELETION - {ex}")
            finally:
                if cursor:
                    cursor.close()
        else:
            sys.stdout.write("Aborted Deletion")


class AsyncMySQLHandler(MySQLHandler):
    """
    Async implementation of the original MySQL handler using aiomysql.
    """

    def __init__(self, database: str, user: str, password: str, host: str, port: int):
        super().__init__(database, user, password, host, port)
        self.pool = None  # aiomysql connection pool

    async def connect(self):
        try:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.database,
                autocommit=True
            )
            logger.debug(f"{self.__class__.__name__} ({self.connect.__name__}) -- CONNECTED TO MYSQL")
        except Exception as ex:
            logger.exception(f"{self.__class__.__name__} ({self.connect.__name__}) -- !!! FAILED CONNECTING TO MYSQL - {ex}")

    async def disconnect(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.debug(f"{self.__class__.__name__} ({self.disconnect.__name__}) -- CLOSED MYSQL CONNECTION")

    async def execute_with_connection(self, func, *args, **kwargs):
        """
        Executes the given function with an active connection.
        Automatically opens and closes the connection.
        """
        try:
            await self.connect()
            result = await func(*args, **kwargs)
            return result
        finally:
            await self.disconnect()

    async def select_executor(self, query: str, params: list = []):
        """
        query example: SELECT * FROM table_name WHERE id = %s AND value = %s;
        params example: [1, 'a']
        """
        logger.info(f"{self.__class__.__name__} ({self.select_executor.__name__}) -- EXECUTING SELECT QUERY: {query} - PARAMS: {params}")

        data = None

        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute(query, params)
                    data = await cursor.fetchall()
                    logger.debug(f"{self.__class__.__name__} ({self.select_executor.__name__}) -- SQL RESULT: {data}")
                except Exception as ex:
                    logger.exception(f"{self.__class__.__name__} ({self.select_executor.__name__}) -- !!! FAILED EXECUTING SQL QUERY - {ex}")
        
        return data

    async def insert_executor(self, query: str, params: list[tuple]):
        """
        query example: INSERT INTO table_name (col1, col2) VALUES (%s, %s);
        params example: [ ('a', 1), ('b', 2) ]
        """
        logger.info(f"{self.__class__.__name__} ({self.insert_executor.__name__}) -- EXECUTING INSERT QUERY: {query} - INSERT PARAMS: {params}")
        
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.executemany(query, params)
                    logger.info(f"{self.__class__.__name__} ({self.insert_executor.__name__}) -- BULK INSERT SUCCESSFUL")
                except Exception as ex:
                    logger.exception(f"{self.__class__.__name__} ({self.insert_executor.__name__}) -- !!! FAILED INSERTION - {ex}")

    async def delete_executor(self, query: str, params: list):
        """
        query example: DELETE FROM table_name WHERE id = %s AND value = %s;
        params example: [1, 'a']
        """
        logger.warning(f"{self.__class__.__name__} ({self.delete_executor.__name__}) -- EXECUTING DELETE QUERY: {query} - PARAMS: {params}")

        user_answer = input("! Confirm Deletion [y / n] >> ")
        if user_answer.strip().lower() == 'y':
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    try:
                        await cursor.execute(query, params)
                        logger.info(f"{self.__class__.__name__} ({self.delete_executor.__name__}) -- DELETE SUCCESSFUL")
                    except Exception as ex:
                        logger.exception(f"{self.__class__.__name__} ({self.delete_executor.__name__}) -- !!! FAILED DELETION - {ex}")
        else:
            sys.stdout.write("Aborted Deletion")

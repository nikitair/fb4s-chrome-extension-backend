import sys

import psycopg2

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

        self.connection = None # psycopg2 connector object

        logger.debug(f"{self.__class__.__name__} ({self.__init__.__name__}) -- CLASS INITIALIZED")


    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.database})"
    

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.database})"


    def connect(self):
        conn = None

        try:
            conn = psycopg2.connect(
                dbname=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.connection = conn
            logger.debug(f"{self.__class__.__name__} ({self.connect.__name__}) -- CONNECTED TO POSTGRES")
        except Exception as ex:
            logger.exception(f"{self.__class__.__name__} ({self.connect.__name__}) -- !!! FAILED CONNECTING TO POSTGRES - {ex}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.debug(f"{self.__class__.__name__} ({self.disconnect.__name__}) -- CLOSED POSTGRES CONNECTION")


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
             if cursor: cursor.close()

    def delete_executor(self, query: str, params: list):
        """
        query example: DELETE FROM table_name WHERE id IN %s AND value = %s;
        params example: [ (1, 2, 3), 'a' ]
        """
        logger.warning(f"{self.__class__.__name__} ({self.insert_executor.__name__}) -- EXECUTING DELETE QUERY: {query} - PARAMS: {params}")

        user_answer = input("! Confirm Deletion [y / n] >> ")
        if user_answer.strip().lower() == 'y':

            cursor = None
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                self.connection.commit()
                logger.info(f"{self.__class__.__name__} ({self.insert_executor.__name__}) -- DELETE SUCCESSFUL")

            except Exception as ex:
                self.connection.rollback()
                logger.exception(f"{self.__class__.__name__} ({self.insert_executor.__name__}) -- !!! FAILED DELETION - {ex}")

            finally:
                cursor.close()
        else:
            sys.stdout.write("Aborted Deletion")

from db.postgres.postgres_connector import PostgresConnector
# from logs.legacy_logging_config import logger
from logs.logging_config import logger

postgres_connector_obj = PostgresConnector()
connector = postgres_connector_obj.connector


class PostgresQueryHandler:

    def __init__(self) -> None:
        logger.info(f"{self.__class__.__name__} ( {self.__init__.__name__} ) -- CLASS INITIALIZED")

    @connector
    def select_executor(self, connector, query: str, params: list = []):
        logger.info(f"{self.__class__.__name__} ( {self.select_executor.__name__} ) -- EXECUTING SQL SELECT QUERY - {query} | PARAMS - {params}")
        cursor = connector.cursor()
        cursor.execute(
            query,
            params
        )
        data = cursor.fetchall()
        return data

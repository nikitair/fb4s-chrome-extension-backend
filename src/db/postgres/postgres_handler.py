from db.postgres.postgres_connector import PostgresConnector
from logs.logging_config import logger

postgres_connector_obj = PostgresConnector()
connector = postgres_connector_obj.connector


class PostgresQueryHandler:

    def __init__(self) -> None:
        logger.info(f"{self.__class__.__name__} ( {self.__init__.__name__} ) -- CLASS INITIALIZED")

    @connector
    async def select_executor(self, connector, query: str, params: list = []):
        logger.info(f"{self.__class__.__name__} ( {self.select_executor.__name__} ) -- EXECUTING SQL SELECT QUERY - {query} | PARAMS - {params}")
        cursor = await connector.cursor()
        await cursor.execute(
            query,
            params
        )
        data = await cursor.fetchall()
        return data

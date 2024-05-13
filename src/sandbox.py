import asyncio

from db.postgres.handler import PostgresQueryHandler

postgres = PostgresQueryHandler()
res = postgres.select_executor(query="SELECT * FROM fub.fub_users")
print(res)


from db.postgres.postgres_handler import PostgresQueryHandler

postgres = PostgresQueryHandler()


print(
    postgres.select_executor(query="SELECT * FROM fub.fub_users")
)


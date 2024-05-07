from db.postgres.postgres_handler import PostgresHandler

postgres = PostgresHandler(True)
postgres.ssh_tunnel_connector()
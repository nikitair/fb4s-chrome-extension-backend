from config.database import (LOCAL_PORT, POSTGRES_HOST, POSTGRES_PORT,
                             SSH_KEY_PATH, SSH_TUNNEL_MODE,
                             SSH_TUNNEL_SERVER_HOST, SSH_TUNNEL_SERVER_PORT,
                             SSH_TUNNEL_SERVER_USERNAME, postgres)

postgres.connect()

postgres.select_executor(
    query="SELECT * FROM fub.fub_users LIMIT 1"
)
postgres.disconnect()

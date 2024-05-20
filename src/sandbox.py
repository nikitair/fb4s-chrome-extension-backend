from config.database import (
    postgres, SSH_TUNNEL_MODE, SSH_KEY_PATH, SSH_TUNNEL_SERVER_HOST, SSH_TUNNEL_SERVER_PORT,
    LOCAL_PORT, SSH_TUNNEL_SERVER_USERNAME, POSTGRES_HOST, POSTGRES_PORT
    
    )


postgres.connect()


postgres.select_executor(
    query="SELECT * FROM fub.fub_users LIMIT 1"
)
postgres.disconnect()
from config.database import (
    postgres, SSH_TUNNEL_MODE, SSH_KEY_PATH, SSH_TUNNEL_SERVER_HOST, SSH_TUNNEL_SERVER_PORT,
    LOCAL_PORT, SSH_TUNNEL_SERVER_USERNAME, POSTGRES_HOST, POSTGRES_PORT
    
    )


postgres.connect(
    ssh_mode=SSH_TUNNEL_MODE,
    ssh_key_path=SSH_KEY_PATH,
    ssh_server_host=SSH_TUNNEL_SERVER_HOST,
    ssh_server_port=SSH_TUNNEL_SERVER_PORT,
    ssh_username=SSH_TUNNEL_SERVER_USERNAME,
    local_bind_address=("localhost", LOCAL_PORT),
    remote_bind_address=(POSTGRES_HOST, POSTGRES_PORT)
)


postgres.select_executor(
    query="SELECT * FROM fub.fub_users LIMIT 1"
)
postgres.disconnect()
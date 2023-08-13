import os
from pydantic_settings import BaseSettings
DEPLOY_ENV = os.getenv("DEPLOY_ENV")

class Settings(BaseSettings):
    database_hostname : str 
    database_port : str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    db_url : str

    class Config:
        if DEPLOY_ENV == "RENDER":
            env_file = "/etc/secrets/.env"
        else:
            env_file = "app/.env"


settings = Settings()
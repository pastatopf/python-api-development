from pydantic import BaseSettings

# Model to check if all needed environment parameters are set


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()

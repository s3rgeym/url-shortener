from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = "postgres"
    db_user: str = "docker"
    db_pass: str = "secret"
    db_name: str = "docker"
    db_port: int = 5432


settings = Settings()

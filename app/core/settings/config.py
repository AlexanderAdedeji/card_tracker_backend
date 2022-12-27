from fastapi import Path
from pydantic import BaseSettings
from pathlib import Path
import os


class AppSettings(BaseSettings):
    APP_Name:str
    DATABASE_NAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_USERNAME: str
    DATABASE_HOSTNAME:str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int
    LASRRA_IDENTITY_API: str
    LASRRA_CARD_TRACKING_API: str
    JWT_TOKEN_PREFIX:str
    HEADER_KEY:str
    RESET_TOKEN_EXPIRE_MINUTES:int

    class Config:
        env_file = os.getenv(
            "ENV_VARIABLE_PATH", Path(__file__).parent / "./env_files/.env"
        )


settings =AppSettings()
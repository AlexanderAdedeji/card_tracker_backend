from typing import List
from pydantic import AnyHttpUrl, validator
from pydantic import  EmailStr
from pydantic_settings import BaseSettings

import os
from pathlib import Path
from pydantic import validator
from starlette.datastructures import CommaSeparatedStrings



class Settings(BaseSettings):
    API_V1_STR: str
    PROJECT_NAME: str
    API_URL_PREFIX:str
    DEBUG:bool
    DEVELOPMENT_DATABASE_URL:str
    PRODUCTION_DATABASE_URL:str
    LASRRA_IDENTITY_API: str
    LASRRA_CARD_TRACKING_API: str
    SECRET_KEY:str
    RESET_TOKEN_EXPIRE_MINUTES:int
    JWT_EXPIRE_MINUTES:int
    JWT_ALGORITHM:str
    JWT_TOKEN_PREFIX:str
    HEADER_KEY:str
    ADMIN_USER:str
    REGULAR_USER:str



    class Config:
        env_file = os.getenv(
            "ENV_VARIABLE_PATH", Path(__file__).parent / "env_files" / ".env"
        )


settings = Settings()





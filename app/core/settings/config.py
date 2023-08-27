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




    class Config:
        env_file = os.getenv(
            "ENV_VARIABLE_PATH", Path(__file__).parent / "env_files" / ".env"
        )


settings = Settings()





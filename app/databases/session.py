from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.settings.config import settings


# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
SQLALCHEMY_DATABASE_URL= f"postgresql://cardportalapi_admin@card-portal-api-server:CardTrackingPortal2022@card-portal-api-server.postgres.database.azure.com:{settings.DATABASE_PORT}/card-portal-api-db"




engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

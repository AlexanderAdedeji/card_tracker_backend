from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings.config import settings


DATABASE_URL = (
    #  "sqlite:///./sql_app.db"
    f"postgresql+psycopg2://"
    f"identikoPostgresSqlDevAdmin@identiko-postgres-dev-server:"
    f"Cheaters2026.@"
    f"identiko-postgres-dev-server.postgres.database.azure.com:"
    f"5432/Eaffidavit"
)


def create_database_engine():
    # if settings.DEBUG:
    #     url = settings.DEVELOPMENT_DATABASE_URL
    # else:
    #     url = settings.PRODUCTION_DATABASE_URL
    return create_engine(DATABASE_URL, pool_pre_ping=True)


engine = create_database_engine()


def create_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = create_session()

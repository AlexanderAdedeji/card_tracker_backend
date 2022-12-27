from app.commonLib.models import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class CardInfo(Base):
    __tablename__ = "card_info"
    id = Column(Integer, primary_key=True, nullable=False)
    lassra_id = Column(Integer, unique=True, nullable=False)
    card_status = Column(String, nullable=False)
    status_description = Column(String, nullable=False)

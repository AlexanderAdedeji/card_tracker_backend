from sqlalchemy import Column, Integer, String
from app.commonLib.models import Base


class LocalGovernments(Base):
    __tablename__ = "local_governments"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True, index=True)

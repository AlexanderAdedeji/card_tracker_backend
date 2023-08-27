from sqlalchemy import Column, Integer, String
from app.commonLib.models.base_class import Base

class LocalGovernment(Base):
    """
    Represents local governments with unique codes.
    """

    __tablename__ = "local_governments"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), nullable=False)
    code = Column(String(length=50), nullable=False, unique=True, index=True)

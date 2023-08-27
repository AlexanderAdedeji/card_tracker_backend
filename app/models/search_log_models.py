from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.commonLib.models.base_class import Base


class SearchLog(Base):
    __tablename__ = "search_logs"
    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    lasrra_id = Column(String, nullable=True)

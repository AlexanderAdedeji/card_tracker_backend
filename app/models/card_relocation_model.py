from app.commonLib.models.base_class import Base
from sqlalchemy import Column, Integer, String


class CardRelocation(Base):

    __tablename__ = "card_relocation"

    id = Column(Integer, primary_key=True, index=True)
    source_local_government_code = Column(String(length=50), nullable=False)
    source_collection_center_code = Column(String(length=50), nullable=False)
    destination_local_government_code = Column(String(length=50), nullable=False)
    destination_collection_center_code = Column(String(length=50), nullable=False)

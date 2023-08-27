from app.commonLib.models.base_class import Base
from sqlalchemy import Column, Integer, String


class CardDelivery(Base):

    __tablename__ = "card_delivery"

    id = Column(Integer, primary_key=True, index=True)
    source_local_government_code = Column(String(length=50), nullable=False)
    source_collection_center_code = Column(String(length=50), nullable=False)
    delivery_address = Column(String(length=50), nullable=False)
    payment_transaction_ref = Column(String(length=50), nullable=False)
    delivery_status= Column(String, nullable=False)

from app.commonLib.models import Base
from sqlalchemy import Column, Integer, String


class CollectionCentre(Base):
    """
    Represents collection centres associated with local government codes.
    """

    __tablename__ = "collection_centres"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(length=50), nullable=False, index=True)
    name = Column(String(length=255), nullable=False, unique=True)
    local_govt_code = Column(String(length=50), nullable=False)

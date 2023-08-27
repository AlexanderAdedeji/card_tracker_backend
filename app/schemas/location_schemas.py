from pydantic import BaseModel
from app.commonLib.schemas.response_model import ResponseWrapper

class LocalGovernmentModel(BaseModel):
    """
    Represents a local government entity.
    """
    name: str
    code: str

class CollectionCentreModel(LocalGovernmentModel):
    """
    Represents a collection centre entity.
    """
    local_govt_code: str


class LocalGovernmentResponse(ResponseWrapper[LocalGovernmentModel]):
    pass

from pydantic import BaseModel

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

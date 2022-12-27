from pydantic import BaseModel





class LocalGovt(BaseModel):
    id:int
    name:str
    code:str


class CollectionCentre(LocalGovt):
    local_govt_code:str

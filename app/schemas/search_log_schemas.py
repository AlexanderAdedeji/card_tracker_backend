from pydantic import BaseModel




class SearchLogBase(BaseModel):
    lasrra_id:str
    ip_address:str


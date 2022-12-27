import email
import string
from typing import List, Optional
from pydantic import BaseModel



class User(BaseModel):
    first_name:str
    last_name:str
    email:str



class FullUser(User):
    is_active:str
    

class UserCreate(User):
    password:str
    


class UserLogin(BaseModel):
    email:str
    password:str

    
class UserValidated(BaseModel):
    first_name:str
    last_name:str
    token:str
    
class DisplayUser(User):
    id:int
    is_active:bool

class ResetUserPassword(BaseModel):
    id:int
    passwordStr:str
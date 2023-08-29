from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  # This will validate the email format
    role: str

class UserCreateForm(UserBase):
    password: str = Field(..., min_length=8, description="Password with a minimum length of 8 characters")


class UserLogin(BaseModel):
    email :EmailStr
    passwword:str


class UserValidated(UserBase):
    token:str

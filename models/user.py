from pydantic import BaseModel, Field
from typing import List

class User(BaseModel):
    email: str
    

class UserCreate(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="securepassword123")

class AllUsers(BaseModel):
    listOfEmail: List[User]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
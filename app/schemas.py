from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    mobile_number : int

class UserRead(BaseModel):
    id: int
    email: str
    mobile_number : Optional[int]

class Token(BaseModel):
    access_token: str
    token_type: str

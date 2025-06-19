from pydantic import BaseModel
from typing import Optional,List

class UserCreate(BaseModel):
    email: str
    password: str
    mobile_number : int
    role : List[str]

class UserRead(BaseModel):
    id: int
    email: str
    mobile_number : Optional[int]

class Token(BaseModel):
    access_token: str
    token_type: str

class RolemasterCrete(BaseModel):
    name : str
    description : Optional[str] = None 

class RolemasterRead(RolemasterCrete):
    id : int

class RolemapRead(BaseModel):
    id : int 
    user : UserRead
    rolemaster : RolemasterRead


from sqlmodel import SQLModel, Field,String,Column,Integer
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mobile_number : int = Field(sa_column=Column("mobile_number",Integer,nullable=True))
    email: str = Field(index=True, unique=True)
    hashed_password: str

class RoleMaster(SQLModel, table=True):
    id : Optional[int]  = Field(default=None,primary_key=True)
    name : str = Field(sa_column=Column("name",String,nullable=False,unique=True))
    description : str = Field(sa_column=Column("description",String,nullable=True))

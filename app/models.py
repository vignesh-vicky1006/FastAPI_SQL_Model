from sqlmodel import SQLModel, Field,String,Column,Integer,Relationship
from sqlalchemy import ForeignKey
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    mobile_number : int = Field(sa_column=Column("mobile_number",Integer,nullable=True))
    email: str = Field(index=True, unique=True)
    hashed_password: str

    role_mapping : Optional["Rolemapping"] = Relationship(back_populates="user")

class RoleMaster(SQLModel, table=True):
    __tablename__ = "rolemaster"

    id : Optional[int]  = Field(default=None,primary_key=True)
    name : str = Field(sa_column=Column("name",String,nullable=False,unique=True))
    description : str = Field(sa_column=Column("description",String,nullable=True))

    role_mapping : Optional["Rolemapping"] = Relationship(back_populates="rolemaster")

class Rolemapping(SQLModel,table=True):
    __tablename__ = "rolemap"

    id : Optional[int]  = Field(default=None,primary_key=True)
    user_id : int = Field(sa_column=Column("user_id",Integer,ForeignKey("users.id"),nullable=True))
    rolemaster_id : int = Field(sa_column=Column("rolemaster_id",Integer,ForeignKey("rolemaster.id"),nullable=True))

    user : Optional["User"] =Relationship(back_populates="role_mapping")
    rolemaster : Optional["RoleMaster"] = Relationship(back_populates="role_mapping")
    

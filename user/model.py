from sqlalchemy import Column, Integer, String,create_engine
from sqlalchemy.orm import declarative_base,relationship
from pydantic import BaseModel,EmailStr
from enum import Enum


engine =create_engine('postgresql://postgres:123456@localhost/postgres')
Base=declarative_base()



class User(Base):
    __tablename__='users'

    user_id =Column(Integer,primary_key =True,autoincrement =True)
    email=Column(String(50),nullable=False,unique=True)
    password=Column(String(50),nullable=False)
    name=Column(String(10),nullable=False)
    surname =Column(String(10),nullable=False)
    user_type=Column(String(10),nullable=False)



class UserEnumStr (str,Enum):
    Student="Student"
    Personel="Personel"

class UserPydantic(BaseModel):
    email:str # bu tanımlama e mail yapısında olacağını belirtir
    password:str
    name:str
    surname:str
    user_type:UserEnumStr




    class Config:
        from_attributes = True

Base.metadata.create_all(engine)

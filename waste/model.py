from sqlalchemy import Column,create_engine,Integer,String,ForeignKey,Enum as SQLAlchemyEnum,DateTime
from sqlalchemy.orm import declarative_base,relationship
from pydantic import BaseModel,EmailStr
from datetime import date,datetime
from enum import Enum



engine=create_engine ('postgresql://postgres:123456@localhost/postgres') #veritabanına bağlanmak için bir veritabanı motoru oluşturur.
Base=declarative_base() #orm modellerinin türetilmesi için temel class oluşturmaya yarar.

class User(Base):
    __tablename__='users'

    user_id =Column(Integer,primary_key =True,autoincrement =True)
    email=Column(String(50),nullable=False,unique=True)
    password=Column(String(50),nullable=False)
    name=Column(String(10),nullable=False)
    surname =Column(String(10),nullable=False)
    user_type=Column(String(10),nullable=False)
    waste_1 = relationship('Waste', back_populates='user')



class UserEnumStr (str,Enum):
    Student="Student"
    Personel="Personel"

class UserPydantic(BaseModel):
    email:EmailStr # bu tanımlama e mail yapısında olacağını belirtir
    password:str
    name:str
    surname:str
    user_type:UserEnumStr


class WasteType(Base):
    __tablename__ = 'waste_type'

    waste_type_id = Column(Integer, primary_key=True,autoincrement=True)
    waste_type_name = Column(String)



class WasteTypePydantic(BaseModel):
    waste_type_name:str

class BuildingTypes(Base):
    __tablename__ = 'building_types'

    building_types_id = Column(Integer, primary_key=True, autoincrement=True)
    building_types_name = Column(String(100), nullable=False)

    build = relationship('Building', back_populates='building_type')
class Building(Base):
    __tablename__ = 'buildings'

    building_id = Column(Integer, primary_key=True, autoincrement=True)
    building_name = Column(String(100), nullable=False)
    building_types_id = Column(Integer, ForeignKey('building_types.building_types_id'), nullable=False)

    building_type = relationship('BuildingTypes', back_populates='build')
    waste = relationship('Waste', back_populates='building')


class BuildingPydantic(BaseModel):
    building_name: str
    building_type_id: int



class Waste(Base):
    __tablename__='waste'

    waste_id=Column (Integer,primary_key=True,autoincrement=True)
    building_id=Column (Integer,ForeignKey('buildings.building_id'),nullable=False)
    user_id=Column(Integer,ForeignKey('users.user_id'),nullable=False)
    quantity=Column(Integer,nullable=False)
    waste_type_id=Column (Integer,ForeignKey('waste_type.waste_type_id'),nullable=False)
    record_date=Column(DateTime,nullable=False, default=datetime.now)  # Varsayılan değer eklendi

    building=relationship('Building',back_populates='waste')
    user =relationship('User',back_populates='waste_1')
    waste_type = relationship('WasteType')  # WasteType ile ilişkiyi ekledik.


class WastePydantic(BaseModel):
    building_id : int
    user_id : int
    quantity : int
    waste_type_id:int
    record_date:datetime

    class Config:
        from_attributes = True #orm modellemesi için bu class yapısı kullanıldı bize pydantic modellemesinde kolaylık sağladı

Base.metadata.create_all(engine) #tanımlanan tüm modelleri veritabanında oluşturur.

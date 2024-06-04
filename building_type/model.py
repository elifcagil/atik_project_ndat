from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base ,relationship
from pydantic import BaseModel


engine = create_engine ('postgresql://postgres:123456@localhost/postgres')
Base = declarative_base()



class BuildingTypes(Base):
    __tablename__='building_types'

    building_types_id = Column(Integer,primary_key=True,autoincrement=True)
    building_types_name=Column(String(100),nullable=False)


class BuildingTypesPydantic(BaseModel):
    building_type_name:str

    class Config:
        from_attributes = True



Base.metadata.create_all(engine)

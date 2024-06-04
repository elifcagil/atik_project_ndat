from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base ,relationship
from pydantic import BaseModel


engine = create_engine ('postgresql://postgres:123456@localhost/postgres')
Base = declarative_base()



class WasteType(Base):
    __tablename__ = 'waste_type'

    waste_type_id = Column(Integer, primary_key=True,autoincrement=True)
    waste_type_name = Column(String)



class WasteTypePydantic(BaseModel):
    waste_type_name:str

    class Config:
        from_attributes = True



Base.metadata.create_all(engine)

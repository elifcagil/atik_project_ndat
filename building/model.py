from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel

engine = create_engine('postgresql://postgres:123456@localhost/postgres')
Base = declarative_base()


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


class BuildingPydantic(BaseModel):
    building_name: str
    building_types_id: int

    class Config:
        from_attributes = True

Base.metadata.create_all(engine)
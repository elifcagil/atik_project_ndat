from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import create_engine
from building_type.model import BuildingTypesPydantic,BuildingTypes


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)
router=APIRouter()

def get_db():
    db = SessionLocal() #Oturum Başlatma
    try:
        yield db #Oturumun Kullanıma Sunulması
    finally:
        db.close() #Oturumun Kapatılması



@router.post("/add_building_type",response_model=BuildingTypesPydantic)
async def add_building_type(building_types:BuildingTypesPydantic,db: Session = Depends(get_db)):
    db_building_type=BuildingTypes(**building_types.dict())
    db.add(db_building_type)
    db.commit()
    db.refresh(db_building_type)
    return db_building_type



@router.delete("/delete_building_type",response_model=BuildingTypesPydantic)
async def delete_building_type(building_types_id:int,db: Session = Depends(get_db)):
    db_building_type=db.query(BuildingTypes).filter(BuildingTypes.building_types_id  == building_types_id).first()
    if db_building_type is None:
        raise HTTPException(status_code=404,detail="Building type not found")

    db.delete(db_building_type)
    db.commit()
    return db_building_type


@router.get("/building_types/", response_model=list[BuildingTypesPydantic])
async def get_building_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    building_types = db.query(BuildingTypes).offset(skip).limit(limit).all()
    return building_types
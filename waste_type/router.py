from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import create_engine
from waste_type.model import WasteTypePydantic,WasteType


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)
router = APIRouter(
    tags=["Waste Type Enpoints"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = SessionLocal() #Oturum Başlatma
    try:
        yield db #Oturumun Kullanıma Sunulması
    finally:
        db.close() #Oturumun Kapatılması



@router.post("/add_waste_type",response_model=WasteTypePydantic)
async def add_waste_type(waste_type:WasteTypePydantic,db: Session = Depends(get_db)):
    db_waste_type=WasteType(**waste_type.dict())
    db.add(db_waste_type)
    db.commit()
    db.refresh(db_waste_type)
    return db_waste_type



@router.delete("/delete_waste_type",response_model=WasteTypePydantic)
async def delete_waste_type(waste_type_id:int,db: Session = Depends(get_db)):
    db_waste_type=db.query(WasteType).filter(WasteType.waste_type_id  == waste_type_id).first()
    if db_waste_type is None:
        raise HTTPException(status_code=404,detail="Building type not found")

    db.delete(db_waste_type)
    db.commit()
    return db_waste_type


@router.get("/waste_types/", response_model=list[WasteTypePydantic])
async def get_waste_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_waste_type = db.query(WasteType).offset(skip).limit(limit).all()
    return db_waste_type
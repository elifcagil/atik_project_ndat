from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session ,sessionmaker
from sqlalchemy import create_engine
from typing import List
from waste.model import Waste,WastePydantic
from datetime import datetime
from waste_type.model import WasteType
from building.model import Building
from user.model import User
from waste.model import Waste


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


router = APIRouter(    #endpointleri gruplamak için burada açıklama ekliyoruz.
    tags=["Waste Enpoints"],
    responses={404: {"description": "Not found"}},
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/waste/", response_model=WastePydantic)
def create_waste(waste: WastePydantic, db: Session = Depends(get_db)):
    # Veri geçerliliği kontrolü
    if waste.quantity <= 0 or waste.quantity > 1000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Miktar 0 ile 1000 arasında olmalıdır.")
    waste_type = db.query(WasteType).filter(WasteType.waste_type_id == waste.waste_type_id).first()
    if not waste_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Belirtilen atık türü bulunamadı.")

    # Building ID kontrolü
    building = db.query(Building).filter(Building.building_id == waste.building_id).first()
    if not building:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Belirtilen bina bulunamadı.")

    # User ID kontrolü
    user = db.query(User).filter(User.user_id == waste.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Belirtilen kullanıcı bulunamadı.")

    # Yukarıdaki kontrollerden geçildiğinde, yeni atık oluşturulabilir.
    db_waste = Waste(**waste.dict())
    db.add(db_waste)
    db.commit()
    db.refresh(db_waste)

    # Değişiklikleri kaydettikten sonra record_date alanını atıyoruz
    db_waste.record_date = datetime.now()
    db.commit()

    return db_waste


@router.put("/waste/{waste_id}", response_model=WastePydantic)
def update_waste(waste_id: int, waste: WastePydantic, db: Session = Depends(get_db)):
    # Belirtilen atık ID'sine sahip atığı veritabanında bul
    db_waste = db.query(Waste).filter(waste_id == Waste.waste_id).first()
    if not db_waste:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Belirtilen atık bulunamadı.")

    # Veri geçerliliği kontrolü
    if waste.quantity <= 0 or waste.quantity > 1000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Miktar 0 ile 1000 arasında olmalıdır.")
    building = db.query(Building).filter(Building.building_id == waste.building_id).first()
    if not building:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Belirtilen bina bulunamadı.")

    # User ID kontrolü
    user = db.query(User).filter(User.user_id == waste.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Belirtilen kullanıcı bulunamadı.")

    # Waste Type ID kontrolü
    waste_type = db.query(WasteType).filter(WasteType.waste_type_id == waste.waste_type_id).first()
    if not waste_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Belirtilen atık türü bulunamadı.")
    # Yukarıdaki kontrollerden geçildiğinde, atığı güncelle
    for key, value in waste.dict().items():
        setattr(db_waste, key, value)

    db.add(db_waste)
    db.commit()
    db.refresh(db_waste)

    # Değişiklikleri kaydettikten sonra record_date alanını atıyoruz
    db_waste.record_date = datetime.now()
    db.commit()

    return db_waste


@router.delete("/waste/{waste_id}", response_model=WastePydantic)
def delete_waste(waste_id: int, db: Session = Depends(get_db)):
    db_waste = db.query(Waste).filter(Waste.waste_id == waste_id).first()
    if not db_waste:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atık bulunamadı")

    db.delete(db_waste)
    db.commit()
    return db_waste




@router.get("/get_wastes/", response_model=list[WastePydantic])
async def get_wastes(skip: int=0,limit:int=100,db: Session = Depends(get_db)):
    db_waste = db.query(Waste).offset(skip).limit(limit).all()
    return db_waste


@router.get("/waste/by_type/{waste_type_id}", response_model=List[WastePydantic])
def get_waste_by_type(waste_type_id: int, db: Session = Depends(get_db)):
    wastes = db.query(Waste).filter(Waste.waste_type_id == waste_type_id).all()
    if not wastes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Belirtilen atık türüne ait atık bulunamadı")

    return wastes


@router.get("/waste/by_building/{building_id}", response_model=List[WastePydantic])
def get_waste_by_building(building_id: int, db: Session = Depends(get_db)):
    wastes = db.query(Waste).filter(Waste.building_id == building_id).all()
    if not wastes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Belirtilen binaya ait atık bulunamadı")

    return wastes


@router.get("/waste/by_user/{user_id}", response_model=List[WastePydantic])
def get_waste_by_user(user_id: int, db: Session = Depends(get_db)):
    wastes = db.query(Waste).filter(Waste.user_id == user_id).all()
    if not wastes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Belirtilen kullanıcıya ait atık bulunamadı")

    return wastes










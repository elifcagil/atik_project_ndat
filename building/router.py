from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from fastapi import APIRouter,Depends,HTTPException,status
from .model import BuildingPydantic,Building
from pydantic import BaseModel,Field
from enum import Enum
from starlette import status





SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)  #veri tabanına kaydetme işlemi otomatik olarak yapılmaz.commit() i çağırmamzı gerekir
 #sessionlocal yeni bir veri tabanı oturumu(session) oluşturur..
#sessionmaker fonksiyonunun içinde temel veritabanı bağlantısı ve oturumun nasıl davrancağını belirtirirz


router = APIRouter(
    tags=["Building Enpoints"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal() #Oturum Başlatma
    try:
        yield db #Oturumun Kullanıma Sunulması
    finally:
        db.close() #Oturumun Kapatılması




@router.get("/buildings/", response_model=list[BuildingPydantic])
async def get_buildings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    building = db.query(Building).offset(skip).limit(limit).all()
    return building


@router.post("/add_building", response_model=BuildingPydantic)
async def add_building(buildings:BuildingPydantic, db: Session = Depends(get_db)):
    try:
        # Yeni bina oluşturma
        db_building = Building(**buildings.dict())
        db.add(db_building)
        db.commit()
        db.refresh(db_building)
        return db_building
    except Exception as e:
        db.rollback() #try bloğunda hata gerçekleşirse yapılan değişiklerş geri almamızı sağlar
        raise HTTPException(status_code=500, detail=str(e))





class UpdateBuildingPydantic(BaseModel): #kullanıcıdan sadece building_types_id alacağımı için ekstra olarak bir pydantic modeli belirledik
    building_types_id: int

    class Config:
        from_attributes = True

@router.put("/update_building/{building_name}", response_model=BuildingPydantic)
async def update_building(building_name: str, update_data: UpdateBuildingPydantic, db: Session = Depends(get_db)): #update_data:YpdateBuildingPydantic olarak tanımladık çünkü değişmesini istediğimiz verileri bu şekilde tanımladık
    db_building = db.query(Building).filter(Building.building_name == building_name).first()
    if db_building is None:
        raise HTTPException(status_code=404, detail="Building not found")

    db_building.building_types_id = update_data.building_types_id #mevcut bina type ına update_data nesnesinden geleni atadık
    db.commit()
    db.refresh(db_building)  # Güncellenen veriyi veritabanından yeniden yükleyin
    return BuildingPydantic.from_orm(db_building)


@router.delete("/delete_building/{building_id}")
async def delete_building(building_id: int, db: Session = Depends(get_db)):
    db_building = db.query(Building).filter(Building.building_id == building_id).first()
    if db_building is None:
        raise HTTPException(status_code=404, detail="Building not found")

    db.delete(db_building)
    db.commit()
    return {"message": "Building deleted successfully"}
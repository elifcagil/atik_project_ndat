from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,EmailStr

import user.model
from .model import UserPydantic,User,UserEnumStr
from sqlalchemy.orm import Session ,sessionmaker
from sqlalchemy import create_engine
from typing import List



SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


router=APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/", response_model = list[UserPydantic]) #referans aldığımız modelden gelen her veri listenin içinde tutuluyor
def get_users (skip: int = 0, limit: int = 10, db: SessionLocal = Depends(get_db)): #skip ve limit veri tabanından alınacak kişilerin sayısını ve aralığını bildirir arada kaç kişi olacağını bildirir
    users = db.query(User).offset(skip).limit(limit).all() #students değişkenine skip ve limit değerleri sınıflandırılarak atanır(aall ile hepsi demek)
    return users #filtrelediğimiz öğrencileri atadığımız değişkeni geri döndürür.

@router.get ("/user/{user_id}",response_model =UserPydantic)
async def get_user_id(user_id:int,db:Session =Depends(get_db)):
    db_user =db.query (User).filter(User.user_id==user_id).first() #.first() sorguda verdiğimiz değerin ilk eşleştiği nesneyi döndürür burada id unique değer olduğu için ilk eşleşen tek olacaktır.
    if db_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    return db_user

#.one() bize tek bir sonuç döndürecektir eğer birden fazla sonuç varsa veya hiç sonuç yoksa hata mesajıyla birlikte fırlatır
#.scalar() sonucun tek bir skaler bir değer döndürmesi gerektiğini söyler. filtrelediğimiz tabloda filtrelediğimiz şeyin tabloda kaç adet bulunduğunu mesela.birlikte kullanılan bağımlılıklar vardır.
#.count() kaç adet eşleşen değer olduğunu döndürür int döndürür
@router.get("/user/user_type/{user_type}",response_model=List[UserPydantic]) #/user_type/{user_type} diye path i belirtmek önemli belirtmediğimizde veri türünü farklı anlayabilir
async def get_user_user_type(user_type:UserEnumStr,db:Session =Depends(get_db)):
    db_user=db.query (User).filter(User.user_type == user_type).all() #.all() sorgudan dönen tüm sonuçları yani type ın eşleştiği her değeri nesnelerin listesini verir
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user


@router.post("/add_user/", response_model=UserPydantic)
async def add_user(user: UserPydantic, db: Session = Depends(get_db)):
    db_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        surname=user.surname,
        user_type=user.user_type.value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


class DeletedUser(BaseModel):
    user_id:int
    email:EmailStr
    password:str
    name:str
    surname:str
    user_type:UserEnumStr

@router.delete("/user_delete/{user_id}",response_model=DeletedUser)
async def delete_user(user_id:int,db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail="student not found")


    db.delete(db_user)
    db.commit()
    return db_user


@router.put("/user_update/{user_id}",response_model=UserPydantic)
async def update_user(user_id:int, user : UserPydantic,db:Session =Depends(get_db)):
    db_user = db.query(User).filter(User.user_id ==user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found")

    for attr,value in vars(user).items(): #vars() fonksiyonu, student objesinin özelliklerini bir sözlük olarak döndürür
        setattr(db_user, attr, value) #bu özelliklerin herbirini (attr) alır ve karşılık gelen değeri (value) setattr() fonksiyonu ile ilgili öğrenci kaydına (db_student) atar.
        #student parametresinde gelen yeni öğrenci bilgilerini, veritabanındaki öğrenci kaydına (db_student) uygular.
    db.commit()
    return db_user
from fastapi import FastAPI
from user.router import router as user_route
from building.router import router as building_route
from building_type.router import router as building_type_route
from waste_type.router import router as waste_type_route



app=FastAPI()

app.include_router(user_route,prefix="/api")
app.include_router(building_route,prefix="/api")
app.include_router(building_type_route,prefix="/api")
app.include_router(waste_type_route,prefix="/api")
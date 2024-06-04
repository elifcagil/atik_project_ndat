from fastapi import FastAPI
from user.router import router as user_route
from building.router import router as building_route



app=FastAPI()

app.include_router(user_route,prefix="/api")
app.include_router(building_route,prefix="/api")
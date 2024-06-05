from fastapi import FastAPI
from user.router import router as user_route
from building.router import router as building_route
from building_type.router import router as building_type_route
from waste_type.router import router as waste_type_route
from waste.router import router as waste_route



from fastapi import FastAPI

app = FastAPI(
    title="WASTE PROJECT API",  #başlangıç sayfasında bilgi vermek için description="This is a very fancy project, with auto docs for the API and everything.") başlıklarık ullanılarak açıklama ve version da eklenebilir
    version="2.5.0",
)


app.include_router(user_route,prefix="/api")
app.include_router(building_route,prefix="/api")
app.include_router(building_type_route,prefix="/api")
app.include_router(waste_type_route,prefix="/api")
app.include_router(waste_route,prefix="/api")
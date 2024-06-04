from fastapi import FastAPI
from user.router import router as user_route



app=FastAPI()

app.include_router(user_route,prefix="/api")
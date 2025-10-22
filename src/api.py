from src.auth.controllers import router as auth_router
from fastapi import FastAPI

def register_routes(app:FastAPI):
    app.include_router(auth_router)
from src.auth.controllers import router as auth_router
from src.route.controllers import router as route_router
from src.partner.controllers import router as partner_router
from fastapi import FastAPI

def register_routes(app:FastAPI):
    app.include_router(auth_router)
    app.include_router(route_router)
    app.include_router(partner_router)
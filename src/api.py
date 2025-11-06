from src.services.partner_service.controllers import router as partner_router
from src.services.driver_service.controllers import router as driver_router
from src.services.route_service.controllers import router as route_router
from fastapi import FastAPI

def register_routes(app:FastAPI):
    app.include_router(partner_router)
    app.include_router(driver_router)
    app.include_router(route_router)
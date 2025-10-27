from src.auth.controllers import router as auth_router
from src.route_service.controllers import router as route_router
from src.partner_service.controllers import router as partner_router
from src.driver_service.controllers import router as driver_router
from src. partner_payout_service.controllers import router as partner_payout_router
from fastapi import FastAPI

def register_routes(app:FastAPI):
    app.include_router(auth_router)
    app.include_router(route_router)
    app.include_router(partner_router)
    app.include_router(driver_router)
    app.include_router(partner_payout_router)
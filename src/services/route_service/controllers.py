from fastapi import APIRouter, Depends, status, Query
from . import services as route_service
from . import models 
from src.database.core import DbSession

router = APIRouter(
    prefix="/routes",
    tags=["routes"]
)

# buat rute baru
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=None)
async def create_route(
    data: models.RequestCreateNewRoute,
    db: DbSession
):
    return route_service.create_new_route(data, db)

# update rute
@router.put("/{route_id}", status_code=status.HTTP_200_OK,response_model=None)
def update_route(
    route_id: int,
    data: models.RequestUpdateRoute,
    db: DbSession
):
    return route_service.update_route(route_id, data, db)


# hapus rute
@router.delete("/{route_id}", status_code=status.HTTP_200_OK,response_model=None)
async def delete_route(
    route_id: int,
    db: DbSession
):
    return route_service.delete_route(route_id, db)

# ambil spesifik rute
@router.get("/{route_id}", status_code=status.HTTP_200_OK,response_model=None)
async def get_route(
    route_id: int,
    db: DbSession
):
    return route_service.get_route(route_id, db)


# ambil semua rute
@router.get("/", status_code=status.HTTP_200_OK,response_model=None)
async def get_all_routes(
    db: DbSession,
    q: str = Query("", description="Cari rute berdasarkan nama")
):
    return route_service.get_all_routes(db=db, q=q)
from fastapi import APIRouter, Depends, status, Query
from . import services as driver_service
from . import models 
from src.database.core import DbSession

router = APIRouter(
    prefix="/drivers",
    tags=["drivers"]
)

# buat driver baru
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=None)
async def create_driver(
    data: models.RequestCreateNewDriver,
    db: DbSession
):
    return driver_service.create_new_driver(data, db)

# update driver
@router.put("/{driver_id}", status_code=status.HTTP_200_OK,response_model=None)
def update_driver(
    driver_id: int,
    data: models.RequestUpdateDriver,
    db: DbSession
):
    return driver_service.update_driver(driver_id, data, db)


# hapus driver
@router.delete("/{driver_id}", status_code=status.HTTP_200_OK,response_model=None)
async def delete_driver(
    driver_id: int,
    db: DbSession
):
    return driver_service.delete_driver(driver_id, db)

# ambil spesifik driver
@router.get("/{driver_id}", status_code=status.HTTP_200_OK,response_model=None)
async def get_driver(
    driver_id: int,
    db: DbSession
):
    return driver_service.get_driver(driver_id, db)


# ambil semua driver
@router.get("/", status_code=status.HTTP_200_OK,response_model=None)
async def get_all_drivers(
    db: DbSession,
    q: str = Query("", description="Cari supir berdasarkan nama")
):
    return driver_service.get_all_drivers(db=db, q=q)
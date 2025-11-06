from fastapi import APIRouter, Depends, status, Query
from . import services as partner_service
from . import models 
from src.database.core import DbSession

router = APIRouter(
    prefix="/partners",
    tags=["Partners"]
)

# buat partner baru
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=None)
async def create_partner(
    data: models.RequestCreateNewPartner,
    db: DbSession
):
    return partner_service.create_new_partner(data, db)

# update partner
@router.put("/{partner_id}", status_code=status.HTTP_200_OK,response_model=None)
def update_partner(
    partner_id: int,
    data: models.RequestUpdatePartner,
    db: DbSession
):
    return partner_service.update_partner(partner_id, data, db)


# hapus partner
@router.delete("/{partner_id}", status_code=status.HTTP_200_OK,response_model=None)
async def delete_partner(
    partner_id: int,
    db: DbSession
):
    return partner_service.delete_partner(partner_id, db)


# tambah fee
@router.patch("/fee/increase", status_code=status.HTTP_200_OK,response_model=None)
async def increase_fee(
    data: models.RequestUpdateFeePartner,
    db: DbSession
):
    return partner_service.increase_fee(data, db)


# kurangi fee
@router.patch("/fee/decrease", status_code=status.HTTP_200_OK,response_model=None)
async def decrease_fee(
    data: models.RequestUpdateFeePartner,
    db: DbSession
):
    return partner_service.decrease_fee(data, db)


# ambil spesifik partner
@router.get("/{partner_id}", status_code=status.HTTP_200_OK,response_model=None)
async def get_partner(
    partner_id: int,
    db: DbSession
):
    return partner_service.get_partner(partner_id, db)


# ambil semua partner
@router.get("/", status_code=status.HTTP_200_OK,response_model=None)
async def get_all_partners(
    db: DbSession,
    q: str = Query("", description="Cari mitra berdasarkan nama")
):
    return partner_service.get_all_partners(db=db, q=q)
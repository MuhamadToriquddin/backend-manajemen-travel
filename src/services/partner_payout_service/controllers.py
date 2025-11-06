from src.rate_limiting import limiter
from src.database.core import DbSession
from fastapi import APIRouter,Request,Path
from starlette import status
from . import services
from . import models
from uuid import UUID

router = APIRouter(prefix="/partner-payout",tags=["Partner Payout"])

@router.get("/",status_code=status.HTTP_200_OK)
@limiter.limit("50/hour")
async def get_all_partner_payouts(request:Request,db:DbSession):
    partner_payouts = services.get_all_partner_payouts(db=db)
    return partner_payouts

@router.post("/",status_code=status.HTTP_201_CREATED)
@limiter.limit("50/hour")
async def create_new_partner_payout(request:Request,db:DbSession,form_data:models.RequestCreateNewPartnerPayout):
    partner_payout_info = services.create_new_partner_payout(db=db,form_data=form_data)
    return partner_payout_info

@router.delete("/{partner_payout_id}",status_code=status.HTTP_201_CREATED)
@limiter.limit("20/hour")
async def delete_partner_payout(request:Request,db:DbSession,partner_payout_id:UUID=Path(...)):
    deleted_partner = services.delete_partner_payout(db=db,partner_payout_id=partner_payout_id)
    return deleted_partner
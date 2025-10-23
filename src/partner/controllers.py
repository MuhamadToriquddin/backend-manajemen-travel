from fastapi import APIRouter,Depends,Request,Path
from starlette import status
from . import services
from . import models
from src.database.core import DbSession
from src.rate_limiting import limiter

router = APIRouter(prefix='/partner',tags=['partner'])

@router.post("/create",status_code=status.HTTP_201_CREATED)
@limiter.limit('50/hour')
async def create_partner(request:Request, db:DbSession, form_data:models.RequestCreateNewPartner):
    new_route:models.Partner = services.create_new_partner(db=db,form_data=form_data)
    partner_name=new_route.partner_name
    return {
        "message":f"Mitra {partner_name} berhasil dibuat"
    }

@router.put("/update/{partner_id}",status_code=status.HTTP_200_OK)
@limiter.limit('50/hour')
async def update_partner(partner_id:int=Path(...),request:Request=None, db:DbSession=None, form_data:models.RequestUpdatePartner=None):
    services.update_partner(partner_id=partner_id,db=db,form_data=form_data)
    return {
        "message":"Berhasil ubah mitra"
    }

@router.delete("/delete/{partner_id}",status_code=status.HTTP_200_OK)
@limiter.limit('50/hour')
async def delete_partner(partner_id:int=Path(...),request:Request=None, db:DbSession=None, form_data:models.RequestUpdateRoute=None):
    deleted_partner:models.Partner =services.delete_partner(db=db,partner_id=partner_id)
    return {
        "message":f"Berhasil hapus mitra {deleted_partner}"
    }

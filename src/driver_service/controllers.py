from fastapi import APIRouter,Depends,Request,Path
from starlette import status
from . import services
from . import models
from src.database.core import DbSession
from src.rate_limiting import limiter

router = APIRouter(prefix='/driver',tags=['driver'])

@router.post("/create",status_code=status.HTTP_201_CREATED)
@limiter.limit('50/hour')
async def create_driver(request:Request, db:DbSession, form_data:models.RequestCreateNewDriver):
    new_driver:models.Driver = services.create_new_driver(db=db,form_data=form_data)
    driver_name=new_driver.driver_name
    return {
        "message":f"Supir {driver_name} berhasil dibuat"
    }

@router.put("/update/{driver_id}",status_code=status.HTTP_200_OK)
@limiter.limit('50/hour')
async def update_driver(driver_id:int=Path(...),request:Request=None, db:DbSession=None, form_data:models.RequestUpdateDriver=None):
    services.update_driver(driver_id=driver_id,db=db,form_data=form_data)
    return {
        "message":"Berhasil ubah supir"
    }

@router.delete("/delete/{driver_id}",status_code=status.HTTP_200_OK)
@limiter.limit('50/hour')
async def delete_driver(driver_id:int=Path(...),request:Request=None, db:DbSession=None):
    deleted_driver:str =services.delete_driver(db=db,partner_id=driver_id)
    return {
        "message":f"Berhasil hapus supir {deleted_driver}"
    }

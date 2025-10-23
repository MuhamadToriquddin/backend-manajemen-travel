from fastapi import APIRouter,Depends,Request,Path
from starlette import status
from . import services
from . import models
from src.database.core import DbSession
from src.rate_limiting import limiter

router = APIRouter(prefix='/route',tags=['route'])

@router.post("/create",status_code=status.HTTP_201_CREATED)
@limiter.limit('50/hour')
async def create_route(request:Request, db:DbSession, form_data:models.RequestCreateNewRoute):
    new_route:models.Route = services.create_new_route(db=db,form_data=form_data)
    route_name=new_route.route_name
    return {
        "message":f"Rute {route_name} berhasil dibuat"
    }

@router.put("/update/{route_id}",status_code=status.HTTP_200_OK)
@limiter.limit('50/hour')
async def update_route(route_id:int=Path(...),request:Request=None, db:DbSession=None, form_data:models.RequestUpdateRoute=None):
    services.update_route(route_id=route_id,db=db,form_data=form_data)
    return {
        "message":"Berhasil ubah rute"
    }

@router.delete("/delete/{route_id}",status_code=status.HTTP_200_OK)
@limiter.limit('50/hour')
async def delete_route(route_id:int=Path(...),request:Request=None, db:DbSession=None, form_data:models.RequestUpdateRoute=None):
    deleted_route:models.Route =services.delete_route(db=db,route_id=route_id)
    return {
        "message":f"Berhasil hapus rute {deleted_route}"
    }

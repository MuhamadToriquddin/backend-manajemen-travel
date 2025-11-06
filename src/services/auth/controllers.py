from fastapi import APIRouter,Depends,Request
from starlette import status
from . import services
from . import models
from src.database.core import DbSession
from src.rate_limiting import limiter
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth',tags=['auth'])

@router.post("/register",status_code=status.HTTP_201_CREATED)
@limiter.limit('3/hour')
async def register_user(request:Request, db:DbSession, data:models.RequestRegisterData):
    services.register_new_user(db=db,data=data)
    
@router.post("/login",status_code=status.HTTP_200_OK)
async def login_user(db:DbSession,form_data:OAuth2PasswordRequestForm=Depends()):
    token = services.login_user(form_data,db)
    return token
    
@router.post("/refresh",status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token:str):
    services.get_new_token(refresh_token)
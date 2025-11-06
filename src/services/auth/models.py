from pydantic import BaseModel,EmailStr
from uuid import UUID
from datetime import datetime

class TokenData(BaseModel):
    access_token:str
    refresh_token:str
    
class RequestRegisterData(BaseModel):
    username:str
    email:EmailStr
    password:str
    
class PayloadToken(BaseModel):
    username:str
    sub:UUID
    role:str
    exp:datetime



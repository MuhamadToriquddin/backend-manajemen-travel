from pydantic import BaseModel
from typing import List

class RequestCreateNewPartner(BaseModel):
    partner_name:str
    phone:str
    address:str | None
    
class RequestUpdatePartner(BaseModel):
    partner_name:str
    phone:str
    address:str | None
    
class Partner(BaseModel):
    id = int
    partner_name = str
    phone = str
    address= str | None
    billable_fee = int
    collected_fee = int
    is_deleted = bool
    
class Partners(BaseModel):
    data:List[Partner]

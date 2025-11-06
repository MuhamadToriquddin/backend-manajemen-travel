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
    
class RequestUpdateFeePartner(BaseModel):
    partner_id:int
    fee:int
    
class Partner(BaseModel):
    id : int
    partner_name : str
    phone : str
    address: str | None
    billable_fee : int
    collected_fee : int
    model_config = {
        "from_attributes": True  
    }
    
class Partners(BaseModel):
    data:List[Partner]

from pydantic import BaseModel
from typing import List
from src.entities.partner_payout import TypePayout

class RequestCreateNewPartnerPayout(BaseModel):
    partner_name:str
    fee:int
    type:TypePayout
    
class PartnerPayout(BaseModel):
    id : int
    partner_name : str
    fee : int
    type: TypePayout
    model_config={
        "from_attributes":True
    }
    
class PartnerPayouts(BaseModel):
    data:List[PartnerPayout]
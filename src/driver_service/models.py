from pydantic import BaseModel
from typing import List

class RequestCreateNewDriver(BaseModel):
    driver_name:str
    phone:str
    address:str | None
    
class RequestUpdateDriver(BaseModel):
    driver_name:str
    phone:str
    address:str | None
    
class Driver(BaseModel):
    id : int
    driver_name : str
    phone : str
    address: str | None
    model_config = {
        "from_attributes": True  
    }
    
class Drivers(BaseModel):
    data:List[Driver]

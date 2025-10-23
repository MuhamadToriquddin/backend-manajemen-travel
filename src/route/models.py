from pydantic import BaseModel
from typing import List

class RequestCreateNewRoute(BaseModel):
    route_name:str
    duration:str
    time_schedules:List[str]
    
class RequestUpdateRoute(BaseModel):
    route_name:str
    duration:str
    time_schedules:List[str]
    
class Route(BaseModel):
    id:int
    route_name:str
    duration:str
    time_schedules:List[str]
    is_deleted:bool
    
class Routes(BaseModel):
    data:List[Route]
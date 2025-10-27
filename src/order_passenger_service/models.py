from pydantic import BaseModel
from datetime import datetime
from src.entities.order_passenger import Status
from uuid import UUID
class OrderDetails(BaseModel):
    passenger_name:str
    phone:str
    pickup_address:str
    destination_address:str
    description:str

class OrderInformationRequest(BaseModel):
    order_date:datetime
    departure_date:datetime
    route_id:int
    departure_time:str
    total_passenger:str
    price_each:int
    discount:int
    status:Status

class RequestCreateNewOrderPassenger(BaseModel):
    order_details:OrderDetails
    order_information:OrderInformationRequest
    partner_give:int|None
    
class RequestUpdateOrderPassenger(BaseModel):
    order_details:OrderDetails
    order_information:OrderInformationRequest

class RequestHandleOrder(BaseModel):
    order_id:UUID
    driver_id:int | None
    partner_id:int|None
    fee:int

class RequestCompletedOrder(BaseModel):
    order_id:UUID
    

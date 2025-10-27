from src.database.core import Base
from sqlalchemy import Column, String,Integer,Boolean,DateTime,Enum
from sqlalchemy.dialects.postgresql import UUID
from enum import StrEnum
import uuid    
from datetime import datetime

class Status(StrEnum):
    progress='PROGRESS' #belum diatur handlenya
    uncompleted='UNCOMPLETED' #udah diatur handlenya tapi belum dibayar feenya
    completed='COMPLETED' #udah dibayar dan selesai
    canceled='CANCELED' #dibatalkan

class OrderPassenger(Base):
    __tablename__="order_passenger"
    
    id = Column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4)
    passenger_name=Column(String,nullable=False)
    phone=Column(String,nullable=False)
    pickup_address=Column(String,nullable=False)
    destination_address=Column(String,nullable=False)
    description=Column(String,nullable=True)
    order_date=Column(DateTime,nullable=False,default=datetime.now)
    departure_date=Column(DateTime,nullable=False)
    route_id=Column(Integer,nullable=False)
    departure_time=Column(String,nullable=False)
    total_passenger=Column(Integer,nullable=False)
    price_each=Column(Integer,nullable=False)
    discount=Column(Integer,nullable=True,default=0)
    status=Column(Enum(Status),nullable=False,default=Status.progress)
    is_deleted = Column(Boolean,nullable=False,default=False)
    
    
    

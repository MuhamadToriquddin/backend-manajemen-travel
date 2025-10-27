from src.database.core import Base
from sqlalchemy import Column, String,Integer,Boolean,DateTime,Enum
from sqlalchemy.dialects.postgresql import UUID

class HandleOrder(Base):
    __tablename__='handle_order'
    
    id=Column(String,nullable=False,primary_key=True,autoincrement=True)
    order_id=Column(UUID(as_uuid=True),nullable=False)
    driver_id=Column(Integer,nullable=True)
    partner_id=Column(Integer,nullable=True)
    fee=Column(Integer,nullable=False)
    
    
    
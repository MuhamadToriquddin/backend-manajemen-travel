from src.database.core import Base
from sqlalchemy import Column,String,Integer,Boolean,Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enum import StrEnum


class TypePayout(StrEnum):
    payment='PAYMENT'
    charge='CHARGE'

class PartnerPayout(Base):
    __tablename__="partner payout"
    
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    partner_name = Column(String,unique=True, nullable=False)
    fee = Column(Integer,nullable=False)
    type = Column(Enum(TypePayout),nullable=False)
    is_deleted = Column(Boolean,nullable=False,default=False)
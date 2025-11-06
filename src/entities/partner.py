from src.database.core import Base
from sqlalchemy import Column,String,Integer,Boolean

class Partner(Base):
    __tablename__="partner"
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    partner_name = Column(String,unique=True, nullable=False)
    phone = Column(String,nullable=False)
    address=Column(String,nullable=True,default="-")
    fee = Column(Integer,nullable=False,default=0)
    is_deleted = Column(Boolean,nullable=False,default=False)
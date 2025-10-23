from src.database.core import Base
from sqlalchemy import Column,String,Integer,Boolean

class Driver(Base):
    __tablename__="driver"
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    driver_name = Column(String,unique=True, nullable=False)
    phone = Column(String,nullable=False)
    address=Column(String,nullable=True,default="-")
    is_deleted = Column(Boolean,nullable=False,default=False)
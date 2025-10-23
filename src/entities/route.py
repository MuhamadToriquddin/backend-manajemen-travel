from src.database.core import Base
from sqlalchemy import Column,String,Integer,ARRAY,Boolean

class Route(Base):
    __tablename__="route"
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    route_name = Column(String,unique=True, nullable=False)
    duration = Column(String,nullable=True)
    time_schedules = Column(ARRAY(String),nullable=False)
    is_deleted = Column(Boolean,nullable=False,default=False)
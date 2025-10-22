from src.database.core import Base
from sqlalchemy import Column,String,Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enum import StrEnum

class Role(StrEnum):
    admin='ADMIN'
    superadmin='SUPERADMIN'
    notauthorized='NOTAUTHORIZED'

class User(Base):
    __tablename__="users"
    
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email = Column(String,unique=True, nullable=False)
    username = Column(String,nullable=False)
    password = Column(String,nullable=False)
    role = Column(Enum(Role), default=Role.notauthorized,nullable=False)
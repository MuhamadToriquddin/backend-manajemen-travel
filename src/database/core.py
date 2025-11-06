from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker,Session
from dotenv import load_dotenv
from fastapi import Depends
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@localhost:{PORT}/{DBNAME}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")
    
def get_db():
    db=SessionLocal()
    try:
        yield db
    except Exception as e:
        # optional logging
        print("DB Error:", e)
        raise  # penting! lempar lagi
    finally:
        db.close()
        
DbSession = Annotated[Session,Depends(get_db)]
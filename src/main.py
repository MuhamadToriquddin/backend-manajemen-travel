from fastapi import FastAPI
from .api import register_routes   
from .database.core import Base, engine
 
app = FastAPI()

register_routes(app)
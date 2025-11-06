from pydantic import BaseModel

class SuccessResponse(BaseModel):
    status:str = "success"
    message:str
    data:dict | list | None = None
    
class ErrorResponse(BaseModel):
    status:str = "error"
    message:str
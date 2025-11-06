from fastapi.responses import JSONResponse
from . import models

def success_response(message:str,data:dict|list|None = None):
    return models.SuccessResponse(
        status="success",
        message=message,
        data=data
    )
    
def error_response(message:str,status_code:int=400):
    return JSONResponse(
        status_code=status_code,
        content=models.ErrorResponse(
            status="error",
            message=message
        ).model_dump()
    )
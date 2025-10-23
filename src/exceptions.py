from fastapi import FastAPI, HTTPException, status

def raise_error(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)

# pre defined exceptions 
def bad_request(detail: str = "Bad Request"):
    raise_error(status.HTTP_400_BAD_REQUEST, detail)

def unauthorized(detail: str = "Unauthorized"):
    raise_error(status.HTTP_401_UNAUTHORIZED, detail)

def forbidden(detail: str = "Forbidden"):
    raise_error(status.HTTP_403_FORBIDDEN, detail)

def not_found(detail: str = "Not Found"):
    raise_error(status.HTTP_404_NOT_FOUND, detail)

def conflict(detail: str = "Conflict"):
    raise_error(status.HTTP_409_CONFLICT, detail)

def internal_error(detail: str = "Internal Server Error"):
    raise_error(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)
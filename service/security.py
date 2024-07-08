from jose import jwt , JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from fastapi import *
from model.model import *

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
security = HTTPBearer()

def create_access_token(data: dict , expires_delta: timedelta = timedelta(days = 7)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 60)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        return payload
    except JWTError:
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response


def get_current_user(token: HTTPAuthorizationCredentials = Security(security)) :
    if token is None :
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
                status_code=status.HTTP_403_FORBIDDEN, 
                content=error_response.dict())
            return response   
    
    user_info = decode_access_token(token.credentials)
    if not user_info:
            error_response = ErrorResponse(error=True, message="User not founded")
            response = JSONResponse (
                status_code=status.HTTP_404_FORBIDDEN, 
                content=error_response.dict())
            return response
    else:
        return user_info
from model.model import UserRead , ErrorResponse
from fastapi.responses import JSONResponse
from starlette import status
import bcrypt

from db.user import *
from service.security import create_access_token 

async def register_user(name: str, email: str, password: str) -> JSONResponse :
    if db_check_user_email_exists(email):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": True, "message": "Email already exists"}
        )
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    if db_insert_new_user(name, email, hashed_password):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"ok": True}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": True, "message": "Failed to create user due to a server error"}
        )

async def authenticate_user(email: str, password: str) -> JSONResponse :
    user_info = db_check_email_password(email, password)
    if user_info:
        access_token = create_access_token(
            data={"id": user_info['id'], "name": user_info['name'], "email": user_info['email']}
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"token": access_token}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": True, "message": "Invalid email or password"}
        )

async def get_user_details(user: dict) -> JSONResponse :
    try:
        if user :

            if "id" not in user or user["id"] is None :
                error_response = ErrorResponse(error=True, message="User bot found")
                response = JSONResponse (
                status_code=status.HTTP_404,
                content={"data": user_model.dict()}
            )           
                return response

            user_model = UserRead(**user)
            response = JSONResponse (
                status_code=status.HTTP_200_OK,
                content={"data": user_model.dict()}
            )           
            return response
        else:
            error_response = ErrorResponse(error=True, message="Failed to get user's data")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response
    
    except Exception :
        error_response = ErrorResponse(error=True, message="User not authenticated")
        response = JSONResponse (
            status_code=status.HTTP_403_FORBIDDEN, 
            content=error_response.dict())
        return response
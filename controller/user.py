from fastapi import Depends, HTTPException
from model.user import UserCreate, UserRead
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
import bcrypt

from db.user import insert_new_user, check_user_email_exists, check_email_password
from service.security import create_access_token , get_current_user

async def register_user(name: str, email: str, password: str):
    if check_user_email_exists(email):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": True, "message": "Email already exists"}
        )
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    if insert_new_user(name, email, hashed_password):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"ok": True}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": True, "message": "Failed to create user due to a server error"}
        )

async def authenticate_user(email: str, password: str):
    user_info = check_email_password(email, password)
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

async def get_user_details(user: dict):
    try:
        user_model = UserRead(**user)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"data": user_model.dict()}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": True, "message": str(e)}
        )
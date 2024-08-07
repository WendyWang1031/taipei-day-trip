from model.model import *
from fastapi.responses import JSONResponse
from starlette import status
import bcrypt

from db.user import *
from service.security import security_create_access_token 

async def register_user(user_request : UserCreateRequest) -> JSONResponse :
    
    try:

        if db_check_user_email_exists(user_request.email) :
            error_response = ErrorResponse(error=True, message="Email already exists")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), bcrypt.gensalt())
        
        if db_insert_new_user(user_request.name, user_request.email, hashed_password) is True :
            success_response = SuccessfulResponseForMemberRegister(ok=True)
            response = JSONResponse(
                status_code=status.HTTP_200_OK,
                content=success_response.dict()
            )
            return response
        else:
            error_response = ErrorResponse(error=True, message="Failed to create user due to a server error")
            response = JSONResponse (
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                content=error_response.dict())
            return response
    
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response


async def authenticate_user(user_login_req : UserLoginRequest) -> JSONResponse :
    
    try:
        user_info = db_check_email_password(user_login_req.email, user_login_req.password)
        
        if user_info:
            access_token = security_create_access_token(UserReadDetail(
                id = user_info['id'],
                name = user_info['name'],
                email = user_info['email']
            ).dict())
            success_response = SuccessfulResponseForMemberBase(token = access_token)
            response = JSONResponse(
                status_code=status.HTTP_200_OK,
                content=success_response.dict()
            )
            return response
        
        else:
            error_response = ErrorResponse(error=True, message="Invalid email or password")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response
    
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
    


async def get_user_details(user: dict) -> JSONResponse :
    try:
        if not user :
            error_response = ErrorResponse(error=True, message="Failed to get user's data")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response
            
        user_model = UserReadDetail(**user)

        if user["id"] is None :
            error_response = ErrorResponse(error=True, message="User not found")
            response = JSONResponse (
            status_code=status.HTTP_404,
            content={"data": user_model.dict()}
        )           
            return response
        
        else:    
            response = JSONResponse (
                status_code=status.HTTP_200_OK,
                content={"data": user_model.dict()}
            )           
            return response

    except KeyError :
        error_response = ErrorResponse(error=True, message="User not authenticated")
        response = JSONResponse (
            status_code=status.HTTP_403_FORBIDDEN, 
            content=error_response.dict())
        return response       

    
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
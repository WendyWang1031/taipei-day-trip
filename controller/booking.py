from model.model import *
from service.security import get_current_user
from db.booking import *
from fastapi import *
from fastapi import  Depends
from fastapi.responses import JSONResponse

async def create_booking(booking: BookingRequest , current_user : dict = Depends(get_current_user)) -> JSONResponse | ErrorResponse:
    try:
        if current_user :
            member_id = current_user["id"]
            result = db_save_or_update_booking(member_id , booking)
            print(result)
            if result:
                response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content={
                    "ok":True
                })
                return response
            else:
                error_response = ErrorResponse(error=True, message="Failed to create booking")
                response = JSONResponse (
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    content=error_response.dict())
                return response
        else:
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
    
    
async def get_booking_details( current_user : dict = Depends(get_current_user)) -> JSONResponse | ErrorResponse :
    try:
        if current_user :
            member_id = current_user["id"]
            booking_details = db_check_booking_detail(member_id)
            print(booking_details)
            if booking_details:
                response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content={
                    "data" : booking_details.model_dump()
                })
                return response
            else:
                response = JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": True,
                    "message": str(e)
                })
                return response
        else:
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
    
async def delete_booking( current_user : dict = Depends(get_current_user)) -> JSONResponse | ErrorResponse :
    try:
        if current_user :
            member_id = current_user["id"]
            delete_booking_result = db_delete_booking_details(member_id)
            
            if delete_booking_result:
                response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content={
                    "ok": True
                })
                return response
            else:
                response = JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": True,
                        "message": str(e)
                    })
                return response
        else:
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
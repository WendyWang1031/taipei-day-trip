from model.model import *
from service.security import get_current_user
from db.booking import *
from fastapi import *
from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse

async def create_booking(booking: Booking , current_user : dict = Depends(get_current_user)):
    try:
        if current_user :
            member_id = current_user["id"]
            result = save_or_update_booking(member_id , booking)
            print(result)
            if result:
                response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content={
                    "ok":True
                })
                return response
            else:
                raise HTTPException(status_code=400, detail="Booking creation failed")
        else:
            raise HTTPException(status_code=403, detail="User not authenticated")
    
    except Exception as e :
        response = JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error":True,
                "message":str(e)
            })
        return response
    
    
async def get_booking_details( current_user : dict = Depends(get_current_user)):
    try:
        if current_user :
            member_id = current_user["id"]
            booking_details = check_booking_detail(member_id)
            print(booking_details)
            if booking_details:
                response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content={
                    "data" : booking_details
                })
                return response
            else:
                raise HTTPException(status_code=400, detail="資料庫沒有該用戶的預約行程")
        else:
            raise HTTPException(status_code=403, detail="User not authenticated")
        
    except Exception as e :
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": str(e)
            })
        return response
    
async def delete_booking( current_user : dict = Depends(get_current_user)):
    try:
        if current_user :
            member_id = current_user["id"]
            delete_booking_result = delete_booking_details(member_id)
            
            if delete_booking_result:
                response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content={
                    "ok": True
                })
                return response
            else:
                raise HTTPException(status_code=400, detail="Delete booking details failed")
        else:
            raise HTTPException(status_code=403, detail="User not authenticated")
        
    except Exception as e :
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": str(e)
            })
        return response
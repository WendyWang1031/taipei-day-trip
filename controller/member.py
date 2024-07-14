from model.model import *
from service.security import security_get_current_user
from db.member import *

from fastapi import *
from fastapi import  Depends
from fastapi.responses import JSONResponse
import boto3


def upload_file_to_s3(file: UploadFile , user_id: str):
    s3_client = boto3.client('s3')
    bucket_name = "taipei-day-trip-images"

    file_key = f"avatars/{user_id}-avatar.jpg"
    content_type = file.content_type
    try:
        s3_client.upload_fileobj(
            file.file,
            bucket_name,
            file_key,
            ExtraArgs={
                'ContentType': content_type  
            }
        )
        return f"https://{bucket_name}.s3.amazonaws.com/{file_key}"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def update_member_data(
        member_data: MemberDataRequest ,
        avatar: UploadFile = File(...), 
        current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        
        if current_user :
            member_id = current_user["id"]
            avatar_url = upload_file_to_s3(avatar , member_id)
            result = db_save_or_update_member_data(member_id , member_data , avatar_url)
            
            if result is True:

                response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content={
                    "ok":True
                })
                return response
            else:
                error_response = ErrorResponse(error=True, message="Failed to create member data")
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
    
    
async def get_member_data( current_user : dict = Depends(security_get_current_user)) -> JSONResponse :
    try:
        if current_user :
            member_id = current_user["id"]
            member_data_details = db_get_member_data(member_id)
            print("member_data_details:" , member_data_details)
            
            if member_data_details:
                success_response = MemberUpdateResponse(ok=True, data=member_data_details)
                response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content=success_response.dict()
                )
                return response
                
            else:
                error_response = ErrorResponse(error=True, message="No Member Data details found for user")
                response = JSONResponse (
                    status_code=status.HTTP_404_NOT_FOUND, 
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
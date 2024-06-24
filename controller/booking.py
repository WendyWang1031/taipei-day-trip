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
			result = insert_new_booking(booking.attraction_id , booking.date , booking.time , booking.price , member_id)
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
	
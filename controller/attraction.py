import json
from model.model import *
from fastapi import *
from fastapi.responses import JSONResponse

from service.cache_service import *
from db.attraction import db_get_attractions_for_pages , db_get_attractions_for_id , db_get_mrts

redis_connection = get_redis_connection()
cache_service = CacheService(redis_connection)


async def get_attractions_for_all(page : int , keyword : str) -> JSONResponse :
	
	try:
		data = db_get_attractions_for_pages(page , keyword)
		# print("get_attractions data:" , data)

		next_page = None if len(data) < 12 else page + 1
		
		success_response = SuccessfulResponseForAttraction(nextPage=next_page, data=data)
		response = JSONResponse(
		status_code = status.HTTP_200_OK,
		content=success_response.dict()
		)
		return response
	
	except Exception as e :
		error_response = ErrorResponse(error=True, message=str(e))
		response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
		return response
		


async def get_attraction_for_id(attractionId : int) -> JSONResponse :
	cache_key = f'attraction:{attractionId}'
	try:
		
		cached_data = cache_service.get_value(cache_key)
		
		if cached_data:
			response = JSONResponse(
				status_code = status.HTTP_200_OK,
				content={
					"data":json.loads(cached_data)
				},
				headers={"X-Cache":"Hit from Redis"})
			
			return response

		data = db_get_attractions_for_id( attractionId )
		

		if not data:
			error_response = ErrorResponse(error=True, message="Not founded the Attraction")
			response = JSONResponse (
            	status_code=status.HTTP_404_NOT_FOUND, 
            	content=error_response.dict())
			return response
		
		cache_service.set_value(cache_key, json.dumps(data), expiry=3600)
		
		
		response = JSONResponse(
			status_code = status.HTTP_200_OK,
			content={
				"data":data
			})
		return response
		
	except ValueError as ve :
		error_response = ErrorResponse(error=True, message=str(ve))
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


async def get_mrts() -> JSONResponse | ErrorResponse:
	try:
		data = db_get_mrts()
		response = JSONResponse(
			status_code = status.HTTP_200_OK,
			content={
				"data":data
			})
		return response
	
	except Exception as e :
		error_response = ErrorResponse(error=True, message=str(e))
		response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
		return response

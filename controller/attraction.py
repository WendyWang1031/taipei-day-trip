import json
from model.model import *
from fastapi import *
from fastapi.responses import JSONResponse

from service.cache_service import *
from db.attraction import get_attractions_for_pages , get_attractions_for_id , get_mrts

redis_connection = get_redis_connection()
cache_service = CacheService(redis_connection)


async def attractions_for_all(page , keyword):
	
	try:
		data = get_attractions_for_pages(page , keyword)

		if not data:
			print("No data found , returing empty list.")
			data = []

		nextPage = None if len(data) < 12 else page + 1
		
		response = JSONResponse(
		status_code = status.HTTP_200_OK,
		content={
			"nextPage":nextPage,
			"data":data
		})
		return response
	
	except Exception as e :
		response = JSONResponse(
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
		content={
			"error":True,
			"message":str(e)
		})
		return response


async def attraction_for_id(attractionId):
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

		data = get_attractions_for_id( attractionId )
		

		if not data:
			response = JSONResponse(
			status_code = status.HTTP_404_NOT_FOUND,
			content={
			"error":True,
			"message":"沒有找到指定的景點"
			
			},
			headers={"X-Cache":"Miss from Redis"})
			
			return response
		
		cache_service.set_value(cache_key, json.dumps(data), expiry=3600)
		
		
		response = JSONResponse(
			status_code = status.HTTP_200_OK,
			content={
				"data":data
			})
		return response
		
	except ValueError as ve :
		response = JSONResponse(
		status_code = status.HTTP_400_BAD_REQUEST,
		content={
			"error":True,
			"message":str(ve)
		})
		return response
	
	except Exception as e :
		response = JSONResponse(
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
		content={
			"error":True,
			"message":str(e)
		})
		return response


async def fetch_mrts():
	try:
		data = get_mrts()
		response = JSONResponse(
			status_code = status.HTTP_200_OK,
			content={
				"data":data
			})
		return response
	
	except Exception as e :
		response = JSONResponse(
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
		content={
			"error":True,
			"message":str(e)
		})
		return response

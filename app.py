from fastapi import *
from fastapi.responses import FileResponse , JSONResponse
from pydantic import BaseModel , Field 
from typing import List , Optional 
from db import get_attractions_for_pages , get_attractions_for_id , get_mrts
app = FastAPI()

#定義資料型別

class Image(BaseModel):
	url:str

class Attraction(BaseModel):
	id: int
	name: str
	category: str
	description: str
	address: str
	transport: str
	mrt: str
	lat: float
	lng: float
	images: List[Image]


class MRTList(BaseModel):
	data: str = Field(..., description="捷運站名稱列表")

class SuccessfulResponse(BaseModel):
	next_page : Optional[int]= Field(None, description = "下一頁的頁碼，若無更多頁面則為 None")
	data : List[Attraction] = Field(..., description = "景點數據列表")

class ErrorResponse(BaseModel):
	error : bool = Field(True, description = "指示是否為錯誤響應")
	message : str = Field(..., description = "錯誤訊息描述")

class SuccessfulResponseForID(BaseModel):
	data : Attraction = Field(..., description = "景點數據列表")
	

@app.get("/api/attractions" , 
		 response_model = Attraction , 
		 summary = "取得景點資料列表",
         description="取得不同分頁的旅遊景點列表資料，也可以根據標題關鍵字、或捷運站名稱篩選",
		 responses = {
			200:{
				"model" : SuccessfulResponse,
				"description" : "正常運作"
			},
			500:{
				"model" : ErrorResponse,
				"description" : "伺服器內部錯誤"
			}
		 })
async def attraction( 
	page: int = Query(description = "要取得的分頁，每頁 12 筆資料" ) , 
	keyword: str = Query(None, description = "用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選")):
	
	try:
		# print(f"Fetching data for page: {page} with keyword: {keyword}")
		data = get_attractions_for_pages(page , keyword)
		# print(f"Data retrieved: {data}")

		if not data:
			print("No data found , returing empty list.")
			data = []

		next_page = None if len(data) < 12 else page + 1
		
		response = JSONResponse(
		status_code = status.HTTP_200_OK,
		content={
			"nextPage":next_page,
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

@app.get("/api/attraction/{attractionId}" , 
		 response_model = SuccessfulResponseForID , 
		 summary = "根據景點編號取得景點資料",
		 responses = {
			200:{
				"model" : SuccessfulResponseForID,
				"description" : "景點資料"
			},
			400:{
				"model" : ErrorResponse,
				"description" : "景點編號不正確"
			},
			500:{
				"model" : ErrorResponse,
				"description" : "伺服器內部錯誤"
			}
		 })
async def attraction_for_id( attractionId: int = Path(..., description = "景點編號")):

	try:
		data = get_attractions_for_id( attractionId )
		# print(f"Data retrieved: {data}")

		if not data:
			response = JSONResponse(
			status_code = status.HTTP_404_NOT_FOUND,
			content={
			"error":True,
			"message":"沒有找到指定的景點"
		})
			return response
		else:
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

@app.get("/api/mrts" , 
		 response_model = MRTList , 
		 summary = "取得捷運站名稱列表",
		 description="取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序",
		 responses = {
			200:{
				"description" : "正常運作"
			},
			500:{
				"model" : ErrorResponse,
				"description" : "伺服器內部錯誤"
			}
		 })
async def fetch_mrts():
	try:
		data = get_mrts()
		# print(f"Data retrieved: {data}")
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


# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")

@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")

@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")

@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")
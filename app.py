from fastapi import *
from fastapi.responses import FileResponse , JSONResponse
from pydantic import BaseModel , Field 
from typing import List , Optional 
from db import get_attractions_for_pages , get_attractions_for_id , get_mrts
from fastapi.staticfiles import StaticFiles
import logging , redis , json
from starlette.middleware.base import BaseHTTPMiddleware


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(message)s' , filename= 'app.log')
r = redis.Redis(host="localhost" , port=6379 , db=0)

#定義資料型別
class LoggingMiddleware(BaseHTTPMiddleware):
	async def dispatch(self , request : Request , call_next):
		logging.info(f'Request from IP: {request.client.host} to URL: {request.url.path}')
		response = await call_next(request)
		return response

app.add_middleware(LoggingMiddleware)

class Image(BaseModel):
	url:str
	

class Attraction(BaseModel):
	id: int = Field(... , example=10)
	name: str = Field(... , example="平安鐘")
	category: str = Field(... , example="公共藝術")
	description: str = Field(... , example="平安鐘祈求大家的平安，這是為了紀念 921 地震週年的設計")
	address: str = Field(... , example="臺北市大安區忠孝東路 4 段 1 號")
	transport: str = Field(... , example="公車：204、212、212直")
	mrt: str = Field(... , example="忠孝復興")
	lat: float = Field(... , example=25.04181)
	lng: float = Field(... , example=121.544814)
	images: List[Image] = Field(..., example=["http://140.112.3.4/images/92-0.jpg"])

class UserBase(BaseModel):
	email: str = Field(... , example="ply@ply.com")
	password: str = Field(... , example="12345678")	

# user_instance = UserBase(email="123@gmail" , password="123")
# print(user_instance)

class UserCreate(BaseModel):
	name: str = Field(... , example="彭彭彭")
	email: str = Field(... , example="ply@ply.com")
	password: str = Field(... , example="12345678")	

class UserRead(BaseModel):
	id: int = Field(...,example=1)
	name: str = Field(... , example="彭彭彭")
	email: str = Field(... , example="ply@ply.com")				

class MRTList(BaseModel):
	data: str = Field(..., description="捷運站名稱列表")

class SuccessfulResponseForAttraction(BaseModel):
	nextPage : Optional[int]= Field(None, example=2, description = "下一頁的頁碼，若無更多頁面則為 None")
	data : List[Attraction] = Field(..., description = "景點數據列表")

class SuccessfulResponseForID(BaseModel):
	data : Attraction = Field(..., description = "景點數據列表")

class SuccessfulResponseForMemberRegister(BaseModel):
	ok : bool = Field(..., description = "註冊成功")

class SuccessfulResponseForMember(BaseModel):
	data : UserRead = Field(..., description = "取得當前登入資訊")

class SuccessfulResponseForMemberBase(BaseModel):
	token : str = Field(..., description = "FHSTHSGHFtrhsthfghs")

class ErrorResponse(BaseModel):
	error : bool = Field(True, description = "指示是否為錯誤響應")
	message : str = Field(..., description = "錯誤訊息描述" , example="請按照情境提供對應的錯誤訊息")

@app.post("/api/user" , 
		 tags= ["User"],
		 response_model = UserCreate ,
		 summary = "註冊一個新會員",
        
		 responses = {
			200:{
				"model" : SuccessfulResponseForMemberRegister,
				"description" : "註冊成功"
			},
			400:{
				"model" : ErrorResponse,
				"description" : "註冊失敗，重複的 Email 或其他原因"
			},
			500:{
				"model" : ErrorResponse,
				"description" : "伺服器內部錯誤"
			}
		 })
async def member_register():
	try:
		response = JSONResponse(
		status_code = status.HTTP_200_OK,
		content={
			"ok":True
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


@app.get("/api/user/auth" , 
		 tags= ["User"],
		 response_model = UserRead ,
		 summary = "取得當前的登入資訊",
        
		 responses = {
			200:{
				"model" : SuccessfulResponseForMember,
				"description" : "已登入的會員資料，null 表示未登入"
			}
		 })
async def get_member():
	try:
		response = JSONResponse(
		status_code = status.HTTP_200_OK,
		content={
			"ok":True
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

@app.put("/api/user/auth" , 
		 tags= ["User"],
		 response_model = UserBase ,
		 summary = "登入會員帳戶",
        
		 responses = {
			200:{
				"model" : SuccessfulResponseForMemberBase,
				"description" : "登入成功，取得有效期為七天的 JWT 加密字串"
			},
			400:{
				"model" : ErrorResponse,
				"description" : "登入失敗，帳號或密碼錯誤或其他原因"
			},
			500:{
				"model" : ErrorResponse,
				"description" : "伺服器內部錯誤"
			}
		 })
async def member_signin():
	try:
		response = JSONResponse(
		status_code = status.HTTP_200_OK,
		content={
			"ok":True
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


@app.get("/api/attractions" , 
		 tags= ["Attraction"],
		 response_model = Attraction , 
		 summary = "取得景點資料列表",
         description="取得不同分頁的旅遊景點列表資料，也可以根據標題關鍵字、或捷運站名稱篩選",
		 responses = {
			200:{
				"model" : SuccessfulResponseForAttraction,
				"description" : "正常運作"
			},
			500:{
				"model" : ErrorResponse,
				"description" : "伺服器內部錯誤"
			}
		 })
async def attraction( 
	page: int = Query(ge=0 , description = "要取得的分頁，每頁 12 筆資料" ) , 
	keyword: str = Query(None, description = "用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選")):
	
	try:
		# print(f"Fetching data for page: {page} with keyword: {keyword}")
		data = get_attractions_for_pages(page , keyword)
		# print(f"Data retrieved: {data}")

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

@app.get("/api/attraction/{attractionId}" ,
		 tags= ["Attraction"],
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
		cached_data = r.get(f'attraction:{attractionId}')
		if cached_data:
			response = JSONResponse(
				status_code = status.HTTP_200_OK,
				content={
					"data":json.loads(cached_data)
				},
				headers={"X-Cache":"Hit from Redis"})
			
			return response

		data = get_attractions_for_id( attractionId )
		# print(f"Data retrieved: {data}")
		

		if not data:
			response = JSONResponse(
			status_code = status.HTTP_404_NOT_FOUND,
			content={
			"error":True,
			"message":"沒有找到指定的景點"
			
			},
			headers={"X-Cache":"Miss from Redis"})
			
			return response
		
		r.setex(f'attraction:{attractionId}' , 3600 , json.dumps(data))
		
		
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
		 tags= ["MRT Station"],
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
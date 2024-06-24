from fastapi import *
from fastapi.responses import FileResponse , JSONResponse
from pydantic import BaseModel , Field 
from typing import List , Optional 
from fastapi.staticfiles import StaticFiles
import  json

from db.attraction import get_attractions_for_pages , get_attractions_for_id , get_mrts
from controller.user import register_user, authenticate_user, get_user_details
from model.model import *
from service.security import get_current_user
from db.booking import *
from controller.booking import *

from service.cache_service import *
from middlewares.logging_middleware import LoggingMiddleware


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(LoggingMiddleware)
redis_connection = get_redis_connection()
cache_service = CacheService(redis_connection)

@app.post("/api/booking",
		tags= ["Booking"],
		response_model = Booking , 
		summary = "建立新的預定行程",
		responses = {
			200:{
				"model" : Booking,
				"description" : "建立成功"
			},
			400:{
				"model" : ErrorResponse,
				"description" : "建立失敗，輸入不正確或其他原因"
			},
			403:{
				"model" : ErrorResponse,
				"description" : "未登入系統，拒絕存取"
			},
			500:{
				"model" : ErrorResponse,
				"description" : "伺服器內部錯誤"
			}
		 }
		 )
async def booking(booking: Booking , current_user : dict = Depends(get_current_user)):
	return await create_booking(booking,current_user)
	
	
		

	
	






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
async def user_register(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    return await register_user(name, email, password)

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
async def get_user(user: dict = Depends(get_current_user)):
    return await get_user_details(user)

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
async def user_signin(email: str = Form(...), password: str = Form(...)):
    return await authenticate_user(email, password)

class MRTList(BaseModel):
	data: str = Field(..., description="捷運站名稱列表")

class SuccessfulResponseForAttraction(BaseModel):
	nextPage : Optional[int]= Field(None, example=2, description = "下一頁的頁碼，若無更多頁面則為 None")
	data : List[Attraction] = Field(..., description = "景點數據列表")

class SuccessfulResponseForID(BaseModel):
	data : Attraction = Field(..., description = "景點數據列表")


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


# class Image(BaseModel):
# 	url:str
	

# class Attraction(BaseModel):
# 	id: int = Field(... , example=10)
# 	name: str = Field(... , example="平安鐘")
# 	category: str = Field(... , example="公共藝術")
# 	description: str = Field(... , example="平安鐘祈求大家的平安，這是為了紀念 921 地震週年的設計")
# 	address: str = Field(... , example="臺北市大安區忠孝東路 4 段 1 號")
# 	transport: str = Field(... , example="公車：204、212、212直")
# 	mrt: str = Field(... , example="忠孝復興")
# 	lat: float = Field(... , example=25.04181)
# 	lng: float = Field(... , example=121.544814)
# 	images: List[Image] = Field(..., example=["http://140.112.3.4/images/92-0.jpg"])

# class UserBase(BaseModel):
# 	email: str = Field(... , example="ply@ply.com")
# 	password: str = Field(... , example="12345678")	


# class UserCreate(BaseModel):
# 	name: str = Field(... , example="彭彭彭")
# 	email: str = Field(... , example="ply@ply.com")
# 	password: str = Field(... , example="12345678")	

# SECRET_KEY = "YOUR_SECRET_KEY"
# ALGORITHM = "HS256"

# class UserRead(BaseModel):
# 	id: str = Field(...,example=1)
# 	name: str = Field(... , example="彭彭彭")
# 	email: str = Field(... , example="ply@ply.com")				


# class SuccessfulResponseForMemberRegister(BaseModel):
# 	ok : bool = Field(..., description = "註冊成功")

# class SuccessfulResponseForMember(BaseModel):
# 	data : UserRead = Field(..., description = "取得當前登入資訊")

# class SuccessfulResponseForMemberBase(BaseModel):
# 	token : str = Field(..., description = "FHSTHSGHFtrhsthfghs")

# class ErrorResponse(BaseModel):
# 	error : bool = Field(True, description = "指示是否為錯誤響應")
# 	message : str = Field(..., description = "錯誤訊息描述" , example="請按照情境提供對應的錯誤訊息")

# logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(message)s' , filename= 'app.log')

# r = redis.Redis(host="localhost" , port=6379 , db=0)

#定義資料型別
# class LoggingMiddleware(BaseHTTPMiddleware):
# 	async def dispatch(self , request : Request , call_next):
# 		logging.info(f'Request from IP: {request.client.host} to URL: {request.url.path}')
# 		response = await call_next(request)
# 		return response



# def create_access_token(data: dict , expires_delta: timedelta = timedelta(days = 7)):
# 	to_encode = data.copy()
# 	if expires_delta:
# 		expire = datetime.utcnow() + expires_delta
# 	else:
# 		expire = datetime.utcnow() + timedelta(minutes = 60)
# 	to_encode.update({"exp":expire})
# 	encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)
# 	return encoded_jwt

# def decode_access_token(token: str):
# 	try:
# 		payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
# 		return payload
# 	except JWTError:
# 		raise HTTPException(status_code=403, detail="Invalid credentials")

# security = HTTPBearer()

# def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
# 	return decode_access_token(token.credentials)

# @app.post("/api/user" , 
# 		 tags= ["User"],
# 		 response_model = UserCreate ,
# 		 summary = "註冊一個新會員",
        
# 		 responses = {
# 			200:{
# 				"model" : SuccessfulResponseForMemberRegister,
# 				"description" : "註冊成功"
# 			},
# 			400:{
# 				"model" : ErrorResponse,
# 				"description" : "註冊失敗，重複的 Email 或其他原因"
# 			},
# 			500:{
# 				"model" : ErrorResponse,
# 				"description" : "伺服器內部錯誤"
# 			}
# 		 })
# async def user_register( name :  Annotated[str, Form()] , email :  Annotated[str, Form()] , password :  Annotated[str, Form()]):
# 	try:
# 		user_exists = check_user_email_exists(email)
		
# 		if user_exists is True :
# 			response = JSONResponse(
# 		status_code = status.HTTP_400_BAD_REQUEST,
# 		content={
# 			"error":True,
# 			"message":"Email already exists"
# 		})
# 			return response

		
		
# 		elif user_exists is False:
# 			hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# 			if insert_new_user(name , email , hashed_password):
# 				response = JSONResponse(
# 				status_code = status.HTTP_200_OK,
# 				content={
# 					"ok":True
# 				})
# 				return response
# 			else:
# 				response = JSONResponse(
# 				status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
# 				content={
# 					"error":True,
# 					"message":"Failed to create user due to a server error"
# 				})
# 				return response
# 		else:
# 			response = JSONResponse(
# 			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
# 			content={
# 				"error":True,
# 				"message":"Failed to perform th check due to a database error"
# 			})
# 			return response
		
# 	except Exception as e :
# 		response = JSONResponse(
# 		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
# 		content={
# 			"error":True,
# 			"message":str(e)
# 		})
# 		return response


# @app.get("/api/user/auth" , 
# 		 tags= ["User"],
# 		 response_model = UserRead ,
# 		 summary = "取得當前的登入資訊",
        
# 		 responses = {
# 			200:{
# 				"model" : SuccessfulResponseForMember,
# 				"description" : "已登入的會員資料，null 表示未登入"
# 			}
# 		 })
# async def get_user(user: dict = Depends(get_current_user)):
# 	try:
# 		user_model = UserRead(**user)
# 		response = JSONResponse(
# 		status_code = status.HTTP_200_OK,
# 		content={
# 			"data":user_model.dict()
# 		})
# 		return response
# 	except Exception as e :
# 		response = JSONResponse(
# 		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
# 		content={
# 			"error":True,
# 			"message":str(e)
# 		})
# 		return response

# @app.put("/api/user/auth" , 
# 		 tags= ["User"],
# 		 response_model = UserBase ,
# 		 summary = "登入會員帳戶",
        
# 		 responses = {
# 			200:{
# 				"model" : SuccessfulResponseForMemberBase,
# 				"description" : "登入成功，取得有效期為七天的 JWT 加密字串"
# 			},
# 			400:{
# 				"model" : ErrorResponse,
# 				"description" : "登入失敗，帳號或密碼錯誤或其他原因"
# 			},
# 			500:{
# 				"model" : ErrorResponse,
# 				"description" : "伺服器內部錯誤"
# 			}
# 		 })
# async def user_signin( email :  Annotated[str, Form()] , password :  Annotated[str, Form()]):
# 	try:
# 		user_info = check_email_password(email , password)
# 		if user_info:
# 			access_token = create_access_token(
# 				data={"id": user_info['id'] , 
# 		  			"name" :user_info['name'], 
# 		  			"email": user_info['email']}
# 			) 
	
# 			response = JSONResponse(
# 			status_code = status.HTTP_200_OK,
# 			content={
# 				"token":access_token
# 			})
# 			return response
			
# 		else:
# 			response = JSONResponse(
# 			status_code = status.HTTP_400_BAD_REQUEST,
# 			content={
# 				"error":True,
# 				"message":"Invalid email or password"
# 			})
# 			return response
	
# 	except KeyError as e:
# 		response = JSONResponse(
# 			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
# 			content={"error": True, 
# 					"message": f"Missing key {e}"}
# 					)
# 		return response

# 	except Exception as e :
# 		response = JSONResponse(
# 		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
# 		content={
# 			"error":True,
# 			"message":str(e)
# 		})
# 		return response




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
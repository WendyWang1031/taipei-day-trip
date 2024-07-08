from fastapi import *
from fastapi.responses import FileResponse 
from fastapi.staticfiles import StaticFiles


from controller.attraction import *
from controller.user import register_user, authenticate_user, get_user_details
from model.model import *
from service.security import get_current_user
from db.booking import *
from controller.booking import *
from controller.order import *

from service.cache_service import *
from middlewares.logging_middleware import LoggingMiddleware


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(LoggingMiddleware)
redis_connection = get_redis_connection()
cache_service = CacheService(redis_connection)

# 預定行程 - 類似購物車
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
async def fetch_post_booking(booking: Booking , current_user : dict = Depends(get_current_user)):
	return await create_booking(booking , current_user)

@app.get("/api/booking",
		tags= ["Booking"],
		response_model = BookingResponse , 
		summary = "建立新的預定行程",
		responses = {
			200:{
				"model" : BookingResponse,
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
async def fetch_get_booking( current_user : dict = Depends(get_current_user) ):
	return await get_booking_details( current_user)	

@app.delete("/api/booking",
		tags= ["Booking"],
		response_model = SuccessfulResponseForBookingDelete , 
		summary = "建立新的預定行程",
		responses = {
			200:{
				"model" : SuccessfulResponseForBookingDelete,
				"description" : "刪除成功"
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
async def fetch_delete_booking_api( current_user : dict = Depends(get_current_user) ):
	return await delete_booking(current_user)		
		


# 會員登入、註冊、確認用戶登入狀況
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
async def fetch_post_user_signup(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
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
async def fetch_get_user(user: dict = Depends(get_current_user)):
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
async def fetch_put_user_signin(email: str = Form(...), password: str = Form(...)):
    return await authenticate_user(email, password)


# 景點頁面
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
async def fetch_get_attraction( 
	page: int = Query(ge=0 , description = "要取得的分頁，每頁 12 筆資料" ) , 
	keyword: str = Query(None, description = "用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選")):
	return await get_attractions_for_all(page , keyword)

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
async def fetch_get_attraction_id( attractionId: int = Path(..., description = "景點編號")):
	return await get_attraction_for_id(attractionId)

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
async def fetch_get_mrts():
	return await get_mrts()

# 訂單處理
@app.post("/api/orders",
		tags= ["Order"],
		response_model = Booking , 
		summary = "建立新的訂單，並完成付款程序",
		responses = {
			200:{
				"model" : PaymentOrderResponse,
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
async def fetch_post_orders(
	current_user : dict = Depends(get_current_user) , 
	order_request : PaymentOrderRequest = Body(...)) -> JSONResponse :
	return await create_order(current_user , order_request)



# ----------------------------------------------------------


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
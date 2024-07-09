from pydantic import BaseModel, Field
from typing import List , Optional 


# 景點
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

class MRTList(BaseModel):
	data: str = Field(..., description="捷運站名稱列表")

class SuccessfulResponseForAttraction(BaseModel):
	nextPage : Optional[int]= Field(None, example=2, description = "下一頁的頁碼，若無更多頁面則為 None")
	data : List[Attraction] = Field(..., description = "景點數據列表")

class SuccessfulResponseForID(BaseModel):
	data : Attraction = Field(..., description = "景點數據列表")


# 用戶
class UserRead(BaseModel):
    id: str = Field(...,example=1)
    name: str = Field(... , example="彭彭彭")
    email: str = Field(... , example="ply@ply.com")				

class UserBase(BaseModel):
    email: str = Field(... , example="ply@ply.com")
    password: str = Field(... , example="12345678")	

class UserCreate(BaseModel):
    name: str = Field(... , example="彭彭彭")
    email: str = Field(... , example="ply@ply.com")
    password: str = Field(... , example="12345678")	

class SuccessfulResponseForMemberRegister(BaseModel):
    ok : bool = Field(..., description = "註冊成功")

class SuccessfulResponseForMember(BaseModel):
    data : UserRead = Field(..., description = "取得當前登入資訊")

class SuccessfulResponseForMemberBase(BaseModel):
    token : str = Field(..., description = "FHSTHSGHFtrhsthfghs")

class ErrorResponse(BaseModel):
    error : bool = Field(True, description = "指示是否為錯誤響應")
    message : str = Field(..., description = "錯誤訊息描述" , example="請按照情境提供對應的錯誤訊息")


# 購物車
class BookingAttraction(BaseModel):
    id: int = Field(... , example=10)
    name: str = Field(... , example="平安鐘")
    address: str = Field(... , example="臺北市大安區忠孝東路 4 段 1 號")
    images: str = Field(..., example="http://140.112.3.4/images/92-0.jpg")

class BookingRequest(BaseModel):
    attraction_id : int = Field(... , example = 1)
    date : str = Field(... , example = "2024-06-24")
    time : str = Field(... , example = "afternoon")
    price : int = Field(... , example = 2500)
    
class BookingDetails(BaseModel):
    attraction : BookingAttraction
    date : str = Field(... , example = "2024-06-24")
    time : str = Field(... , example = "afternoon")
    price : int = Field(... , example = 2500)
    
class BookingResponse(BaseModel):
    data : BookingDetails

class SuccessfulResponseForBookingDelete(BaseModel):
    ok : bool = Field(..., description = "刪除成功")


# 訂單與聯絡資訊
class Contact(BaseModel):
    name: str = Field(..., example="彭彭彭")
    email: str = Field(..., example="ply@ply.com")
    phone: str = Field(..., example="0912345678")

class Trip(BaseModel):
    attraction: BookingAttraction
    date: str = Field(..., example="2022-01-31")
    time: str = Field(..., example="afternoon")

class Order(BaseModel):
    price: int = Field(..., example=2000)
    trip: Trip
    contact: Contact

class PaymentOrderRequest(BaseModel):
    prime: str = Field(..., example="前端從第三方金流 TapPay 取得的交易碼")
    order: Order

class PaymentInfo(BaseModel):
    status: int = Field(..., example=0)
    message: str = Field(..., example="付款成功")

class PaymentOrderResponse(BaseModel):
    number: str = Field(..., example="20210425121135")
    payment: PaymentInfo


class PaymentOrderDetailsResponse(BaseModel):
    number: str
    price: int
    trip: BookingDetails
    contact: Contact
    status: int

# 登入相關Error Response
class ServiceError(BaseModel):
     error : bool
     status : int 
     error_code : str
     error_message :str

class ForbiddenError(ServiceError):
     error : bool = Field(True , description="錯誤")
     status : int = Field(403 , description = "403-禁止訪問")
     error_code : str = Field("403-001" , description = "403-禁止訪問")
     error_message : str = Field("無權限" , description = "該用戶並無權限")

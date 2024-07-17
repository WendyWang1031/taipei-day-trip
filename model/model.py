from pydantic import BaseModel, Field , field_validator
from typing import List , Optional 
from datetime import datetime


# 景點

class Attraction(BaseModel):
    id: int = Field(... , example=10)
    name: str = Field(... , example="平安鐘")
    category: str = Field(... , example="公共藝術")
    description: str = Field(... , example="平安鐘祈求大家的平安，這是為了紀念 921 地震週年的設計")
    address: str = Field(... , example="臺北市大安區忠孝東路 4 段 1 號")
    transport: str = Field(... , example="公車：204、212、212直")
    mrt: Optional[str] = Field(... , example="忠孝復興")
    lat: float = Field(... , example=25.04181)
    lng: float = Field(... , example=121.544814)
    image: List[str] = Field(..., example=["http://140.112.3.4/images/92-0.jpg"])

class MRTList(BaseModel):
	data: str = Field(..., description="捷運站名稱列表")

class SuccessfulResponseForAttraction(BaseModel):
	nextPage : Optional[int]= Field(None, example=2, description = "下一頁的頁碼，若無更多頁面則為 None")
	data : List[Attraction] = Field(..., description = "景點數據列表")

class SuccessfulResponseForID(BaseModel):
	data : Attraction = Field(..., description = "景點數據列表")


# 用戶
class UserReadDetail(BaseModel):
    id: str = Field(...,example=1)
    name: str = Field(... , example="彭彭彭")
    email: str = Field(... , example="ply@ply.com")				

class UserLoginRequest(BaseModel):
    email: str = Field(... , example="ply@ply.com")
    password: str = Field(... , example="12345678")
    
    @field_validator("*")
    def validate_login_space(cls , v):
        if isinstance(v,str) and (not v or v.isspace()):
             raise ValueError("The Login Input Value can not be blank.")
        return v

class UserCreateRequest(BaseModel):
    name: str = Field(... , example="彭彭彭")
    email: str = Field(... , example="ply@ply.com")
    password: str = Field(... , example="12345678")	
    
    @field_validator("*")
    def validate_register_space(cls , v):
        if isinstance(v,str) and (not v or v.isspace()):
             raise ValueError("The Register Input Value can not be blank.")
        return v
    
    @field_validator("email")
    def validate_email(cls , v):
        if "@" not in v :
             raise ValueError("Email must included '@'")
        return v

class SuccessfulResponseForMemberRegister(BaseModel):
    ok : bool = Field(..., description = "註冊成功")

class SuccessfulResponseForMember(BaseModel):
    data : UserReadDetail = Field(..., description = "取得當前登入資訊")

class SuccessfulResponseForMemberBase(BaseModel):
    token : str = Field(..., description = "FHSTHSGHFtrhsthfghs")

class ErrorResponse(BaseModel):
    error : bool = Field(True, description = "指示是否為錯誤響應")
    message : str = Field(..., description = "錯誤訊息描述" , example="請按照情境提供對應的錯誤訊息")


# 購物車
class BookingAttractionAndUser(BaseModel):
    id: int = Field(... , example=10)
    attraction_id : int = Field(... , example=1)
    date : str = Field(... , example = "2024-06-24")
    time : str = Field(... , example = "afternoon")
    price : int = Field(... , example = 2500)
    member_id : str = Field(... , example = "4gdr-u545-638-5sdf")
    status: int = Field(..., example=0)

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

    @field_validator("*")
    def validate_booking_requset_space(cls , v ,field):
        if isinstance(v,str) and (not v or v.isspace()):
            raise ValueError("f{field.name} Input Value can not be blank or just spaces.")
        if v is None:
            raise ValueError("f{field.name} Input Value can not be null.")
        return v
    
    @field_validator("date")
    def validate_date(cls , v):
        input_date = datetime.strptime(v,"%Y-%m-%d")
        current_date = datetime.now().date()
        if input_date.date() < current_date :
            raise ValueError("The date must be today or in the future.")
        return v
    
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

    @field_validator("phone")
    def validate_phone(cls , v):
         if not v.startswith("09"):
              raise ValueError("Phone number must start with 09")
         return v

class Trip(BaseModel):
    attraction: BookingAttraction
    date: str = Field(..., example="2022-01-31")
    time: str = Field(..., example="afternoon")

class Order(BaseModel):
    price: int = Field(..., example=2000)
    trip: Trip
    contact: Contact

    @field_validator("price")
    def validate_price(cls , v):
         if v <= 0:
              raise ValueError("Price must be greater than 0")
         return v

class PaymentOrderRequest(BaseModel):
    prime: str = Field(..., example="前端從第三方金流 TapPay 取得的交易碼")
    order: Order

    @field_validator("*")
    def validate_order_request_space(cls , v, field):
        if isinstance(v,str) and (not v or v.isspace()):
            raise ValueError("f{field.name} Input Value can not be blank or just spaces.")
        if v is None:
            raise ValueError("f{field.name} Input Value can not be null.")
        return v

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


# 會員頁面
class MemberDataRequest(BaseModel):
    name: Optional[str] = Field(None, example="彭彭彭")
    email: Optional[str] = Field(None, example="ply@ply.com")
    phone: Optional[str] = Field(None, example="0912345678")
    

    @field_validator("*")
    def validate_member_data_space(cls , v):
        if v is not None and (not v or v.isspace()):
             raise ValueError("The Register Input Value can not be blank.")
        return v
    
    @field_validator("email")
    def validate_member_data_email(cls , v):
        if v is not None and "@" not in v:
             raise ValueError("Email must included '@'")
        return v

    @field_validator("phone")
    def validate_member_data_phone(cls , v):
         if v is not None:
            if not v.startswith("09"):
                raise ValueError("Phone number must start with 09")
            if len(v) != 10:
                raise ValueError("Phone number must be 10 digits long")
         return v


class MemberData(BaseModel):
    name: str = Field(..., example="彭彭彭")
    email: str = Field(..., example="ply@ply.com")
    phone_number: Optional[str] = Field(None, example="0912345678")
    avatar: Optional[str]= Field(None, example="http://123456789/images/92-0.jpg")

class MemberGetResponse(BaseModel):
    ok: bool
    data: MemberData

class MemberUpdateResponse(BaseModel):
    ok: bool = Field(..., example="會員更新成功")

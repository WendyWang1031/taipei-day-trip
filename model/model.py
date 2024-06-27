from pydantic import BaseModel, Field
from typing import List 
from datetime import date as date_use

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

class BookingAttraction(BaseModel):
	id: int = Field(... , example=10)
	name: str = Field(... , example="平安鐘")
	address: str = Field(... , example="臺北市大安區忠孝東路 4 段 1 號")
	images: Image = Field(..., example="http://140.112.3.4/images/92-0.jpg")

class Booking(BaseModel):
	attraction_id : int = Field(... , example = 1)
	date : date_use = Field(... , example = "2024-06-24")
	time : str = Field(... , example = "afternoon")
	price : int = Field(... , example = 2500)
	

class BookingDatails(BaseModel):
	attraction : BookingAttraction
	date : date_use = Field(... , example = "2024-06-24")
	time : str = Field(... , example = "afternoon")
	price : int = Field(... , example = 2500)

class BookingResponse(BaseModel):
	data : BookingDatails

class SuccessfulResponseForBookingDelete(BaseModel):
	ok : bool = Field(..., description = "刪除成功")

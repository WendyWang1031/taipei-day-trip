from pydantic import BaseModel, Field

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

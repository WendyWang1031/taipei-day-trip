from jose import jwt , JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
security = HTTPBearer()

def create_access_token(data: dict , expires_delta: timedelta = timedelta(days = 7)):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes = 60)
	to_encode.update({"exp":expire})
	encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)
	return encoded_jwt

def decode_access_token(token: str):
	try:
		payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
		return payload
	except JWTError:
		raise HTTPException(status_code=403, detail="Invalid credentials")


def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
    user_info = decode_access_token(token.credentials)
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info
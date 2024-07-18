import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(message)s' , filename= 'app.log')

class LoggingMiddleware(BaseHTTPMiddleware):
    EXCLUDED_IPS = ['192.168.68.1', '52.89.39.93' , '127.0.0.1' ]
    
    async def dispatch(self , request , call_next):
        
        response: Response = await call_next(request)
        
        if request.client.host not in self.EXCLUDED_IPS:
            logging.info(
                f"Request IP: {request.client.host}, Method: {request.method}, URL: {request.url.path} | "
                f"Response Status: {response.status_code}"
            )
        
        return response

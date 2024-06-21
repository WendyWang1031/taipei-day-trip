import logging
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(message)s' , filename= 'app.log')

class LoggingMiddleware(BaseHTTPMiddleware):
	async def dispatch(self , request , call_next):
		logging.info(f'Request from IP: {request.client.host} to URL: {request.url.path}')
		response = await call_next(request)
		return response

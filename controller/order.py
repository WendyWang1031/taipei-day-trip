from service.security import security_get_current_user
from db.payment import *
from model.model import *
from fastapi import *
from fastapi import  Depends
from fastapi.responses import JSONResponse
import httpx
import json
from dotenv import load_dotenv
import os
from typing import Any

load_dotenv()
api_key = os.getenv("API_KEY")
partner_KEY = os.getenv("PARTNER_KEY")

async def create_order(
          current_user : dict = Depends(security_get_current_user) ,
          order_request : PaymentOrderRequest = Body(...)) -> JSONResponse :
    try:
        if current_user is None:
            error_response = ErrorResponse(error=True, message="User not authenticated")
            response = JSONResponse (
            status_code=status.HTTP_403_FORBIDDEN, 
            content=error_response.dict())
            return response
        
        member_id = current_user["id"]
        payment_result = await process_payment(order_request)
        if payment_result is None or payment_result["status"] != 0:
            error_response = ErrorResponse(error=True, message="status error")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        order_number = db_save_order(member_id , order_request)
        if  not order_number :
            error_response = ErrorResponse(error=True, message="Failed to create order")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response
    
        order_details = db_get_order_detail(order_number)
        if not order_details :
            error_response = ErrorResponse(error=True, message="Failed to create order")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response

        response_data = PaymentOrderResponse(
            number = order_details["number"],
            payment = PaymentInfo(
                    status = 0,
                    message = "付款成功"
            )
        )                     

        response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"data" : response_data.dict()}
        )
        return response
            
            
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
    

async def process_payment(payment_request: PaymentOrderRequest) ->  dict [str, Any] | JSONResponse:
    
    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    headers = {
        "Content-Type" : "application/json",
        "x-api-key" : api_key
    }

    details_data = [ {
             "item_id" : str(payment_request.order.trip.attraction.id),
             "item_name" : "Taipei day trip", 
             "item_quantity" : 1 , 
             "item_price" : payment_request.order.price,
        } ]
    details_string = json.dumps(details_data)

    body = {
        "prime" : payment_request.prime,
        "partner_key" : partner_KEY ,
        "merchant_id" : "WendyWang_GP_POS_3" , 
        "amount" : payment_request.order.price , 
        "details" :details_string,
        "cardholder" : {
                  "phone_number" : payment_request.order.contact.phone, 
                  "name" :  payment_request.order.contact.name, 
                  "email" :  payment_request.order.contact.email, 
        }
    }
    
    async with httpx.AsyncClient() as client :
        response = await client.post(url , json = body , headers = headers)
        
        if response.status_code == 200:
            data = response.json()
            # print("process_payment_data:" , data)
            if data.get("status") == 0 :
                return data
            else:
                return None
        else:
            error_response = ErrorResponse(error=True, message="HTTP error during payment processing")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response
        
async def get_order_detail_on_thankyou(order_number : str , current_user : dict = Depends(security_get_current_user)) -> JSONResponse :

    try:
        if current_user :
            member_id = current_user["id"]
            order_details = db_get_order_detail_for_thankyou(order_number , member_id)
                
            if order_details:

                response_data = PaymentOrderDetailsResponse(
                    number = order_details["number"],
                    price = order_details["price"],
                    trip = order_details["trip"],
                    contact = order_details["contact"],
                    status = order_details["status"]
                )                     

                response = JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {"data" : response_data.dict()}
                )
                return response
            else:
                error_response = ErrorResponse(error=True, message="No order found with the provided order number")
                response = JSONResponse (
                    status_code=status.HTTP_404_NOT_FOUND, 
                    content=error_response.dict())
                return response
        
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response

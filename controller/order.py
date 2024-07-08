from service.security import get_current_user
from db.payment import *
from model.model import *
from fastapi import *
from fastapi import  Depends
from fastapi.responses import JSONResponse
import httpx
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
partner_KEY = os.getenv("PARTNER_KEY")

async def create_order(
          current_user : dict = Depends(get_current_user) ,
          order_request : PaymentOrderRequest = Body(...)):
    try:
        if current_user :
            member_id = current_user["id"]
            payment_result = await process_payment(order_request)
            
            
            if payment_result and payment_result["status"] == 0:
                result = save_order(member_id , order_request)
                if result:
                    order_details = get_order_detail(member_id)
                    if order_details:

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
                else:
                    error_response = ErrorResponse(error=True, message="Failed to create order")
                    response = JSONResponse (
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        content=error_response.dict())
                    return response
            else:
                error_response = ErrorResponse(error=True, message="status error")
                response = JSONResponse (
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    content=error_response.dict())
                return response
        else:
                error_response = ErrorResponse(error=True, message="User not authenticated")
                response = JSONResponse (
                    status_code=status.HTTP_403_FORBIDDEN, 
                    content=error_response.dict())
                return response
    except Exception as e :
        error_response = ErrorResponse(error=True, message=str(e))
        response = JSONResponse (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content=error_response.dict())
        return response
    

async def process_payment(payment_request: PaymentOrderRequest):
    print("payment_request:" ,  payment_request)
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
    print("body:" ,  body)
    async with httpx.AsyncClient() as client :
        response = await client.post(url , json = body , headers = headers)
        print("status_code:" ,  response.status_code)
        if response.status_code == 200:
            data = response.json()
            print(data)
            return data
        else:
            error_response = ErrorResponse(error=True, message="Payment failed")
            response = JSONResponse (
                status_code=status.HTTP_400_BAD_REQUEST, 
                content=error_response.dict())
            return response
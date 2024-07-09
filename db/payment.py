from datetime import datetime
from typing import Any
import random

from model.model import BookingAttraction , BookingDetails , PaymentOrderRequest , Contact , PaymentOrderDetailsResponse
from db.booking import get_existing_booking 

import pymysql.cursors
from .connection import get_db_connection_pool

def generate_order_number(member_id : str):
    current_time = datetime.now()
    random_number = random.randint(100,999)
    order_number = f"{current_time.strftime("%Y%m%d%H%M%S")}{random_number}{member_id}"
    return order_number

def save_order(member_id : str, order_request : PaymentOrderRequest) -> bool:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    order_number = generate_order_number(member_id)
    user_booking = get_existing_booking(member_id)
    
    contact_phone = order_request.order.contact.phone
    
    try:

        if user_booking : 
            sql = """insert into payment 
            ( order_number , member_id , attraction_id , date , time ,  price , payment_time ,  status ) 
            values ( %s , %s , %s , %s , %s , %s , NOW() , %s)
            """
            cursor.execute(sql ,
                           (order_number , 
                            member_id , 
                            user_booking["attraction_id"] ,
                            user_booking["date"] ,
                            user_booking["time"] ,
                            user_booking["price"] ,
                            0))

            sql_contact = """insert into contact 
            (  member_id , phone_number ) 
            values ( %s , %s  )
            on DUPLICATE KEY UPDATE phone_number = VALUES (phone_number)
            """
            cursor.execute(sql_contact ,( member_id , contact_phone))
            
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting new payment: {e}") 
        return False
    finally:
        cursor.close()
        connection.close()

def get_order_detail(member_id : str) -> dict [str, Any] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        sql = """
        select 
        payment.order_number AS number , 
        payment.price,
        location.id AS attraction_id ,
        location.name AS attraction_name ,
        location.address AS address ,
        URL_file.images AS image ,
        payment.date , 
        payment.time , 
        member.name AS contact_name , 
        member.email AS contact_email , 
        contact.phone_number AS contact_phone , 
        payment.status

        FROM payment
        JOIN location on payment.attraction_id = location.id
        JOIN URL_file on location.id = URL_file.location_id
        JOIN contact on payment.member_id = contact.member_id
        JOIN member on member.id = contact.member_id
        
        where payment.member_id = %s
        """
        cursor.execute( sql , (member_id ,))
        order_details = cursor.fetchone()
        
        if order_details:
                
                formatted_date = order_details["date"].strftime("%Y-%m-%d")
                attraction = BookingAttraction(
                                id = order_details['attraction_id'],
                                name = order_details['attraction_name'],
                                address = order_details['address'],
                                images = order_details['image'],
                )

                trip_details = BookingDetails(
                            attraction = attraction,
                            date =  formatted_date,  
                            time = order_details['time'],
                            price = order_details['price'],
                )

                contact_details = Contact(
                    name = order_details['contact_name'] ,
                    email = order_details['contact_email'] ,
                    phone = order_details['contact_phone']
                )

                response = PaymentOrderDetailsResponse(
                    number = order_details['number'] ,
                    price = order_details['price'] ,
                    trip = trip_details,
                    contact = contact_details ,
                    status = order_details['status']
                )

                
                return response.dict()      
    
        else:
            return None

    except Exception as e:
        print(f"Error retrieving order details: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
    
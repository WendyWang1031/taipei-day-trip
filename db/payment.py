from datetime import datetime
from typing import Any
import random

from model.model import BookingAttraction , BookingDetails , PaymentOrderRequest , Contact , PaymentOrderDetailsResponse
from db.booking import db_get_existing_booking 

import pymysql.cursors
from .connection import get_db_connection_pool

## insert 4

## select 1.3.5
## select 1.3.4.5 = 13

## connection.begin()
## select 1.3.5
## select 1.3.5 = 9
## connection.commit()

def db_generate_order_number(member_id : str):
    current_time = datetime.now()
    random_number = random.randint(100,999)
    order_number = f"{current_time.strftime("%Y%m%d%H%M%S")}{random_number}{member_id}"
    return order_number

def db_save_order(member_id : str, order_request : PaymentOrderRequest) -> bool:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    order_number = db_generate_order_number(member_id)
    contact_phone = order_request.order.contact.phone
    
    try:
        connection.begin()

        # 查詢用戶預定行程
        check_user_booking_sql = "select * from booking where member_id = %s"
        cursor.execute(check_user_booking_sql , (member_id , ))
        user_booking = cursor.fetchone()

        if not user_booking:
            print("No booking found for user.")
            connection.rollback()
            return False
        
        # 創建訂單
        add_user_order_sql = """ insert into trip_order 
        ( order_number , member_id , attraction_id , date , time ,  price , payment_time ,  status ) 
        values ( %s , %s , %s , %s , %s , %s , NOW() , %s)
        """
        cursor.execute(add_user_order_sql ,
                        (order_number , 
                        member_id , 
                        user_booking["attraction_id"] ,
                        user_booking["date"] ,
                        user_booking["time"] ,
                        user_booking["price"] ,
                        0))

        # 更新電話號碼
        update_user_phone_sql = " update member set phone_number = %s where id = %s "
        cursor.execute(update_user_phone_sql , ( contact_phone , member_id ))

        # 刪除該用戶的預定行程
        delete_user_booking_sql = " delete from booking where member_id = %s "
        cursor.execute(delete_user_booking_sql , ( member_id , ))
            
        connection.commit()
        return order_number
    
    except Exception as e:
        print(f"Error inserting new order: {e}") 
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def db_get_order_detail(order_number : str) -> dict [str, Any] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        sql = """
        
        select 
        trip_order.order_number AS number , 
        trip_order.price,
        location.id AS attraction_id ,
        location.name AS attraction_name ,
        location.address AS address ,
        URL_file.images AS image ,
        trip_order.date , 
        trip_order.time , 
        member.name AS contact_name , 
        member.email AS contact_email , 
        member.phone_number AS contact_phone , 
        trip_order.status

        FROM trip_order
        JOIN location on trip_order.attraction_id = location.id
        JOIN URL_file on location.id = URL_file.location_id
        JOIN member on trip_order.member_id = member.id
        
        where trip_order.order_number = %s
        Order By trip_order.payment_time DESC 
        limit 1 ;

        """
        cursor.execute( sql , (order_number ,))
        order_details = cursor.fetchone()

        connection.commit()
        
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
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def db_get_order_detail_for_thankyou(order_number: str , member_id : str) -> dict [str, Any] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        sql = """
        
        select 
        trip_order.order_number AS number , 
        trip_order.price,
        location.id AS attraction_id ,
        location.name AS attraction_name ,
        location.address AS address ,
        URL_file.images AS image ,
        trip_order.date , 
        trip_order.time , 
        member.name AS contact_name , 
        member.email AS contact_email , 
        member.phone_number AS contact_phone , 
        trip_order.status

        FROM trip_order
        JOIN location on trip_order.attraction_id = location.id
        JOIN URL_file on location.id = URL_file.location_id
        JOIN member on trip_order.member_id = member.id
        
        where trip_order.member_id = %s and trip_order.order_number = %s
        Order By trip_order.payment_time DESC 
        limit 1 ;

        """
        cursor.execute( sql , (member_id , order_number))
        order_details = cursor.fetchone()

        connection.commit()
        
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
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()
from model.model import BookingAttraction , BookingDetails , Booking
import pymysql.cursors
from typing import Any
from .connection import get_db_connection_pool

def get_existing_booking( member_id : str ) -> dict [str, Any] | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "select * from booking where member_id = %s"
        cursor.execute( sql , (member_id ,))
        user_booking = cursor.fetchone()
        print("user_booking:" , user_booking)
        return user_booking
    except Exception as e:
        print(f"Error getting booking details: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
    

def db_save_or_update_booking(member_id : str  , booking_data : Booking) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    booking_existing = get_existing_booking(member_id)
    try:
        if booking_existing : 
            sql = """update booking 
                SET date = %s , time = %s , price = %s , attraction_id = %s 
                where member_id = %s
            """
            cursor.execute(sql ,(booking_data.date , booking_data.time , booking_data.price , booking_data.attraction_id , member_id))
            
        else:
            sql = "insert into booking ( attraction_id , date , time , price , member_id) values ( %s , %s , %s , %s , %s)"
            cursor.execute(sql ,( booking_data.attraction_id , booking_data.date , booking_data.time , booking_data.price , member_id))
        
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting new booking: {e}") 
        return False
    finally:
        cursor.close()
        connection.close()




def db_check_booking_detail(member_id : str ) -> BookingDetails | None :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        sql = """select location.id , location.name , location.address ,
                DATE_FORMAT(booking.date, '%%Y-%%m-%%d') AS formatted_date,
                booking.date , booking.time , booking.price ,
                URL_file.images AS image
        from booking 
        JOIN location on booking.attraction_id = location.id
        JOIN URL_file on location.id = URL_file.location_id
        where booking.member_id = %s;
        """
        cursor.execute( sql , (member_id ,))
        user_booking = cursor.fetchone()
        
        if user_booking:
                attraction = BookingAttraction(
                                id= user_booking['id'],
                                name= user_booking['name'],
                                address= user_booking['address'],
                                images= user_booking['image'],
                )

                details = BookingDetails(
                            attraction = attraction,
                            date =  user_booking['formatted_date'],  
                            time= user_booking['time'],
                            price= user_booking['price']
                )
                return details
        else:
            return None

    except Exception as e:
        print(f"Error retrieving booking details: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
    

def db_delete_booking_details(member_id : str ) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "delete from booking where member_id = %s "
        cursor.execute(sql , ( member_id , ))
        connection.commit()  

        if cursor.rowcount > 0:
            return True
        return False
        
    
    except Exception as e:
        print(f"Error deleting user's booking: {e}")
        return False

    finally:
        cursor.close()
        connection.close()


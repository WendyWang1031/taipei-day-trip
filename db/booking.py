import bcrypt
import pymysql.cursors
from .connection import get_db_connection_pool


def insert_new_booking(attractionId , date , time , price , member_id):
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "insert into booking ( attraction_id , date , time , price , member_id) values ( %s , %s , %s , %s , %s)"
        cursor.execute(sql ,( attractionId,  date , time , price , member_id))
        connection.commit()

        if cursor.rowcount>0:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error inserting new booking: {e}") 
        return False
    finally:
        cursor.close()
        connection.close()

def check_booking_detail(member_id):
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
            return {
                "attraction": {
                        "id": user_booking['id'],
                        "name": user_booking['name'],
                        "address": user_booking['address'],
                        "image": user_booking['image']
                    },
                    "date": user_booking['formatted_date'],  # Use formatted date
                    "time": user_booking['time'],
                    "price": user_booking['price']
            }
            

    except Exception as e:
        print(f"Error retrieving username: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
    

def delete_booking(email , password):
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "select id , name , email , password from member where email = %s "
        cursor.execute(sql , ( email , ))
        user_record = cursor.fetchone()
        stored_password = user_record['password']
        if user_record :
            if bcrypt.checkpw(password.encode('utf-8') , stored_password.encode('utf-8')):
                user_info = {}
                for key in user_record:
                    if key!= 'password':
                        user_info[key] =  user_record[key]
                return user_info
        return False
        
    
    except Exception as e:
        print(f"Error checking new user: {e}")
        return False

    finally:
        cursor.close()
        connection.close()


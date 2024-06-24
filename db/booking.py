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

def check_booking_detail(email):
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "select email from member where email = %s"
        cursor.execute( sql , (email,))
        user_email = cursor.fetchone()
    except Exception as e:
        print(f"Error retrieving username: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
    
    return user_email is not None   

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


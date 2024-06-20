import bcrypt
import uuid
import pymysql.cursors
from .connection import get_db_connection_pool


def insert_new_user(name , email , hashed_password):
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        user_id = str(uuid.uuid4())
        sql = "insert into member (id , name , email , password) values (%s , %s , %s , %s)"
        cursor.execute(sql ,(user_id,  name , email , hashed_password))
        connection.commit()

        if cursor.rowcount>0:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error inserting new user: {e}") 
        return False
    finally:
        cursor.close()
        connection.close()

def check_user_email_exists(email):
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

def check_email_password(email , password):
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


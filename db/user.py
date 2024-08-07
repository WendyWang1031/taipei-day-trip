import bcrypt
import uuid
import pymysql.cursors
from typing import Any
from .connection import get_db_connection_pool


def db_insert_new_user(name : str  , email : str  , hashed_password : str) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()

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
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def db_check_user_email_exists(email : str) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()

        sql = "select email from member where email = %s"
        cursor.execute( sql , (email,))
        user_email = cursor.fetchone()

        connection.commit()

    except Exception as e:
        print(f"Error retrieving username: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()
    
    return user_email is not None   

def db_check_email_password(email : str  , password : str ) -> dict [str, Any] | bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        sql = "select id , name , email , password from member where email = %s "
        cursor.execute(sql , ( email , ))
        user_record = cursor.fetchone()
        
        connection.commit()

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
        print(f"Error checking user , wrong email or password : {e}")
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()


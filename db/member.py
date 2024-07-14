from model.model import *
import pymysql.cursors
from typing import Any
from .connection import get_db_connection_pool


def db_get_member_data( member_id : str ) -> MemberData | None:
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        connection.begin()
        
        sql = "select id , name , email , phone_number , avatar from member where id = %s"
        cursor.execute( sql , (member_id ,))
        member_data = cursor.fetchone()
        
        connection.commit()
        
        return member_data
    
    except Exception as e:
        print(f"Error getting member data details: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

def db_save_or_update_member_data(member_id : str  , member_data : MemberDataRequest , avatar_url : str) -> bool :
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    try:
        connection.begin()
        
        sql = """update member 
            SET name = %s , email = %s , phone_number = %s , avatar = %s 
            where id = %s
        """
        cursor.execute(sql ,( member_data.name , member_data.email , member_data.phone , avatar_url , member_id))
    
        connection.commit()
        
        return True
    
    except Exception as e:
        print(f"Error inserting Member Data: {e}")
        connection.rollback() 
        return False
    finally:
        cursor.close()
        connection.close()
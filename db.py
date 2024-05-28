import pymysql.cursors
from dbutils.pooled_db import PooledDB
import pymysql

pool = PooledDB(
    creator = pymysql,
    maxconnections = 3,
    database = "taipei_day_trip",
    user = "root",
    password = "test",
    host = "localhost",
    port = 3306
)


def get_db_connection_pool():
    try:
        connetion = pool.connection()
        print("Database connect successful")
    except Exception as err:
        print(f"Database connection failed : {err}")
        raise
    return connetion

def get_attractions_for_pages(page , keyword = None):
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        offset = page * 12
        if keyword:
            sql = """select 
                    id , name , category , description , address , transport ,  mrt , lat , lng  
                    from location 
                    where name LIKE %s OR MRT = %s 
                    LIMIT 12 OFFSET %s
            """
            cursor.execute(sql , ('%' + keyword + '%' , keyword , offset))
        else:
            sql = """select 
                    id , name , category , description , address , transport ,  mrt , lat , lng 
                    from location 
                    LIMIT 12 OFFSET %s
            """
            cursor.execute(sql , (offset,))
        
        results = cursor.fetchall()

        for result in results:
            image_sql = "select images from URL_file where location_id = %s"
            cursor.execute(image_sql , (result["id"], ))
            images = cursor.fetchall()
            result["images"] = [img["images"] for img in images]
        return results
    
        # if results:
        #     print(f"Retrieved {len(results)} records successfully.")
        #     for result in results:
        #         print(result)
        # else:
        #     print("No records found.")
    
    except Exception as err:
        print(f'Error retrieving attractions : {err}')
        raise
    finally:
        cursor.close()
        connection.close()

def get_attractions_for_id(id):
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        if id is not None:
            sql = "select id , name , category , description , address , transport ,  mrt , lat , lng  from location where id = %s"
            cursor.execute(sql ,(id, ))
            result = cursor.fetchone()

            if result:
                image_sql = "select images from URL_file where location_id = %s"
                cursor.execute(image_sql , (result["id"], ))
                images = cursor.fetchall()
                result["images"] = [img["images"] for img in images]
            
            
            return result
        
        else:
            raise ValueError("No valid ID provided")
    
    except Exception as err:
        print(f'Error retrieving attractions : {err}')
        raise
    finally:
        cursor.close()
        connection.close()

def get_mrts():
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:

        sql = """select mrt
                    from location
                    where mrt is not null 
                    group by mrt  
                    order by count(*) DESC;
            """
        cursor.execute(sql ,)
        results = cursor.fetchall()
    
        mrt_list = [result["mrt"] for result in results]
        return mrt_list
        
    except Exception as err:
        print(f'Error retrieving mrts : {err}')
        raise
    finally:
        cursor.close()
        connection.close()

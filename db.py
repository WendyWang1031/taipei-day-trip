import pymysql.cursors
from dbutils.pooled_db import PooledDB
import pymysql
import bcrypt
import math
import uuid

pool = PooledDB(
    creator = pymysql,
    maxconnections = 3,
    database = "taipei_day_trip",
    user = "test",
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



def get_attractions_for_pages(page , keyword = None):
    connection = get_db_connection_pool()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        if keyword:
            count_sql = """SELECT COUNT(*) as total from location 
                        where name LIKE %s OR MRT = %s 
                        """
            cursor.execute(count_sql , ('%' + keyword + '%' , keyword ))
        else:
            count_sql = """SELECT COUNT(*) as total from location 
                        """
            cursor.execute(count_sql)
        total_records = cursor.fetchone()["total"]
        print(total_records)
        total_pages = math.ceil(total_records / 12)

        if page >= total_pages:
            page = max(0 , total_pages-1)
        offset = page * 12
        
        
        

        if keyword:
            sql = """select 
                    id , name , category , description , address , transport ,  mrt , 
                    CAST(lat AS DOUBLE) AS lat, CAST(lng AS DOUBLE) AS lng 
                    from location
                    where name LIKE %s OR MRT = %s 
                    LIMIT 12 OFFSET %s
            """
            cursor.execute(sql , ('%' + keyword + '%' , keyword  , offset))
        else:
            sql = """select 
                    id , name , category , description , address , transport ,  mrt , 
                    CAST(lat AS DOUBLE) AS lat, CAST(lng AS DOUBLE) AS lng
                    from location
                    LIMIT 12 OFFSET %s
            """
            cursor.execute(sql , (offset))
        
        # 從db取出景點的資訊
        locations = cursor.fetchall()
        
        # 取出該分頁的所有id
        location_ids =[]
        for location in locations:
            location_ids.append(location['id'])
        
        print(f"location_ids:{location_ids}")
        if not location_ids:
            return []
        

        # 將取出的景點id列表以,分開變成“字串”，代表12個數量的通位符的元素
        format_string = ','.join(["%s"] * len(location_ids))
        

        images_sql = f"""select location_id , GROUP_CONCAT(images SEPARATOR ',') AS image
                        FROM URL_file
                        where location_id IN ({format_string})
                        GROUP BY location_id
                    """
    
        # 將對應的景點id對應進去，取出對應的URL
        cursor.execute(images_sql , tuple(location_ids))
        images_results = cursor.fetchall()
        

        # 創建字典來映射locaion_id到images
        images_dict ={}
        for image_result in images_results:
            if 'image' in image_result:
                images_dict[image_result["location_id"]] = image_result["image"].split(",")
            else:
                images_dict[image_result["location_id"]] = []
        # print(f"images_dict:{images_dict}")
        # 把images分配給對應的locations
        for location in locations:
            if location["id"] in images_dict:
                location["image"] = images_dict[location["id"]]
            else:
                location["image"] = []
        
        return locations

    
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
            sql = "select id , name , category , description , address , transport ,  mrt ,  CAST(lat AS DOUBLE) AS lat, CAST(lng AS DOUBLE) AS lng  from location where id = %s"
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





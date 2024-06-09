import pymysql.cursors
from dbutils.pooled_db import PooledDB
import pymysql
import math

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

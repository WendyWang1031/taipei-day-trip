import json
import pymysql
import re

with open('data/taipei-attractions.json') as data_details:
    data = json.load(data_details)

data_results = data["result"]["results"]




db =  pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password = "test",
    db = "taipei_day_trip"
)

cursor = db.cursor()

insert_location_sql = """insert into location(_id,name,MRT,SERIAL_NO,address,RowNumber,rate,direction,
date,avBegin,avEnd,longitude,latitude,REF_WP,langinfo,CAT,MEMO_TIME,POI,idpt,description)
values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

insert_URL_file_sql = """insert into URL_file( location_id , url)
values(%s,%s)
"""

try:
    for item in data_results:
        cursor.execute(insert_location_sql , (
            item["_id"] , item["name"], item["MRT"], item["SERIAL_NO"] , item["address"],
            item["RowNumber"] , item["rate"] , item["direction"] , item["date"],
            item["avBegin"] , item["avEnd"] , item["longitude"] , item["latitude"],
            item["REF_WP"] , item["langinfo"] , item["CAT"] , item["MEMO_TIME"] , item["POI"],
            item["idpt"] , item["description"]
        ))
        if "file" in item:
            data_files = item["file"]
            urls_seperate = re.findall(r'https?://[^\s]+?\.(?:jpg|JPG|png|PNG)' , data_files)
        for url in urls_seperate:
            cursor.execute(insert_URL_file_sql , (
                item["_id"] , url
            ))

    db.commit()
except Exception as e:
    print("Error:" , e)
    db.rollback()
finally:
    cursor.close()
    db.close()






   
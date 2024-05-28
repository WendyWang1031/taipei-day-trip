import json
import pymysql
import re




db =  pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "test",
    password = "test",
    db = "taipei_day_trip"
)

cursor = db.cursor()

create_location_sql = """
CREATE TABLE IF NOT EXISTS location(
    id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    mrt VARCHAR(255),
    SERIAL_NO VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    RowNumber VARCHAR(255) NOT NULL,
    langinfo VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    rate BIGINT NOT NULL,
    transport TEXT NOT NULL,
    date DATETIME NOT NULL,
    avBegin DATETIME NOT NULL,
    avEnd DATETIME NOT NULL,
    lng VARCHAR(255) NOT NULL,
    lat VARCHAR(255) NOT NULL,
    REF_WP VARCHAR(255) NOT NULL,
    MEMO_TIME VARCHAR(255),
    POI VARCHAR(255) NOT NULL,
    idpt VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY (id)
);
"""

create_url_file_sql = """
CREATE TABLE IF NOT EXISTS URL_file(
    file_id BIGINT NOT NULL AUTO_INCREMENT,
    location_id BIGINT NOT NULL,
    images VARCHAR(255) NOT NULL,
    PRIMARY KEY (file_id),
    FOREIGN KEY (location_id) REFERENCES location(id)
);
"""

try:
    cursor.execute(create_location_sql)
    cursor.execute(create_url_file_sql)
    db.commit()
except Exception as e :
    print("Error creating tables:" , e)
    db.rollback()


with open('data/taipei-attractions.json') as data_details:
    data = json.load(data_details)

data_results = data["result"]["results"]

insert_location_sql = """insert ignore into location(id,name,mrt,SERIAL_NO,address,RowNumber,rate,transport,
date,avBegin,avEnd,lng,lat,REF_WP,langinfo,category,MEMO_TIME,POI,idpt,description)
values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

insert_URL_file_sql = """insert ignore into URL_file( location_id , images)
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






   
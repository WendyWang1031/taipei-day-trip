
import pymysql


db =  pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "test",
    password = "test",
    db = "taipei_day_trip"
)

cursor = db.cursor()

create_member_table_sql = """
        CREATE TABLE IF NOT EXISTS member (
        id char(36) primary key,
        name varchar(255) not null,
        password varchar(255) not null,
        email varchar(255) unique not null
);
"""


try:
    cursor.execute("BEGIN;")
    cursor.execute(create_member_table_sql)
    db.commit()
except Exception as e :
    print("Error creating tables:" , e)
    db.rollback()








   
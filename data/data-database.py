
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("connection_db_user")
password = os.getenv("connection_db_password")


db =  pymysql.connect(
    host = "localhost",
    port = 3306,
    user = user,
    password = password,
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

alter_member_table_sql = """
        alter table member 
        add column phone_number varchar(255);
"""

alter_member_table_add_avatar_sql = """
        alter table member 
        add column avatar varchar(255);
"""

create_booking_table_sql = """
        CREATE TABLE IF NOT EXISTS booking (
        id int AUTO_INCREMENT primary key,
        attraction_id BIGINT not null,
        date DATE not null,
        time varchar(255) not null,
        price int not null,
        member_id char(36) not null,
        FOREIGN KEY (attraction_id) REFERENCES location(id),
        FOREIGN KEY (member_id) REFERENCES member(id)
);
"""

alter_booking_table_unique_sql = """
        ALTER TABLE booking
        ADD CONSTRAINT unique_member_id UNIQUE (member_id);

"""



create_order_table_sql = """
        CREATE TABLE IF NOT EXISTS trip_order (
        id int AUTO_INCREMENT primary key,
        order_number varchar(255) not null,
        member_id varchar(255) not null,
        attraction_id BIGINT not null,
        date DATE not null,
        time varchar(255) not null,
        price int not null,
        payment_time Datetime,
        status int not null,
        FOREIGN KEY (member_id) REFERENCES member(id),
        FOREIGN KEY (attraction_id) REFERENCES location(id)
);
"""
alter_order_table_unique_sql = """
        ALTER TABLE order
        ADD CONSTRAINT unique_order_number UNIQUE (order_number);

"""


try:
    cursor.execute("BEGIN;")

    cursor.execute(create_member_table_sql)
    
    cursor.execute(alter_member_table_sql)
    cursor.execute(alter_member_table_add_avatar_sql)

    cursor.execute(create_booking_table_sql)
    cursor.execute(alter_booking_table_unique_sql)
    
    cursor.execute(create_order_table_sql)
    cursor.execute(alter_order_table_unique_sql)

    db.commit()
except Exception as e :
    print("Error creating tables:" , e)
    db.rollback()








   
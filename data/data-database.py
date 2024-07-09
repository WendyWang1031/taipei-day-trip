
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

alter_member_table_sql = """
        alter table member
        add column phone_number varchar(255);
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



try:
    cursor.execute("BEGIN;")

    cursor.execute(create_member_table_sql)
    cursor.execute(alter_member_table_sql)

    cursor.execute(create_booking_table_sql)
    cursor.execute(create_order_table_sql)

    db.commit()
except Exception as e :
    print("Error creating tables:" , e)
    db.rollback()








   
import pymysql
from dbutils.pooled_db import PooledDB

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

import time
import pymysql
import os

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_NAME = os.getenv("MYSQL_NAME")

while True:
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_NAME
        )
        conn.close()
        print("✅ MySQL listo")
        break

    except Exception as e:
        print("⏳ Esperando MySQL...", e)
        time.sleep(3)
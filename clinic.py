import mysql.connector
from datetime import datetime, timedelta, date
import config 

def create_connection():
    try: 
        return mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None










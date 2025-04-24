import os
from dotenv import load_dotenv
import psycopg2


# Connect to database
def load_config():
    """ Connect to the PostgreSQL database server """
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    config = {}
    config["host"] = DB_HOST
    config["database"] = DB_NAME
    config["user"] = DB_USER
    config["password"] = DB_PASSWORD
    return config

def get_conn():
    config = load_config()
    try:
        conn = psycopg2.connect(**config)
        return conn
    except Exception as e:
        print("Error connecting the database:", e)
        return None

def close_conn(conn):
    if conn:
        conn.close()

if __name__ == '__main__':
    conn = get_conn()

import sys
import os

import psycopg2
from .connection import load_config

base_dir = os.path.dirname(os.path.abspath(__file__))
sql_path = os.path.join(base_dir, 'ddl.sql')
def init_database():
    """ Create tables in the PostgreSQL database"""
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(sql_path, 'r') as commands: # read ddl.sql file
                    cur.execute(commands.read())
                    cur.close()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally: 
        if conn:
            conn.close()

if __name__ == '__main__':
    init_database()
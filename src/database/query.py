import sys
import os
# Add the folder containing the Python file to sys.path
sys.path.append(os.path.abspath("./src/database/config"))

import psycopg2
from config import load_config

def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = """
        SELECT * FROM IBNR;
        """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                cur.execute(commands)
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    create_tables()
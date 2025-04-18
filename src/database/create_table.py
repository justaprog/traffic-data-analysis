import sys
import os

import psycopg2
from config.config import load_config

def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = """
    CREATE TABLE Departure (
        departure_id SERIAL PRIMARY KEY,
        departure_time TIMESTAMP,
        planned_platform VARCHAR(50),
        path TEXT,
        evaNo INT,
        FOREIGN KEY (evaNo) REFERENCES IBNR(evaNo)
    )
        """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                try:
                    cur.execute("SELECT * FROM Departure")
                except:
                    print("WTF?")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    create_tables()
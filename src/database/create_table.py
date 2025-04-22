import sys
import os

import psycopg2
from .config import load_config

def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = """
CREATE TABLE IF NOT EXISTS IBNR(
    evaNo INT PRIMARY KEY,
    station VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS Arrival (
    arrival_id SERIAL PRIMARY KEY,
    arrival_time TIMESTAMP,
    line VARCHAR(50),
    planned_platform VARCHAR(50),
    path TEXT,
    evaNo INT,
    FOREIGN KEY (evaNo) REFERENCES IBNR(evaNo),
    UNIQUE(arrival_time,path)
);
CREATE TABLE IF NOT EXISTS Departure (
    departure_id SERIAL PRIMARY KEY,
    departure_time TIMESTAMP,
    line VARCHAR(50),
    planned_platform VARCHAR(50),
    path TEXT,
    evaNo INT,
    FOREIGN KEY (evaNo) REFERENCES IBNR(evaNo),
    UNIQUE(departure_time,path)
)


        """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands)
                cur.close()

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally: 
        if conn:
            conn.close()

if __name__ == '__main__':
    create_tables()
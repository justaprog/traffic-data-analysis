import sys
import os

import psycopg2
from .config.config import load_config

def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = """
DROP TABLE IF EXISTS Departure;
DROP TABLE IF EXISTS Arrival;
DROP TABLE IF EXISTS IBNR;      
CREATE TABLE IBNR(
    evaNo INT PRIMARY KEY,
    station VARCHAR(255)
);
CREATE TABLE Arrival (
    arrival_id SERIAL PRIMARY KEY,
    arrival_time TIMESTAMP,
    planned_platform VARCHAR(50),
    path TEXT,
    evaNo INT,
    FOREIGN KEY (evaNo) REFERENCES IBNR(evaNo)
);
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
                cur.execute(commands)

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    create_tables()
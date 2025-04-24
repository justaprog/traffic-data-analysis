CREATE TABLE IF NOT EXISTS IBNR(
    evaNo INT PRIMARY KEY,
    station VARCHAR(255) UNIQUE
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
);
CREATE TABLE IF NOT EXISTS Distance (
    distance_id SERIAL PRIMARY KEY,
    evaNo_1 INT,
    evaNo_2 INT,
    distance DECIMAL(10,2),
    UNIQUE(evaNo_1,evaNo_2),
    FOREIGN KEY (evaNo_1) REFERENCES IBNR(evaNo),
    FOREIGN KEY (evaNo_2) REFERENCES IBNR(evaNo)
);
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
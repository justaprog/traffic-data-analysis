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
    FOREIGN KEY (evaNo) REFERENCES IBNR(evaNo)
);
CREATE TABLE IF NOT EXISTS Departure (
    departure_id SERIAL PRIMARY KEY,
    departure_time TIMESTAMP,
    line VARCHAR(50),
    planned_platform VARCHAR(50),
    path TEXT,
    evaNo INT,
    FOREIGN KEY (evaNo) REFERENCES IBNR(evaNo)
)
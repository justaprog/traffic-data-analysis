CREATE TABLE IBNR(
    eva INT,
    station VARCHAR(255)
);
CREATE TABLE Stops (
    stop_id VARCHAR(255) PRIMARY KEY,
    arrival_time TIMESTAMP,
    departure_time TIMESTAMP,
    planned_platform VARCHAR(50),
    path TEXT,
    IBNR INT REFERENCES IBNR(eva)
);

INSERT INTO IBNR VALUES (8000105, 'Frankfurt(Main)Hbf');
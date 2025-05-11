CREATE TABLE IF NOT EXISTS ibnrs(
    evaNo INT PRIMARY KEY,
    station VARCHAR(255) UNIQUE
);
CREATE TABLE IF NOT EXISTS arrivals (
    arrival_id VARCHAR(128) PRIMARY KEY,
    arrival_planned_time TIMESTAMP,
    arrival_changed_time TIMESTAMP,
    line VARCHAR(50),
    planned_platform VARCHAR(50),
    path TEXT,
    evaNo INT,
    FOREIGN KEY (evaNo) REFERENCES ibnrs(evaNo),
    UNIQUE(arrival_time,path)
);
CREATE TABLE IF NOT EXISTS departures (
    departure_id SERIAL PRIMARY KEY,
    departure_planned_time TIMESTAMP,
    departure_changed_time TIMESTAMP,
    line VARCHAR(50),
    planned_platform VARCHAR(50),
    path TEXT,
    evaNo INT,
    FOREIGN KEY (evaNo) REFERENCES ibnrs(evaNo),
    UNIQUE(departure_time,path)
);
CREATE TABLE IF NOT EXISTS distances (
    distance_id SERIAL PRIMARY KEY,
    evaNo_1 INT,
    evaNo_2 INT,
    distance DECIMAL(10,2),
    UNIQUE(evaNo_1,evaNo_2),
    FOREIGN KEY (evaNo_1) REFERENCES ibnrs(evaNo),
    FOREIGN KEY (evaNo_2) REFERENCES ibnrs(evaNo)
);
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    user_name VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
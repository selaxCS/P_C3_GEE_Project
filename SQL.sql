DROP TABLE IF EXISTS Readings;
DROP TABLE IF EXISTS Sensors;


-- 1. Taula per definir els tipus de sensors
CREATE TABLE  Sensors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- 2. Taula per emmagatzemar les lectures associades a un sensor
CREATE TABLE Readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL,
    value REAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sensor
      FOREIGN KEY(sensor_id) 
      REFERENCES Sensors(id)
);

-- Inserció inicial
INSERT INTO Sensors (name) VALUES 
('temperature'), 
('humidity'), 
('irrigation'), 
('rain_gauge')
DROP TABLE IF EXISTS readings;
DROP TABLE IF EXISTS sensors;

-- 1. Table to define the sensor types
CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- 2. Table to store the readings
CREATE TABLE readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL,
    value REAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sensor
      FOREIGN KEY(sensor_id) 
      REFERENCES sensors(id)
);

-- Initial insertion
INSERT INTO sensors (name) VALUES 
('temperature'), 
('humidity'), 
('irrigation'), 
('rain_gauge');
import socket
import json
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

# SQLAlchemy database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sensors_data.db") # Added fallback for testing
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define the 'Sensor' table schema
class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    # Define relationship with readings
    readings = relationship("Reading", back_populates="sensor")

# Define the 'Reading' table schema to store sensor values
class Reading(Base):
    __tablename__ = 'readings'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    # Establish link back to the parent sensor
    sensor = relationship("Sensor", back_populates="readings")

# Create all tables in the database
Base.metadata.create_all(engine)

def save_to_database(sensor_name, value):
    session = SessionLocal()
    try:
        sensor = session.query(Sensor).filter_by(name=sensor_name).first()
        if not sensor:
            sensor = Sensor(name=sensor_name)
            session.add(sensor)
            session.commit()
        
        new_reading = Reading(sensor_id=sensor.id, value=value)
        session.add(new_reading)
        session.commit()
    except Exception as e:
        print(f"Error saving to DB: {e}")
        session.rollback()
    finally:
        session.close() # Always close the session

def run_receiver():

    HOST = '127.0.0.1'
    PORT = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}...")
        
        # Dictionary to map incoming JSON keys to expected value keys
        value_key = {
            "temperature": "Temperature",
            "humidity": "Humidity",
            "irrigation": "Water Flow",
            "rain_gauge": "Precipitation"
        }

        while True:
            # Accept an incoming connection from the client
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                if not data: continue
                
                # Decode and parse the incoming JSON payload
                sensors_readings = json.loads(data.decode('utf-8'))
                
                # Iterate through the received sensor data
                for sensor_name, sensor_data in sensors_readings.items():
                    if sensor_name in value_key:
                        name_key = value_key[sensor_name]
                        value_ac = sensor_data[name_key]
             
                        # Save the extracted value to the DB
                        save_to_database(sensor_name, value_ac)
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Data processed from {addr} and saved to DB.")

if __name__ == "__main__":
    run_receiver()
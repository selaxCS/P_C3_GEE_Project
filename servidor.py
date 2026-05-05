import socket
import json
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

# SQLAlchemy configuration
DATABASE_URL =os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    readings = relationship("Reading", back_populates="sensor")

class Reading(Base):
    __tablename__ = 'readings'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sensor = relationship("Sensor", back_populates="readings")

Base.metadata.create_all(engine)

# ORM function to save data
def SaveToDatabase(sensor_name, value):
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
        session.close()

def run_receiver():
    HOST = '127.0.0.1'
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening to {HOST}:{PORT}...")
        

        claus_valors = {
            "temperature": "Temperature",
            "humidity": "Humidity",
            "irrigation": "Water Flow",
            "rain_gauge": "Precipitation"
        }

        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                if not data: continue
                
                sensors_readings = json.loads(data.decode('utf-8'))
                
                for sensor_name, sensor_data in sensors_readings.items():
                    
                    if sensor_name in claus_valors:
                        
                        name_key = claus_valors[sensor_name]
                        value_ac = sensor_data[name_key]
             
                        SaveToDatabase(sensor_name, value_ac)
                
                print(f"Data processed from {addr} and saved to the database.")
if __name__ == "__main__":
    run_receiver()
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

# Database Connection Logic
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sensors_data.db")


if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
   
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ORM Models
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

# Schema Synchronization
Base.metadata.create_all(engine)
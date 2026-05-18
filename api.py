
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
from contextlib import asynccontextmanager
import uvicorn
import logging

from servidor import SessionLocal, Reading, Sensor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- SCHEMAS ---

class OrderEnum(str, Enum):
    ascendant = "ascendant"
    descendant = "descendant"

class ReadingCreate(BaseModel):
    sensor: str = Field(..., example="new_sensor_name")
    value: float = Field(..., example=10.5)

class ReadingSchema(BaseModel):
    id: int
    sensor: str
    value: float
    timestamp: datetime

    class Config:
        from_attributes = True

# --- DYNAMIC SCHEMA HELPER ---

def update_openapi_schema(app: FastAPI):

    db = SessionLocal()
    try:
        # Fetch existing sensors to create the dropdown menu 
        db_sensors = db.query(Sensor.name).all()
        sensor_names = [s[0] for s in db_sensors]
        
        if sensor_names:
            # Get the existing schema or generate a new one
            schema = app.openapi()
            for path in schema["paths"].values():
                for method in path.values():
                    for param in method.get("parameters", []):
                        # Find the parameter named 'Sensor'
                        if param["name"] == "Sensor":
                            param["schema"]["enum"] = sensor_names
            app.openapi_schema = schema
            logger.info(f"Dynamic dropdown populated with: {sensor_names}")
    except Exception as e:
        logger.error(f"Startup error (dropdown generation failed): {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    update_openapi_schema(app)
    yield

app = FastAPI(
    title="Dynamic Sensor API",
    description="API that updates its documentation dynamically as new sensors are added.",
    version="2.1.0",
    lifespan=lifespan
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- POST ENDPOINT  ---

@app.post("/api/data", response_model=ReadingSchema, status_code=201)
def create_reading(reading_data: ReadingCreate, db: Session = Depends(get_db)):
    # Check/Create sensor
    sensor = db.query(Sensor).filter(Sensor.name == reading_data.sensor).first()
    
    new_sensor_created = False
    if not sensor:
        sensor = Sensor(name=reading_data.sensor)
        db.add(sensor)
        db.commit()
        db.refresh(sensor)
        new_sensor_created = True
        logger.info(f"New sensor registered: {sensor.name}")

    # Create reading
    new_reading = Reading(sensor_id=sensor.id,value=reading_data.value,timestamp=datetime.utcnow()
    )
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)

    
    if new_sensor_created:
        update_openapi_schema(app)
    
    return {
        "id": new_reading.id,
        "sensor": sensor.name,
        "value": new_reading.value,
        "timestamp": new_reading.timestamp
    }

# --- GET ENDPOINT  ---

@app.get("/api/data", response_model=List[ReadingSchema])

def get_sensor_data(
    
    sensor: Optional[str] = Query(None, alias="Sensor"),
    order: OrderEnum = Query(OrderEnum.ascendant, alias="Order"),
    init_date: Optional[date] = Query(None, alias="Init date Ex: YYYY-MM-DD"),
    end_date: Optional[date] = Query(None, alias="End date Ex: YYYY-MM-DD"),
    db: Session = Depends(get_db)
):

    try:
        query = db.query(Reading).join(Sensor)

        if sensor:
            
            query = query.filter(Sensor.name == sensor)
            
        if init_date:
            query = query.filter(Reading.timestamp >= datetime.combine(init_date, datetime.min.time()))
        if end_date:
            query = query.filter(Reading.timestamp <= datetime.combine(end_date, datetime.max.time()))

        # Order by value as requested by the user
        if order == OrderEnum.descendant:
            query = query.order_by(Reading.value.desc())
        else:
            query = query.order_by(Reading.value.asc())

        results = query.all()
        return [
            {
                "id": r.id,
                "sensor": r.sensor.name,
                "value": r.value,
                "timestamp": r.timestamp
            } for r in results
        ]
    except Exception as e:
        logger.error(f"GET Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Database access failed.")

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
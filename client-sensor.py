import random
import time
from datetime import datetime

import requests  # Replaces socket for API communication 


API_URL = "http://127.0.0.1:8000/api/data"

class Sensor:

    def __init__(self):
        # Initialize sensor data with random baseline values
        self.temp = random.uniform(-2, 40)
        self.hum = random.uniform(0, 100)
        self.flow = random.uniform(0, 1)
        self.rain = random.uniform(0, 1)
    
    def get_timestamp(self):
        # Generate the current timestamp as a formatted string
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    def update_sensor_values(self):

        self.temp = max(0, min(40, self.temp + random.uniform(-0.5, 0.5)))
        self.hum = max(0, min(100, self.hum + random.uniform(-0.5, 0.5)))
        self.flow = max(0, self.flow + random.uniform(-0.05, 0.05))
        self.rain = max(0, min(1, self.rain + random.uniform(-0.02, 0.02)))

    def generate_sensor_data(self):

        self.update_sensor_values()
        
        return {
            "temperature": {
                "value": round(self.temp, 2),
                "Timestamp": self.get_timestamp()
            },
            "humidity": {
                "value": round(self.hum, 2),
                "Timestamp": self.get_timestamp()
            },
            "irrigation": {
                "value": round(self.flow, 2),
                "Timestamp": self.get_timestamp()
            },
            "rain_gauge": {
                "value": round(self.rain, 2),
                "Timestamp": self.get_timestamp()
            }
        }

def run_sender():

    sensor1 = Sensor()

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting API-based data transmission...")

    while True:
        # Generate the structured batch of sensor data
        data_batch = sensor1.generate_sensor_data()
        

        for sensor_name, details in data_batch.items():
            payload = {
                "sensor": sensor_name,
                "value": details["value"]
            }
            
            try:
                # Perform the HTTP POST request as mandated 
                response = requests.post(API_URL, json=payload, timeout=5)
                
                if response.status_code == 201:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {sensor_name} stored successfully.")
                else:
                    print(f"Error: API returned status {response.status_code} for {sensor_name}.")
                    
            except requests.exceptions.RequestException as e:
                print(f"Connection Error: Could not reach the API server at {API_URL}.")

        
        time.sleep(3)

if __name__ == "__main__":
    run_sender()
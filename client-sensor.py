import random
import time
from datetime import datetime
import json
import socket

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

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
                "Temperature": round(self.temp, 2),
                "Timestamp": self.get_timestamp()
            },
            "humidity": {
                "Humidity": round(self.hum, 2),
                "Timestamp": self.get_timestamp()
            },
            "irrigation": {
                "Water Flow": round(self.flow, 2),
                "Timestamp": self.get_timestamp()
            },
            "rain_gauge": {
                "Precipitation": round(self.rain, 2),
                "Timestamp": self.get_timestamp()
            }
        }

def run_sender():

    sensor1 = Sensor()

    while True:
        try:
            # Create a socket and connect to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                
                # Generate new data and encode it as JSON
                data = sensor1.generate_sensor_data()
                message = json.dumps(data).encode('utf-8')
                
                # Send the encoded data payload
                s.sendall(message)
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Data sent correctly.")
                
        except ConnectionRefusedError:
            print("Error: Could not connect to the receiver server.")

        
        time.sleep(3)

if __name__ == "__main__":
    run_sender()
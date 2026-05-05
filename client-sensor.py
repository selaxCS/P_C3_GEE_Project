import random
import time
from datetime import datetime
import json
import socket

HOST = '127.0.0.1'
PORT = 65432

class sensor:

    def __init__(self):
        
        self.temp = random.uniform(-2,40)
        self.hum = random.uniform(0,100)
        self.flow = random.uniform(0,1)
        self.rain = random.uniform(0,1)
    
    def Timestamp(self):

        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    def SensorAct(self):
        
        self.temp = max(0,min(40,self.temp+random.uniform(-0.5, 0.5)))
        self.hum = max(0, min(100, self.hum + random.uniform(-0.5, 0.5)))
        self.flow = max(0, self.flow + random.uniform(-0.05, 0.05))
        self.rain = max(0,min(1,self.rain + random.uniform(-0.02, 0.02)))


    def GenSensor(self):
        self.SensorAct()
        
        return {
            "temperature": {
                "Temperature": round(self.temp, 2),
                "Timestamp": self.Timestamp()
            },
            "humidity": {
                "Humidity": round(self.hum, 2),
                "Timestamp": self.Timestamp()
            },
            "irrigation": {
                "Water Flow": round(self.flow, 2),
                "Timestamp": self.Timestamp()
            },
            "rain_gauge": {
                "Precipitation": round(self.rain, 2),
                "Timestamp": self.Timestamp()
            }
        }


def run_sender():

    sensor1= sensor()

    while True:

        try:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                
                data = sensor1.GenSensor()
                
                message = json.dumps(data).encode('utf-8')
                s.sendall(message)
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Data sent correctly.")
                
        except ConnectionRefusedError:
            print("Error: It is not possible to connect to the receiver.")


        time.sleep(3)


if __name__ == "__main__":
    run_sender()
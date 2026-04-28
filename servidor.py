import socket
import json
import os
from datetime import datetime


HOST = '127.0.0.1'
PORT = 65432

def SaveJson(sensor_name, data):

    today_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_date}.json"

    base_path = os.path.join(sensor_name, today_date)

    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"Directories created: {base_path}")

    full_path = os.path.join(base_path, filename)

    file_data = []

    if os.path.exists(full_path):
        try:
            with open(full_path, 'r') as f:
                file_data = json.load(f)
        except :
            file_data = []

    file_data.append(data)

    with open(full_path, 'w') as file:
        json.dump(file_data, file, indent=4)

def run_receiver():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening to {HOST}:{PORT}...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                if not data:
                    break
                
                sensors_readings = json.loads(data.decode('utf-8'))
                
                for sensor_name, reading in sensors_readings.items():
                    SaveJson(sensor_name, reading)
                
                print(f"Data received from {addr} and stored.")

if __name__ == "__main__":
    run_receiver()

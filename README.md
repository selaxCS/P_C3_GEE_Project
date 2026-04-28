# Project 1: Sensor Data Extraction and Socket Communication

**Subject:** Programming and Communications 3
**Degree:** Electronic Engineering
**Students:** Alexandru Anton Catrinoi Sfarghie
**Date:** April 28, 2026

## Task 1: Sensor Mocking
### Brief Description
The objective of this task is to create a digital mock-up of four different sensors (Temperature, Humidity, Irrigation, and Rain Gauge) using Python. These sensors must generate data with specific decimal precision and timestamps in a standardized format.

### Solution Description
A `sensor` class was implemented to simulate the behavior of the field devices.
- **Sensor Logic:** Each sensor (Temperature, Humidity, Water Flow, and Precipitation) is initialized with a random value and updated every cycle using the `SensorAct()` and `GenSensor()` method to simulate natural fluctuations.
- **Data Format:** All values are rounded to 2 decimal places. The timestamp follows the `YYYY-mm-ddTHH:MM:SS` format as required.
- **Output:** The `GenSensor()` method returns a structured dictionary containing the readings for all four sensors, ready for serialization.

## Task 2: Timed Process and Socket Communication
### Brief Description
This task involves creating a pipeline using standard Python sockets to send the generated sensor data from an intermediary device (sender) to a final server (receiver) every 3 seconds.

### Solution Description
The communication is handled through a TCP/IP socket connection.
- **Sender Implementation:** The `run_sender()` function initializes the sensor object and enters a loop. Every 3 seconds, it establishes a connection to `127.0.0.1:65432`, sends the JSON-encoded data, and closes the connection.
- **Error Handling:** A `try-except` block is included to catch `ConnectionRefusedError` in case the server is not reachable, ensuring the client doesn't crash.

## Task 3: Data Storage
### Brief Description
The final device acts as a receiver that must store the incoming data into readable JSON files. Data must be organized by sensor type and by day to act as a basic database.

### Solution Description
The server listens for incoming connections and processes the received data packets.
- **Directory Structure:** The server automatically creates a directory structure (e.g., `sensor_name/YYYY-MM-DD/`) to keep the data organized.
- **JSON Management:** The `SaveJson` function checks if a file for the current day already exists (`%Y-%m-%d.json`). If it does, it loads the existing data, appends the new reading, and saves it back. If not, it creates a new file.
- **Concurrency:** The server is designed to handle individual connections sequentially, processing all sensor readings included in the received message.

---

## Resources Used
- **DateTime Library:** Used for generating timestamps and managing file naming conventions.
- **Random Library:** Used for generating simulated sensor values.
- **JSON Library:** Used for data serialization between the client and server, and for persistent storage.
- **Socket Library:** Used for implementing the TCP communication pipeline.
- **OS Library:** Used for directory management and file path operations.

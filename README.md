# Project 4: Storage Through API

**Subject:** Programming and Communications III  
**Degree:** Electronic Engineering  
**Student Name:** Alexandru Anton Catrinoi Sfarghie  
  


## Task 1 & 2: API Data Insertion 

### Brief description of the task 
The main goal of Project 4 is to centralize data operations within the API. Previously, data was inserted into the database through a dedicated socket server. In this project, we need to: 
1. **Task 1**: Implement `POST` endpoints in the FastAPI application to handle data insertion. 
2. **Task 2**: Change the sensor simulation (client) to use the `requests` library for sending data to the API using HTTP POST requests instead of raw sockets. 
### Brief description of the solution 
The solution updates `api.py` to include a new route `@app.post("/api/data")`. This endpoint receives a JSON payload that represents a sensor reading, validates it using Pydantic with the `ReadingCreate` schema, and saves it to the PostgreSQL database using SQLAlchemy. The `client-sensor.py` has been completely rewritten to remove socket logic. It now goes through generated sensor data and sends individual HTTP POST requests to the API while handling success and error statuses.


### Table Definitions

| Table Name | Columns | Type | Constraints | Descriptions |
| :--- | :--- | :--- | :--- | :--- |
| **sensors** | id | Int | Primary Key, Auto-gen | Unique identifier for the sensor. |
| | name | String | Unique, Not Null | Name of the sensor type (e.g., temperature). |
| **readings** | id | Int | Primary Key, Auto-gen | Unique identifier for the reading. |
| | sensor_id | Int | Foreign Key (sensors.id) | Link to the sensor table. |
| | value | Float | Not Null | Numerical value recorded. |
| | timestamp | DateTime | Default: Now | Date and time of the record. |

### Endpoint Definitions

| Verb | Endpoint | Params | Body | Return |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/api/data` | `Sensor` (Optional)<br>`Order`<br>`Init date`<br>`End date` | None | JSON list of readings with sensor names and timestamps. |
| **POST** | `/api/data` | None | `{"sensor": "str", "value": 0.0}` | The created reading object or an error message. |

## Previous Tasks Modifications

### Project 3 to Project 4 Transition
The following structural changes were made to evolve the project from a read-only API to a full data management service:

* **Removal of Socket Communication**: The socket-based `servidor.py` receiver logic was deprecated. Data insertion is now handled directly by the FastAPI web server.
* **Client Refactoring**: The client-side code transitioned from sending byte-encoded JSON via TCP sockets to sending structured JSON via HTTP POST using the `requests` library.
* **API Schema Extension**: Added `ReadingCreate` and `ReadingSchema` Pydantic models to strictly define the input and output data structures, ensuring the API is more robust.
* **Database Integration in API**: The data insertion logic previously found in `servidor.py` was moved into the API routes to maintain a single point of entry for the database.

### Libraries Used
* **FastAPI**: To handle both GET (retrieval) and POST (storage) requests.
* **SQLAlchemy**: To manage database interactions.
* **Requests**: (New in P4) Used by the client to communicate with the API.
* **Pydantic**: For data validation of the incoming POST bodies.
* **Uvicorn**, **Psycopg2**, **Dotenv**: For server execution and DB connectivity.
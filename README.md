# Project 3: Data Access

**Subject:** Programming and Communications 3
**Degree:** Electronic Engineering
**Students:** Alexandru Anton Catrinoi Sfarghie 

## Task 1: API Development

### Brief description of the task 
The goal of this task is to create a RESTful API with the FastAPI framework. This API will help users access sensor data stored in a PostgreSQL database. It serves as a secure layer, allowing users to query, filter, and sort data using standard HTTP requests. Users do not need direct database access or SQL knowledge. 

### Brief description of the solution 
The solution involves a FastAPI application (`api.py`) that uses SQLAlchemy as an ORM to interact with the database. It includes a strong endpoint that supports dynamic filtering by sensor type and date ranges, along with sorting. The system employs environment variables for secure database setup and Pydantic schemas for data validation.

### Table Definitions

| Table Name | Columns | Type | Constraints | Descriptions |
| :--- | :--- | :--- | :--- | :--- |
| **sensors** | id | Int | Primary Key, Auto-gen | Unique identifier for the sensor category. |
| | name | String | Unique, Not Null | The human-readable name of the sensor (e.g., temperature). |
| **readings** | id | Int | Primary Key, Auto-gen | Unique identifier for each specific data entry. |
| | sensor_id | Int | Foreign Key (sensors.id) | Links the reading to a specific sensor in the 'sensors' table. |
| | value | Float | Not Null | The numerical measurement captured by the sensor. |
| | timestamp | DateTime | Default: Now | The exact date and time when the reading was recorded. |

### Endpoint Definitions

| Verb | Endpoint | Params | Body | Return |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/api/data` | `Sensor`: String (Optional)<br>`Order`: String (ascendant/descendant)<br>`Init date`: Date (YYYY-MM-DD)<br>`End date`: Date (YYYY-MM-DD) | None | A JSON list of objects containing `id`, `sensor` name, `value`, and `timestamp`. |

## Previous Tasks Modifications

### Project 1 & 2 Refactoring
To ensure consistency across the entire project and adhere to the required coding standards, the following modifications were implemented in the code from previous phases:

* **Python Naming Conventions**: All method and function names were refactored from PascalCase (e.g., `SaveToDatabase`, `GenSensor`) to **snake_case** (e.g., `save_to_database`, `generate_sensor_data`). This aligns with PEP 8 standards and improves code readability.
* **SQL Schema Standardization**: Table names in the SQL scripts and ORM models were converted to **lowercase** (e.g., `Sensors` to `sensors`, `Readings` to `readings`). This avoids case-sensitivity issues across different SQL environments and follows common database naming conventions.
* **Git Conflict Resolution**: Conflict markers previously found in `SQL.sql` were removed, and the schema was cleaned to provide a single, valid initialization script.
* **Model Integration**: The `Reading` and `Sensor` classes in `servidor.py` were updated to reflect the new table names and relationships, ensuring the API can correctly query the existing data structure.

### Libraries Used
* **FastAPI**: Modern web framework for building APIs.
* **SQLAlchemy**: SQL toolkit and Object-Relational Mapper.
* **Uvicorn**: Lightning-fast ASGI server implementation.
* **Pydantic**: Data validation and settings management using Python type annotations.
* **Psycopg2-binary**: PostgreSQL database adapter.
* **Python-dotenv**: Reads key-value pairs from a .env file and sets them as environment variables.
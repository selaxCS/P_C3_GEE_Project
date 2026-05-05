# Project 2: Storage and Data Modelling

**Subject:** Programming and Communications 3
**Degree:** Electronic Engineering
**Students:** Alexandru Anton Catrinoi Sfarghie

## Overview
This project is part of the **Programming and Communications 3** course. The primary objective is to transition from a local filesystem-based storage system (using JSON files) to a structured **Relational Database Management System (RDBMS)** using SQL.

As data volume increases over time, file-based storage becomes inefficient for querying and filtering. By implementing a relational model, the system ensures data consistency and provides powerful tools for data analysis.

## System Architecture
The system follows a **Client-Server architecture** communicating through TCP network sockets.

### 1. Data Producer (Client Simulator)
The client acts as an autonomous sensing unit. It simulates the capture of four distinct environmental variables: **Temperature**, **Humidity**, **Irrigation** (Water Flow), and **Rain Gauge** (Precipitation).

### 2. Data Ingestor (Server / Receiver)
The server remains in a listening state for incoming transmissions. It uses an **ORM layer** to translate the received data into database entities and persist them into the SQL schema.

## Database Modelling
The data is organized into a relational schema designed to maintain referential integrity through a **One-to-Many (1:N)** relationship.

### Table: Sensors
This table acts as a catalog for the different types of sensors.

| Columns | Type | Constraints | Descriptions |
| :--- | :--- | :--- | :--- |
| id | Serial (Int) | Primary Key, auto generated | Unique identifier for each sensor type. |
| name | Text | Not Null, Unique | The specific name of the sensor (e.g., temperature). |

### Table: Readings
This table stores the historical log of all measurements captured.

| Columns | Type | Constraints | Descriptions |
| :--- | :--- | :--- | :--- |
| id | Serial (Int) | Primary Key, auto generated | Unique identifier for each individual reading. |
| sensor_id | Integer | Not Null, Foreign Key | References the ID in the Sensors table. |
| value | Real | Not Null | The numerical value recorded by the sensor. |
| timestamp | Timestamp | Default CURRENT_TIMESTAMP | The exact date and time of the reading. |

## Deployment and Workflow
To ensure the correct operation of the system, follow these steps:
1.  **Database Initialization**: Run the SQL scripts to establish the table structures.
2.  **Environment Configuration**: Set the `DATABASE_URL` in a `.env` file.
3.  **Server Activation**: Launch the receiver component to open the communication port.
4.  **Client Activation**: Launch the simulator to begin the data transmission.

## Overview
This project is part of the **Programming and Communications 3** course. The primary objective is to transition from a local filesystem-based storage system (using JSON files) to a structured **Relational Database Management System (RDBMS)** using SQL.

As data volume increases over time, file-based storage becomes inefficient for querying and filtering. By implementing a relational model, the system ensures data consistency and provides powerful tools for data analysis.

## Technologies and Libraries
The project is developed using Python and relies on the following libraries:

*   **Socket**: Used to implement the TCP/IP communication protocol between the client and the server.
*   **JSON**: Used to serialize the sensor data for transmission and deserialize it upon reception.
*   **SQLAlchemy**: An Object-Relational Mapper (ORM) used to manage the database interactions using Python objects instead of raw SQL.
*   **Psycopg2**: The PostgreSQL adapter for Python, required by SQLAlchemy to connect to the database.
*   **Python-dotenv**: Used to manage sensitive information, such as database credentials, through environment variables (.env).
*   **Random & Datetime**: Used in the simulator to generate synthetic sensor values and their respective timestamps.

## System Architecture
The system follows a **Client-Server architecture** communicating through TCP network sockets.

### 1. Data Producer (Client Simulator)
The client acts as an autonomous sensing unit. It simulates the capture of four distinct environmental variables: **Temperature**, **Humidity**, **Irrigation** (Water Flow), and **Rain Gauge** (Precipitation).

### 2. Data Ingestor (Server / Receiver)
The server remains in a listening state for incoming transmissions. It uses an **ORM layer** to translate the received data into database entities and persist them into the SQL schema.

## Database Modelling
The data is organized into a relational schema designed to maintain referential integrity through a **One-to-Many (1:N)** relationship.

### Table: Sensors
This table acts as a catalog for the different types of sensors.

| Columns | Type | Constraints | Descriptions |
| :--- | :--- | :--- | :--- |
| id | Serial (Int) | Primary Key, auto generated | Unique identifier for each sensor type. |
| name | Text | Not Null, Unique | The specific name of the sensor (e.g., temperature). |

### Table: Readings
This table stores the historical log of all measurements captured.

| Columns | Type | Constraints | Descriptions |
| :--- | :--- | :--- | :--- |
| id | Serial (Int) | Primary Key, auto generated | Unique identifier for each individual reading. |
| sensor_id | Integer | Not Null, Foreign Key | References the ID in the Sensors table. |
| value | Real | Not Null | The numerical value recorded by the sensor. |
| timestamp | Timestamp | Default CURRENT_TIMESTAMP | The exact date and time of the reading. |

## Deployment and Workflow
To ensure the correct operation of the system, follow these steps:
1.  **Database Initialization**: Run the SQL scripts to establish the table structures.
2.  **Environment Configuration**: Set the `DATABASE_URL` in a `.env` file.
3.  **Server Activation**: Launch the receiver component to open the communication port.
4.  **Client Activation**: Launch the simulator to begin the data transmission.
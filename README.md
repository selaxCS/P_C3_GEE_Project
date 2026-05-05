# Project 2: Storage and Data Modelling

**Subject:** Programming and Communications 3
**Degree:** Electronic Engineering
**Students:** Alexandru Anton Catrinoi Sfarghie

## Overview
This project is part of the **Programming and Communications 3** course. The primary objective is to transition from a local filesystem-based storage system (using JSON files) to a structured **Relational Database Management System (RDBMS)** using SQL.

As data volume increases over time, file-based storage becomes inefficient for querying and filtering. By implementing a relational model, the system ensures data consistency and provides powerful tools for data analysis.


## Tasks and Solutions

### Task 1: Database Initialization
**Description**: The first task consists of creating the scripts to initialize the database and the related tables using SQL.

**Solution**: A SQL script was developed to establish the relational schema. It defines two main entities: `Sensors`, which acts as a catalog for the available sensor types, and `Readings`, which stores every individual data point. They are linked via a **One-to-Many (1:N)** relationship using a foreign key.

#### Table: Sensors
| Columns | Type | Constraints | Descriptions |
| :--- | :--- | :--- | :--- |
| id | Serial (Int) | Primary Key, auto generated | Unique identifier for each sensor type. |
| name | Text | Not Null, Unique | The specific name of the sensor (e.g., temperature). |

#### Table: Readings
| Columns | Type | Constraints | Descriptions |
| :--- | :--- | :--- | :--- |
| id | Serial (Int) | Primary Key, auto generated | Unique identifier for each individual reading. |
| sensor_id | Integer | Not Null, Foreign Key | References the ID in the Sensors table. |
| value | Real | Not Null | The numerical value recorded by the sensor. |
| timestamp | Timestamp | Default CURRENT_TIMESTAMP | The exact date and time of the reading. |

---

### Task 2: Data Ingestion and Persistence
**Description**: The second task focuses on modifying the storage method. Instead of saving data as JSON files, the receiver must store the incoming data directly into the SQL database.

**Solution**: The solution implements a central receiver that utilizes **SQLAlchemy (ORM)**. This component listens for incoming TCP connections from the client simulator. Once the JSON payload is received, the server maps the data to the corresponding Python classes and automatically persists the records into the database. This approach replaces manual file management with automated relational storage.

## System Architecture
The system follows a **Client-Server architecture** communicating through TCP network sockets.

### 1. Data Producer (Client Simulator)
The client acts as an autonomous sensing unit. It simulates the capture of four distinct environmental variables: **Temperature**, **Humidity**, **Irrigation** (Water Flow), and **Rain Gauge** (Precipitation).

### 2. Data Ingestor (Server / Receiver)
The server remains in a listening state for incoming transmissions. It uses an **ORM layer** to translate the received data into database entities and persist them into the SQL schema.

## Deployment and Workflow
1.  **Database Initialization**: Run the SQL scripts to establish the table structures.
2.  **Environment Configuration**: Set the `DATABASE_URL` in a `.env` file.
3.  **Server Activation**: Launch the receiver component to open the communication port.

## Libraries
The project is developed using Python and relies on the following libraries:

*   **Socket**: Used to implement the TCP/IP communication protocol between the client and the server.
*   **JSON**: Used to serialize the sensor data for transmission and deserialize it upon reception.
*   **SQLAlchemy**: An Object-Relational Mapper (ORM) used to manage the database interactions using Python objects.
*   **Psycopg2**: The PostgreSQL adapter for Python, required by SQLAlchemy to connect to the database.
*   **Python-dotenv**: Used to manage sensitive information (database credentials) through environment variables (.env).
*   **Random & Datetime**: Used in the simulator to generate synthetic sensor values and timestamps.


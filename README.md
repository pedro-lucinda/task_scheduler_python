# Asynchronous Task Scheduler

## Overview

This project is an Asynchronous Task Scheduler built using Python's `asyncio` and `APScheduler`. It allows users to schedule, run, and manage tasks asynchronously through a web interface. The project also includes task monitoring, logging, and a REST API for task management.

### Features

- **Task Scheduling**: Cron-like scheduling for recurring tasks.
- **Asynchronous Execution**: Tasks run asynchronously without blocking the main thread.
- **Web Interface**: Built with FastAPI to allow users to interact with the scheduler via REST API.
- **Monitoring and Logging**: Real-time task monitoring and logging for debugging and auditing.
- **Database Integration**: Tasks and their schedules are saved in a database.

## Technologies

- **Python 3.8+**
- **FastAPI**
- **APScheduler**
- **SQLite / PostgreSQL**
- **SQLAlchemy**
- **Loguru for logging**
- **JWT authentication using PyJWT**
- **bcrypt for secure password hashing**

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd task_scheduler
```

### 2. Set up the virtual environment

```bash
python3 -m venv task_scheduler_env
source task_scheduler_env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

The project uses SQLite for simplicity. If you want to use PostgreSQL, update the database connection in app/db/models.py.

```bash
python -c 'from app.db.models import init_db; init_db()'
```

## Running the Application

Start the FastAPI application with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The server will run at http://127.0.0.1:8000.

### API Endpoints

- Register a user:  ```bash POST /register/?username=<username>&password=<password>```
- Login to get a token:  ```bash POST /token with form data username and password```
- Schedule a task:  ```bash POST /schedule/?cron_expression=<expression>&task_id=<id> (requires JWT token)```
- Remove a task:  ```bash DELETE /remove/?task_id=<id> (requires JWT token)```
- Check task status:  ```bash GET /status/?task_id=<id> (requires JWT token)```

## Example usage

```bash
# Register a user:
curl -X POST "http://127.0.0.1:8000/register/?username=user&password=password"

#Login and get a token:
curl -X POST "http://127.0.0.1:8000/token?username=user&password=password"

#Schedule a task:
curl -X POST "http://127.0.0.1:8000/schedule/?cron_expression=%2A%2F1%20%2A%20%2A%20%2A%20%2A&task_id=task1" \
-H "Authorization: Bearer <JWT_TOKEN_HERE>"

# Remove a task:
curl -X DELETE "http://127.0.0.1:8000/remove/?task_id=task1" \
-H "Authorization: Bearer <JWT_TOKEN_HERE>"

#Check task status:
curl "http://127.0.0.1:8000/status/?task_id=task1" -H "Authorization: Bearer <JWT_TOKEN_HERE>"
```

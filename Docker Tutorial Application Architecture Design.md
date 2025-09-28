# Docker Tutorial Application Architecture Design

This document outlines the architectural design for a simple web application, built with Python Flask and PostgreSQL, intended for a Docker tutorial. The goal is to demonstrate containerization of both the application and its database, ensuring a zero-setup.

## 1. Application Overview: To-Do List Manager

The application will be a basic **To-Do List Manager**. This choice provides clear, understandable functionality involving fundamental database operations (Create, Read, Update, Delete - CRUD) without introducing unnecessary complexity. Users will be able to:

*   Add new tasks.
*   View existing tasks.
*   Mark tasks as complete.
*   Delete tasks.

## 2. Application Structure (Python Flask)

The Flask application will follow a standard, minimalist structure to keep it easy to understand. The key components will be:

*   `app.py`: The main Flask application file, handling routing, business logic, and database interactions.
*   `templates/`: A directory containing HTML templates for rendering the web pages (e.g., `index.html` for the main To-Do list view).
*   `static/`: A directory for static assets like CSS files (e.g., `style.css`).
*   `requirements.txt`: Lists Python dependencies (Flask, Psycopg2 for PostgreSQL).

```
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── requirements.txt
```

## 3. Database Schema (PostgreSQL)

The database will consist of a single table named `tasks` to store the To-Do items. The schema will be straightforward:

| Column Name | Data Type | Constraints      | Description             |
| :---------- | :-------- | :--------------- | :---------------------- |
| `id`        | `SERIAL`  | `PRIMARY KEY`    | Unique identifier for the task |
| `description` | `VARCHAR(255)` | `NOT NULL`       | Description of the To-Do item |
| `completed` | `BOOLEAN` | `DEFAULT FALSE` | Status of the task (true if completed, false otherwise) |

This simple schema allows for easy demonstration of data persistence and manipulation within a containerized environment.

## 4. Interaction Flow

The application and database will interact as follows:

1.  **User Request:** A user accesses the web application via their browser.
2.  **Flask Application:** The `app.py` Flask application receives the request.
3.  **Database Connection:** The Flask application establishes a connection to the PostgreSQL database using environment variables for connection details (host, database name, user, password). This is crucial for Docker, as it allows for flexible configuration without hardcoding.
4.  **SQL Queries:** Based on the user's action (e.g., adding a task, viewing tasks), the Flask application executes appropriate SQL queries against the PostgreSQL database.
5.  **Data Retrieval/Manipulation:** The database processes the queries, returning results or confirming data changes.
6.  **Render Response:** The Flask application processes the database response, renders the appropriate HTML template with the updated data, and sends it back to the user's browser.

## 5. Dockerization Considerations

The architecture is designed with Docker in mind:

*   **Separation of Concerns:** The application and database are distinct services, making them ideal candidates for separate Docker containers.
*   **Environment Variables:** Database connection details will be passed to the Flask application container via environment variables, enabling easy configuration and secure handling of credentials within Docker Compose.
*   **Volume Mounting:** Data persistence for the PostgreSQL database will be achieved using Docker volumes, ensuring that data is not lost when the database container is stopped or recreated.
*   **Network Configuration:** Docker Compose will be used to define a custom network, allowing the application and database containers to communicate with each other using service names (e.g., `db` for the PostgreSQL container) instead of IP addresses.

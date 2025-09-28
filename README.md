# Docker Tutorial: Zero-Setup To-Do Application with Flask and PostgreSQL

This tutorial provides a step-by-step guide to setting up and running a simple To-Do list web application using Python Flask and PostgreSQL, all containerized with Docker. The goal is to demonstrate the power of Docker for creating isolated, reproducible development environments with minimal setup.

## 1. Introduction to the Application

Our application is a basic To-Do list manager. It allows users to add, view, mark as complete, and delete tasks. The backend is built with **Python Flask**, and data is persisted in a **PostgreSQL** database. Both the Flask application and the PostgreSQL database will run in separate Docker containers, orchestrated by Docker Compose.

**Key Features:**
*   **Zero Setup:** With Docker installed, you can get the entire application stack running with a single command.
*   **Containerization:** Learn how to containerize a web application and its database.
*   **Database Persistence:** Understand how Docker volumes ensure your database data is saved.
*   **Inter-container Communication:** See how containers communicate with each other within a Docker network.

## 2. Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Docker Desktop:** This includes Docker Engine, Docker CLI, Docker Compose, and Kubernetes. Download and install it from the official Docker website: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

    *Verify Installation:*
    ```bash
    docker --version
    docker compose version
    ```

## 3. Getting the Application Code

First, you need to get the application code. You can clone it from a Git repository or download it directly.

```bash
git clone https://github.com/BlasmethiaN/docker-tutorial-app.git
cd docker-tutorial-app

# If downloading directly, ensure all files are in a directory named 'docker-tutorial-app'
# and navigate into it.
```

## 4. Understanding the Project Structure

Navigate into the `docker-tutorial-app` directory. You will find the following files and folders:

```
├── app.py                  # Main Flask application file
├── templates/              # HTML templates for the web interface
│   └── index.html
├── static/                 # Static assets like CSS
│   └── style.css
├── requirements.txt        # Python dependencies for the Flask app
├── Dockerfile              # Instructions to build the Flask app Docker image
└── docker-compose.yml      # Defines and runs the multi-container Docker application
```

## 5. Running the Application with Docker Compose

Docker Compose allows you to define and run multi-container Docker applications. Our `docker-compose.yml` file sets up two services: `web` (our Flask app) and `db` (our PostgreSQL database).

1.  **Build and Run:**
    Open your terminal, navigate to the `docker-tutorial-app` directory, and run the following command:

    ```bash
    docker compose up --build
    ```

    *   `docker compose up`: Starts the services defined in `docker-compose.yml`.
    *   `--build`: Builds the Docker images before starting the containers. This is important the first time you run it or if you've made changes to the `Dockerfile`.

    You will see a lot of output as Docker downloads images, builds your application image, and starts both containers. Once everything is up and running, you should see messages indicating that the Flask application is running on `http://0.0.0.0:5000`.

2.  **Access the Application:**
    Open your web browser and go to `http://localhost:5000`.

    You should now see the To-Do application interface. You can add new tasks, mark them as complete, and delete them. All your data will be stored in the PostgreSQL database running in its own container.

3.  **Verify Containers:**
    You can open another terminal window and run `docker ps` to see the running containers:

    ```bash
    docker ps
    ```
    You should see two containers listed: one for your Flask `web` service and one for the `db` (PostgreSQL) service.

## 6. Stopping and Cleaning Up

To stop the application and clean up the containers and network:

1.  **Stop the Application:**
    In the terminal where `docker compose up` is running, press `Ctrl+C`.

2.  **Remove Containers, Networks, and Volumes:**
    To remove the containers, networks, and the volume used for PostgreSQL data (which means your To-Do items will be deleted), run:

    ```bash
    docker compose down -v
    ```

    *   `docker compose down`: Stops and removes containers and networks.
    *   `-v`: Removes named volumes declared in the `volumes` section of the `docker-compose.yml` file. This is important if you want a fresh database state next time.

    If you want to stop the containers but keep the data (e.g., to restart later with the same tasks), simply run `docker compose down` without the `-v` flag.

## 7. Exploring Docker Concepts

### `Dockerfile`

The `Dockerfile` defines how your Flask application's Docker image is built. It specifies the base image, copies your code, installs dependencies, exposes ports, and defines the command to run your application.

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
CMD ["flask", "run"]
```

### `docker-compose.yml`

This file orchestrates the multiple services (web app and database) that make up your application. It defines:

*   **`services`**: Individual containers (e.g., `web`, `db`).
*   **`build`**: Instructions for building the `web` service's image from the `Dockerfile`.
*   **`ports`**: Maps container ports to host ports (e.g., `5000:5000` means host port 5000 maps to container port 5000).
*   **`environment`**: Passes environment variables to containers, crucial for database connection details.
*   **`depends_on`**: Ensures the `db` service starts before the `web` service.
*   **`volumes`**: Mounts host directories or named volumes into containers for data persistence (e.g., `postgres_data` for the database).

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      FLASK_APP: app.py
      FLASK_RUN_HOST: 0.0.0.0
      SECRET_KEY: your-secret-key-here # In a real app, use a strong, randomly generated key
      DB_HOST: db # This refers to the 'db' service name in docker-compose
      DB_NAME: todoapp
      DB_USER: postgres
      DB_PASSWORD: password
    depends_on:
      - db
    volumes:
      - .:/app # Mounts the current directory into the container for live code changes (development)

  db:
    image: postgres:13 # Uses the official PostgreSQL 13 Docker image
    environment:
      POSTGRES_DB: todoapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data # Persist database data

volumes:
  postgres_data: # Define the named volume
```

## 8. Conclusion

Congratulations! You have successfully set up and run a multi-container application using Docker Compose. This example demonstrates how Docker simplifies the deployment and management of applications and their dependencies, providing a consistent environment across different machines. You can now use this foundation to explore more advanced Docker concepts and build your own containerized applications.

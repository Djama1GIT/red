# Red

RED is a project based on Django.

## Installation and setup

1. Install Docker and Docker Compose if they are not already installed on your system.

2. Clone the project repository:

```bash
git clone https://github.com/Djama1GIT/red.git
cd red
```

3. Configure environment variables in the .env file (not required if you don't plan to use email functionality).

4. Run the project:

```bash
docker-compose up --build
```

## User Interface

Home Page: http://localhost:8000

## Technologies Used

- Python - The programming language used in the project.
- Django - A high-level Python web framework used to develop web applications.
- Redis - An in-memory database used in the project for caching data and storing Celery tasks.
- Celery - A library for executing background tasks used in the project for processing long-running operations in the background.
- PostgreSQL - A relational database used in the project to store information.
- Docker - A platform for creating, deploying, and managing containers used in the project to run the application in an isolated environment.

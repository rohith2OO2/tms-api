Overview
This Task Management System API is built with FastAPI, PostgreSQL, Redis, and Celery. It provides endpoints to manage projects and tasks, with asynchronous background processing handled by Celery workers.

Setup Instructions
Local Setup (Development)
Clone repository:

bash
git clone <your-repo-url>
cd tms-api
Create .env file in the project root with contents similar to:

text
DB_HOST=tms_db
DB_PORT=5432
DB_NAME=tms_database
DB_USER=postgres
DB_PASSWORD=your_password

APP_ENV=production
APP_DEBUG=false
API_KEY=your_api_key_here
PORT=3000

REDIS_URL=redis://tms_redis:6379/0
DATABASE_URL=postgresql+asyncpg://postgres:your_password@tms_db:5432/tms_database
CELERY_BROKER_URL=${REDIS_URL}
CELERY_RESULT_BACKEND=${REDIS_URL}
Ensure Docker and Docker Compose are installed.

Build and run the containers:

bash
docker compose build --no-cache
docker compose up -d
Check all containers are up:

bash
docker ps
Apply database migrations (if using Alembic):

bash
docker compose exec web alembic upgrade head
Access API:
Visit http://localhost:3000 (adjust port if needed).

Deployment (Production)
Use Docker Compose or Kubernetes for deployment.

Secure .env secrets with environment management solutions.

Use managed/production-grade PostgreSQL and Redis instances if possible.

Set up a reverse proxy such as Nginx for SSL/TLS termination.

Include logging and monitoring for containers.

Database Schema Diagram
text
+-------------------+      +---------------------+
|     projects      |      |        tasks        |
+-------------------+      +---------------------+
| id  (PK)          |<-----| id  (PK)            |
| name              |      | title               |
| description       |      | description         |
| owner_id (FK)     |      | status              |
+-------------------+      | priority            |
                           | assigned_to_email    |
+-------------------+      | due_date             |
|      users        |      | project_id (FK)      |
+-------------------+      | assignee_id (FK)     |
| id  (PK)          |      +---------------------+
| email             |
| hashed_password   |
| full_name         |
+-------------------+
Projects belong to Users.

Tasks belong to Projects and may have an assigned user.

How to Get a Token (Optional Authentication)
The API uses JWT authentication.

Obtain a token by posting credentials to /auth/login, for example:

bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"your_password"}'
The response contains a JWT token.

Use the token in the Authorization header for API requests:

bash
curl -H "Authorization: Bearer <your_token>" http://localhost:3000/tasks
Celery Worker Setup
Celery worker and beat run as separate Docker services.

Redis is used as the broker and result backend.

Celery tasks are defined in celery_app/tasks.py.

Tasks are invoked asynchronously from FastAPI endpoints, e.g.:

python
send_email_task.delay(to_email, subject, body)
Celery workers pick up and process tasks in the background, decoupling long-running jobs from the request lifecycle.

Docker Compose ensures healthy dependencies and restart policies.

Sample cURL Requests
Create a Task
bash
curl -X POST http://localhost:3000/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "description": "Task details", "assigned_to_email": "user@example.com", "due_date": "2025-08-15"}'
List Tasks
bash
curl -H "Authorization: Bearer <token>" http://localhost:3000/tasks
Update Task Status
bash
curl -X PATCH http://localhost:3000/tasks/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

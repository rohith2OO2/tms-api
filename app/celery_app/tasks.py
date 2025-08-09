from celery import Celery
from app.email import send_email  # <-- We'll create this file
import os

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery.task
def example_task():
    print("This is an example task")

@celery.task
def send_email_task(to_email: str, subject: str, body: str):
    """Send an email asynchronously using Celery."""
    send_email(to_email, subject, body)

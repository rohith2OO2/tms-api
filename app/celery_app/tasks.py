# app/celery_app/tasks.py

from celery import shared_task
import models
import schemas
from email_utils import send_email  # adjust if located elsewhere

@shared_task
def send_email_task(to_email: str, subject: str, body: str):
    """
    Background task to send an email.
    This gets queued by Celery and processed by the worker.
    """
    send_email(
        to_email=to_email,
        subject=subject,
        body=body
    )
    return f"Email sent to {to_email} with subject '{subject}'"


# Example: another task (optional)
@shared_task
def example_task(data: dict):
    """
    Just an example task.
    """
    # Perform background processing here
    print(f"Processing data: {data}")
    return {"status": "completed", "data": data}

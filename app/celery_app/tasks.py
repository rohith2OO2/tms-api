from celery import Celery
from celery.schedules import crontab
from app.services.email import send_email
from app.database import SessionLocal
from app import models
import os
from datetime import datetime

celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0")
)

@celery.task
def send_email_task(to_email: str, subject: str, body: str):
    send_email(to_email, subject, body)

@celery.task
def send_overdue_summary():
    """Send daily summary of overdue tasks to each user."""
    db = SessionLocal()
    today = datetime.utcnow().date()
    
    users = db.query(models.User).all()
    for user in users:
        overdue_tasks = db.query(models.Task).filter(
            models.Task.assigned_to == user.id,
            models.Task.due_date < today,
            models.Task.status != "completed"
        ).all()

        if overdue_tasks:
            task_list = "\n".join([f"- {t.title} (due {t.due_date})" for t in overdue_tasks])
            body = f"Hello {user.name},\n\nYou have overdue tasks:\n{task_list}"
            send_email_task.delay(user.email, "Daily Overdue Task Summary", body)

    db.close()

# Celery Beat schedule
celery.conf.beat_schedule = {
    "send-overdue-summary-every-day": {
        "task": "app.celery_app.tasks.send_overdue_summary",
        "schedule": crontab(hour=9, minute=0),  # every day at 9:00 UTC
    },
}
celery.conf.timezone = "UTC"

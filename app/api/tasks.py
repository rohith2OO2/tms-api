from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db
from celery_app.tasks import send_email_task

router = APIRouter()


@router.post("/tasks", response_model=schemas.TaskRead)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    """Create a new task and notify the assigned user via email."""
    task = models.Task(**task_in.dict())
    db.add(task)
    db.commit()
    db.refresh(task)

    # Send assignment email
    if task.assigned_to_email:
        send_email_task.delay(
            to_email=task.assigned_to_email,
            subject="New Task Assigned",
            body=f"You have been assigned a new task: '{task.title}' "
                 f"with due date {task.due_date}."
        )

    return task


@router.get("/tasks", response_model=List[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    """List all tasks."""
    return db.query(models.Task).all()


@router.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a single task by ID."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/tasks/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update a task and notify the user if status changes."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task.status

    for key, value in task_in.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    # Notify if status changed
    if task.status != old_status and task.assigned_to_email:
        send_email_task.delay(
            to_email=task.assigned_to_email,
            subject="Task Status Updated",
            body=f"Your task '{task.title}' status has been updated to '{task.status}'."
        )

    return task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

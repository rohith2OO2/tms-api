from typing import List, Optional
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, desc, asc

from database import get_session
from models import Task, User
from schemas import TaskCreate, TaskRead, TaskBase
from auth.deps import get_current_user

router = APIRouter()


@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new task under a project owned by current user.
    """
    # Optionally validate project ownership here.

    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status or "todo",
        priority=task_in.priority or "medium",
        due_date=task_in.due_date,
        project_id=task_in.project_id,
        assignee_id=task_in.assignee_id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.get(
    "/",
    response_model=List[TaskRead],
    summary="Retrieve tasks with filtering, sorting, and pagination",
)
async def get_tasks(
    status: Optional[str] = Query(
        None, description="Filter by task status"
    ),
    priority: Optional[str] = Query(
        None, description="Filter by task priority"
    ),
    due_date: Optional[str] = Query(
        None,
        description="Filter by due date (ISO format YYYY-MM-DD)",
    ),
    sort_by: Optional[str] = Query(
        None,
        regex="^(title|due_date|priority|status)$",
        description="Sort field",
    ),
    sort_order: Optional[str] = Query(
        "asc",
        regex="^(asc|desc)$",
        description="Sort order",
    ),
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of records to return",
    ),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve tasks owned by the current user with optional filtering,
    sorting, and pagination.
    """
    filters = []

    # Import inside function to avoid circular dependencies
    from sqlalchemy.orm import joinedload
    from app.models import Project

    stmt = (
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .options(joinedload(Task.project))
        .where(Project.owner_id == current_user.id)
    )

    if status:
        filters.append(Task.status == status)
    if priority:
        filters.append(Task.priority == priority)
    if due_date:
        filters.append(Task.due_date == due_date)

    if filters:
        stmt = stmt.where(and_(*filters))

    if sort_by:
        order_func = asc if sort_order == "asc" else desc
        order_column = getattr(Task, sort_by)
        stmt = stmt.order_by(order_func(order_column))
    else:
        stmt = stmt.order_by(asc(Task.id))

    stmt = stmt.offset(skip).limit(limit)

    result = await session.execute(stmt)
    tasks = result.scalars().all()
    return tasks


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    summary="Get a task by ID",
)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a single task if it belongs to a project owned by current user.
    """
    from models import Project

    stmt = (
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(
            Task.id == task_id,
            Project.owner_id == current_user.id,
        )
    )
    result = await session.execute(stmt)
    task = result.scalars().first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.put(
    "/{task_id}",
    response_model=TaskRead,
    summary="Update a task",
)
async def update_task(
    task_id: int,
    task_in: TaskBase,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Update fields of a task if it belongs to current user's project.
    """
    from models import Project

    stmt = (
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(
            Task.id == task_id,
            Project.owner_id == current_user.id,
        )
    )
    result = await session.execute(stmt)
    task = result.scalars().first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    update_data = task_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a task if it belongs to a project owned by current user.
    """
    from models import Project

    stmt = (
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(
            Task.id == task_id,
            Project.owner_id == current_user.id,
        )
    )
    result = await session.execute(stmt)
    task = result.scalars().first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    await session.delete(task)
    await session.commit()



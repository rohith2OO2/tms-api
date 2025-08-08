import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    Enum,
    Date
)
from sqlalchemy.orm import relationship
from app.database import Base


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    hashed_password = Column(
        String,
        nullable=False
    )
    is_active = Column(
        Boolean,
        default=True
    )

    projects = relationship(
        "Project",
        back_populates="owner",
        cascade="all, delete"
    )
    tasks = relationship(
        "Task",
        back_populates="assignee"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String,
        nullable=False
    )
    description = Column(
        Text,
        nullable=True
    )
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="projects"
    )
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    title = Column(
        String,
        nullable=False
    )
    description = Column(
        String,
        nullable=True
    )
    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.todo,
        nullable=False
    )
    priority = Column(
        Enum(TaskPriority),
        default=TaskPriority.medium,
        nullable=False
    )
    due_date = Column(
        Date,
        nullable=True
    )
    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )
    assignee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )
    assignee = relationship(
        "User",
        back_populates="tasks"
    )

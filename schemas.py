from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional


# --- User Schemas ---


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool


# --- Project Schemas ---


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    owner_id: int


# --- Task Schemas ---


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    project_id: int
    assignee_id: Optional[int] = None


class TaskRead(TaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None

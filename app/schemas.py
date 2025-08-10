from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# --- User Schemas ---

class UserBase(BaseModel):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)  # Pydantic v2

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool


# --- Project Schemas ---

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(TaskBase):
    project_id: int
    assignee_id: Optional[int] = None

class TaskRead(TaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None

class TaskUpdate(BaseModel):
    """Fields allowed to be updated"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

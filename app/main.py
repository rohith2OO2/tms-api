from fastapi import FastAPI
from models import Base
from database import engine

# Create all tables immediately
Base.metadata.create_all(bind=engine)

# Import your routers
from api.projects import router as projects_router
from api.tasks import router as tasks_router
from auth.auth import router as auth_router

app = FastAPI()

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

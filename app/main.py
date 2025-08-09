from fastapi import FastAPI
from models import Base
from database import engine
from sqlalchemy import create_engine
from config import get_settings

# Import your routers
from api.projects import router as projects_router
from api.tasks import router as tasks_router
from auth.auth import router as auth_router

app = FastAPI()

# Create a sync engine for table creation
settings = get_settings()
# Convert async URL to sync URL (remove +asyncpg, use psycopg2)
sync_database_url = str(settings.database_url).replace("+asyncpg", "")
sync_engine = create_engine(sync_database_url)

# Create tables using sync engine
Base.metadata.create_all(bind=sync_engine)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

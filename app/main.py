from fastapi import FastAPI
from models import Base
from database import engine
from api.projects import router as projects_router
from api.tasks import router as tasks_router
from auth.auth import router as auth_router

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Create tables using the async engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

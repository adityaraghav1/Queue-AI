from fastapi import FastAPI

from app.core.config import settings
from app.routes.health import router as health_router
from app.database.database import Base, engine
from app.database import models
from app.routes.auth import router as auth_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

app.include_router(health_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Welcome to QueueAI"
    }
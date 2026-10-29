from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.routes.health import router as health_router
from app.database.database import Base, engine
from app.database import models
from app.routes.auth import router as auth_router
from app.routes.tickets import router as tickets_router


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

# Serve CSS and JavaScript files.
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Load HTML templates.
templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

# Register existing API routers.
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(tickets_router)

# Create database tables.
Base.metadata.create_all(bind=engine)


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )

@app.get("/admin-dashboard")
def admin_dashboard_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={}
    )
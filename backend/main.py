from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from database.connection import Base, engine
from database import models
from routes.event_routes import router as event_router
from routes.inspection_routes import router as inspection_router
from routes.passport_routes import router as passport_router
from routes.piece_routes import router as piece_router
from routes.user_routes import router as user_router


# ---------------------------------------------------------
# CREATE DATABASE TABLES
# ---------------------------------------------------------

Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# UPLOAD DIRECTORY CONFIGURATION
# ---------------------------------------------------------

UPLOAD_DIRECTORY = Path("uploads")

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="TrustTrace API",
    description="Backend API for the TrustTrace jewellery manufacturing prototype",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS CONFIGURATION
# ---------------------------------------------------------

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# SERVE UPLOADED FILES
# ---------------------------------------------------------

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIRECTORY)),
    name="uploads"
)


# ---------------------------------------------------------
# REGISTER API ROUTERS
# ---------------------------------------------------------

app.include_router(piece_router)
app.include_router(user_router)
app.include_router(event_router)
app.include_router(inspection_router)
app.include_router(passport_router)


# ---------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to TrustTrace API"
    }


# ---------------------------------------------------------
# APPLICATION HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "TrustTrace"
    }


# ---------------------------------------------------------
# DATABASE HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health/database")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }
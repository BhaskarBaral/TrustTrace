from fastapi import FastAPI
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
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="TrustTrace API",
    description="Backend API for the TrustTrace jewellery manufacturing prototype",
    version="1.0.0",
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
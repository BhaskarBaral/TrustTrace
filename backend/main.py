from fastapi import FastAPI
from sqlalchemy import text

from database.connection import Base, engine
from database import models
from routes.piece_routes import router as piece_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="TrustTrace API",
    description="Backend API for the TrustTrace jewellery manufacturing prototype",
    version="1.0.0",
)


app.include_router(piece_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to TrustTrace API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "TrustTrace"
    }


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
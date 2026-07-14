"""Module: database/models.py"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    operator_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="operator",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


class Piece(Base):
    __tablename__ = "pieces"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    piece_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )

    product_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    material: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    current_stage: Mapped[str] = mapped_column(
        String(100),
        default="Registered",
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="In Production",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


class ProductionEvent(Base):
    __tablename__ = "production_events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    piece_id: Mapped[str] = mapped_column(
        ForeignKey("pieces.piece_id"),
        index=True,
        nullable=False
    )

    operator_id: Mapped[str] = mapped_column(
        ForeignKey("users.operator_id"),
        index=True,
        nullable=False
    )

    stage: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    piece_id: Mapped[str] = mapped_column(
        ForeignKey("pieces.piece_id"),
        index=True,
        nullable=False
    )

    inspector_id: Mapped[str] = mapped_column(
        ForeignKey("users.operator_id"),
        index=True,
        nullable=False
    )

    image_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    defect_detected: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    defect_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    inspection_status: Mapped[str] = mapped_column(
        String(50),
        default="Completed",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
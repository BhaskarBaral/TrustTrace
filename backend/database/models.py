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

    pin_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="operator",
        nullable=False
    )

    station_id: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    batch_id: Mapped[str] = mapped_column(
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

    piece_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    gold_lot: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    alloy_batch: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    stone_parcel: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
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

    batch_id: Mapped[str | None] = mapped_column(
        ForeignKey("batches.batch_id"),
        index=True,
        nullable=True
    )

    product_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    material: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    weight_expected: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
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

    weight_in: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    weight_out: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
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


class StageWeightLog(Base):
    __tablename__ = "stage_weight_logs"

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

    stage: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    operator_id: Mapped[str] = mapped_column(
        ForeignKey("users.operator_id"),
        index=True,
        nullable=False
    )

    weight_in: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    weight_out: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    expected_weight: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    variance: Mapped[float | None] = mapped_column(
        Float,
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


class QualityGate(Base):
    __tablename__ = "quality_gates"

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

    stage: Mapped[str] = mapped_column(
        String(100),
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

    ai_verdict: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
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

    human_review: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    reviewed_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.operator_id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
"""
Seed Script — Populate TrustTrace with realistic demo data.
Run from the backend/ directory.

Usage (from repository root):
  cd backend && ..\.venv\Scripts\python.exe seed_demo.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from database.connection import SessionLocal, Base, engine
from database import models
from schemas.user_schema import UserCreate
from schemas.event_schema import EventCreate
from schemas.piece_schema import PieceCreate
from services.user_service import create_user
from services.piece_service import create_piece
from services.event_service import create_event
from services.quality_service import create_quality_gate, run_ai_inspection
from services.batch_service import create_batch, create_pieces_from_batch


def seed():
    print("=== Seeding TrustTrace Demo Data ===\n")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # ---- Step 1: Users ----
    print("[1/5] Creating users...")
    users = [
        create_user(db, UserCreate(
            name="Rajesh Kumar", operator_id="OP-001",
            email="rajesh@trusttrace.com", password="demo123",
            pin="1111", role="operator", station_id="ST-CAST",
        )),
        create_user(db, UserCreate(
            name="Priya Sharma", operator_id="OP-002",
            email="priya@trusttrace.com", password="demo123",
            pin="2222", role="operator", station_id="ST-FILE",
        )),
        create_user(db, UserCreate(
            name="Amit Singh", operator_id="OP-003",
            email="amit@trusttrace.com", password="demo123",
            pin="3333", role="operator", station_id="ST-SET",
        )),
        create_user(db, UserCreate(
            name="Sneha Patel", operator_id="OP-004",
            email="sneha@trusttrace.com", password="demo123",
            pin="4444", role="operator", station_id="ST-POL",
        )),
        create_user(db, UserCreate(
            name="Vikram Joshi", operator_id="INSP-001",
            email="vikram@trusttrace.com", password="demo123",
            pin="5555", role="inspector",
        )),
        create_user(db, UserCreate(
            name="Ananya Gupta", operator_id="INSP-002",
            email="ananya@trusttrace.com", password="demo123",
            pin="6666", role="inspector",
        )),
        create_user(db, UserCreate(
            name="Rahul Verma", operator_id="ADMIN-001",
            email="rahul@trusttrace.com", password="demo123",
            pin="7777", role="admin",
        )),
    ]
    print(f"  Created {len(users)} users")

    # ---- Step 2: Batches ----
    print("[2/5] Creating batches with gold provenance...")
    batch1 = create_batch(
        db, product_type="Gold Necklace", material="22K Gold",
        piece_count=3, gold_lot="GL-JUN-2026-01",
        alloy_batch="AB-22K-045", stone_parcel="SP-KG-033",
    )
    batch2 = create_batch(
        db, product_type="Diamond Ring", material="18K Gold",
        piece_count=2, gold_lot="GL-JUN-2026-02",
        alloy_batch="AB-18K-012", stone_parcel="SP-CB-007",
    )
    print(f"  Created {batch1.batch_id}, {batch2.batch_id}")

    # ---- Step 3: Generate Pieces ----
    print("[3/5] Generating pieces from batches...")
    batch1_pieces = create_pieces_from_batch(db, batch1.batch_id, 3)
    batch2_pieces = create_pieces_from_batch(db, batch2.batch_id, 2)
    all_pieces = batch1_pieces + batch2_pieces

    extra = create_piece(db, PieceCreate(
        product_type="Gold Earring", material="22K Gold",
        weight_expected=8.5,
    ))
    all_pieces.append(extra)
    print(f"  Created {len(all_pieces)} pieces: {[p.piece_id for p in all_pieces]}")

    for i, p in enumerate(all_pieces):
        weights = [22.0, 18.5, 20.0, 12.0, 15.0, 8.5]
        p.weight_expected = weights[i]
    db.commit()

    # ---- Step 4: Production Events ----
    print("[4/5] Creating production events with weight tracking...")
    now = datetime.utcnow()

    events_data = [
        (0, "OP-001", "Casting", 25.0, 24.7, 6),
        (0, "OP-002", "Filing", 24.7, 23.8, 4.5),
        (0, "OP-003", "Stone Setting", 23.8, 23.2, 3),
        (0, "OP-004", "Polishing", 23.2, 22.3, 1.5),
        (1, "OP-001", "Casting", 22.0, 21.8, 5),
        (1, "OP-002", "Filing", 21.8, 21.0, 3.5),
        (1, "OP-003", "Stone Setting", 21.0, 20.4, 2),
        (2, "OP-001", "Casting", 24.0, 23.5, 4),
        (2, "OP-002", "Filing", 23.5, 22.7, 2),
        (3, "OP-001", "Casting", 15.0, 14.6, 7),
        (3, "OP-002", "Filing", 14.6, 13.9, 5.5),
        (3, "OP-003", "Stone Setting", 13.9, 13.2, 4),
        (3, "OP-004", "Polishing", 13.2, 12.5, 2.5),
        (4, "OP-001", "Casting", 18.0, 17.4, 3),
        (5, "OP-001", "Casting", 10.0, 9.6, 2),
    ]

    for piece_idx, op_id, stage, w_in, w_out, hrs_ago in events_data:
        ev = create_event(db, EventCreate(
            piece_id=all_pieces[piece_idx].piece_id,
            operator_id=op_id,
            stage=stage,
            event_type="Stage Completed",
            weight_in=w_in,
            weight_out=w_out,
        ))
        ev.timestamp = now - timedelta(hours=hrs_ago)
        db.commit()

    print(f"  Created {len(events_data)} production events")

    # ---- Step 5: Quality Gates ----
    print("[5/5] Creating quality gate records with AI verdicts...")

    pieces_with_gates = [
        (0, "casting", "INSP-001"),
        (0, "stone-setting", "INSP-001"),
        (0, "polishing", "INSP-002"),
        (1, "casting", "INSP-001"),
        (1, "stone-setting", "INSP-001"),
        (2, "casting", "INSP-001"),
        (3, "casting", "INSP-002"),
        (3, "stone-setting", "INSP-002"),
        (3, "polishing", "INSP-002"),
        (4, "casting", "INSP-002"),
        (5, "casting", "INSP-001"),
    ]

    gate_count = 0
    for piece_idx, stage, insp_id in pieces_with_gates:
        gate = create_quality_gate(
            db=db,
            piece_id=all_pieces[piece_idx].piece_id,
            stage=stage,
            inspector_id=insp_id,
            image_path=f"seed/{stage}_demo.jpg",
        )
        gate = run_ai_inspection(db, gate.id)
        if gate:
            gate_count += 1

    print(f"  Created {gate_count} quality gates with AI verdicts")

    db.close()
    print("\n=== Seed Complete! ===")
    print("\nOpen http://localhost:5173 to see the populated data.")
    print("Check /inspections, /passport, and /analytics pages.")


if __name__ == "__main__":
    seed()

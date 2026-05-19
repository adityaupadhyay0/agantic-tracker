from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.schemas.telemetry import TelemetryEvent, BehavioralState
from app.models.telemetry import Telemetry as TelemetryModel
from app.services.interpretation.engine import InterpretationEngine
from app.services.compression.engine import CompressionEngine
from typing import List

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

@router.post("/ingest")
async def ingest_telemetry(event: TelemetryEvent, db: AsyncSession = Depends(get_db)):
    db_event = TelemetryModel(
        source=event.source,
        user_id=event.user_id,
        timestamp=event.timestamp,
        event_type=event.event_type,
        metadata_json=event.metadata
    )
    db.add(db_event)
    await db.commit()

    # Trigger interpretation engine (async)
    # For now, we call it synchronously to demonstrate the flow
    engine = InterpretationEngine(db)
    await engine.process_event(event)

    return {"status": "success", "event_id": event.event_id}

@router.post("/compress")
async def compress_telemetry(user_id: str, db: AsyncSession = Depends(get_db)):
    """
    Manually trigger compression. In production, this would be a background task.
    """
    engine = CompressionEngine(db)
    await engine.compress_individual_patterns(user_id)
    await engine.compress_team_patterns("engineering_team_a")
    await engine.compress_org_patterns()
    return {"status": "compression complete"}

@router.get("/sessions/{user_id}", response_model=List[BehavioralState])
async def get_user_sessions(user_id: str, db: AsyncSession = Depends(get_db)):
    # Implementation to fetch sessions from DB
    pass

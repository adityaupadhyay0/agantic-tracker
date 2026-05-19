from sqlalchemy import Column, String, DateTime, JSON, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid
from app.schemas.telemetry import TelemetrySource, WorkState

class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(SQLEnum(TelemetrySource))
    user_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    event_type = Column(String)
    metadata_json = Column(JSON)

class BehavioralSession(Base):
    __tablename__ = "behavioral_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    state = Column(SQLEnum(WorkState))
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime, nullable=True)
    confidence = Column(Float)
    evidence = Column(JSON)
    metadata_json = Column(JSON)

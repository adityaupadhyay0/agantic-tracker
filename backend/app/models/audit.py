from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Float
from app.db.base import Base
from datetime import datetime
import uuid

class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    actor_id = Column(String, index=True) # User or Agent ID
    action = Column(String, index=True) # e.g., "BCO_CREATED", "TELEMETRY_INGESTED", "API_ACCESS"
    resource_id = Column(String, index=True) # ID of the affected BCO, Session, etc.
    scope = Column(String) # individual, team, org
    details = Column(JSON) # Action-specific metadata
    client_ip = Column(String)

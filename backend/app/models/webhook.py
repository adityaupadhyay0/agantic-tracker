from sqlalchemy import Column, String, Boolean, DateTime
from app.db.base import Base
from datetime import datetime
import uuid

class WebhookModel(Base):
    __tablename__ = "webhooks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String, nullable=False)
    secret = Column(String, nullable=True) # For HMAC signing
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    events = Column(String, default="BCO_CREATED,BCO_UPDATED") # Comma-separated event types

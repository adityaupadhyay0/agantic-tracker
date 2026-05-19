from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, Dict

class AuditLogBase(BaseModel):
    action: str
    actor_id: str
    resource_id: Optional[str] = None
    scope: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    client_ip: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True

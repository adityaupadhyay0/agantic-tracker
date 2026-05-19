from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLogModel
from app.schemas.audit import AuditLogCreate
import json

class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(self, entry: AuditLogCreate):
        db_log = AuditLogModel(
            actor_id=entry.actor_id,
            action=entry.action,
            resource_id=entry.resource_id,
            scope=entry.scope,
            details=entry.details,
            client_ip=entry.client_ip
        )
        self.db.add(db_log)
        await self.db.commit()
        return db_log

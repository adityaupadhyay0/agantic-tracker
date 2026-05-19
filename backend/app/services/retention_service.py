from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from app.models.bco import BCOModel
from app.models.telemetry import Telemetry, BehavioralSession
from app.services.audit_service import AuditService
from app.schemas.audit import AuditLogCreate
from datetime import datetime
import json

class RetentionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def detect_drift(self):
        """
        Identifies BCOs whose validity window has passed and flags them as drifted.
        In a full implementation, this would trigger a re-validation or compression pass.
        """
        result = await self.db.execute(select(BCOModel).where(BCOModel.drift_flag == False))
        bcos = result.scalars().all()

        now = datetime.utcnow()
        drift_count = 0

        for bco in bcos:
            # validity_window is ISO8601 duration like P7D, P30D
            # Simplified logic for demo: default to 7 days if not parseable
            last_validated = datetime.fromisoformat(bco.temporal_json.get("last_validated"))
            if (now - last_validated).days >= 7:
                bco.drift_flag = True
                # Update the JSON structure
                new_temporal = dict(bco.temporal_json)
                new_temporal["drift_flag"] = True
                bco.temporal_json = new_temporal
                drift_count += 1

        if drift_count > 0:
            await self.db.commit()

        return drift_count

    async def delete_user_data(self, user_id: str, actor_id: str):
        """
        Implements 'Right to Deletion' (PV-04).
        Removes all raw telemetry, behavioral sessions, and individual-scope BCOs for a user.
        """
        # Delete Telemetry
        await self.db.execute(delete(Telemetry).where(Telemetry.user_id == user_id))

        # Delete Sessions
        await self.db.execute(delete(BehavioralSession).where(BehavioralSession.user_id == user_id))

        # Delete Individual BCOs
        await self.db.execute(delete(BCOModel).where(
            BCOModel.scope == "individual",
            BCOModel.scope_id == user_id
        ))

        # Audit Log for Deletion
        audit = AuditService(self.db)
        await audit.log(AuditLogCreate(
            action="DATA_DELETION_REQUEST",
            actor_id=actor_id,
            resource_id=user_id,
            scope="individual",
            details={"status": "completed", "reason": "GDPR/CCPA Right to Deletion"}
        ))

        await self.db.commit()
        return True

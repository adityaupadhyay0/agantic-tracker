from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.telemetry import BehavioralSession
from app.models.bco import BCOModel
from app.schemas.bco import BCOScope, BCOType
from datetime import datetime, timedelta
import json

class CompressionEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def compress_individual_patterns(self, user_id: str):
        """
        Analyzes behavioral sessions for a user and compresses them into BCOs.
        """
        # Fetch recent sessions for the user
        result = await self.db.execute(
            select(BehavioralSession).where(BehavioralSession.user_id == user_id)
        )
        sessions = result.scalars().all()

        if not sessions:
            return

        # Simple logic: Identify if user has a dominant "Deep Focus" rhythm
        deep_focus_sessions = [s for s in sessions if s.state == "deep_focus"]

        if len(deep_focus_sessions) >= 3:
            # Create a Rhythm BCO
            bco = BCOModel(
                scope=BCOScope.INDIVIDUAL,
                scope_id=user_id,
                type=BCOType.RHYTHM,
                label="Consistent Deep Focus Pattern",
                evidence=["Detected 3+ deep focus sessions in the last observation window"],
                confidence=0.85,
                temporal_json={
                    "first_observed": datetime.utcnow().isoformat(),
                    "last_validated": datetime.utcnow().isoformat(),
                    "validity_window": "P7D",
                    "drift_flag": False
                },
                context_json={
                    "domain": "engineering",
                    "conditions": ["High edit velocity", "Minimal communication"],
                    "exceptions": ["Meeting overlap"]
                },
                version="1.0.0",
                lineage=[]
            )
            self.db.add(bco)
            await self.db.commit()

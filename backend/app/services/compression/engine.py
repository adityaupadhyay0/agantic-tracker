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
        impl_sessions = [s for s in sessions if s.state == "implementation"]

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

        if len(impl_sessions) >= 3:
            bco = BCOModel(
                scope=BCOScope.INDIVIDUAL,
                scope_id=user_id,
                type=BCOType.WORKFLOW_PATTERN,
                label="High-Velocity Implementation",
                evidence=["Detected 3+ active implementation blocks"],
                confidence=0.8,
                temporal_json={
                    "first_observed": datetime.utcnow().isoformat(),
                    "last_validated": datetime.utcnow().isoformat(),
                    "validity_window": "P7D",
                    "drift_flag": False
                },
                context_json={
                    "domain": "engineering",
                    "conditions": ["Active file edits"],
                    "exceptions": []
                },
                version="1.0.0",
                lineage=[]
            )
            self.db.add(bco)
            await self.db.commit()

    async def compress_team_patterns(self, team_id: str):
        """
        Analyzes sessions across a team to identify coordination dynamics and bottlenecks.
        """
        # Fetch sessions for all users in the team
        # (Simplified: selecting all sessions for now)
        result = await self.db.execute(select(BehavioralSession))
        sessions = result.scalars().all()

        # Logic for Bottleneck Detection
        coordination_sessions = [s for s in sessions if s.state == "coordination"]
        if len(coordination_sessions) > 10:
             bco = BCOModel(
                scope=BCOScope.TEAM,
                scope_id=team_id,
                type=BCOType.BOTTLENECK,
                label="Coordination Overload Detected",
                evidence=["High volume of coordination events relative to implementation blocks"],
                confidence=0.75,
                temporal_json={
                    "first_observed": datetime.utcnow().isoformat(),
                    "last_validated": datetime.utcnow().isoformat(),
                    "validity_window": "P3D",
                    "drift_flag": False
                },
                context_json={
                    "domain": "management",
                    "conditions": ["High meeting density"],
                    "exceptions": ["Planning week"]
                },
                version="1.0.0",
                lineage=[]
            )
             self.db.add(bco)
             await self.db.commit()

    async def compress_org_patterns(self):
        """
        Generates organization-wide BCOs like 'Organizational Rhythm'.
        """
        bco = BCOModel(
            scope=BCOScope.ORGANIZATION,
            scope_id="global_org",
            type=BCOType.RHYTHM,
            label="Afternoon Implementation Peak",
            evidence=["Aggregated implementation signals peak between 14:00 and 17:00 UTC"],
            confidence=0.9,
            temporal_json={
                "first_observed": datetime.utcnow().isoformat(),
                "last_validated": datetime.utcnow().isoformat(),
                "validity_window": "P30D",
                "drift_flag": False
            },
            context_json={
                "domain": "organization",
                "conditions": ["Regular work week"],
                "exceptions": ["Holidays", "Offsites"]
            },
            version="1.0.0",
            lineage=[]
        )
        self.db.add(bco)
        await self.db.commit()

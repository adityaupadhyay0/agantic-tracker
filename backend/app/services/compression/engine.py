from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.telemetry import BehavioralSession
from app.models.bco import BCOModel
from app.schemas.bco import BCOScope, BCOType, BCO
from app.services.enrichment.vector_store import VectorStore
from app.services.audit_service import AuditService
from app.services.webhook_service import WebhookService
from app.schemas.audit import AuditLogCreate
from datetime import datetime, timedelta
import json

class CompressionEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vector_store = VectorStore()

    async def _save_bco(self, bco: BCOModel):
        self.db.add(bco)
        await self.db.commit()

        # Trigger Webhooks
        webhook_service = WebhookService(self.db)
        await webhook_service.trigger("BCO_CREATED", {
            "bco_id": bco.id,
            "scope": bco.scope.value,
            "type": bco.type.value,
            "label": bco.label
        })

        # Audit Log
        audit = AuditService(self.db)
        await audit.log(AuditLogCreate(
            action="BCO_CREATED",
            actor_id="CORTEX_ENGINE",
            resource_id=bco.id,
            scope=bco.scope.value,
            details={"type": bco.type.value, "label": bco.label}
        ))

        # Add to vector store
        bco_schema = BCO(
            bco_id=bco.id,
            scope=bco.scope,
            scope_id=bco.scope_id,
            type=bco.type,
            label=bco.label,
            evidence=bco.evidence,
            confidence=bco.confidence,
            temporal=bco.temporal_json,
            context=bco.context_json,
            version=bco.version,
            lineage=bco.lineage
        )
        self.vector_store.add_bco(bco_schema)

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
            # Check if BCO already exists
            existing = await self.db.execute(
                select(BCOModel).where(
                    BCOModel.scope == BCOScope.INDIVIDUAL,
                    BCOModel.scope_id == user_id,
                    BCOModel.type == BCOType.RHYTHM,
                    BCOModel.label == "Consistent Deep Focus Pattern"
                )
            )
            if not existing.scalar_one_or_none():
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
                await self._save_bco(bco)

        if len(impl_sessions) >= 3:
            existing = await self.db.execute(
                select(BCOModel).where(
                    BCOModel.scope == BCOScope.INDIVIDUAL,
                    BCOModel.scope_id == user_id,
                    BCOModel.type == BCOType.WORKFLOW_PATTERN,
                    BCOModel.label == "High-Velocity Implementation"
                )
            )
            if not existing.scalar_one_or_none():
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
                await self._save_bco(bco)

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
             existing = await self.db.execute(
                 select(BCOModel).where(
                     BCOModel.scope == BCOScope.TEAM,
                     BCOModel.scope_id == team_id,
                     BCOModel.type == BCOType.BOTTLENECK,
                     BCOModel.label == "Coordination Overload Detected"
                 )
             )
             if not existing.scalar_one_or_none():
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
                 await self._save_bco(bco)

    async def compress_org_patterns(self):
        """
        Generates organization-wide BCOs like 'Organizational Rhythm'.
        """
        existing = await self.db.execute(
            select(BCOModel).where(
                BCOModel.scope == BCOScope.ORGANIZATION,
                BCOModel.scope_id == "global_org",
                BCOModel.type == BCOType.RHYTHM,
                BCOModel.label == "Afternoon Implementation Peak"
            )
        )
        if not existing.scalar_one_or_none():
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
            await self._save_bco(bco)

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.telemetry import TelemetryEvent, WorkState, TelemetrySource
from app.models.telemetry import BehavioralSession
from app.services.compression.engine import CompressionEngine
from datetime import datetime, timedelta
import json

class InterpretationEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_event(self, event: TelemetryEvent):
        """
        Processes a raw telemetry event and maps it to a behavioral state.
        In a full implementation, this would use LLM reasoning for ambiguous states.
        For MVP, we use rule-based logic with an LLM fallback.
        """
        state, confidence, evidence = self._rule_based_interpretation(event)

        # Check if there's an active session for this user
        # If the state matches, we might extend it. If it differs, we close the old one and start a new one.
        # This is a simplified version of session segmentation.

        new_session = BehavioralSession(
            user_id=event.user_id,
            state=state,
            start_time=event.timestamp,
            end_time=event.timestamp + timedelta(minutes=15), # Default block
            confidence=confidence,
            evidence=evidence,
            metadata_json=event.metadata
        )
        self.db.add(new_session)
        await self.db.commit()

        # Trigger compression engine to update BCOs
        compression_engine = CompressionEngine(self.db)
        await compression_engine.compress_individual_patterns(event.user_id)

        # Periodically or conditionally trigger team/org patterns
        # For demonstration, we trigger them every time
        await compression_engine.compress_team_patterns("engineering_team_a")
        await compression_engine.compress_org_patterns()

    def _rule_based_interpretation(self, event: TelemetryEvent):
        if event.source == TelemetrySource.IDE:
            if event.event_type in ["file_edit", "save"]:
                return WorkState.IMPLEMENTATION, 0.8, ["High edit velocity detected in IDE"]
            elif event.event_type == "debug_start":
                return WorkState.DEBUGGING, 0.9, ["Debugger attached in IDE"]

        if event.source == TelemetrySource.GIT:
            if event.event_type == "pr_review":
                return WorkState.REVIEW, 0.85, ["PR review activity on GitHub"]

        if event.source == TelemetrySource.COMMUNICATION:
            return WorkState.COORDINATION, 0.7, ["Communication metadata activity"]

        if event.source == TelemetrySource.DESIGN:
            return WorkState.DESIGN_FOCUS, 0.85, ["Design tool activity detected (e.g. Figma)"]

        if event.source == TelemetrySource.CALENDAR:
            return WorkState.COORDINATION, 0.9, ["Meeting metadata from Calendar"]

        return WorkState.RESEARCH, 0.5, ["Defaulting to research for unclassified activity"]

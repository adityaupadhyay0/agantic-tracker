from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class TelemetrySource(str, Enum):
    IDE = "ide"
    GIT = "git"
    COMMUNICATION = "communication"
    AGENT = "agent"
    CALENDAR = "calendar"
    TICKET = "ticket"

class TelemetryEvent(BaseModel):
    event_id: str
    source: TelemetrySource
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: str
    metadata: Dict[str, Any]

class WorkState(str, Enum):
    DEEP_FOCUS = "deep_focus"
    RESEARCH = "research"
    IMPLEMENTATION = "implementation"
    REVIEW = "review"
    DEBUGGING = "debugging"
    COORDINATION = "coordination"
    PLANNING = "planning"
    LEARNING = "learning"
    IDLE = "idle"

class BehavioralState(BaseModel):
    user_id: str
    state: WorkState
    start_time: datetime
    end_time: Optional[datetime] = None
    confidence: float
    evidence: List[str]
    metadata: Dict[str, Any] = {}

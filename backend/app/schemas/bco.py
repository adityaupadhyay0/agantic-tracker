from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class BCOScope(str, Enum):
    INDIVIDUAL = "individual"
    TEAM = "team"
    ORGANIZATION = "organization"

class BCOType(str, Enum):
    WORKFLOW_PATTERN = "workflow_pattern"
    EXPERTISE_SIGNAL = "expertise_signal"
    COORDINATION_DYNAMIC = "coordination_dynamic"
    RHYTHM = "rhythm"
    BOTTLENECK = "bottleneck"

class TemporalMetadata(BaseModel):
    first_observed: datetime
    last_validated: datetime
    validity_window: str
    drift_flag: bool = False

class BCOContext(BaseModel):
    domain: str
    conditions: List[str]
    exceptions: List[str]

class BCO(BaseModel):
    bco_id: str
    scope: BCOScope
    scope_id: str
    type: BCOType
    label: str
    evidence: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    temporal: TemporalMetadata
    context: BCOContext
    version: str = "1.0.0"
    lineage: List[str] = []

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class PredictionType(str, Enum):
    COORDINATION_RISK = "coordination_risk"
    EXPERTISE_GAP = "expertise_gap"
    BEHAVIORAL_DRIFT = "behavioral_drift"
    RHYTHM_SHIFT = "rhythm_shift"

class Prediction(BaseModel):
    prediction_id: str
    type: PredictionType
    label: str
    probability: float = Field(ge=0.0, le=1.0)
    forecast_window: str # e.g., "Next 7 days"
    evidence: List[str]
    impact_score: float = Field(ge=0.0, le=1.0)
    remediation_steps: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

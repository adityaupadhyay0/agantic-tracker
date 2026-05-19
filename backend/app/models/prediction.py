from sqlalchemy import Column, String, DateTime, JSON, Float, Enum as SQLEnum
from app.db.base import Base
import uuid
from app.schemas.prediction import PredictionType

class PredictionModel(Base):
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(SQLEnum(PredictionType))
    label = Column(String)
    probability = Column(Float)
    forecast_window = Column(String)
    evidence = Column(JSON)
    impact_score = Column(Float)
    remediation_steps = Column(JSON)
    created_at = Column(DateTime)

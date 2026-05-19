from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.schemas.prediction import Prediction
from app.models.prediction import PredictionModel
from app.services.prediction_service import PredictionService
from typing import List

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/generate", response_model=List[Prediction])
async def generate_predictions(db: AsyncSession = Depends(get_db)):
    service = PredictionService(db)
    models = await service.generate_predictions()
    return [
        Prediction(
            prediction_id=m.id,
            type=m.type,
            label=m.label,
            probability=m.probability,
            forecast_window=m.forecast_window,
            evidence=m.evidence,
            impact_score=m.impact_score,
            remediation_steps=m.remediation_steps,
            created_at=m.created_at
        ) for m in models
    ]

@router.get("/", response_model=List[Prediction])
async def list_predictions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PredictionModel).order_by(PredictionModel.created_at.desc()))
    models = result.scalars().all()

    return [
        Prediction(
            prediction_id=m.id,
            type=m.type,
            label=m.label,
            probability=m.probability,
            forecast_window=m.forecast_window,
            evidence=m.evidence,
            impact_score=m.impact_score,
            remediation_steps=m.remediation_steps,
            created_at=m.created_at
        ) for m in models
    ]

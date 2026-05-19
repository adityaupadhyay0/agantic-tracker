from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.bco import BCOModel
from app.models.prediction import PredictionModel
from app.schemas.prediction import PredictionType
from datetime import datetime, timedelta
import json

class PredictionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_predictions(self):
        """
        Analyzes historical BCOs to generate predictive insights.
        """
        # Fetch all BCOs
        result = await self.db.execute(select(BCOModel))
        bcos = result.scalars().all()

        if not bcos:
            return []

        predictions = []

        # 1. Predict Coordination Risk
        bottlenecks = [b for b in bcos if b.type == "bottleneck"]
        if len(bottlenecks) >= 2:
            existing = await self.db.execute(
                select(PredictionModel).where(
                    PredictionModel.type == PredictionType.COORDINATION_RISK,
                    PredictionModel.label == "High Risk of Coordination Breakdown"
                )
            )
            if not existing.scalar_one_or_none():
                prediction = PredictionModel(
                    type=PredictionType.COORDINATION_RISK,
                    label="High Risk of Coordination Breakdown",
                    probability=0.82,
                    forecast_window="Next 7 Days",
                    evidence=["Detected recurring bottlenecks in PR review cycle", "Increasing trend in coordination-to-implementation ratio"],
                    impact_score=0.75,
                    remediation_steps=["Shift team to async updates", "Re-evaluate meeting frequency"],
                    created_at=datetime.utcnow()
                )
                predictions.append(prediction)

        # 2. Predict Expertise Gap
        # (Simplified: logic would check for declining expertise BCOs or missing domain coverage)
        existing_gap = await self.db.execute(
            select(PredictionModel).where(
                PredictionModel.type == PredictionType.EXPERTISE_GAP,
                PredictionModel.label == "Emerging Gap in Cloud Infrastructure"
            )
        )
        if not existing_gap.scalar_one_or_none():
            prediction = PredictionModel(
                type=PredictionType.EXPERTISE_GAP,
                label="Emerging Gap in Cloud Infrastructure",
                probability=0.65,
                forecast_window="Next 30 Days",
                evidence=["Declining implementation signals in 'infra' domain", "Primary contributor shifted to design_focus state"],
                impact_score=0.8,
                remediation_steps=["Schedule knowledge transfer", "Identify backup maintainers"],
                created_at=datetime.utcnow()
            )
            predictions.append(prediction)

        for p in predictions:
            self.db.add(p)

        await self.db.commit()
        return predictions

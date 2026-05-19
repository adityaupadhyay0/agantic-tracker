from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.core.auth import get_current_user, UserContext
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter(prefix="/enterprise", tags=["enterprise"])

class OntologyExtension(BaseModel):
    state: str
    definition: str
    signals: List[str]

@router.post("/ontology/customize")
async def customize_ontology(
    extension: OntologyExtension,
    db: AsyncSession = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can customize the ontology")

    # In a full implementation, this would update a persistent Ontology configuration table.
    # For now, we return success to simulate the configuration.
    return {
        "status": "success",
        "message": f"Ontology extended with state '{extension.state}'",
        "applied_to_org": "global_org"
    }

@router.get("/usage")
async def get_usage_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    # Simulated usage metrics for the Billing dashboard
    return {
        "active_users": 142,
        "total_telemetry_events": 850432,
        "active_bcos": 1245,
        "api_calls_last_30d": 45200,
        "storage_used_gb": 1.2,
        "billing_tier": "Enterprise"
    }

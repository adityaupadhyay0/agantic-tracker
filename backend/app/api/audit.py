from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.schemas.audit import AuditLog
from app.models.audit import AuditLogModel
from app.core.auth import get_current_user, UserContext
from typing import List

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("/", response_model=List[AuditLog])
async def list_audit_logs(
    db: AsyncSession = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    # Only Admin can see full audit logs in production
    # For now, we allow access for demonstration
    result = await db.execute(select(AuditLogModel).order_by(AuditLogModel.timestamp.desc()).limit(100))
    logs = result.scalars().all()
    return logs

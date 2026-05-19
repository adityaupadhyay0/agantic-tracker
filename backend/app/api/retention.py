from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.services.retention_service import RetentionService
from app.core.auth import get_current_user, UserContext

router = APIRouter(prefix="/retention", tags=["retention"])

@router.post("/drift-check")
async def trigger_drift_check(db: AsyncSession = Depends(get_db)):
    service = RetentionService(db)
    count = await service.detect_drift()
    return {"status": "success", "drifted_bcos_found": count}

@router.delete("/user/{user_id}")
async def delete_user_data(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    # Only Admin or the User themselves can delete data
    if current_user.role != "admin" and current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this data")

    service = RetentionService(db)
    await service.delete_user_data(user_id, current_user.user_id)
    return {"status": "success", "message": f"All data for user {user_id} has been deleted."}

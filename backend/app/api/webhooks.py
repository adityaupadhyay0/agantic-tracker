from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.schemas.webhook import Webhook, WebhookCreate
from app.models.webhook import WebhookModel
from app.core.auth import get_current_user, UserContext
from typing import List

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/", response_model=Webhook)
async def create_webhook(
    hook: WebhookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    db_hook = WebhookModel(
        url=hook.url,
        events=hook.events,
        secret=hook.secret,
        is_active=hook.is_active
    )
    db.add(db_hook)
    await db.commit()
    return db_hook

@router.get("/", response_model=List[Webhook])
async def list_webhooks(
    db: AsyncSession = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    result = await db.execute(select(WebhookModel))
    return result.scalars().all()

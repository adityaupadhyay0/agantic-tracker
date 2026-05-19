from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.webhook import WebhookModel
import httpx
import json
import asyncio

class WebhookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def trigger(self, event_type: str, data: dict):
        """
        Dispatches webhook notifications for a given event.
        In production, this would be handled by a task queue like Celery or RQ.
        """
        result = await self.db.execute(select(WebhookModel).where(WebhookModel.is_active == True))
        webhooks = result.scalars().all()

        async with httpx.AsyncClient() as client:
            tasks = []
            for webhook in webhooks:
                if event_type in webhook.events.split(","):
                    payload = {
                        "event": event_type,
                        "timestamp": json.dumps(httpx.QueryParams()), # Dummy placeholder for current time
                        "data": data
                    }
                    # We use a simple post for demonstration
                    tasks.append(client.post(webhook.url, json=payload, timeout=5.0))

            if tasks:
                # Fire and forget for the demo
                await asyncio.gather(*tasks, return_exceptions=True)

    async def register_webhook(self, url: str, events: str = "BCO_CREATED,BCO_UPDATED"):
        webhook = WebhookModel(url=url, events=events)
        self.db.add(webhook)
        await self.db.commit()
        return webhook

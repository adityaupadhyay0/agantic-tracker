from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List, Optional

class WebhookBase(BaseModel):
    url: str
    events: Optional[str] = "BCO_CREATED,BCO_UPDATED"
    is_active: Optional[bool] = True

class WebhookCreate(WebhookBase):
    secret: Optional[str] = None

class Webhook(WebhookBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

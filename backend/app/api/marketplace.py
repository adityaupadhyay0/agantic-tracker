from fastapi import APIRouter, Depends
from app.services.marketplace import TemplateMarketplace, BCOTemplate
from typing import List

router = APIRouter(prefix="/marketplace", tags=["marketplace"])
marketplace = TemplateMarketplace()

@router.get("/templates", response_model=List[BCOTemplate])
async def list_templates():
    return marketplace.list_templates()

@router.get("/templates/{template_id}", response_model=BCOTemplate)
async def get_template(template_id: str):
    return marketplace.get_template(template_id)

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.schemas.bco import BCO, BCOScope, BCOType
from app.models.bco import BCOModel
from app.core.auth import get_current_user, check_scope_access, UserContext
from app.services.enrichment.vector_store import VectorStore
from app.services.audit_service import AuditService
from app.schemas.audit import AuditLogCreate
from typing import List, Optional

router = APIRouter(prefix="/bcos", tags=["bcos"])
vector_store = VectorStore()

@router.get("/", response_model=List[BCO])
async def list_bcos(
    scope: Optional[BCOScope] = None,
    scope_id: Optional[str] = None,
    type: Optional[BCOType] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    if scope:
        check_scope_access(current_user, scope.value, scope_id)

    query = select(BCOModel)
    if scope:
        query = query.where(BCOModel.scope == scope)
    if scope_id:
        query = query.where(BCOModel.scope_id == scope_id)
    if type:
        query = query.where(BCOModel.type == type)

    result = await db.execute(query)
    models = result.scalars().all()

    return [
        BCO(
            bco_id=m.id,
            scope=m.scope,
            scope_id=m.scope_id,
            type=m.type,
            label=m.label,
            evidence=m.evidence,
            confidence=m.confidence,
            temporal=m.temporal_json,
            context=m.context_json,
            version=m.version,
            lineage=m.lineage
        ) for m in models
    ]

@router.get("/search", response_model=List[BCO])
async def search_bcos(
    q: str = Query(..., description="Semantic search query"),
    db: AsyncSession = Depends(get_db)
):
    bco_ids = vector_store.search_bcos(q)
    result = await db.execute(select(BCOModel).where(BCOModel.id.in_(bco_ids)))
    models = result.scalars().all()

    return [
        BCO(
            bco_id=m.id,
            scope=m.scope,
            scope_id=m.scope_id,
            type=m.type,
            label=m.label,
            evidence=m.evidence,
            confidence=m.confidence,
            temporal=m.temporal_json,
            context=m.context_json,
            version=m.version,
            lineage=m.lineage
        ) for m in models
    ]

@router.get("/{bco_id}", response_model=BCO)
async def get_bco(
    bco_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    result = await db.execute(select(BCOModel).where(BCOModel.id == bco_id))
    m = result.scalar_one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail="BCO not found")

    # Audit Log
    audit = AuditService(db)
    await audit.log(AuditLogCreate(
        action="BCO_ACCESS",
        actor_id=current_user.user_id,
        resource_id=m.id,
        scope=m.scope.value,
        details={"label": m.label}
    ))

    return BCO(
        bco_id=m.id,
        scope=m.scope,
        scope_id=m.scope_id,
        type=m.type,
        label=m.label,
        evidence=m.evidence,
        confidence=m.confidence,
        temporal=m.temporal_json,
        context=m.context_json,
        version=m.version,
        lineage=m.lineage
    )

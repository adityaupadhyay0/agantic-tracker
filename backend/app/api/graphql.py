import strawberry
from typing import List, Optional
from strawberry.fastapi import GraphQLRouter
from app.models.bco import BCOModel
from sqlalchemy import select
from app.db.base import AsyncSessionLocal
from enum import Enum

class ScopeEnumBase(str, Enum):
    INDIVIDUAL = "individual"
    TEAM = "team"
    ORGANIZATION = "organization"

@strawberry.enum
class ScopeEnum(Enum):
    INDIVIDUAL = "individual"
    TEAM = "team"
    ORGANIZATION = "organization"

@strawberry.type
class BCOTypeGraphQL:
    id: strawberry.ID
    scope: str
    scope_id: str
    type: str
    label: str
    confidence: float
    version: str

@strawberry.type
class Query:
    @strawberry.field
    async def bcos(self, scope: Optional[ScopeEnum] = None, scope_id: Optional[str] = None) -> List[BCOTypeGraphQL]:
        async with AsyncSessionLocal() as db:
            query = select(BCOModel)
            if scope:
                query = query.where(BCOModel.scope == scope.value)
            if scope_id:
                query = query.where(BCOModel.scope_id == scope_id)

            result = await db.execute(query)
            models = result.scalars().all()

            return [
                BCOTypeGraphQL(
                    id=strawberry.ID(m.id),
                    scope=m.scope,
                    scope_id=m.scope_id,
                    type=m.type,
                    label=m.label,
                    confidence=m.confidence,
                    version=m.version
                ) for m in models
            ]

schema = strawberry.Schema(query=Query)
router = GraphQLRouter(schema)

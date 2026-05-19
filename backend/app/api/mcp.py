from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.api.bcos import list_bcos
from typing import Dict, Any, List

router = APIRouter(prefix="/mcp", tags=["mcp"])

@router.get("/resources")
async def list_resources():
    """MCP standard for listing available resources."""
    return {
        "resources": [
            {
                "uri": "cortex://bcos",
                "name": "Behavioral Context Objects",
                "description": "Durable semantic context about organizational behavior",
                "mimeType": "application/json"
            }
        ]
    }

@router.get("/tools")
async def list_tools():
    """MCP standard for listing available tools for agents."""
    return {
        "tools": [
            {
                "name": "query_context",
                "description": "Retrieve relevant behavioral context for a user or team",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "user_id": {"type": "string"},
                        "scope": {"type": "string", "enum": ["individual", "team", "organization"]}
                    },
                    "required": ["query"]
                }
            }
        ]
    }

@router.post("/tools/query_context")
async def query_context(
    params: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    # This would call the VectorStore and then retrieve full BCOs from the DB
    # For now, we reuse the existing BCO listing logic
    return await list_bcos(db=db)

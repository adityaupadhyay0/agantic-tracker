import httpx
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class CortexClient:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url

    async def ingest_telemetry(self, event_type: str, source: str, user_id: str, metadata: Dict[str, Any]):
        async with httpx.AsyncClient() as client:
            payload = {
                "event_id": f"evt_{int(datetime.utcnow().timestamp())}",
                "source": source,
                "user_id": user_id,
                "event_type": event_type,
                "metadata": metadata,
                "timestamp": datetime.utcnow().isoformat()
            }
            response = await client.post(f"{self.api_url}/telemetry/ingest", json=payload)
            response.raise_for_status()
            return response.json()

    async def get_context(self, user_id: Optional[str] = None, scope: str = "organization"):
        async with httpx.AsyncClient() as client:
            params = {"scope": scope}
            if user_id:
                params["scope_id"] = user_id
            response = await client.get(f"{self.api_url}/bcos/", params=params)
            response.raise_for_status()
            return response.json()

# LangChain Integration Example
class CortexLangChainTool:
    def __init__(self, client: CortexClient):
        self.client = client
        self.name = "cortex_context_retriever"
        self.description = "Use this tool to retrieve organizational and behavioral context about users and teams."

    async def _arun(self, query: str, user_id: Optional[str] = None):
        return await self.client.get_context(user_id=user_id)

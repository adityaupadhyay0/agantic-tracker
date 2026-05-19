import pytest
from httpx import AsyncClient
from app.main import app
from app.db.base import get_db
from app.schemas.telemetry import TelemetrySource

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

import httpx

from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_ingest_telemetry():
    payload = {
        "event_id": "test_evt_1",
        "source": "ide",
        "user_id": "test_user",
        "event_type": "file_edit",
        "timestamp": "2026-05-18T10:00:00Z",
        "metadata": {"file": "test.py"}
    }

    # Mock database dependency
    mock_db = AsyncMock()
    app.dependency_overrides[get_db] = lambda: mock_db

    async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        with patch("app.api.telemetry.InterpretationEngine", return_value=AsyncMock()):
            response = await ac.post("/telemetry/ingest", json=payload)

    app.dependency_overrides = {}
    assert response.status_code == 200
    assert response.json()["status"] == "success"

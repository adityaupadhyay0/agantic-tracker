import asyncio
import httpx
from datetime import datetime, timedelta
import random

API_URL = "http://localhost:8000"

async def simulate_user_activity(user_id: str):
    print(f"Simulating activity for {user_id}...")

    # 1. Implementation Session
    print("-> Starting Implementation Session")
    for _ in range(3):
        payload = {
            "event_id": f"evt_impl_{random.randint(1000, 9999)}",
            "source": "ide",
            "user_id": user_id,
            "event_type": "file_edit",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {"file": "app/main.py", "lines_changed": 15}
        }
        async with httpx.AsyncClient() as client:
            await client.post(f"{API_URL}/telemetry/ingest", json=payload)
        await asyncio.sleep(0.5)

    # 2. Debugging Session
    print("-> Starting Debugging Session")
    payload = {
        "event_id": f"evt_debug_{random.randint(1000, 9999)}",
        "source": "ide",
        "user_id": user_id,
        "event_type": "debug_start",
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {"debugger": "pdb", "breakpoints": 2}
    }
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/telemetry/ingest", json=payload)

    # 3. Git Activity
    print("-> Starting Git Activity")
    payload = {
        "event_id": f"evt_git_{random.randint(1000, 9999)}",
        "source": "git",
        "user_id": user_id,
        "event_type": "pr_review",
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {"repo": "cortex-agent", "pr_id": 42}
    }
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/telemetry/ingest", json=payload)

    print(f"Simulation for {user_id} complete.")

async def main():
    users = ["user_dev_01", "user_lead_02"]
    await asyncio.gather(*[simulate_user_activity(u) for u in users])

if __name__ == "__main__":
    asyncio.run(main())

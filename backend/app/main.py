from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import telemetry, bcos, mcp

app = FastAPI(title="CORTEX — Behavioral Context Enrichment Agent", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to CORTEX API", "status": "active"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(telemetry.router)
app.include_router(bcos.router)
app.include_router(mcp.router)

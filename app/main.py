from fastapi import FastAPI
from app.api import agent_api

app = FastAPI(title="AI Agent Reservation Service")

app.include_router(agent_api.router, prefix="/agent", tags=["Agent"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
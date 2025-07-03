from fastapi import FastAPI
from app.api import agent_api

from app.core.logger import logger
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 {app.title} 서버가 시작되었습니다!")
    logger.info("📄 Swagger 문서: http://127.0.0.1:8000/docs")
    yield
    logger.info("🛑 FastAPI 서버가 종료됩니다.")
app = FastAPI(
    title="AI Agent Reservation Service",
    lifespan=lifespan
)

app.include_router(agent_api.router, prefix="/agent", tags=["Agent"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
from dotenv import load_dotenv
import os

# .env 파일 로드 (루트 경로에 위치한 .env)
load_dotenv()

# Google Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 서비스 환경 (local / dev / prod)
APP_ENV = os.getenv("APP_ENV", "local")

# FastAPI 서버 기본 설정
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# 로깅 설정 (기본값 INFO)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# 예: 향후 Redis 연동 시 사용 가능
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 예: 향후 VectorDB (ex: Qdrant) API Endpoint
VECTORDB_API_URL = os.getenv("VECTORDB_API_URL", "http://localhost:6333")

# 기타 공통 설정 추가 가능
# 예: Debug 모드 설정
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# 사용 예시 (다른 모듈에서 import 후 사용):
# from app.core.config import GOOGLE_API_KEY, APP_ENV, DEBUG

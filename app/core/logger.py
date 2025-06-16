import logging
import sys
from logging.config import dictConfig
from app.core.config import LOG_LEVEL

def setup_logger():
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
        },
        "root": {
            "level": LOG_LEVEL,
            "handlers": ["default"],
        },
    }

    dictConfig(log_config)

# 로거 초기화 및 전역 logger 객체
setup_logger()
logger = logging.getLogger("app")

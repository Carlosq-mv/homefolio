from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

from app.api.v1.api import api_router
from app.db.base import Base, engine
from app.core.exceptions import UserError, JwtError
from app.core.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.exception_handler(UserError)
async def user_error_handler(_, exc: UserError):
    logger.warning(f"{exc.__class__.__name__}-{exc.message}(code={exc.status_code})")

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail" : exc.message}
    )

@app.exception_handler(JwtError)
async def user_error_handler(_, exc: JwtError):
    logger.warning(f"{exc.__class__.__name__}-{exc.message}(code={exc.status_code})")

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail" : exc.message}
    )

app.include_router(api_router, prefix="/api/v1")

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.v1.api import api_router
from app.db.base import Base, engine
from app.core.exceptions import UserError

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.exception_handler(UserError)
async def user_error_handler(_, exc: UserError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail" : exc.message}
    )

app.include_router(api_router, prefix="/api/v1")

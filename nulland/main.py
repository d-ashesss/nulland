from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from .db.session import init_db
from .routes import auth
from .routes import notes
from .logging import init_logging


@asynccontextmanager
async def lifespan(_: FastAPI):
    """ Application startup initialization."""
    init_logging()
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(notes.router)


@app.get("/", include_in_schema=False)
def read_root():
    """Simple status check endpoint."""
    return {"status": "HellWorld"}


@app.middleware("http")
async def generic_exception_handler(request, call_next) -> JSONResponse:
    try:
        return await call_next(request)
    except Exception as exc:
        import logging
        logger = logging.getLogger(__name__)
        logger.critical("Absolutely unexpected exception: %s", exc, exc_info=True)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

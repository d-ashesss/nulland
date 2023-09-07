from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from nulland.db.session import init_db
from nulland.routes import auth
from nulland.routes import notes
from nulland.logging import init_logging
from nulland.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """ Application startup initialization."""
    init_logging()
    init_db()
    yield


app = FastAPI(
    title="Nulland",
    summary="Note-taking REST API with Python and FastAPI.",
    version="0.1.0",
    license_info={
        "name": "MIT License",
    },
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(notes.router)


@app.get("/", include_in_schema=False)
def read_root():
    """Simple status check endpoint."""
    return {"status": "HellWorld"}


@app.middleware("http")
async def generic_exception_handler(request, call_next) -> JSONResponse:
    """Catching all unexpected in middleware because FastAPI/Starlette error handling mechanism
    still pushes them through event if handled properly leading to excessive exception logging."""
    try:
        return await call_next(request)
    except Exception as exc:
        import logging
        logger = logging.getLogger(__name__)
        logger.critical("Absolutely unexpected exception: %s", exc, exc_info=True)
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

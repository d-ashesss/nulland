from fastapi import FastAPI
from contextlib import asynccontextmanager

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

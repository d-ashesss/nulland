import uuid

from authlib.integrations.requests_client import OAuth2Session
from fastapi import FastAPI, Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from typing import Annotated

from .auth import get_current_user
from .crud import crud_notes
from .db.session import init_db, get_db
from .schemas.auth import TokenRequest, TokenResponse
from .schemas.auth import User
from .schemas.notes import Note
from .schemas.notes import NoteCreate
from .schemas.notes import NoteUpdate
from .settings import Settings, get_settings


def lifespan(app):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"status": "HellWorld"}


@app.post("/token", include_in_schema=False)
async def get_token(settings: Annotated[Settings, Depends(get_settings)], req: Annotated[TokenRequest, Depends()]):
    oauth_sess = OAuth2Session(
        client_id=req.client_id,
        client_secret=req.client_secret,
    )
    try:
        token = oauth_sess.fetch_token(
            settings.auth_token_endpoint,
            grant_type=req.grant_type,
            code=req.code,
            redirect_uri=req.redirect_uri,
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to fetch the token")
    if "id_token" not in token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Received invalid token")
    return TokenResponse(access_token=token["id_token"], token_type=token["token_type"])


@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Create new note
    """
    note_obj = crud_notes.create_user_note(note, user, db=db)
    return note_obj


@app.get("/notes", response_model=list[Note])
def read_notes(
    user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """
    Get all notes
    """
    return crud_notes.read_user_notes(user, db=db)


@app.get(
    "/notes/{note_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Note not found"}},
    response_model=Note,
)
def get_note(
    note_id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Get single note by id
    """
    db_note = crud_notes.get_user_note_by_id(note_id, user, db=db)
    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return db_note


@app.patch(
    "/notes/{note_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Note not found"}},
    response_model=Note,
)
def update_note(
    note_id: uuid.UUID,
    note: NoteUpdate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Update single note by id
    """
    db_note = crud_notes.get_user_note_by_id(note_id, user, db=db)
    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    crud_notes.update_note(db_note, note, db=db)
    return db_note


@app.delete(
    "/notes/{note_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Note not found"}},
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Delete single note by id
    """
    db_note = crud_notes.get_user_note_by_id(note_id, user, db=db)
    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    crud_notes.delete_note(db_note, db=db)
    return None

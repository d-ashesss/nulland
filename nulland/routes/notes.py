import uuid

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from typing import Annotated

from nulland.auth import get_current_user
from nulland.crud import crud_notes
from nulland.db.session import get_db
from nulland.schemas.auth import User
from nulland.schemas.notes import Note
from nulland.schemas.notes import NoteCreate
from nulland.schemas.notes import NoteUpdate
from nulland.events import get_emitter, EventEmmiter


router = APIRouter()


@router.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    events: Annotated[EventEmmiter, Depends(get_emitter)],
):
    """Create a note owned by the current user."""
    db_note = crud_notes.create_user_note(note, user, db=db)
    events.emit("created", db_note)
    return db_note


@router.get("/notes", response_model=list[Note])
def read_notes(
    user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Get all notes owned by the current user."""
    return crud_notes.read_user_notes(user, db=db)


@router.get(
    "/notes/{note_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Note not found"}},
    response_model=Note,
)
def get_note(
    note_id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Get single note by id."""
    db_note = crud_notes.get_user_note_by_id(note_id, user, db=db)
    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return db_note


@router.patch(
    "/notes/{note_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Note not found"}},
    response_model=Note,
)
def update_note(
    note_id: uuid.UUID,
    note: NoteUpdate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    events: Annotated[EventEmmiter, Depends(get_emitter)],
):
    """Update single note by id."""
    db_note = crud_notes.get_user_note_by_id(note_id, user, db=db)
    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    crud_notes.update_note(db_note, note, db=db)
    events.emit("updated", db_note)
    return db_note


@router.delete(
    "/notes/{note_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Note not found"}},
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    events: Annotated[EventEmmiter, Depends(get_emitter)],
):
    """Delete single note by id."""
    db_note = crud_notes.get_user_note_by_id(note_id, user, db=db)
    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    crud_notes.delete_note(db_note, db=db)
    events.emit("deleted", db_note)
    return None

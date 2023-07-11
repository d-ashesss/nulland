import uuid

from datetime import datetime
from fastapi import FastAPI, Depends
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .crud import crud_notes
from .db.session import init_db, get_db
from .schemas import Note
from .schemas import NoteCreate
from .schemas import NoteUpdate


def lifespan(app):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

notes: dict[str, dict] = {}


@app.get("/")
def read_root():
    return {"status": "HellWorld"}


@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """
    Create new note
    """
    note_obj = crud_notes.create_note(note, db=db)
    return note_obj


@app.get("/notes", response_model=list[Note])
def read_notes(db: Session = Depends(get_db)):
    """
    Get all notes
    """
    return crud_notes.read_notes(db=db)


@app.get(
    "/notes/{note_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Note not found"}},
    response_model=Note,
)
def get_note(note_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Get single note by id
    """
    note = crud_notes.get_note_by_id(note_id, db=db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@app.patch(
    "/notes/{note_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Note not found"}},
    response_model=Note,
)
def update_note(note_id: uuid.UUID, note: NoteUpdate):
    """
    Update single note by id
    """
    if note_id not in notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    notes[note_id].update(note.model_dump(exclude_unset=True))
    return notes[note_id]


@app.delete(
    "/notes/{note_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Note not found"}},
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(note_id: uuid.UUID):
    """
    Delete single note by id
    """
    if note_id not in notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    del notes[note_id]
    return None

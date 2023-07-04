import uuid

from datetime import datetime
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException

from .schemas import NoteCreate, Note

app = FastAPI()

notes: dict[str, dict] = {}


@app.get("/")
def read_root():
    return {"status": "HellWorld"}


@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate):
    """
    Create new note
    """
    note_obj = {
        "id": uuid.uuid4(),
        "created_at": datetime.now(),
        "meta": "do not mind me"
    }
    note_obj.update(note.model_dump())
    notes[note_obj["id"]] = note_obj
    return note_obj


@app.get("/notes", response_model=list[Note])
def read_notes():
    """
    Get all notes
    """
    return list(notes.values())


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: uuid.UUID):
    """
    Get single note by id
    """
    if note_id not in notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return notes[note_id]
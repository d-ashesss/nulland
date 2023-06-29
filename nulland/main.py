import uuid

from datetime import datetime
from fastapi import FastAPI, status

from .schemas import CreateNoteRequest, GetNoteResponse

app = FastAPI()

notes: dict[str, dict] = {}


@app.get("/")
def read_root():
    return {"status": "HellWorld"}


@app.post("/notes", response_model=GetNoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: CreateNoteRequest):
    """
    Create new note
    """
    global notes
    note_obj = {
        "id": uuid.uuid4(),
        "created_at": datetime.now(),
        "meta": "do not mind me"
    }
    note_obj.update(note.model_dump())
    notes[note_obj["id"]] = note_obj
    return note_obj

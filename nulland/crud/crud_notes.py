import uuid
from sqlalchemy.orm import Session

from nulland.models.notes import Note
from nulland.schemas import NoteCreate


def create_note(
    note: NoteCreate,
    db: Session,
) -> Note:
    """
    Create new note
    """
    note_obj = Note(
        id=uuid.uuid4(),
        **note.model_dump(),
    )
    db.add(note_obj)
    db.commit()
    db.refresh(note_obj)
    return note_obj


def read_notes(db: Session) -> list[Note]:
    """
    Get all notes
    """
    return db.query(Note).all()


def get_note_by_id(note_id: uuid.UUID, db: Session) -> Note:
    """
    Get note by id
    """
    return db.query(Note).filter(Note.id == note_id).first()

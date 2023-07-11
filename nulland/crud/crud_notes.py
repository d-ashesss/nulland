import uuid
from sqlalchemy.orm import Session

from nulland.models.notes import Note


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

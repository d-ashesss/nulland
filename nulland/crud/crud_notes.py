import uuid
from sqlalchemy.orm import Session

from nulland.models.notes import Note
from nulland.schemas import NoteCreate, NoteUpdate


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


def update_note(db_note: Note, note: NoteUpdate, db: Session) -> Note:
    """
    Update note by id
    """
    db.query(Note).filter(Note.id == db_note.id).update(note.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(db_note)
    return db_note
    

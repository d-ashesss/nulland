import uuid
from sqlalchemy.orm import Session

from nulland.models.notes import Note
from nulland.schemas.auth import User
from nulland.schemas.notes import NoteCreate, NoteUpdate


def create_user_note(
    note: NoteCreate,
    user: User,
    db: Session,
) -> Note:
    """
    Create new note
    """
    note_obj = Note(
        id=uuid.uuid4(),
        user_id=user.id,
        **note.model_dump(),
    )
    db.add(note_obj)
    db.commit()
    db.refresh(note_obj)
    return note_obj


def read_user_notes(user: User, db: Session) -> list[Note]:
    """
    Get all notes
    """
    return db.query(Note).filter(Note.user_id == user.id).all()


def get_user_note_by_id(note_id: uuid.UUID, user: User, db: Session) -> Note:
    """
    Get note by id
    """
    return db.query(Note).filter(Note.id == note_id, Note.user_id == user.id).first()


def update_note(db_note: Note, note: NoteUpdate, db: Session) -> None:
    """
    Update note
    """
    db.query(Note).filter(Note.id == db_note.id).update(note.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(db_note)


def delete_note(db_note: Note, db: Session) -> None:
    """
    Delete note
    """
    db.query(Note).filter(Note.id == db_note.id).delete()
    db.commit()

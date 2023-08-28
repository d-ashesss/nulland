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
    """Saves a note into the database."""
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
    """Retrieves all notes owned by the user."""
    return db.query(Note).filter(Note.user_id == user.id).all()


def get_user_note_by_id(note_id: uuid.UUID, user: User, db: Session) -> Note:
    """Gets a single note by id owned by the user."""
    return db.query(Note).filter(Note.id == note_id, Note.user_id == user.id).first()


def update_note(db_note: Note, note: NoteUpdate, db: Session) -> None:
    """Save changes to a note into the database."""
    db.query(Note).filter(Note.id == db_note.id).update(note.model_dump(exclude_unset=True))
    db.commit()
    db.add(db_note)
    db.refresh(db_note)


def delete_note(db_note: Note, db: Session) -> None:
    """Deletes a note from the database."""
    db.query(Note).filter(Note.id == db_note.id).delete()
    db.commit()

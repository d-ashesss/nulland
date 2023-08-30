import pytest
import uuid

from sqlalchemy.orm import Session
from unittest import TestCase

from nulland.crud import crud_notes as crud
from nulland.models.notes import Note
from nulland.schemas.auth import User
from nulland.schemas.notes import NoteCreate, NoteUpdate


class TestCrudNotes(TestCase):
    @pytest.fixture(autouse=True)
    def setup(self, db: Session):
        self.db = db
        self.user = User(
            sub=str(uuid.uuid4()),
            name="Test User",
            email="test@localhost",
        )

    def _insert_note(self) -> Note:
        note = Note(
            id=uuid.uuid4(),
            user_id=self.user.id,
            title="Test Note",
            content="The text of test note.",
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def test_create_user_note(self):
        note_in = NoteCreate(
            title="Test Note",
            content="The text of test note.",
        )
        note_obj = crud.create_user_note(
            note=note_in,
            user=self.user,
            db=self.db,
        )
        self.assertIsInstance(note_obj, Note)
        self.assertIsNotNone(note_obj.id)
        self.assertEqual(note_obj.title, note_in.title)
        self.assertEqual(note_obj.content, note_in.content)

    def test_read_user_no_notes(self):
        notes = crud.read_user_notes(
            user=self.user,
            db=self.db,
        )
        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 0)

    def test_read_user_notes(self):
        self._insert_note()
        self.db.expunge_all()

        notes = crud.read_user_notes(
            user=self.user,
            db=self.db,
        )
        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 1)

    def test_get_user_note_by_id(self):
        note_db = self._insert_note()
        self.db.expunge_all()

        note_obj = crud.get_user_note_by_id(
            note_id=note_db.id,
            user=self.user,
            db=self.db,
        )
        self.assertIsInstance(note_obj, Note)
        self.assertEqual(note_obj.id, note_db.id)
        self.assertEqual(note_obj.title, note_db.title)
        self.assertEqual(note_obj.content, note_db.content)

    def test_get_user_note_by_id_not_found(self):
        note_obj = crud.get_user_note_by_id(
            note_id=uuid.uuid4(),
            user=self.user,
            db=self.db,
        )
        self.assertIsNone(note_obj)

    def test_update_note_title(self):
        note_db = self._insert_note()
        self.db.expunge_all()

        note_update = NoteUpdate(
            title="Updated Test Note",
        )
        crud.update_note(
            db_note=note_db,
            note=note_update,
            db=self.db,
        )
        self.db.expunge_all()

        note_obj = crud.get_user_note_by_id(
            note_id=note_db.id,
            user=self.user,
            db=self.db,
        )
        self.assertIsInstance(note_obj, Note)
        self.assertEqual(note_obj.id, note_db.id)
        self.assertEqual(note_obj.title, note_update.title)
        self.assertEqual(note_obj.content, note_db.content)
        self.assertEqual(note_db.title, note_update.title)

    def test_update_note_content(self):
        note_db = self._insert_note()
        self.db.expunge_all()

        note_update = NoteUpdate(
            content="Updated content.",
        )
        crud.update_note(
            db_note=note_db,
            note=note_update,
            db=self.db,
        )
        self.db.expunge_all()

        note_obj = crud.get_user_note_by_id(
            note_id=note_db.id,
            user=self.user,
            db=self.db,
        )
        self.assertIsInstance(note_obj, Note)
        self.assertEqual(note_obj.id, note_db.id)
        self.assertEqual(note_obj.title, note_db.title)
        self.assertEqual(note_obj.content, note_update.content)
        self.assertEqual(note_db.content, note_update.content)

    def test_delete_note(self):
        note_db = self._insert_note()
        self.db.expunge_all()

        crud.delete_note(
            db_note=note_db,
            db=self.db,
        )
        self.db.expunge_all()

        note_obj = crud.get_user_note_by_id(
            note_id=note_db.id,
            user=self.user,
            db=self.db,
        )
        self.assertIsNone(note_obj)

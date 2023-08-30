from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session
import unittest
import pytest
import uuid

from nulland.models.notes import Note
from nulland.tests.utils.auth import auth_headers


class TestNotes(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient, db: Session):
        self.client = client
        self.db = db

    def _insert_note(self, user_id) -> Note:
        note = Note(
            id=user_id,
            user_id=user_id,
            title="New Test Note",
            content="The text of the new test note.",
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def test_unauthorized(self):
        response = self.client.get("/notes")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_notes(self):
        user_id = uuid.uuid4()
        self._insert_note(user_id)

        response = self.client.get(
            "/notes",
            headers=auth_headers(user_id),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notes_resp = response.json()
        self.assertEqual(len(notes_resp), 1)

    def test_list_notes_empty_list(self):
        response = self.client.get(
            "/notes",
            headers=auth_headers(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.text, "[]")

    def test_create_note(self):
        response = self.client.post(
            "/notes",
            json={"title": "Test Note", "content": "The text of test note."},
            headers=auth_headers(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        note_resp = response.json()
        self.assertIn("id", note_resp)

        note_db = self.db.get(Note, note_resp["id"])
        self.assertEqual(note_db.title, "Test Note")
        self.assertEqual(note_db.content, "The text of test note.")

    def test_create_note_missing_title(self):
        response = self.client.post(
            "/notes",
            json={"content": "The text of test note."},
            headers=auth_headers(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_create_note_missing_content(self):
        response = self.client.post(
            "/notes",
            json={"title": "Test Note"},
            headers=auth_headers(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_note(self):
        user_id = uuid.uuid4()
        note_db = self._insert_note(user_id)

        response = self.client.get(
            f"/notes/{note_db.id}",
            headers=auth_headers(user_id),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note_resp = response.json()
        self.assertEqual(note_resp["id"], str(note_db.id))
        self.assertEqual(note_resp["title"], "New Test Note")
        self.assertEqual(note_resp["content"], "The text of the new test note.")

    def test_get_note_not_found(self):
        response = self.client.get(
            f"/notes/{uuid.uuid4()}",
            headers=auth_headers(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_note_not_owner(self):
        user_id = uuid.uuid4()
        note_db = self._insert_note(user_id)

        response = self.client.get(
            f"/notes/{note_db.id}",
            headers=auth_headers(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_note_title(self):
        user_id = uuid.uuid4()
        note_db = self._insert_note(user_id)

        response = self.client.patch(
            f"/notes/{note_db.id}",
            json={"title": "Updated Test Note"},
            headers=auth_headers(user_id),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note_resp = response.json()
        self.assertEqual(note_resp["id"], str(note_db.id))
        self.assertEqual(note_resp["title"], "Updated Test Note")
        self.assertEqual(note_resp["content"], "The text of the new test note.")

        self.db.refresh(note_db)
        self.assertEqual(note_db.title, "Updated Test Note")
        self.assertEqual(note_db.content, "The text of the new test note.")

    def test_update_note_content(self):
        user_id = uuid.uuid4()
        note_db = self._insert_note(user_id)

        response = self.client.patch(
            f"/notes/{note_db.id}",
            json={"content": "Updated content."},
            headers=auth_headers(user_id),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note_resp = response.json()
        self.assertEqual(note_resp["id"], str(note_db.id))
        self.assertEqual(note_resp["title"], "New Test Note")
        self.assertEqual(note_resp["content"], "Updated content.")

        self.db.refresh(note_db)
        self.assertEqual(note_db.title, "New Test Note")
        self.assertEqual(note_db.content, "Updated content.")

    def test_update_note_not_found(self):
        response = self.client.patch(
            f"/notes/{uuid.uuid4()}",
            json={"title": "Updated Test Note"},
            headers=auth_headers(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_note_not_owner(self):
        user_id = uuid.uuid4()
        note_db = self._insert_note(user_id)

        response = self.client.patch(
            f"/notes/{note_db.id}",
            json={"title": "Updated Test Note"},
            headers=auth_headers(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note(self):
        user_id = uuid.uuid4()
        note_db = self._insert_note(user_id)

        response = self.client.delete(
            f"/notes/{note_db.id}",
            headers=auth_headers(user_id),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.db.expunge_all()

        note_db = self.db.get(Note, note_db.id)
        self.assertIsNone(note_db)

    def test_delete_note_not_found(self):
        response = self.client.delete(
            f"/notes/{uuid.uuid4()}",
            headers=auth_headers(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note_not_owner(self):
        user_id = uuid.uuid4()
        note_db = self._insert_note(user_id)

        response = self.client.delete(
            f"/notes/{note_db.id}",
            headers=auth_headers(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.db.expunge_all()

        note_db = self.db.get(Note, note_db.id)
        self.assertIsNotNone(note_db)

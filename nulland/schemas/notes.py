from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from uuid import UUID


class BaseNote(BaseModel):
    title: str = Field(max_length=100, description="The title of the note.", examples=["My note"])
    content: str = Field(description="The content of the note.", examples=["This is my note content"])


class NoteCreate(BaseNote):
    pass


class NoteUpdate(BaseNote):
    title: str | None = Field(max_length=100, description="The title of the note.", examples=["My note"], default=None)
    content: str | None = Field(description="The content of the note.", examples=["This is my note content"], default=None)


class Note(BaseNote):
    id: UUID = Field(description="The unique identifier of the note.")
    created_at: datetime = Field(description="The time the note was created.")

    model_config = ConfigDict(from_attributes=True)


class NoteLog(Note):
    user_id: str = Field(description="The user who created the note.")

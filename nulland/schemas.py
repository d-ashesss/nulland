from datetime import datetime
from pydantic import BaseModel, Field


class BaseNoteSchema(BaseModel):
    title: str = Field(max_length=100, description="The title of the note", examples=["My note"])
    content: str = Field(description="The content of the note", examples=["This is my note content"])

class CreateNoteRequest(BaseNoteSchema):
    pass

class GetNoteResponse(BaseNoteSchema):
    id: str = Field(description="The unique identifier of the note")
    created_at: datetime = Field(description="The time the note was created")

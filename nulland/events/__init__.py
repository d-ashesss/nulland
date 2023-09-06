from nulland.config import settings, EventProducer
from nulland.events import stdout
from nulland.models.notes import Note
from nulland.schemas.notes import NoteLog


if settings.event_producer == EventProducer.KAFKA:
    pass
else:
    producer = stdout.Producer()


def emit(action: str, note: Note):
    producer.produce("notes", action, NoteLog.model_validate(note).model_dump_json())

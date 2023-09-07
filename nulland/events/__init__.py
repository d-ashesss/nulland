from functools import lru_cache

from nulland.config import settings
from nulland.events import none, stdout, kafka
from nulland.models.notes import Note
from nulland.schemas.notes import NoteLog


class Producer:
    def produce(self, topic, key, value):
        pass


class EventEmmiter:
    def __init__(self, producer: Producer):
        self.producer = producer

    def emit(self, action: str, note: Note):
        self.producer.produce("notes", action, NoteLog.model_validate(note).model_dump_json())


@lru_cache
def get_emitter():
    if settings.event_producer == settings.EventProducer.KAFKA:
        producer = kafka.Producer()
    elif settings.event_producer == settings.EventProducer.STDOUT:
        producer = stdout.Producer()
    else:
        producer = none.Producer()
    return EventEmmiter(producer)

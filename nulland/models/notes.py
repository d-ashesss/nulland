from uuid import UUID
from datetime import datetime

from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from nulland.db.base_class import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

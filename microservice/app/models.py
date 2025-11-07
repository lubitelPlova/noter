from sqlalchemy import ForeignKey, Text
from app.database import Base, int_pk
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Note(Base):
    id: Mapped[int_pk]
    title: Mapped[str]
    content: Mapped[str] = mapped_column(Text, nullable=True)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}), "
                f"title={self.title!r}, "
                f"text={self.content[:5]}...)")

    def __repr__(self):
        return str(self)


class Tag(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    note_id: Mapped[int] = mapped_column(
        ForeignKey('notes.id'), nullable=False
        )
    note: Mapped['Note'] = relationship('Note', back_populates='tags')

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.name})")

    def __repr__(self):
        return str(self)

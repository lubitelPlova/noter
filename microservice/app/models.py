from sqlalchemy import ForeignKey, Text, String, Column, Table
from app.database import Base, int_pk
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List


note_tags = Table(
    'note_tags',
    Base.metadata,
    Column('note_id', ForeignKey('notes.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)


class Note(Base):
    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text, nullable=True)

    tags: Mapped[List['Tag']] = relationship(
        'Tag',
        secondary=note_tags,
        back_populates='notes',
        lazy='selectin'
    )

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}), "
                f"title={self.title!r}, "
                f"text={self.content[:5]}...)")

    def __repr__(self):
        return str(self)


class Tag(Base):
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(50))

    notes: Mapped[List['Note']] = relationship(
        'Note',
        secondary=note_tags,
        back_populates='tags',
        lazy='selectin'
    )

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.name})")

    def __repr__(self):
        return str(self)

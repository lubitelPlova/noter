from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MetaInfoMixin:
    id: int
    created_at: datetime
    updated_at: datetime


class TagBase(BaseModel):
    name: str


class Tag(TagBase, MetaInfoMixin):
    pass


class NoteBase(BaseModel):
    title: str
    content: str = None


class NoteRequest(NoteBase):
    tags: Optional[List[TagBase]] = None


class NoteResponse(NoteBase):
    tags: Optional[List[Tag]] = None


class Note(NoteResponse, MetaInfoMixin):
    pass


class GetNotesFilter(BaseModel):
    count: int = Field(10, gt=0, le=100)
    page: int = Field(1, ge=1)
    tags: Optional[List[str]] = None

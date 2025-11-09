from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from . import models, schemas
from typing import List


async def get_notes(
    db: AsyncSession,
    filter: schemas.GetNotesFilter
):
    offset = (filter.page-1)*filter.count
    limit = filter.count

    stmt = (
        select(models.Note)
        .options(selectinload(models.Note.tags))
        .order_by(models.Note.id)
    )

    # Добавляем фильтрацию по тегам если указаны
    if filter.tags:
        # Фильтруем заметки, которые имеют ВСЕ указанные теги
        stmt = stmt.join(models.Note.tags).where(
            models.Tag.name.in_(filter.tags)
        ).group_by(models.Note.id).having(
            func.count(models.Tag.id) == len(filter.tags)
        )

    stmt = stmt.offset(offset).limit(limit)

    result = await db.execute(stmt)
    notes = result.scalars().all()
    return notes


async def get_note_by_id(
    db: AsyncSession,
    note_id: int
):
    """Найти note по ID или выбросить 404"""
    stmt = (
        select(models.Note)
        .options(selectinload(models.Note.tags))
        .where(models.Note.id == note_id)
    )
    result = await db.execute(stmt)
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    return note


async def create_note_with_tags(
    db: AsyncSession,
    note: schemas.NoteRequest
) -> models.Note:
    """Создать заметку с тегами"""

    new_note = models.Note(title=note.title, content=note.content)

    if note.tags:
        tags = await get_or_create_tags(db, note.tags)
        new_note.tags.extend(tags)

    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)

    return new_note


async def get_or_create_tags(
    db: AsyncSession,
    tags: List[schemas.TagBase]
) -> List[models.Tag]:
    """Получить существующие теги или создать новые"""
    tags_new = []

    for tag in tags:
        stmt = select(models.Tag).where(models.Tag.name == tag.name)
        result = await db.execute(stmt)
        tag_from_db = result.scalar_one_or_none()

        if not tag_from_db:
            tag_from_db = models.Tag(name=tag.name)
            db.add(tag_from_db)

        tags_new.append(tag_from_db)

    return tags_new


async def update_note(
        db: AsyncSession,
        note_id: int,
        note_r: schemas.NoteRequest
) -> models.Note:

    stmt = (
        select(models.Note)
        .options(selectinload(models.Note.tags))
        .where(models.Note.id == note_id)
    )
    result = await db.execute(stmt)
    note: models.Note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    note.title = note_r.title
    note.content = note_r.content
    note.tags = await get_or_create_tags(db, note_r.tags)

    await db.commit()

    return note


async def delete_note_by_id(
    db: AsyncSession,
    note_id: int
) -> models.Note:
    """Удалить заметку по ID"""
    stmt = select(models.Note).where(models.Note.id == note_id)
    result = await db.execute(stmt)
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    await db.delete(note)
    await db.commit()
    return note

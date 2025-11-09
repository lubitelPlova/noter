from fastapi import APIRouter, Query, Depends
from typing_extensions import Annotated
from typing import List
from .schemas import (
    GetNotesFilter, NoteRequest, Note
)
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_async_session
from . import crud


router = APIRouter()


@router.get('/health')
async def health_check():
    '''The healthcheck endpoint'''
    return {"status": "OK"}


@router.get('/notes/')
async def get_notes_list(
    filter_query: Annotated[GetNotesFilter, Query()],
    db: AsyncSession = Depends(get_async_session)
) -> List[Note]:
    '''Get list of all notes'''
    return await crud.get_notes(db, filter_query)


@router.post('/notes/add', status_code=201)
async def add_note(
    note: NoteRequest,
    db=Depends(get_async_session)
) -> Note:
    '''Create a note'''
    new_note = await crud.create_note_with_tags(
        db,
        note
    )
    return new_note


@router.get('/notes/{note_id}')
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_async_session)
) -> Note:
    '''Get note with id == note_id'''
    return await crud.get_note_by_id(db, note_id)


@router.put('/notes/{note_id}')
async def update_note(
    note_id: int,
    note: NoteRequest,
    db: AsyncSession = Depends(get_async_session)
) -> Note:
    '''Update note with id == note_id'''
    return await crud.update_note(db, note_id, note)


@router.delete('/notes/{note_id}')
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_async_session)
) -> Note:
    '''Deletes note with id==note+id'''
    note = await crud.delete_note_by_id(db, note_id)
    return note

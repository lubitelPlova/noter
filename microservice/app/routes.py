from fastapi import APIRouter


router = APIRouter()


@router.get('/health')
def health_check():
    '''The healthcheck endpoint'''
    pass


@router.get('/notes/')
def get_notes_list():
    '''Get list of all notes'''
    pass


@router.post('/notes/add')
def add_note():
    '''Create a note'''
    pass


@router.get('/notes/{note_id}')
def get_note(note_id: int):
    '''Get note with id == note_id'''
    pass


@router.put('/notes/{note_id}')
def update_note(note_id: int):
    '''Update note with id == note_id'''
    pass


@router.delete('/notes/{note_id}')
def delete_note(note_id: int):
    '''Deletes note with id==note+id'''
    pass

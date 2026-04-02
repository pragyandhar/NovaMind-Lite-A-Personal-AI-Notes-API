from app.schemas.note import NoteCreate, NoteResponse
from app.dependencies import get_db, get_current_user
from app.models.database import Note, User
# -------------------------------------
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status, HTTPException
# -------------------------------------


router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


# List all notes, with skip and limit query params
@router.get("/", response_model=list[NoteResponse])
def get_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), skip: int = 0, limit: int = 100):
    return db.query(Note).offset(skip).limit(limit).all()


# Get a single note by ID, return 404 if not found
@router.get("/{note_id}", response_model=NoteResponse)
def get_notes_by_id(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note Was Not Found"
        )
    return note


# Create a note, return 201
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_note = Note(title=note.title, content=note.content, tags=note.tags)
    db.add(new_note)
    db.commit()
    db.refresh(new_note) # This autogenerates random IDs
    return new_note


# Delete a note, return 404 if not found
@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note Was Not Found"
        )
    db.delete(note)
    db.commit()

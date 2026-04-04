from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# ----------------------------------------
from app.dependencies import get_current_user, get_db
from app.models.database import Note, User
from app.schemas.note import NoteResponse
from app.services.ai_service import summarize_note
# ----------------------------------------

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.get("/summarize/{note_id}")
async def aiml(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Note Found. Recheck the ID"
        )
    summary = await summarize_note(note.title, note.content)
    return {"summary": summary}

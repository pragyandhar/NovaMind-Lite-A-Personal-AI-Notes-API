from app.db.session import SessionLocal
from app.services.auth_service import decode_access_token
from app.models.database import User
from app.schemas.user import UserResponse
# -----------------------------------------
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
# -----------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:        # Handles connection leaks
        db.close()
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_access_token(token)
    db_saved_user = db.query(User).filter(User.id == int(user_id)).first()
    if not db_saved_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The User Is Not Availble In The Database"
        )
    return UserResponse.model_validate(db_saved_user)

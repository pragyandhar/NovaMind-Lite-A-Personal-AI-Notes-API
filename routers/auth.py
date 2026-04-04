from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# ------------------------------
from app.exceptions import UserAlreadyExistsException
from app.schemas.user import UserCreate, UserResponse, Token
from app.dependencies import get_db
from app.models.database import User
from app.services.auth_service import hash_password, create_access_token, verify_password
# ------------------------------

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

def send_welcome_message(email: str):
    print(f"Welcome to {email} NovaLite: Notes API")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    email_check = db.query(User).filter(user.email == User.email).first()
    if email_check:
        raise UserAlreadyExistsException(user.email)
    
    hpass = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hpass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    background_tasks.add_task(send_welcome_message, user.email)
    return UserResponse.model_validate(new_user)

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username
    password = form_data.password

    db_saved_email = db.query(User).filter(User.email==email).first()
    if not db_saved_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not created yet, register first"
        )
    
    if not verify_password(password, db_saved_email.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password not same"
        )
    
    token = create_access_token({"sub": db_saved_email.id})
    return Token(access_token=token, token_type="bearer")

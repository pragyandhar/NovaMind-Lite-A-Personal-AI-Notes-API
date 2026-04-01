from app.db.session import SessionLocal
# -----------------------------------------
from fastapi import Depends
# -----------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:        # Handles connection leaks
        db.close() 
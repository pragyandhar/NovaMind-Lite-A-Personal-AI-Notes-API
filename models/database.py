from app.db.session import Base
# ----------------------------------------------
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import JSON
# ----------------------------------------------
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    tags = Column(JSON)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

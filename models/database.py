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

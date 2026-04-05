from app.db.session import Base
from app.dependencies import get_current_user, get_db
from app.main import app
from app.models.database import User
# -----------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# -----------------------------------------------------

# Fake DB 
def override_get_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fake User
def override_get_current_user():
    return User(id=1, email="test@gmail.com", hashed_password="ultra_secret_do_not_look")

# Overriding the current normal working functions with fake ones
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
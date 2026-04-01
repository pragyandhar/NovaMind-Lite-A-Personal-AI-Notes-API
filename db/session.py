from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# ----------------------------------------------------------

# Create an engine
SQLALCHEMY_DB_URL = "sqlite:///./novamind.db"
engine = create_engine(
    SQLALCHEMY_DB_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

# Create a session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Declare a base
Base = declarative_base()
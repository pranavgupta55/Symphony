"""
Database models and initialization
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .database import Base, AnalysisJob
from ..core.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["AnalysisJob", "init_db", "get_db", "Session"]

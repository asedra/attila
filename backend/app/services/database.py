"""
Database service for SQLite connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os
from pathlib import Path
import logging

from ..models import *

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        # Create database directory
        db_dir = Path(__file__).parent.parent.parent / "data"
        db_dir.mkdir(exist_ok=True)
        
        # SQLite database path
        db_path = db_dir / "attila.db"
        
        # Create engine
        self.engine = create_engine(
            f"sqlite:///{db_path}",
            echo=False,  # Set to True for SQL query logging
            connect_args={"check_same_thread": False}
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        self.create_tables()
        
        logger.info(f"Database initialized at {db_path}")
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    @contextmanager
    def get_session(self) -> Session:
        """Get database session with context manager"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def get_session_sync(self) -> Session:
        """Get database session (non-context manager)"""
        return self.SessionLocal()

# Global database service instance
db_service = DatabaseService() 
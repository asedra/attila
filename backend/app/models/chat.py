"""
Chat models for database storage
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

class ChatSession(Base):
    """Chat Session Model"""
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    extra_data = Column(JSON)  # For storing additional session info
    
    # Relationship to messages
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    
    def to_dict(self):
        # Use preloaded message count if available, otherwise try to access messages
        if hasattr(self, '_message_count'):
            message_count = self._message_count
        else:
            try:
                message_count = len(self.messages) if self.messages else 0
            except:
                # If we can't access messages (detached session), set to 0
                message_count = 0
            
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
            "metadata": self.extra_data,
            "message_count": message_count
        }

class ChatMessage(Base):
    """Chat Message Model"""
    __tablename__ = "chat_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(50), nullable=False)  # 'user', 'assistant', 'system', 'error'
    timestamp = Column(DateTime, default=func.now())
    extra_data = Column(JSON)  # For storing functions, tokens, etc.
    
    # Relationship to session
    session = relationship("ChatSession", back_populates="messages")
    
    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "content": self.content,
            "type": self.message_type,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "metadata": self.extra_data
        } 
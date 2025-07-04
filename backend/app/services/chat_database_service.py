"""
Chat Database Service for managing chat sessions and messages
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
import logging
from datetime import datetime

from ..models.chat import ChatSession, ChatMessage
from .database import db_service

logger = logging.getLogger(__name__)

class ChatDatabaseService:
    def __init__(self):
        self.db = db_service
    
    # Session Management
    def create_session(self, title: str, description: str = None, metadata: Dict = None) -> ChatSession:
        """Create a new chat session"""
        with self.db.get_session() as session:
            chat_session = ChatSession(
                title=title,
                description=description,
                extra_data=metadata or {}
            )
            session.add(chat_session)
            session.flush()
            session.refresh(chat_session)
            # Get message count and attach it to avoid relationship access
            message_count = session.query(ChatMessage).filter(ChatMessage.session_id == chat_session.id).count()
            chat_session._message_count = message_count
            session.expunge(chat_session)
            return chat_session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        with self.db.get_session() as session:
            chat_session = session.query(ChatSession).filter(ChatSession.id == session_id).first()
            if chat_session:
                # Get message count and attach it to avoid relationship access
                message_count = session.query(ChatMessage).filter(ChatMessage.session_id == chat_session.id).count()
                chat_session._message_count = message_count
                session.expunge(chat_session)
            return chat_session
    
    def get_all_sessions(self, limit: int = 100, include_inactive: bool = False) -> List[ChatSession]:
        """Get all chat sessions"""
        with self.db.get_session() as session:
            query = session.query(ChatSession)
            
            if not include_inactive:
                query = query.filter(ChatSession.is_active == True)
            
            chat_sessions = query.order_by(desc(ChatSession.updated_at)).limit(limit).all()
            
            # Get message count for each session to avoid relationship access
            for chat_session in chat_sessions:
                message_count = session.query(ChatMessage).filter(ChatMessage.session_id == chat_session.id).count()
                chat_session._message_count = message_count
                session.expunge(chat_session)
            
            return chat_sessions
    
    def update_session(self, session_id: str, title: str = None, description: str = None, 
                      metadata: Dict = None) -> Optional[ChatSession]:
        """Update a chat session"""
        with self.db.get_session() as session:
            chat_session = session.query(ChatSession).filter(ChatSession.id == session_id).first()
            
            if not chat_session:
                return None
            
            if title is not None:
                chat_session.title = title
            if description is not None:
                chat_session.description = description
            if metadata is not None:
                chat_session.extra_data = metadata
            
            chat_session.updated_at = func.now()
            session.flush()
            session.refresh(chat_session)
            # Get message count and attach it to avoid relationship access
            message_count = session.query(ChatMessage).filter(ChatMessage.session_id == chat_session.id).count()
            chat_session._message_count = message_count
            session.expunge(chat_session)
            return chat_session
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session (soft delete)"""
        with self.db.get_session() as session:
            chat_session = session.query(ChatSession).filter(ChatSession.id == session_id).first()
            
            if not chat_session:
                return False
            
            chat_session.is_active = False
            chat_session.updated_at = func.now()
            return True
    
    def delete_session_permanently(self, session_id: str) -> bool:
        """Permanently delete a chat session and all its messages"""
        with self.db.get_session() as session:
            chat_session = session.query(ChatSession).filter(ChatSession.id == session_id).first()
            
            if not chat_session:
                return False
            
            session.delete(chat_session)
            return True
    
    # Message Management
    def add_message(self, session_id: str, content: str, message_type: str, 
                   metadata: Dict = None) -> Optional[ChatMessage]:
        """Add a message to a chat session"""
        with self.db.get_session() as session:
            # Check if session exists
            chat_session = session.query(ChatSession).filter(ChatSession.id == session_id).first()
            if not chat_session:
                logger.error(f"Chat session {session_id} not found")
                return None
            
            # Create message
            message = ChatMessage(
                session_id=session_id,
                content=content,
                message_type=message_type,
                extra_data=metadata or {}
            )
            
            session.add(message)
            
            # Update session timestamp
            chat_session.updated_at = func.now()
            
            session.flush()
            session.refresh(message)
            # Expunge to make it detached from session
            session.expunge(message)
            return message
    
    def get_session_messages(self, session_id: str, limit: int = 1000, 
                           offset: int = 0) -> List[ChatMessage]:
        """Get all messages for a chat session"""
        with self.db.get_session() as session:
            messages = (session.query(ChatMessage)
                       .filter(ChatMessage.session_id == session_id)
                       .order_by(ChatMessage.timestamp)
                       .offset(offset)
                       .limit(limit)
                       .all())
            
            # Expunge messages to make them detached from session
            for message in messages:
                session.expunge(message)
            
            return messages
    
    def get_recent_messages(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        """Get recent messages for a chat session"""
        with self.db.get_session() as session:
            messages = (session.query(ChatMessage)
                       .filter(ChatMessage.session_id == session_id)
                       .order_by(desc(ChatMessage.timestamp))
                       .limit(limit)
                       .all())
            
            # Expunge messages to make them detached from session
            for message in messages:
                session.expunge(message)
            
            return messages
    
    def delete_message(self, message_id: str) -> bool:
        """Delete a specific message"""
        with self.db.get_session() as session:
            message = session.query(ChatMessage).filter(ChatMessage.id == message_id).first()
            
            if not message:
                return False
            
            session.delete(message)
            return True
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a chat session"""
        with self.db.get_session() as session:
            chat_session = session.query(ChatSession).filter(ChatSession.id == session_id).first()
            
            if not chat_session:
                return {}
            
            message_count = session.query(ChatMessage).filter(ChatMessage.session_id == session_id).count()
            
            user_messages = (session.query(ChatMessage)
                           .filter(ChatMessage.session_id == session_id,
                                  ChatMessage.message_type == 'user')
                           .count())
            
            assistant_messages = (session.query(ChatMessage)
                                .filter(ChatMessage.session_id == session_id,
                                       ChatMessage.message_type == 'assistant')
                                .count())
            
            return {
                "session_id": session_id,
                "title": chat_session.title,
                "total_messages": message_count,
                "user_messages": user_messages,
                "assistant_messages": assistant_messages,
                "created_at": chat_session.created_at.isoformat() if chat_session.created_at else None,
                "updated_at": chat_session.updated_at.isoformat() if chat_session.updated_at else None
            }
    
    def search_messages(self, query: str, session_id: str = None, limit: int = 50) -> List[ChatMessage]:
        """Search messages by content"""
        with self.db.get_session() as session:
            query_obj = session.query(ChatMessage).filter(ChatMessage.content.contains(query))
            
            if session_id:
                query_obj = query_obj.filter(ChatMessage.session_id == session_id)
            
            messages = query_obj.order_by(desc(ChatMessage.timestamp)).limit(limit).all()
            
            # Expunge messages to make them detached from session
            for message in messages:
                session.expunge(message)
            
            return messages

# Global service instance
chat_db_service = ChatDatabaseService() 
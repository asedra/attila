"""
Chat API endpoints for session and message management
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

from ..services.chat_database_service import chat_db_service
from ..services.openai_service import openai_service
from ..models.chat import ChatSession, ChatMessage

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models for request/response
class ChatSessionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatSessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatMessageCreate(BaseModel):
    content: str
    message_type: str
    metadata: Optional[Dict[str, Any]] = None

class TitleGenerateRequest(BaseModel):
    message: str

class ChatSessionResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    created_at: str
    updated_at: str
    is_active: bool
    metadata: Optional[Dict[str, Any]]
    message_count: int

class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    content: str
    type: str
    timestamp: str
    metadata: Optional[Dict[str, Any]]

# Session endpoints
@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(session_data: ChatSessionCreate):
    """Create a new chat session"""
    try:
        session = chat_db_service.create_session(
            title=session_data.title,
            description=session_data.description,
            metadata=session_data.metadata
        )
        return ChatSessionResponse(**session.to_dict())
    except Exception as e:
        logger.error(f"Failed to create chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions(
    limit: int = Query(100, ge=1, le=1000),
    include_inactive: bool = Query(False)
):
    """Get all chat sessions"""
    try:
        sessions = chat_db_service.get_all_sessions(limit=limit, include_inactive=include_inactive)
        return [ChatSessionResponse(**session.to_dict()) for session in sessions]
    except Exception as e:
        logger.error(f"Failed to get chat sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(session_id: str):
    """Get a specific chat session"""
    try:
        session = chat_db_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return ChatSessionResponse(**session.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/sessions/{session_id}", response_model=ChatSessionResponse)
async def update_chat_session(session_id: str, session_data: ChatSessionUpdate):
    """Update a chat session"""
    try:
        session = chat_db_service.update_session(
            session_id=session_id,
            title=session_data.title,
            description=session_data.description,
            metadata=session_data.metadata
        )
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return ChatSessionResponse(**session.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{session_id}")
async def delete_chat_session(session_id: str, permanent: bool = Query(False)):
    """Delete a chat session (soft delete by default)"""
    try:
        if permanent:
            success = chat_db_service.delete_session_permanently(session_id)
        else:
            success = chat_db_service.delete_session(session_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        return {"message": "Chat session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Message endpoints
@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def add_message(session_id: str, message_data: ChatMessageCreate):
    """Add a message to a chat session"""
    try:
        message = chat_db_service.add_message(
            session_id=session_id,
            content=message_data.content,
            message_type=message_data.message_type,
            metadata=message_data.metadata
        )
        if not message:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return ChatMessageResponse(**message.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_session_messages(
    session_id: str,
    limit: int = Query(1000, ge=1, le=5000),
    offset: int = Query(0, ge=0)
):
    """Get all messages for a chat session"""
    try:
        messages = chat_db_service.get_session_messages(
            session_id=session_id,
            limit=limit,
            offset=offset
        )
        return [ChatMessageResponse(**message.to_dict()) for message in messages]
    except Exception as e:
        logger.error(f"Failed to get session messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/messages/recent", response_model=List[ChatMessageResponse])
async def get_recent_messages(
    session_id: str,
    limit: int = Query(10, ge=1, le=100)
):
    """Get recent messages for a chat session"""
    try:
        messages = chat_db_service.get_recent_messages(session_id=session_id, limit=limit)
        # Reverse to get chronological order
        messages.reverse()
        return [ChatMessageResponse(**message.to_dict()) for message in messages]
    except Exception as e:
        logger.error(f"Failed to get recent messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/messages/{message_id}")
async def delete_message(message_id: str):
    """Delete a specific message"""
    try:
        success = chat_db_service.delete_message(message_id)
        if not success:
            raise HTTPException(status_code=404, detail="Message not found")
        return {"message": "Message deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/stats")
async def get_session_stats(session_id: str):
    """Get statistics for a chat session"""
    try:
        stats = chat_db_service.get_session_stats(session_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get session stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=List[ChatMessageResponse])
async def search_messages(
    query: str = Query(..., min_length=1),
    session_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500)
):
    """Search messages by content"""
    try:
        messages = chat_db_service.search_messages(
            query=query,
            session_id=session_id,
            limit=limit
        )
        return [ChatMessageResponse(**message.to_dict()) for message in messages]
    except Exception as e:
        logger.error(f"Failed to search messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions/{session_id}/generate-title")
async def generate_session_title(session_id: str, request: TitleGenerateRequest):
    """Generate a title for a chat session based on the first message"""
    try:
        # Verify session exists
        session = chat_db_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Generate title using OpenAI
        result = await openai_service.generate_chat_title(request.message)
        
        if result["success"]:
            # Update session title
            updated_session = chat_db_service.update_session(
                session_id=session_id,
                title=result["title"]
            )
            
            if updated_session:
                return {
                    "success": True,
                    "title": result["title"],
                    "usage": result.get("usage")
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to update session title")
        else:
            # Return fallback title if AI generation fails
            fallback_title = result.get("title", f"Chat {request.message[:20]}...")
            updated_session = chat_db_service.update_session(
                session_id=session_id,
                title=fallback_title
            )
            
            return {
                "success": False,
                "title": fallback_title,
                "error": result.get("error")
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate session title: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 
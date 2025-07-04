"""
Simple Chat API for basic session management
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from pathlib import Path
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

# Simple file-based storage for testing
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
SESSIONS_FILE = DATA_DIR / "sessions.json"

# Pydantic models
class ChatSessionCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    created_at: str
    updated_at: str
    message_count: int

class ChatMessageCreate(BaseModel):
    content: str
    message_type: str

class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    content: str
    type: str
    timestamp: str

def load_sessions():
    """Load sessions from file"""
    if SESSIONS_FILE.exists():
        try:
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load sessions: {e}")
    return {"sessions": [], "messages": []}

def save_sessions(data):
    """Save sessions to file"""
    try:
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to save sessions: {e}")

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(session_data: ChatSessionCreate):
    """Create a new chat session"""
    try:
        data = load_sessions()
        
        session_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        new_session = {
            "id": session_id,
            "title": session_data.title,
            "description": session_data.description,
            "created_at": now,
            "updated_at": now,
            "message_count": 0
        }
        
        data["sessions"].append(new_session)
        save_sessions(data)
        
        return ChatSessionResponse(**new_session)
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions():
    """Get all chat sessions"""
    try:
        data = load_sessions()
        
        # Sort by updated_at descending
        sessions = sorted(data["sessions"], key=lambda x: x["updated_at"], reverse=True)
        
        return [ChatSessionResponse(**session) for session in sessions]
    except Exception as e:
        logger.error(f"Failed to get sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(session_id: str):
    """Get a specific chat session"""
    try:
        data = load_sessions()
        
        session = next((s for s in data["sessions"] if s["id"] == session_id), None)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return ChatSessionResponse(**session)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/sessions/{session_id}", response_model=ChatSessionResponse)
async def update_chat_session(session_id: str, session_update: ChatSessionCreate):
    """Update a chat session"""
    try:
        data = load_sessions()
        
        session = next((s for s in data["sessions"] if s["id"] == session_id), None)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session["title"] = session_update.title
        if session_update.description is not None:
            session["description"] = session_update.description
        session["updated_at"] = datetime.now().isoformat()
        
        save_sessions(data)
        
        return ChatSessionResponse(**session)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{session_id}")
async def delete_chat_session(session_id: str):
    """Delete a chat session"""
    try:
        data = load_sessions()
        
        original_count = len(data["sessions"])
        data["sessions"] = [s for s in data["sessions"] if s["id"] != session_id]
        data["messages"] = [m for m in data["messages"] if m["session_id"] != session_id]
        
        if len(data["sessions"]) == original_count:
            raise HTTPException(status_code=404, detail="Session not found")
        
        save_sessions(data)
        
        return {"message": "Session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def add_message(session_id: str, message_data: ChatMessageCreate):
    """Add a message to a session"""
    try:
        data = load_sessions()
        
        session = next((s for s in data["sessions"] if s["id"] == session_id), None)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        message_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        new_message = {
            "id": message_id,
            "session_id": session_id,
            "content": message_data.content,
            "type": message_data.message_type,
            "timestamp": now
        }
        
        data["messages"].append(new_message)
        
        # Update session
        session["message_count"] = len([m for m in data["messages"] if m["session_id"] == session_id])
        session["updated_at"] = now
        
        save_sessions(data)
        
        return ChatMessageResponse(**new_message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_session_messages(session_id: str):
    """Get all messages for a session"""
    try:
        data = load_sessions()
        
        messages = [m for m in data["messages"] if m["session_id"] == session_id]
        messages.sort(key=lambda x: x["timestamp"])
        
        return [ChatMessageResponse(**message) for message in messages]
    except Exception as e:
        logger.error(f"Failed to get messages: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 
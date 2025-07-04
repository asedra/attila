"""
Settings API endpoints for OpenAI configuration
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import logging

from ..services.openai_service import openai_service

logger = logging.getLogger(__name__)
router = APIRouter()

class OpenAISettings(BaseModel):
    openaiApiKey: str
    selectedModel: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    maxTokens: int = 2000
    systemPrompt: str = "You are Attila, a helpful AI assistant for project management, idea development, and task automation."

class TestConnectionRequest(BaseModel):
    apiKey: str
    model: str = "gpt-3.5-turbo"

@router.post("/openai")
async def save_openai_settings(settings: OpenAISettings):
    """Save OpenAI configuration settings"""
    try:
        success = openai_service.configure(settings.dict())
        
        if success:
            return {"success": True, "message": "Settings saved successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to configure OpenAI service")
            
    except Exception as e:
        logger.error(f"Failed to save OpenAI settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-openai")
async def test_openai_connection(request: TestConnectionRequest):
    """Test OpenAI API connection"""
    try:
        result = await openai_service.test_connection(request.apiKey, request.model)
        return result
        
    except Exception as e:
        logger.error(f"Failed to test OpenAI connection: {e}")
        return {
            "success": False,
            "error": f"Connection test failed: {str(e)}"
        }

@router.get("/openai/models")
async def get_available_models():
    """Get list of available OpenAI models"""
    try:
        models = openai_service.get_available_models()
        return {"models": models}
        
    except Exception as e:
        logger.error(f"Failed to get models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/openai/status")
async def get_openai_status():
    """Get current OpenAI configuration status"""
    try:
        return {
            "configured": openai_service.is_configured(),
            "model": openai_service.model,
            "temperature": openai_service.temperature,
            "max_tokens": openai_service.max_tokens
        }
        
    except Exception as e:
        logger.error(f"Failed to get OpenAI status: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 
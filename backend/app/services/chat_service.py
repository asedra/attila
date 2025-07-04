"""
Chat service for handling conversation logic
"""
import logging
from typing import Dict, Any, List
from datetime import datetime

from .openai_service import openai_service

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.conversation_history = []
        self.session_histories = {}  # Store conversation history per session
    
    async def process_message(self, message: str, functions: List[str] = None, session_id: str = None) -> Dict[str, Any]:
        """
        Process user message and generate response
        
        Args:
            message: User message content
            functions: List of active function names
            session_id: Optional session ID for conversation context
            
        Returns:
            Dict containing response message
        """
        try:
            # Get or create session history
            if session_id:
                if session_id not in self.session_histories:
                    self.session_histories[session_id] = []
                conversation_history = self.session_histories[session_id]
            else:
                conversation_history = self.conversation_history
            
            # Store user message in history
            user_msg = {
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat(),
                "functions": functions or []
            }
            conversation_history.append(user_msg)
            
            # Generate AI response
            if openai_service.is_configured():
                ai_response = await openai_service.generate_response(
                    message=message,
                    conversation_history=conversation_history,
                    functions=functions
                )
                
                if ai_response["success"]:
                    response_content = ai_response["content"]
                    
                    # Store AI response in history
                    ai_msg = {
                        "role": "assistant",
                        "content": response_content,
                        "timestamp": datetime.now().isoformat(),
                        "model": ai_response.get("model"),
                        "usage": ai_response.get("usage")
                    }
                    conversation_history.append(ai_msg)
                    
                    return {
                        "id": str(len(conversation_history)),
                        "type": "ai",
                        "content": response_content,
                        "timestamp": datetime.now().isoformat(),
                        "model": ai_response.get("model"),
                        "usage": ai_response.get("usage"),
                        "session_id": session_id
                    }
                else:
                    # OpenAI API error
                    error_response = f"❌ AI Error: {ai_response.get('error', 'Unknown error')}"
                    return {
                        "id": str(len(conversation_history)),
                        "type": "ai",
                        "content": error_response,
                        "timestamp": datetime.now().isoformat(),
                        "error": True,
                        "session_id": session_id
                    }
            else:
                # OpenAI not configured - provide helpful message
                fallback_response = self._generate_fallback_response(message, functions)
                return {
                    "id": str(len(conversation_history)),
                    "type": "ai", 
                    "content": fallback_response,
                    "timestamp": datetime.now().isoformat(),
                    "fallback": True,
                    "session_id": session_id
                }
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Use appropriate conversation history for error response
            conversation_history = self.session_histories.get(session_id, self.conversation_history) if session_id else self.conversation_history
            return {
                "id": str(len(conversation_history)),
                "type": "ai",
                "content": f"❌ System Error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": True,
                "session_id": session_id
            }
    
    def _generate_fallback_response(self, message: str, functions: List[str] = None) -> str:
        """Generate a helpful fallback response when OpenAI is not configured"""
        
        responses = [
            "🤖 **OpenAI API not configured**\n\nTo get real AI responses, please:\n1. Click the **Settings** button in the top-right\n2. Add your OpenAI API key\n3. Select your preferred model\n\nGet your API key from [OpenAI Dashboard](https://platform.openai.com/api-keys)",
            
            "⚙️ **Configure OpenAI to unlock AI power!**\n\nI'm ready to help you with:\n• Project management\n• Idea development\n• Jira ticket creation\n• Confluence documentation\n\nJust add your OpenAI API key in Settings to get started!",
            
            "🚀 **Setup Required**\n\nI can see you want to chat, but I need my AI brain first!\n\nQuick setup:\n1. Get API key from OpenAI\n2. Open Settings (gear icon)\n3. Paste your key and save\n\nThen we can have real conversations!"
        ]
        
        # Add function-specific responses
        if functions:
            if "Create Idea" in functions:
                return "💡 **Idea Creation Ready!**\n\nI see you want to create ideas. Once you configure OpenAI in Settings, I can help you:\n• Brainstorm creative solutions\n• Structure your thoughts\n• Generate detailed project concepts\n\nAdd your API key to unlock this feature!"
            
            elif "Create Jira Ticket" in functions:
                return "🎫 **Jira Integration Available!**\n\nTo create Jira tickets with AI assistance:\n1. Configure OpenAI API in Settings\n2. Set up your Jira credentials\n3. Let me help generate detailed tickets!\n\nI can create comprehensive descriptions, acceptance criteria, and more."
        
        # Rotate through general responses
        import random
        return random.choice(responses)
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

# Global service instance
chat_service = ChatService() 
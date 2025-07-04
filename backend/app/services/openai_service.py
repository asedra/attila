"""
OpenAI Service for chat completions and model management
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import openai
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = None
        self.api_key = None
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.7
        self.max_tokens = 2000
        self.system_prompt = "You are Attila, a helpful AI assistant for project management, idea development, and task automation. You can help with Jira tickets, Confluence documentation, and idea analysis."
        
        # Config file path
        self.config_path = Path(__file__).parent.parent.parent / "config" / "settings.json"
        self.config_path.parent.mkdir(exist_ok=True)
        
        # Try to load from saved config first, then environment
        self._load_from_config()
        if not self.api_key:
            self._load_from_env()
    
    def _load_from_config(self):
        """Load OpenAI configuration from saved config file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                self.api_key = config.get("openaiApiKey")
                self.model = config.get("selectedModel", self.model)
                self.temperature = config.get("temperature", self.temperature)
                self.max_tokens = config.get("maxTokens", self.max_tokens)
                self.system_prompt = config.get("systemPrompt", self.system_prompt)
                
                if self.api_key:
                    self.client = OpenAI(api_key=self.api_key)
                    logger.info("OpenAI client initialized from saved config")
                    
        except Exception as e:
            logger.warning(f"Failed to load config from file: {e}")
    
    def _load_from_env(self):
        """Load OpenAI configuration from environment variables"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            logger.info("OpenAI client initialized from environment")
    
    def _save_to_config(self, settings: Dict[str, Any]):
        """Save settings to config file"""
        try:
            # Create a copy of settings to save (excluding sensitive data in logs)
            config_to_save = {
                "selectedModel": settings.get("selectedModel", self.model),
                "temperature": settings.get("temperature", self.temperature),
                "maxTokens": settings.get("maxTokens", self.max_tokens),
                "systemPrompt": settings.get("systemPrompt", self.system_prompt)
            }
            
            # Only save API key if provided
            if "openaiApiKey" in settings and settings["openaiApiKey"]:
                config_to_save["openaiApiKey"] = settings["openaiApiKey"]
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
                
            logger.info("Settings saved to config file")
            
        except Exception as e:
            logger.error(f"Failed to save config to file: {e}")
    
    def configure(self, settings: Dict[str, Any]) -> bool:
        """
        Configure OpenAI with provided settings
        
        Args:
            settings: Dictionary containing API key, model, temperature, etc.
            
        Returns:
            bool: True if configuration was successful
        """
        try:
            if "openaiApiKey" in settings:
                self.api_key = settings["openaiApiKey"]
                self.client = OpenAI(api_key=self.api_key)
            
            if "selectedModel" in settings:
                self.model = settings["selectedModel"]
            
            if "temperature" in settings:
                self.temperature = float(settings["temperature"])
            
            if "maxTokens" in settings:
                self.max_tokens = int(settings["maxTokens"])
            
            if "systemPrompt" in settings:
                self.system_prompt = settings["systemPrompt"]
            
            # Save settings to config file
            self._save_to_config(settings)
            
            logger.info(f"OpenAI configured with model: {self.model}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to configure OpenAI: {e}")
            return False
    
    async def test_connection(self, api_key: str, model: str) -> Dict[str, Any]:
        """
        Test OpenAI API connection with provided credentials
        
        Args:
            api_key: OpenAI API key to test
            model: Model to test with
            
        Returns:
            Dict with success status and error message if any
        """
        try:
            test_client = OpenAI(api_key=api_key)
            
            # Try a simple completion to test the connection
            response = test_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            return {
                "success": True,
                "message": "Connection successful",
                "model_used": response.model,
                "usage": response.usage.dict() if response.usage else None
            }
            
        except openai.AuthenticationError:
            return {
                "success": False,
                "error": "Invalid API key"
            }
        except openai.NotFoundError:
            return {
                "success": False,
                "error": f"Model '{model}' not found or not accessible"
            }
        except openai.RateLimitError:
            return {
                "success": False,
                "error": "Rate limit exceeded"
            }
        except openai.APIConnectionError:
            return {
                "success": False,
                "error": "Failed to connect to OpenAI API"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    async def generate_response(
        self, 
        message: str, 
        conversation_history: List[Dict[str, str]] = None,
        functions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate AI response for given message
        
        Args:
            message: User message
            conversation_history: Previous messages in conversation
            functions: List of active functions
            
        Returns:
            Dict containing response and metadata
        """
        if not self.client:
            return {
                "success": False,
                "error": "OpenAI client not configured. Please add your API key in settings."
            }
        
        try:
            # Build conversation messages
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history
            if conversation_history:
                for msg in conversation_history[-10:]:  # Keep last 10 messages
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            # Add context about active functions
            if functions:
                function_context = f"\n\nActive functions: {', '.join(functions)}"
                if messages and messages[-1]["role"] == "user":
                    messages[-1]["content"] += function_context
                else:
                    messages.append({"role": "user", "content": message + function_context})
            else:
                messages.append({"role": "user", "content": message})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                } if response.usage else None,
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return {
                "success": False,
                "error": f"Failed to generate response: {str(e)}"
            }
    
    async def generate_chat_title(self, first_message: str) -> Dict[str, Any]:
        """
        Generate a concise chat title based on the first user message
        
        Args:
            first_message: The first user message in the conversation
            
        Returns:
            Dict containing the generated title and metadata
        """
        if not self.client:
            return {
                "success": False,
                "error": "OpenAI client not configured. Please add your API key in settings."
            }
        
        try:
            title_prompt = f"""Based on the following user message, generate a short, descriptive title for this chat conversation. The title should be:
- Maximum 5-6 words
- Descriptive but concise
- In Turkish language
- No quotes or special characters
- Capture the main topic or intent

User message: "{first_message}"

Please respond with only the title, nothing else."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use faster model for title generation
                messages=[
                    {"role": "user", "content": title_prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent titles
                max_tokens=20
            )
            
            title = response.choices[0].message.content.strip()
            
            # Clean up the title (remove quotes if any)
            title = title.strip('"').strip("'").strip()
            
            return {
                "success": True,
                "title": title,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                } if response.usage else None
            }
            
        except Exception as e:
            logger.error(f"Failed to generate chat title: {e}")
            return {
                "success": False,
                "error": f"Failed to generate title: {str(e)}",
                "title": f"Chat {first_message[:20]}..."  # Fallback title
            }
    
    def get_available_models(self) -> List[Dict[str, str]]:
        """Get list of available OpenAI models"""
        return [
            {
                "id": "gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "description": "Fast and efficient for most tasks"
            },
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "description": "More capable, better reasoning"
            },
            {
                "id": "gpt-4-turbo",
                "name": "GPT-4 Turbo",
                "description": "Latest GPT-4 with improved performance"
            },
            {
                "id": "gpt-4o",
                "name": "GPT-4o",
                "description": "Multimodal capabilities"
            },
            {
                "id": "gpt-4o-mini",
                "name": "GPT-4o Mini",
                "description": "Faster and more affordable"
            }
        ]
    
    def is_configured(self) -> bool:
        """Check if OpenAI service is properly configured"""
        return self.client is not None and self.api_key is not None

# Global service instance
openai_service = OpenAIService() 
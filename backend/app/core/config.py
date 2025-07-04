"""
Configuration settings for the application
"""
import os
from typing import Optional

class Settings:
    def __init__(self):
        # Jira settings
        self.jira_instance_url: Optional[str] = os.getenv("JIRA_INSTANCE_URL")
        self.jira_api_key: Optional[str] = os.getenv("JIRA_API_KEY")
        self.jira_user_email: Optional[str] = os.getenv("JIRA_USER_EMAIL")
        
        # Confluence settings
        self.confluence_url: Optional[str] = os.getenv("CONFLUENCE_URL")
        self.confluence_api_key: Optional[str] = os.getenv("CONFLUENCE_API_KEY")
        self.confluence_username: Optional[str] = os.getenv("CONFLUENCE_USERNAME")
        
        # OpenAI settings
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        
        # Database settings
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
        
        # Application settings
        self.app_name: str = "Attila AI Assistant"
        self.app_version: str = "1.0.0"
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"

# Global settings instance
settings = Settings() 
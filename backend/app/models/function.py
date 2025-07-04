"""
Function models for database storage
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from datetime import datetime
import uuid
from .chat import Base

class Function(Base):
    """Function Model"""
    __tablename__ = "functions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    icon = Column(String(50), default='gear')
    category = Column(String(100), nullable=False)
    parameters = Column(JSON, default=list)  # Array of parameter objects
    is_enabled = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)  # System functions cannot be deleted
    implementation = Column(Text)  # Function implementation code or reference
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    extra_data = Column(JSON)  # For storing additional function info
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "category": self.category,
            "parameters": self.parameters or [],
            "isEnabled": self.is_enabled,
            "isSystem": self.is_system,
            "implementation": self.implementation,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "metadata": self.extra_data
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Function from dictionary"""
        return cls(
            name=data.get('name'),
            description=data.get('description'),
            icon=data.get('icon', 'gear'),
            category=data.get('category'),
            parameters=data.get('parameters', []),
            is_enabled=data.get('isEnabled', True),
            implementation=data.get('implementation'),
            extra_data=data.get('metadata')
        ) 
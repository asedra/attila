"""
Function database service for managing functions
"""
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from .database import db_service
from ..models.function import Function

logger = logging.getLogger(__name__)

class FunctionDatabaseService:
    def __init__(self):
        self.db = db_service
        self._create_default_functions()
    
    def _create_default_functions(self):
        """Create default system functions if they don't exist"""
        default_functions = [
            {
                'name': 'Create Idea',
                'description': 'Convert thoughts into structured ideas',
                'icon': 'lightbulb',
                'category': 'idea',
                'parameters': [
                    {'name': 'title', 'type': 'string', 'description': 'Idea title', 'required': True},
                    {'name': 'description', 'type': 'string', 'description': 'Idea description', 'required': True}
                ],
                'isEnabled': True,
                'isSystem': True,
                'implementation': 'mcp:idea-create'
            },
            {
                'name': 'Create Jira Ticket',
                'description': 'Create a new Jira ticket from conversation',
                'icon': 'ticket',
                'category': 'task',
                'parameters': [
                    {'name': 'title', 'type': 'string', 'description': 'Ticket title', 'required': True},
                    {'name': 'description', 'type': 'string', 'description': 'Ticket description', 'required': True}
                ],
                'isEnabled': True,
                'isSystem': True,
                'implementation': 'mcp:jira-create'
            },
            {
                'name': 'Web Search',
                'description': 'Search the web for information',
                'icon': 'search',
                'category': 'analysis',
                'parameters': [
                    {'name': 'query', 'type': 'string', 'description': 'Search query', 'required': True}
                ],
                'isEnabled': True,
                'isSystem': True,
                'implementation': 'mcp:web-search'
            }
        ]
        
        try:
            with self.db.get_session() as session:
                # Check if any functions exist
                existing_count = session.query(Function).count()
                if existing_count == 0:
                    logger.info("Creating default functions...")
                    for func_data in default_functions:
                        function = Function.from_dict(func_data)
                        session.add(function)
                    logger.info(f"Created {len(default_functions)} default functions")
        except Exception as e:
            logger.error(f"Failed to create default functions: {e}")
    
    def get_all_functions(self, include_disabled: bool = False) -> List[dict]:
        """Get all functions"""
        try:
            with self.db.get_session() as session:
                query = session.query(Function)
                if not include_disabled:
                    query = query.filter(Function.is_enabled == True)
                functions = query.order_by(desc(Function.created_at)).all()
                # Convert to dictionaries to avoid session detachment issues
                return [func.to_dict() for func in functions]
        except Exception as e:
            logger.error(f"Failed to get functions: {e}")
            return []
    
    def get_function(self, function_id: str) -> Optional[dict]:
        """Get a specific function by ID"""
        try:
            with self.db.get_session() as session:
                function = session.query(Function).filter(Function.id == function_id).first()
                return function.to_dict() if function else None
        except Exception as e:
            logger.error(f"Failed to get function {function_id}: {e}")
            return None
    
    def create_function(self, name: str, description: str = None, icon: str = 'gear', 
                       category: str = 'custom', parameters: List[Dict] = None, 
                       implementation: str = None, metadata: Dict = None) -> Optional[dict]:
        """Create a new function"""
        try:
            with self.db.get_session() as session:
                function = Function(
                    name=name,
                    description=description,
                    icon=icon,
                    category=category,
                    parameters=parameters or [],
                    implementation=implementation,
                    extra_data=metadata
                )
                
                session.add(function)
                session.flush()  # To get the ID
                
                # Get the data before session closes
                function_dict = function.to_dict()
                
                logger.info(f"Created function: {function.name} (ID: {function.id})")
                return function_dict
                
        except Exception as e:
            logger.error(f"Failed to create function: {e}")
            return None
    
    def update_function(self, function_id: str, name: str = None, description: str = None,
                       icon: str = None, category: str = None, parameters: List[Dict] = None,
                       is_enabled: bool = None, implementation: str = None,
                       metadata: Dict = None) -> Optional[dict]:
        """Update an existing function"""
        try:
            with self.db.get_session() as session:
                function = session.query(Function).filter(Function.id == function_id).first()
                
                if not function:
                    return None
                
                # Update fields if provided
                if name is not None:
                    function.name = name
                if description is not None:
                    function.description = description
                if icon is not None:
                    function.icon = icon
                if category is not None:
                    function.category = category
                if parameters is not None:
                    function.parameters = parameters
                if is_enabled is not None:
                    function.is_enabled = is_enabled
                if implementation is not None:
                    function.implementation = implementation
                if metadata is not None:
                    function.extra_data = metadata
                
                session.flush()
                
                # Get the data before session closes
                function_dict = function.to_dict()
                
                logger.info(f"Updated function: {function.name} (ID: {function.id})")
                return function_dict
                
        except Exception as e:
            logger.error(f"Failed to update function {function_id}: {e}")
            return None
    
    def delete_function(self, function_id: str) -> bool:
        """Delete a function (only if not system function)"""
        try:
            with self.db.get_session() as session:
                function = session.query(Function).filter(Function.id == function_id).first()
                
                if not function:
                    return False
                
                if function.is_system:
                    logger.warning(f"Cannot delete system function: {function.name}")
                    return False
                
                session.delete(function)
                logger.info(f"Deleted function: {function.name} (ID: {function.id})")
                return True
                
        except Exception as e:
            logger.error(f"Failed to delete function {function_id}: {e}")
            return False
    
    def get_functions_by_category(self, category: str) -> List[dict]:
        """Get functions by category"""
        try:
            with self.db.get_session() as session:
                functions = session.query(Function)\
                    .filter(Function.category == category, Function.is_enabled == True)\
                    .order_by(desc(Function.created_at)).all()
                return [func.to_dict() for func in functions]
        except Exception as e:
            logger.error(f"Failed to get functions by category {category}: {e}")
            return []
    
    def get_categories(self) -> List[str]:
        """Get all function categories"""
        try:
            with self.db.get_session() as session:
                categories = session.query(Function.category)\
                    .filter(Function.is_enabled == True)\
                    .distinct().all()
                return [cat[0] for cat in categories]
        except Exception as e:
            logger.error(f"Failed to get categories: {e}")
            return []

# Global service instance
function_db_service = FunctionDatabaseService() 
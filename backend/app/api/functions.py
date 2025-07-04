"""
Functions API endpoints for managing available functions
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from ..services.mcp_service import mcp_service
from ..services.function_database_service import function_db_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class FunctionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    icon: str = 'gear'
    category: str = 'custom'
    parameters: List[Dict[str, Any]] = []
    implementation: Optional[str] = None

class FunctionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    category: Optional[str] = None
    parameters: Optional[List[Dict[str, Any]]] = None
    is_enabled: Optional[bool] = None
    implementation: Optional[str] = None

class FunctionResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    icon: str
    category: str
    parameters: List[Dict[str, Any]]
    isEnabled: bool
    isSystem: bool
    implementation: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

@router.get("/", response_model=List[FunctionResponse])
async def get_available_functions(include_disabled: bool = False):
    """Get list of available functions from database"""
    try:
        functions = function_db_service.get_all_functions(include_disabled=include_disabled)
        return [FunctionResponse(**func) for func in functions]
        
    except Exception as e:
        logger.error(f"Failed to get functions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=FunctionResponse)
async def create_function(function_data: FunctionCreate):
    """Create a new function"""
    try:
        function = function_db_service.create_function(
            name=function_data.name,
            description=function_data.description,
            icon=function_data.icon,
            category=function_data.category,
            parameters=function_data.parameters,
            implementation=function_data.implementation
        )
        
        if not function:
            raise HTTPException(status_code=400, detail="Failed to create function")
        
        return FunctionResponse(**function)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create function: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_function_categories():
    """Get all function categories"""
    try:
        categories = function_db_service.get_categories()
        return {"categories": categories}
        
    except Exception as e:
        logger.error(f"Failed to get categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{function_id}", response_model=FunctionResponse)
async def get_function(function_id: str):
    """Get a specific function"""
    try:
        function = function_db_service.get_function(function_id)
        
        if not function:
            raise HTTPException(status_code=404, detail="Function not found")
            
        return FunctionResponse(**function)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get function: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{function_id}", response_model=FunctionResponse)
async def update_function(function_id: str, function_data: FunctionUpdate):
    """Update an existing function"""
    try:
        function = function_db_service.update_function(
            function_id=function_id,
            name=function_data.name,
            description=function_data.description,
            icon=function_data.icon,
            category=function_data.category,
            parameters=function_data.parameters,
            is_enabled=function_data.is_enabled,
            implementation=function_data.implementation
        )
        
        if not function:
            raise HTTPException(status_code=404, detail="Function not found")
        
        return FunctionResponse(**function)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update function: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{function_id}")
async def delete_function(function_id: str):
    """Delete a function"""
    try:
        success = function_db_service.delete_function(function_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Function not found or cannot be deleted")
        
        return {"message": "Function deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete function: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{function_id}/toggle")
async def toggle_function(function_id: str):
    """Toggle function active status"""
    try:
        # Get current status
        current = mcp_service.get_function_status(function_id)
        if "error" in current:
            raise HTTPException(status_code=404, detail=current["error"])
        
        # Toggle active status
        new_active = not current.get("active", False)
        result = mcp_service.update_function_status(function_id, active=new_active)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to toggle function: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{function_id}/execute")
async def execute_function(function_id: str, params: Dict[str, Any]):
    """Execute a specific function with parameters"""
    try:
        result = await mcp_service.execute_function(function_id, params)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to execute function: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 
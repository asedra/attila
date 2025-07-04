from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from pydantic import BaseModel

from ...services.mcp_service import MCPService

router = APIRouter()

# Initialize MCP service
mcp_service = MCPService()


class FunctionExecuteRequest(BaseModel):
    params: Dict[str, Any]


class FunctionStatusUpdate(BaseModel):
    enabled: bool = None
    active: bool = None


@router.get("/functions", response_model=List[Dict[str, Any]])
async def get_functions():
    """Get all available functions"""
    return await mcp_service.get_available_functions()


@router.get("/functions/{function_id}")
async def get_function(function_id: str):
    """Get details of a specific function"""
    status = mcp_service.get_function_status(function_id)
    if "error" in status:
        raise HTTPException(status_code=404, detail=status["error"])
    return status


@router.post("/functions/{function_id}/execute")
async def execute_function(function_id: str, request: FunctionExecuteRequest):
    """Execute a specific function"""
    result = await mcp_service.execute_function(function_id, request.params)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.put("/functions/{function_id}/status")
async def update_function_status(function_id: str, update: FunctionStatusUpdate):
    """Update function status"""
    result = mcp_service.update_function_status(
        function_id, 
        enabled=update.enabled, 
        active=update.active
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/functions/categories")
async def get_function_categories():
    """Get available function categories"""
    functions = await mcp_service.get_available_functions()
    categories = list(set(func["category"] for func in functions))
    return {"categories": categories}


@router.get("/functions/category/{category}")
async def get_functions_by_category(category: str):
    """Get functions by category"""
    functions = await mcp_service.get_available_functions()
    filtered = [func for func in functions if func["category"] == category]
    return {"category": category, "functions": filtered} 
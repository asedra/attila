from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import asyncio
import uuid
from datetime import datetime
from typing import Dict, List
import uvicorn

# Import with try-catch to handle missing files gracefully
try:
    from app.core.config import settings
except ImportError:
    # Fallback settings if config file doesn't exist
    class FallbackSettings:
        app_name = "Attila AI Assistant"
        debug = True
    settings = FallbackSettings()

try:
    from app.services.chat_service import ChatService
    from app.services.mcp_service import MCPService
    from app.api.v1 import functions
    from app.api import chat
    services_available = True
except ImportError as e:
    print(f"Warning: Some services not available: {e}")
    services_available = False

app = FastAPI(title="Attila AI Assistant", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes if services are available
if services_available:
    try:
        app.include_router(functions.router, prefix="/api/v1", tags=["functions"])
        app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
        # Initialize services
        chat_service = ChatService()
        mcp_service = MCPService()
    except Exception as e:
        print(f"Warning: Could not initialize services: {e}")
        services_available = False

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"Client {client_id} connected")
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            print(f"Client {client_id} disconnected")
    
    async def send_message(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_text(json.dumps(message))
    
    async def broadcast(self, message: dict):
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except:
                # Remove disconnected clients
                self.disconnect(client_id)

manager = ConnectionManager()

@app.websocket("/api/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    client_id = str(uuid.uuid4())
    
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process the message
            response = await process_chat_message(message_data)
            
            # Send response back to client
            await manager.send_message(client_id, response)
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")
        manager.disconnect(client_id)

async def process_chat_message(message_data: dict) -> dict:
    """Process incoming chat message and return response"""
    try:
        user_message = message_data.get('message', '')
        functions = message_data.get('functions', [])
        
        # If services are available, use them
        if services_available and 'chat_service' in globals():
            response = await chat_service.process_message(
                message=user_message,
                active_functions=functions
            )
            
            return {
                'id': response.get('id'),
                'type': 'assistant',
                'content': response.get('content'),
                'timestamp': datetime.now().isoformat(),
                'functionResult': response.get('function_result')
            }
        else:
            # Fallback simple response
            return {
                'id': str(uuid.uuid4()),
                'type': 'assistant',
                'content': f'Hello! I received your message: "{user_message}". The full backend services are still loading. Please try again in a moment.',
                'timestamp': datetime.now().isoformat()
            }
        
    except Exception as e:
        return {
            'id': str(uuid.uuid4()),
            'type': 'error',
            'content': f'Error processing message: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

@app.get("/api/functions")
async def get_functions():
    """Get available functions"""
    if services_available and 'mcp_service' in globals():
        return await mcp_service.get_available_functions()
    else:
        return [
            {
                "id": "demo-function",
                "name": "Demo Function",
                "description": "A demo function while services are loading",
                "icon": "gear",
                "category": "demo",
                "parameters": [],
                "isEnabled": False,
                "isActive": False
            }
        ]

@app.post("/api/functions/{function_id}/execute")
async def execute_function(function_id: str, params: dict):
    """Execute a specific function"""
    if services_available and 'mcp_service' in globals():
        return await mcp_service.execute_function(function_id, params)
    else:
        return {"error": "Services not yet available"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "chat": "running" if services_available else "loading",
            "mcp": "running" if services_available else "loading"
        }
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Attila AI Assistant API", "status": "running"}

if __name__ == "__main__":
    print("🚀 Starting Attila AI Assistant Backend...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔗 WebSocket Chat: ws://localhost:8000/api/ws/chat")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 
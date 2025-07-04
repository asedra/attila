"""
FastAPI main application
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import logging

from .services.chat_service import chat_service
from .services.mcp_service import mcp_service
from .api import functions, settings, chat
from .api import simple_chat

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Attila AI Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(functions.router, prefix="/api/functions", tags=["functions"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(simple_chat.router, prefix="/api/simple-chat", tags=["simple-chat"])

@app.get("/")
async def root():
    return {"message": "Attila AI Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message = message_data.get("message", "")
            functions = message_data.get("functions", [])
            session_id = message_data.get("session_id")
            
            logger.info(f"Received message: {message}")
            logger.info(f"Active functions: {functions}")
            logger.info(f"Session ID: {session_id}")
            
            # Process message with session context
            response = await chat_service.process_message(message, functions, session_id)
            
            # Send response back to client
            await websocket.send_text(json.dumps(response))
            
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close() 
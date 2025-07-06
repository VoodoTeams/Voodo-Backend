import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn
from dotenv import load_dotenv

from app.api import api_router
from app.sockets import init_socketio, sio

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="Voodo Backend",
    description="Backend for Voodo Video Chat Application",
    version="0.1.0"
)

# Setup CORS
origins = [
    "http://localhost:5173",  # Vite default dev server
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost",
    "*",  # For development - restrict in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Create a Socket.IO ASGI app and wrap it with FastAPI
socket_app = socketio.ASGIApp(sio)
app.mount("/socket.io", socket_app)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Voodo Backend API"}

# Startup event
@app.on_event("startup")
async def startup_event():
    # Initialize Socket.IO events
    await init_socketio()
    print("Socket.IO events initialized")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 5000)),
        reload=True if os.getenv("DEBUG", "False").lower() == "true" else False,
        log_level="info"
    )

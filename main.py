import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn
from dotenv import load_dotenv
from pymongo import MongoClient
import uuid
from typing import Dict, List, Set, Tuple, Optional

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Voodo Backend", description="Backend for Voodo Video Chat Application")

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

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["voodo_db"]

# Socket.IO setup with async mode for compatibility with FastAPI
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=origins,
    logger=True,
    engineio_logger=True
)

# Create a Socket.IO ASGI app and wrap it with FastAPI
socket_app = socketio.ASGIApp(sio)
app.mount("/socket.io", socket_app)

# In-memory user management
# These will be moved to MongoDB in a production environment
video_chat_users = {}  # socket_id: user_data
waiting_for_video_match = set()  # socket_ids of users waiting for a video match
text_chat_pairs = {}  # socket_id: partner_socket_id
waiting_for_text_match = set()  # socket_ids of users waiting for a text match

# User count for statistics
online_users_count = 0

@app.get("/")
async def root():
    return {"message": "Welcome to Voodo Backend API"}

@sio.event
async def connect(sid, environ, auth):
    """Handle new socket connections"""
    global online_users_count
    print(f"Client connected: {sid}")
    online_users_count += 1
    
    # Broadcast updated user count
    await sio.emit('updateUserCount', online_users_count)

@sio.event
async def disconnect(sid):
    """Handle socket disconnections"""
    global online_users_count, waiting_for_video_match, waiting_for_text_match
    print(f"Client disconnected: {sid}")
    
    # Remove from waiting lists if present
    if sid in waiting_for_video_match:
        waiting_for_video_match.remove(sid)
    
    if sid in waiting_for_text_match:
        waiting_for_text_match.remove(sid)
    
    # Handle video chat disconnection
    if sid in video_chat_users:
        del video_chat_users[sid]
    
    # Handle text chat disconnection
    if sid in text_chat_pairs:
        partner_sid = text_chat_pairs[sid]
        if partner_sid in text_chat_pairs:
            del text_chat_pairs[partner_sid]
            await sio.emit('chatDisconnected', room=partner_sid)
        del text_chat_pairs[sid]
    
    # Update user count
    online_users_count = max(0, online_users_count - 1)
    await sio.emit('updateUserCount', online_users_count)

@sio.event
async def findPartner(sid):
    """Match users for video chat"""
    global waiting_for_video_match
    
    # Add user to waiting list
    waiting_for_video_match.add(sid)
    
    # Check if there's another user waiting
    if len(waiting_for_video_match) > 1:
        # Find a partner who isn't the current user
        partner = next((user for user in waiting_for_video_match if user != sid), None)
        
        if partner:
            # Remove both users from waiting list
            waiting_for_video_match.remove(sid)
            waiting_for_video_match.remove(partner)
            
            # Create the connection between the two users
            await sio.emit('callUser', {
                'from': partner,
                'signal': None,  # Signal will be sent through WebRTC
                'name': 'Anonymous'
            }, room=sid)

@sio.event
async def callUser(sid, data):
    """Handle call initiation"""
    userToCall = data.get('userToCall')
    signalData = data.get('signalData')
    from_user = data.get('from')
    
    await sio.emit('callUser', {
        'signal': signalData,
        'from': from_user,
        'name': data.get('name', 'Anonymous')
    }, room=userToCall)

@sio.event
async def answerCall(sid, data):
    """Handle call being answered"""
    to_user = data.get('to')
    signal = data.get('signal')
    
    await sio.emit('callAccepted', signal, room=to_user)

@sio.event
async def endCall(sid):
    """Handle call ending"""
    # Implementation depends on how you want to handle call endings
    pass

@sio.event
async def findTextChat(sid):
    """Match users for text chat"""
    global waiting_for_text_match, text_chat_pairs
    
    # If user was already in a chat, disconnect them from previous partner
    if sid in text_chat_pairs:
        old_partner = text_chat_pairs[sid]
        if old_partner in text_chat_pairs:
            del text_chat_pairs[old_partner]
            await sio.emit('chatDisconnected', room=old_partner)
        del text_chat_pairs[sid]
    
    # Add user to waiting list
    waiting_for_text_match.add(sid)
    
    # Check if there's another user waiting
    if len(waiting_for_text_match) > 1:
        # Find a partner who isn't the current user
        partner = next((user for user in waiting_for_text_match if user != sid), None)
        
        if partner:
            # Remove both users from waiting list
            waiting_for_text_match.remove(sid)
            waiting_for_text_match.remove(partner)
            
            # Create the chat pairing
            text_chat_pairs[sid] = partner
            text_chat_pairs[partner] = sid
            
            # Notify both users
            await sio.emit('chatConnected', room=sid)
            await sio.emit('chatConnected', room=partner)

@sio.event
async def sendMessage(sid, message):
    """Send a message to chat partner"""
    if sid in text_chat_pairs:
        partner_sid = text_chat_pairs[sid]
        await sio.emit('receiveMessage', message, room=partner_sid)

@sio.event
async def typing(sid):
    """Send typing indicator to chat partner"""
    if sid in text_chat_pairs:
        partner_sid = text_chat_pairs[sid]
        await sio.emit('typing', room=partner_sid)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        reload=True,
        log_level="info"
    )

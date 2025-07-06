from typing import Dict, List, Set, Tuple, Optional
import socketio

# Create Socket.IO instance
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=["*"],  # Configure based on environment
    logger=True,
    engineio_logger=True
)

# In-memory storage for video chat
video_chat_users = {}  # socket_id: user_data
waiting_for_video_match = set()  # socket_ids of users waiting for a match
online_users_count = 0

async def setup_video_events():
    """Register all video chat related socket events"""
    
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
        global online_users_count, waiting_for_video_match
        print(f"Client disconnected: {sid}")
        
        # Remove from waiting list if present
        if sid in waiting_for_video_match:
            waiting_for_video_match.remove(sid)
        
        # Clean up user data
        if sid in video_chat_users:
            del video_chat_users[sid]
        
        # Update user count
        online_users_count = max(0, online_users_count - 1)
        await sio.emit('updateUserCount', online_users_count)

    @sio.event
    async def findPartner(sid):
        """Match users for video chat"""
        global waiting_for_video_match
        
        print(f"User {sid} is looking for a video partner")
        
        # Add user to waiting list
        waiting_for_video_match.add(sid)
        
        # Check if there's another user waiting
        if len(waiting_for_video_match) > 1:
            # Find a partner who isn't the current user
            partner = next((user for user in waiting_for_video_match if user != sid), None)
            
            if partner:
                print(f"Matching {sid} with {partner} for video chat")
                
                # Remove both users from waiting list
                waiting_for_video_match.remove(sid)
                waiting_for_video_match.remove(partner)
                
                # Create the connection between the two users
                # In WebRTC, one user needs to initiate the call
                await sio.emit('callUser', {
                    'from': partner,
                    'signal': None,  # Signal data will be sent in subsequent events
                    'name': 'Anonymous'
                }, room=sid)

    @sio.event
    async def callUser(sid, data):
        """Handle WebRTC call initiation"""
        userToCall = data.get('userToCall')
        signalData = data.get('signalData')
        from_user = data.get('from')
        name = data.get('name', 'Anonymous')
        
        print(f"User {from_user} is calling {userToCall}")
        
        # Forward the call data to the recipient
        await sio.emit('callUser', {
            'signal': signalData,
            'from': from_user,
            'name': name
        }, room=userToCall)

    @sio.event
    async def answerCall(sid, data):
        """Handle call being answered with WebRTC signal data"""
        to_user = data.get('to')
        signal = data.get('signal')
        
        print(f"User {sid} answered call from {to_user}")
        
        # Forward the answer to the caller
        await sio.emit('callAccepted', signal, room=to_user)

    @sio.event
    async def endCall(sid):
        """Handle call ending"""
        print(f"User {sid} ended call")
        
        # You might want to notify the partner that the call has ended
        # but this depends on your application flow
        # For now, the frontend handles this by destroying the peer connection
        
        # Implementation depends on how you want to handle call endings
        pass

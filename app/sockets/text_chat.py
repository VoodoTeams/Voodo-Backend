from typing import Dict, Set
from app.sockets.video_chat import sio

# In-memory storage for text chat
text_chat_pairs = {}  # socket_id: partner_socket_id
waiting_for_text_match = set()  # socket_ids of users waiting for a match

async def setup_text_chat_events():
    """Register all text chat related socket events"""
    
    @sio.event
    async def findTextChat(sid):
        """Match users for text chat"""
        global waiting_for_text_match, text_chat_pairs
        
        print(f"User {sid} is looking for a text chat partner")
        
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
                print(f"Matching {sid} with {partner} for text chat")
                
                # Remove both users from waiting list
                waiting_for_text_match.remove(sid)
                waiting_for_text_match.remove(partner)
                
                # Create the chat pairing
                text_chat_pairs[sid] = partner
                text_chat_pairs[partner] = sid
                
                # Notify both users that they're connected
                await sio.emit('chatConnected', room=sid)
                await sio.emit('chatConnected', room=partner)

    @sio.event
    async def sendMessage(sid, message):
        """Send a message to chat partner"""
        if sid in text_chat_pairs:
            partner_sid = text_chat_pairs[sid]
            print(f"Message from {sid} to {partner_sid}: {message[:20]}...")
            await sio.emit('receiveMessage', message, room=partner_sid)

    @sio.event
    async def typing(sid):
        """Send typing indicator to chat partner"""
        if sid in text_chat_pairs:
            partner_sid = text_chat_pairs[sid]
            await sio.emit('typing', room=partner_sid)
            
    # Handle disconnection (this complements the disconnect event in video_chat.py)
    # We need to extend the existing disconnect handler to handle text chat disconnections
    @sio.on("disconnect")
    async def handle_text_chat_disconnect(sid):
        """Handle text chat specific disconnect logic"""
        global text_chat_pairs, waiting_for_text_match
        
        # Remove from text chat waiting list if present
        if sid in waiting_for_text_match:
            waiting_for_text_match.remove(sid)
        
        # Handle text chat disconnection
        if sid in text_chat_pairs:
            partner_sid = text_chat_pairs[sid]
            if partner_sid in text_chat_pairs:
                del text_chat_pairs[partner_sid]
                await sio.emit('chatDisconnected', room=partner_sid)
            del text_chat_pairs[sid]

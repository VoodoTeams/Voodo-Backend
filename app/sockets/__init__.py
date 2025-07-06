# Socket.IO initialization
from app.sockets.video_chat import sio, setup_video_events
from app.sockets.text_chat import setup_text_chat_events

async def init_socketio():
    """Initialize all Socket.IO event handlers"""
    await setup_video_events()
    await setup_text_chat_events()
    
    return sio

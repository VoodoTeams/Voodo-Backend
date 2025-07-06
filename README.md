# Voodo Backend Server

This is the backend server for the Voodo video/text chat application. It provides the following features:

- Real-time video chat using WebRTC and Socket.IO
- Real-time text chat with typing indicators
- Hangouts (posts) feature
- WebRTC TURN/STUN server integration

## Technology Stack

- Python 3.9+
- FastAPI - Web framework
- Socket.IO - Real-time communication
- MongoDB - Database
- aiortc - WebRTC capabilities

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

3. Update the `.env` file with your configuration settings, particularly:
   - MongoDB connection details
   - TURN server credentials

## Running the Server

```bash
python run.py
```

The server will start on port 5000 by default (configurable in `.env`).

## API Documentation

FastAPI automatically generates API documentation. Access it at:

- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

## Socket.IO Events

### Video Chat Events

- `connect` - Client connects to server
- `disconnect` - Client disconnects
- `findPartner` - Client requests a video chat partner
- `callUser` - Initiate a WebRTC call to another user
- `answerCall` - Answer an incoming WebRTC call
- `endCall` - End a WebRTC call

### Text Chat Events

- `findTextChat` - Client requests a text chat partner
- `sendMessage` - Send a text message to chat partner
- `typing` - Send typing indicator to chat partner
- `chatConnected` - Notification that a chat connection has been established
- `chatDisconnected` - Notification that a chat partner has disconnected

## Development and Production

For development, set `DEBUG=True` in `.env` to enable hot-reloading.

For production, set `DEBUG=False` and consider using a production ASGI server like Gunicorn with Uvicorn workers.

# Voodo Desktop Backend

This is the backend server for Voodo Desktop, an Omegle-inspired video and text chat application.

## Features

- Real-time video chat using WebRTC
- Text chat with typing indicators
- Hangouts posts system
- Socket.IO for real-time communication
- Self-hosted CoTURN server for NAT traversal

## Technologies

- Node.js
- Express.js
- Socket.IO
- WebRTC
- MongoDB
- CoTURN server

## Setup

### Prerequisites

- Node.js 16.x or higher
- MongoDB (or use the Docker setup)
- CoTURN server (or use the Docker setup)

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file based on the `.env.example` file
4. Start the server:
   ```
   npm run dev
   ```

### Docker Setup

1. Make sure you have Docker and Docker Compose installed
2. Run:
   ```
   docker-compose up -d
   ```

## API Endpoints

### Hangouts

- `GET /api/hangouts` - Get all hangouts
- `GET /api/hangouts/:id` - Get a single hangout
- `POST /api/hangouts` - Create a new hangout
- `PUT /api/hangouts/like/:id` - Like a hangout
- `DELETE /api/hangouts/:id` - Delete a hangout

### Users

- `GET /api/users/turnCredentials` - Get TURN server credentials
- `GET /api/users/stats` - Get user stats (online count, etc.)

## Socket.IO Events

### Video Chat

- `findPartner` - Find a new video chat partner
- `callUser` - Initiate a call to another user
- `answerCall` - Accept an incoming call
- `endCall` - End the current call
- `callEnded` - Notification that a call has ended
- `partnerFound` - Notification that a partner has been found
- `updateUserCount` - Update the count of online users

### Text Chat

- `findTextChat` - Find a new text chat partner
- `sendMessage` - Send a message to your chat partner
- `receiveMessage` - Receive a message from your chat partner
- `typing` - Notify that you are typing
- `chatConnected` - Notification that a text chat has been established
- `chatDisconnected` - Notification that your chat partner has disconnected

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is proprietary and confidential. Unauthorized copying, transferring or reproduction of the contents of this repository, via any medium is strictly prohibited.

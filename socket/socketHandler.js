// Main socket handler that combines all socket functionality
import { v4 as uuidv4 } from 'uuid';

// Keep track of users waiting for partners
let videoWaitingUsers = [];
let textWaitingUsers = [];

// Track active connections
let userConnections = new Map();
let textChatPairs = new Map();

/**
 * Set up all socket handlers
 * @param {SocketIO.Server} io - Socket.IO server instance
 */
const setupSocketHandlers = (io) => {
  io.on('connection', (socket) => {
    console.log(`User connected: ${socket.id}`);
    
    // Update online user count for all connected clients
    updateUserCount(io);
    
    // WebRTC Video Chat Handlers
    handleWebRTCEvents(socket, io);
    
    // Text Chat Handlers
    handleTextChatEvents(socket, io);
    
    // Handle disconnection
    socket.on('disconnect', () => {
      console.log(`User disconnected: ${socket.id}`);
      
      // Remove from waiting queues
      videoWaitingUsers = videoWaitingUsers.filter(id => id !== socket.id);
      textWaitingUsers = textWaitingUsers.filter(id => id !== socket.id);
      
      // Handle disconnection from any active call
      const partnerId = userConnections.get(socket.id);
      if (partnerId) {
        const partnerSocket = io.sockets.sockets.get(partnerId);
        if (partnerSocket) {
          partnerSocket.emit('callEnded');
        }
        userConnections.delete(partnerId);
        userConnections.delete(socket.id);
      }
      
      // Handle disconnection from text chat
      const textPartnerId = findTextChatPartner(socket.id);
      if (textPartnerId) {
        const partnerSocket = io.sockets.sockets.get(textPartnerId);
        if (partnerSocket) {
          partnerSocket.emit('chatDisconnected');
        }
        removeTextChatPair(socket.id, textPartnerId);
      }
      
      // Update online user count
      updateUserCount(io);
    });
  });
};

/**
 * Handle WebRTC related socket events
 * @param {Socket} socket - Socket instance for the user
 * @param {SocketIO.Server} io - Socket.IO server instance
 */
const handleWebRTCEvents = (socket, io) => {
  // Find a new video chat partner
  socket.on('findPartner', () => {
    console.log(`${socket.id} is looking for a video partner`);
    
    // Check if there are any users waiting
    if (videoWaitingUsers.length > 0) {
      // Get the first waiting user
      const partnerId = videoWaitingUsers.shift();
      const partnerSocket = io.sockets.sockets.get(partnerId);
      
      // Make sure the partner is still connected
      if (partnerSocket) {
        console.log(`Matching ${socket.id} with ${partnerId} for video chat`);
        
        // Create a connection between the two users
        userConnections.set(socket.id, partnerId);
        userConnections.set(partnerId, socket.id);
        
        // Tell the partner to call this user
        partnerSocket.emit('partnerFound', { partnerId: socket.id });
      } else {
        // If partner is no longer connected, add this user to the waiting list
        videoWaitingUsers.push(socket.id);
      }
    } else {
      // No partners available, add to waiting list
      videoWaitingUsers.push(socket.id);
    }
  });
  
  // Handle call initiation
  socket.on('callUser', ({ userToCall, signalData, from, name }) => {
    console.log(`${from} is calling ${userToCall}`);
    
    const userSocket = io.sockets.sockets.get(userToCall);
    if (userSocket) {
      userSocket.emit('callUser', { from, signal: signalData, name });
    }
  });
  
  // Handle call acceptance
  socket.on('answerCall', ({ signal, to }) => {
    console.log(`${socket.id} answered call from ${to}`);
    
    const userSocket = io.sockets.sockets.get(to);
    if (userSocket) {
      userSocket.emit('callAccepted', signal);
    }
  });
  
  // Handle call ending
  socket.on('endCall', () => {
    console.log(`${socket.id} ended the call`);
    
    const partnerId = userConnections.get(socket.id);
    if (partnerId) {
      const partnerSocket = io.sockets.sockets.get(partnerId);
      if (partnerSocket) {
        partnerSocket.emit('callEnded');
      }
      
      // Remove connection
      userConnections.delete(partnerId);
      userConnections.delete(socket.id);
    }
  });
};

/**
 * Handle Text Chat related socket events
 * @param {Socket} socket - Socket instance for the user
 * @param {SocketIO.Server} io - Socket.IO server instance
 */
const handleTextChatEvents = (socket, io) => {
  // Find a new text chat partner
  socket.on('findTextChat', () => {
    console.log(`${socket.id} is looking for a text chat partner`);
    
    // Check if there are any users waiting
    if (textWaitingUsers.length > 0) {
      // Get the first waiting user
      const partnerId = textWaitingUsers.shift();
      const partnerSocket = io.sockets.sockets.get(partnerId);
      
      // Make sure the partner is still connected
      if (partnerSocket) {
        console.log(`Matching ${socket.id} with ${partnerId} for text chat`);
        
        // Create a connection between the two users
        createTextChatPair(socket.id, partnerId);
        
        // Notify both users about the connection
        socket.emit('chatConnected');
        partnerSocket.emit('chatConnected');
      } else {
        // If partner is no longer connected, add this user to the waiting list
        textWaitingUsers.push(socket.id);
      }
    } else {
      // No partners available, add to waiting list
      textWaitingUsers.push(socket.id);
    }
  });
  
  // Handle sending messages
  socket.on('sendMessage', (message) => {
    const partnerId = findTextChatPartner(socket.id);
    
    if (partnerId) {
      const partnerSocket = io.sockets.sockets.get(partnerId);
      if (partnerSocket) {
        partnerSocket.emit('receiveMessage', message);
      }
    }
  });
  
  // Handle typing indicator
  socket.on('typing', () => {
    const partnerId = findTextChatPartner(socket.id);
    
    if (partnerId) {
      const partnerSocket = io.sockets.sockets.get(partnerId);
      if (partnerSocket) {
        partnerSocket.emit('typing');
      }
    }
  });
};

/**
 * Update the online user count for all clients
 * @param {SocketIO.Server} io - Socket.IO server instance
 */
const updateUserCount = (io) => {
  const count = io.sockets.sockets.size;
  io.emit('updateUserCount', count);
};

/**
 * Find the text chat partner for a user
 * @param {string} userId - User socket ID
 * @returns {string|null} - Partner socket ID or null
 */
const findTextChatPartner = (userId) => {
  for (const [key, _] of textChatPairs.entries()) {
    if (key.includes(userId)) {
      return key.split(':').find(id => id !== userId);
    }
  }
  return null;
};

/**
 * Create a new text chat pair
 * @param {string} user1 - First user socket ID
 * @param {string} user2 - Second user socket ID
 */
const createTextChatPair = (user1, user2) => {
  const pairId = [user1, user2].sort().join(':');
  textChatPairs.set(pairId, { startTime: Date.now() });
};

/**
 * Remove a text chat pair
 * @param {string} user1 - First user socket ID
 * @param {string} user2 - Second user socket ID
 */
const removeTextChatPair = (user1, user2) => {
  const pairId = [user1, user2].sort().join(':');
  textChatPairs.delete(pairId);
};

export { setupSocketHandlers };

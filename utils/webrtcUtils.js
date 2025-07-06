/**
 * WebRTC utility functions
 */
import process from 'process';

/**
 * Generate ICE server configuration object
 * @returns {Object} ICE server configuration
 */
const getIceServers = () => {
  return {
    iceServers: [
      {
        urls: process.env.STUN_SERVER_URL || 'stun:stun.l.google.com:19302'
      },
      {
        urls: process.env.TURN_SERVER_URL || 'turn:your-turn-server:3478',
        username: process.env.TURN_SERVER_USERNAME || 'username',
        credential: process.env.TURN_SERVER_CREDENTIAL || 'password'
      }
    ]
  };
};

export {
  getIceServers
};

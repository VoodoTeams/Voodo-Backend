import express from 'express';
import { v4 as uuidv4 } from 'uuid';
import process from 'process';

const router = express.Router();

// @route   GET /api/users/turnCredentials
// @desc    Get TURN server credentials
// @access  Public
router.get('/turnCredentials', (req, res) => {
  try {
    // In a production environment, you would generate temporary credentials
    // that expire after a short period for security
    const credentials = {
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
    
    res.json(credentials);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// @route   GET /api/users/stats
// @desc    Get user stats (online count, etc.)
// @access  Public
router.get('/stats', (req, res) => {
  try {
    const io = req.app.get('io');
    
    const stats = {
      onlineUsers: io ? io.sockets.sockets.size : 0
    };
    
    res.json(stats);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

export default router;

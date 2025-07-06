import express from 'express';
import Hangout from '../models/Hangout.js';

const router = express.Router();

// @route   GET /api/hangouts
// @desc    Get all hangouts
// @access  Public
router.get('/', async (req, res) => {
  try {
    const hangouts = await Hangout.find()
      .sort({ createdAt: -1 }) // Sort by newest first
      .limit(20); // Limit to 20 posts
    
    res.json(hangouts);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// @route   GET /api/hangouts/:id
// @desc    Get hangout by ID
// @access  Public
router.get('/:id', async (req, res) => {
  try {
    const hangout = await Hangout.findById(req.params.id);
    
    if (!hangout) {
      return res.status(404).json({ message: 'Hangout not found' });
    }
    
    res.json(hangout);
  } catch (error) {
    console.error(error);
    if (error.kind === 'ObjectId') {
      return res.status(404).json({ message: 'Hangout not found' });
    }
    res.status(500).json({ message: 'Server error' });
  }
});

// @route   POST /api/hangouts
// @desc    Create a hangout
// @access  Private (will be restricted in the future)
router.post('/', async (req, res) => {
  try {
    const { username, imageUrl, description, tags } = req.body;
    
    // Create a new hangout
    const newHangout = new Hangout({
      username,
      imageUrl,
      description,
      tags,
      likes: 0,
      comments: 0
    });
    
    const hangout = await newHangout.save();
    
    res.json(hangout);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// @route   PUT /api/hangouts/like/:id
// @desc    Like a hangout
// @access  Public (for now, will require auth later)
router.put('/like/:id', async (req, res) => {
  try {
    const hangout = await Hangout.findById(req.params.id);
    
    if (!hangout) {
      return res.status(404).json({ message: 'Hangout not found' });
    }
    
    hangout.likes += 1;
    await hangout.save();
    
    res.json({ likes: hangout.likes });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
});

// @route   DELETE /api/hangouts/:id
// @desc    Delete a hangout
// @access  Private (admin only in the future)
router.delete('/:id', async (req, res) => {
  try {
    const hangout = await Hangout.findById(req.params.id);
    
    if (!hangout) {
      return res.status(404).json({ message: 'Hangout not found' });
    }
    
    await hangout.deleteOne();
    
    res.json({ message: 'Hangout removed' });
  } catch (error) {
    console.error(error);
    if (error.kind === 'ObjectId') {
      return res.status(404).json({ message: 'Hangout not found' });
    }
    res.status(500).json({ message: 'Server error' });
  }
});

export default router;

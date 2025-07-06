import mongoose from 'mongoose';

const HangoutSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true
  },
  imageUrl: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  likes: {
    type: Number,
    default: 0
  },
  comments: {
    type: Number,
    default: 0
  },
  tags: {
    type: [String],
    default: []
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

const Hangout = mongoose.model('Hangout', HangoutSchema);

export default Hangout;

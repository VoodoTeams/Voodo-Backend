import mongoose from 'mongoose';
import dotenv from 'dotenv';
import process from 'process';
import Hangout from './models/Hangout.js';
import { connectDB } from './config/db.js';

// Load environment variables
dotenv.config();

// Sample data
const hangouts = [
  {
    username: 'night_owl',
    imageUrl: 'https://images.unsplash.com/photo-1485470733090-0aae1788d5af?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1391&q=80',
    description: 'Late night vibes. Anyone up for a chat?',
    likes: 234,
    comments: 56,
    tags: ['night', 'vibes', 'chat']
  },
  {
    username: 'aesthetic_dreams',
    imageUrl: 'https://images.unsplash.com/photo-1620503374956-c942862f0372?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80',
    description: 'Found this perfect spot for stargazing. The sky was unreal.',
    likes: 512,
    comments: 89,
    tags: ['sky', 'stars', 'night']
  },
  {
    username: 'digital_wanderer',
    imageUrl: 'https://images.unsplash.com/photo-1638803040283-7a5ffd48dad5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1374&q=80',
    description: 'Cyberpunk dreams. Feeling the neon tonight.',
    likes: 789,
    comments: 104,
    tags: ['cyberpunk', 'neon', 'aesthetic']
  },
  {
    username: 'mindful_explorer',
    imageUrl: 'https://images.unsplash.com/photo-1502899576159-f224dc2349fa?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1528&q=80',
    description: 'Just taking a moment to appreciate the view. Who wants to join?',
    likes: 342,
    comments: 78,
    tags: ['nature', 'mindfulness', 'peace']
  },
  {
    username: 'city_lights',
    imageUrl: 'https://images.unsplash.com/photo-1545843809-8fffa7c6d0de?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
    description: 'City vibes tonight. Anyone in town want to chat?',
    likes: 567,
    comments: 134,
    tags: ['city', 'urban', 'nightlife']
  }
];

// Import data function
const importData = async () => {
  try {
    await connectDB();
    
    // Clear existing data
    await Hangout.deleteMany();
    
    // Insert new data
    await Hangout.insertMany(hangouts);
    
    console.log('Data imported successfully!');
    process.exit(0);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

// Delete all data function
const destroyData = async () => {
  try {
    await connectDB();
    
    // Clear existing data
    await Hangout.deleteMany();
    
    console.log('Data destroyed successfully!');
    process.exit(0);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

// Run the appropriate function based on command line args
if (process.argv[2] === '-d') {
  destroyData();
} else {
  importData();
}

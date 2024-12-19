// require('dotenv').config();
import 'dotenv/config';
import app from './app.js';
import connectDB from './src/config/db.js';
// import app from './app';
// Connect to MongoDB
connectDB();

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Student Service running on port ${PORT}`);
});

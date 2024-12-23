import 'dotenv/config';
import app from './app.js';
import connectDB from './src/config/db.js';

// Connect to MongoDB
connectDB();

const PORT = process.env.PORT || 6000;

app.listen(PORT, () => {
  console.log(`Teacher Service running on port ${PORT}`);
});
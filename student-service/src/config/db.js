import { connect } from 'mongoose';

const connectDB = async () => {
  try {
    const conn = await connect("mongodb+srv://yordanosdev1:VhQWtPoLNC3rq5jX@cluster0.2h58v.mongodb.net/students-db", {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log(`MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

export default connectDB;

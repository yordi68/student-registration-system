import 'dotenv/config';
import app from './app.js';
import connectDB from './src/config/db.js';
import amqplib from 'amqplib';

const RABBITMQ_HOST = process.env.RABBITMQ_HOST || "localhost";
const QUEUE_NAME = "student_updates";
const RETRY_INTERVAL = 5000; // Retry every 5 seconds
const MAX_RETRIES = 5; // Maximum number of retries

async function connectToRabbitMQ(retries = 0) {
  try {
    const connection = await amqplib.connect(`amqp://${RABBITMQ_HOST}`);
    const channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME);
    console.log(`Student Service has Connected to RabbitMQ, queue: ${QUEUE_NAME}`);

    // Example: Publish a message to the queue
    const message = JSON.stringify({ studentId: "12345", status: "registered" });
    channel.sendToQueue(QUEUE_NAME, Buffer.from(message));
    console.log(`Sent message: ${message}`);
  } catch (err) {
    console.error(`Error connecting to RabbitMQ (attempt ${retries + 1}/${MAX_RETRIES}):`, err);

    if (retries < MAX_RETRIES) {
      console.log(`Retrying in ${RETRY_INTERVAL / 1000} seconds...`);
      setTimeout(() => connectToRabbitMQ(retries + 1), RETRY_INTERVAL);
    } else {
      console.error("Failed to connect to RabbitMQ after multiple attempts. Exiting...");
      process.exit(1); // Exit the process if connection fails after retries
    }
  }
}

// Start connecting to RabbitMQ
connectToRabbitMQ();

// Connect to MongoDB
connectDB();

const PORT = process.env.PORT || 8000;

app.listen(PORT, () => {
  console.log(`Student Service running on port ${PORT}`);
});

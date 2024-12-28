import 'dotenv/config';
import app from './app.js';
import connectDB from './src/config/db.js';
import  amqplib from 'amqplib';

const RABBITMQ_HOST = process.env.RABBITMQ_HOST || "localhost";
const QUEUE_NAME = "student_updates";

async function connectToRabbitMQ() {
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
    console.error("Error connecting to RabbitMQ:", err);
  }
}

connectToRabbitMQ();

// Connect to MongoDB
connectDB();

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Student Service running on port ${PORT}`);
});

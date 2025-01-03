import amqplib from "amqplib";
import dotenv from "dotenv";
import connectDB from "./src/config/db.js";
import app from "./app.js";
import pkg from "body-parser";



const { json } = pkg;
dotenv.config(); 

const PORT = process.env.PORT || 5000;

// Consul configuration
const CONSUL_HOST = process.env.CONSUL_HOST || "localhost";
const CONSUL_PORT = process.env.CONSUL_PORT || "8500";
const SERVICE_NAME = "student-service";



async function registerWithConsul() {
  try {
    const payload = {
      Name: SERVICE_NAME,
      Address: "student-service", // Use "localhost" or correct network address here
      Port: PORT,
      Check: {
        HTTP: `http://student-service:${PORT}/health`, // Make sure the health check URL is correct
        Interval: "10s",
      },
    };

    console.log("Registering with Consul with payload:", payload, CONSUL_HOST,CONSUL_PORT, SERVICE_NAME, PORT); // Log the payload

    const response = await fetch(`http://${CONSUL_HOST}:${CONSUL_PORT}/v1/agent/service/register`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Failed to register service with Consul: ${response.statusText}`);
    }

    console.log(`${SERVICE_NAME} registered with Consul`);
  } catch (error) {
    console.error(`Error registering ${SERVICE_NAME} with Consul:`, error.message);
  }
}

// RabbitMQ configuration
const RABBITMQ_HOST = process.env.RABBITMQ_HOST || "localhost";
const QUEUE_NAME = "student_updates";

// Connect to RabbitMQ
async function connectToRabbitMQ() {
  try {
    const connection = await amqplib.connect(`amqp://${RABBITMQ_HOST}`);
    const channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME);
    console.log(`Student Service has connected to RabbitMQ, queue: ${QUEUE_NAME}`);

    // Example: Publish a message to the queue
    const message = JSON.stringify({ studentId: "12345", status: "registered" });
    channel.sendToQueue(QUEUE_NAME, Buffer.from(message));
    console.log(`Sent message: ${message}`);
  } catch (err) {
    console.error("Error connecting to RabbitMQ:", err);
  }
}

// Healthcheck endpoint
app.get("/health", (req, res) => {
  res.status(200).send("OK");
});

// Basic route
app.get("/", (req, res) => {
  res.send("Welcome to the Student Service");
});

// Connect to MongoDB (assuming connectDB is defined correctly)
connectDB();

// Start the Express server and register with Consul
app.listen(PORT, async () => {
  console.log(`Student Service running on port ${PORT}`);
  await registerWithConsul();
  connectToRabbitMQ(); // Connect to RabbitMQ once the server is running
});

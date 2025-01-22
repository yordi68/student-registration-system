import { connect } from "amqplib";

const RABBITMQ_HOST = "rabbitmq";
const QUEUE_NAME = "registration_events";
const RETRY_INTERVAL = 5000; // Retry every 5 seconds
const MAX_RETRIES = 10;

async function sendNotification(e) {
  const url = "http://localhost:8080/student/api/students/email/";
  console.log("Sending notification to user:", e);
  try {
    // Make a GET request
    const response = await fetch(url);

    // Check if the response is OK (status code 200-299)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Parse the response as JSON
    const data = await response.json();

    // Log the fetched data
    console.log("Fetched data:", data);
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

async function connectToRabbitMQ(retries = 0) {
  try {
    const connection = await connect(`amqp://${RABBITMQ_HOST}`);
    const channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME);
    console.log(
      `Notification Service has Connected to RabbitMQ, queue: ${QUEUE_NAME}`
    );

    console.log(
      " [*] Waiting for messages in %s. To exit press CTRL+C",
      QUEUE_NAME
    );

    channel.consume(
      QUEUE_NAME,
      (msg) => {
        if (msg !== null) {
          const event = JSON.parse(msg.content.toString());
          console.log(" [x] Received event:", event);

          // sendNotification(event);

          channel.ack(msg);
        }
      },
      { noAck: false }
    );
  } catch (err) {
    console.error(
      `Error connecting to RabbitMQ (attempt ${retries + 1}/${MAX_RETRIES}):`,
      err
    );

    if (retries < MAX_RETRIES) {
      console.log(`Retrying in ${RETRY_INTERVAL / 1000} seconds...`);
      setTimeout(() => connectToRabbitMQ(retries + 1), RETRY_INTERVAL);
    } else {
      console.error(
        "Failed to connect to RabbitMQ after multiple attempts. Exiting..."
      );
      process.exit(1); // Exit the process if connection fails after retries
    }
  }
}

connectToRabbitMQ();

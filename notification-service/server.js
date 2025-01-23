import { connect } from 'amqplib';
import nodemailer from 'nodemailer';

const RABBITMQ_HOST = 'rabbitmq';
const QUEUE_NAME = 'registration_events';
const RETRY_INTERVAL = 5000;
const MAX_RETRIES = 10;
const token = process.env.TOKEN;
const EMAIL_KEY = 'f5CIAOozH3wFDf_cJ';
const SERVICE_ID = 'service_6o76805';
const TEMPLATE_ID = 'template_zawzkx5';

const sendEmail = (email) => {
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    host: 'smtp.gmail.com',
    port: 587,
    secure: false,
    auth: {
      user: 'ketemayodahe@gmail.com',
      pass: 'eswp aimr ewad symx'
    },
  });
  console.log("Sending email...", email);

  const mailOptions = {
    from: 'buleboyyy2@gmail.com',
    to: email.student_email,
    subject: 'Course Registration Confirmation',
    html: `
      <p>Hello ${email.student_name},</p>
      <p>You have registered for the new year </p>
      <p style="padding: 12px; border-left: 4px solid #d0d0d0; font-style: italic;">
        ${email.message}
      </p>
      <p>
        Good luck on you studies !!
      </p>
    `
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.log('FAILED...', error);
    } else {
      console.log('SUCCESS!', info.response);
    }
  });
};

async function connectToRabbitMQ(retries = 0) {
  try {
    const connection = await connect(`amqp://${RABBITMQ_HOST}`);
    const channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME);
    console.log(`Notification Service has Connected to RabbitMQ, queue: ${QUEUE_NAME}`);

    console.log(' [*] Waiting for messages in %s. To exit press CTRL+C', QUEUE_NAME);

    channel.consume(QUEUE_NAME, (msg) => {
      if (msg !== null) {
        const event = JSON.parse(msg.content.toString());
        console.log(" [x] Received event:", event);
        const courses = event.course_list.join(", ");
        const message = "You have successfully registered for the following courses: " + courses + ". Thank you!";

        sendEmail({
          student_email: event.student_email,
          student_name: event.student_name,
          message: message,
        })

        // sendNotification(event);

        channel.ack(msg);
      }
    }, { noAck: false });

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

connectToRabbitMQ();
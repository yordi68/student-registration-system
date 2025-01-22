from fastapi import FastAPI
from app.routes import router
import pika
import os
import threading
import time


# rabbitmq set up
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "student_updates"
REGISTRATION_QUEUE_NAME = "registration_events"

def start_rabbitmq_listener():
    print("Inside function")
    while True:
        try:
            print("Inside try.")
            # Establish connection with RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            print("Registration Service Connected with RabbitMQ")
            channel = connection.channel()

            # Declare queues before consuming messages
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.queue_declare(queue=REGISTRATION_QUEUE_NAME, durable=True)
            print(f"Queues '{QUEUE_NAME}' and '{REGISTRATION_QUEUE_NAME}' declared successfully.")

            # Callback function to process messages
            def callback(ch, method, properties, body):
                print("Received message:", body.decode())

            # Start consuming messages from the queue
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
            print("Listening for messages...")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying in 5 seconds...")
            time.sleep(5)

        except Exception as e:
            print(f"Error in RabbitMQ listener: {e}")
            time.sleep(5)


app = FastAPI()

app.include_router(router, prefix="/api/registrations", tags=["Registrations"])

@app.on_event("startup")
def rabbitmq_startup():
    print("Starting RabbitMQ listener...")
    # Start RabbitMQ listener in a separate thread
    threading.Thread(target=start_rabbitmq_listener, daemon=True).start()
    print("RabbitMQ listener started successfully.")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Registration Service API"}

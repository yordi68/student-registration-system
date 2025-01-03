from fastapi import FastAPI
import requests
import os
import pika
import threading
import time
from app.routes import router  # Assuming you have routes defined in this module

# FastAPI application instance
app = FastAPI()

# Consul configuration
CONSUL_HOST = os.getenv("CONSUL_HOST", "localhost")
CONSUL_PORT = os.getenv("CONSUL_PORT", "8500")
SERVICE_NAME = "registration-service"
SERVICE_PORT = 8001

# RabbitMQ configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "student_updates"

def register_with_consul():
    """Registers the service with Consul"""
    try:
        response = requests.put(
            f"http://{CONSUL_HOST}:{CONSUL_PORT}/v1/agent/service/register",
            json={
                "Name": SERVICE_NAME,
                "Address": "registration-service",
                "Port": SERVICE_PORT,
                "Check": {
                    "HTTP": f"http://registration-service:{SERVICE_PORT}/health",
                    "Interval": "10s",
                },
            },
        )
        # print(response.json)
        if response.status_code == 200:
            print(f"{SERVICE_NAME, SERVICE_PORT, CONSUL_HOST, CONSUL_PORT} registered with Consul")
        else:
            print(f"Failed to register {SERVICE_NAME} with Consul:", response.text)
    except Exception as e:
        print(f"Error registering {SERVICE_NAME} with Consul:", str(e))


def start_rabbitmq_listener():
    """Starts listening to RabbitMQ messages"""
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            print("Registration Service Connected with RabbitMQ")
            break
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying in 5 seconds...")
            time.sleep(5)

    channel = connection.channel()
    try:
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
    except pika.exceptions.ChannelClosedByBroker as e:
        print(f"Queue declaration failed: {e}")
        return

    def callback(ch, method, properties, body):
        print("Received message:", body.decode())

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    print("Listening for messages...")
    channel.start_consuming()


@app.on_event("startup")
def startup_event():
    """Handles startup tasks like Consul registration and RabbitMQ listener"""
    register_with_consul()
    # Start RabbitMQ listener in a separate thread
    threading.Thread(target=start_rabbitmq_listener, daemon=True).start()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "OK"}


@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint"""
    return {"message": "Welcome to the Registration Service API"}


# Include the registration-related routes
app.include_router(router, prefix="/api/registrations", tags=["Registrations"])

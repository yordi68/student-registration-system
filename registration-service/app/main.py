from fastapi import FastAPI
from app.routes import router
import pika
import os
import threading
import time


# rabbitmq set up
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "student_updates"

def start_rabbitmq_listener():
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



app = FastAPI()

app.include_router(router, prefix="/api/registrations", tags=["Registrations"])

@app.on_event("startup")
def rabbitmq_startup():
    # Start RabbitMQ listener in a separate thread
    threading.Thread(target=start_rabbitmq_listener, daemon=True).start()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Registration Service API"}

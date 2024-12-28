from fastapi import APIRouter, HTTPException, status
from app.models import Registration, PyObjectId
from app.database import registrations_collection
from bson import ObjectId
import pika
import os

router = APIRouter()

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "registration_events"

# Utility function to publish events to RabbitMQ
def publish_event(event: dict):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=str(event),
            properties=pika.BasicProperties(delivery_mode=2),  # Make message persistent
        )
        connection.close()
    except Exception as e:
        print(f"Error publishing message to RabbitMQ: {e}")

# Create a new registration
@router.post("/", response_description="Register a student", status_code=status.HTTP_201_CREATED)
async def create_registration(registration: Registration):
    result = registrations_collection.insert_one(registration.model_dump(by_alias=True, exclude={"id"}))
    registration_id = str(result.inserted_id)

    # Publish event to RabbitMQ
    event = {
        "event": "RegistrationCreated",
        "registration_id": registration_id,
        "student_id": registration.student_id,
        "course_id": registration.course_id,
        "registration_date": registration.registration_date,
    }
    publish_event(event)

    return {"message": "Registration created successfully", "id": registration_id}

# Get all registrations
@router.get("/", response_description="List all registrations")
async def get_registrations():
    registrations = list(registrations_collection.find())
    return [Registration(**registration) for registration in registrations]

# Get a specific registration by ID
@router.get("/{id}", response_description="Get a single registration")
async def get_registration(id: str):
    registration = registrations_collection.find_one({"_id": ObjectId(id)})
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    return Registration(**registration)

# Update a registration
@router.put("/{id}", response_description="Update a registration")
async def update_registration(id: str, registration: Registration):
    result = registrations_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": registration.model_dump(by_alias=True, exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Registration not found")

    # Publish event to RabbitMQ
    event = {
        "event": "RegistrationUpdated",
        "registration_id": id,
        "student_id": registration.student_id,
        "course_id": registration.course_id,
        "registration_date": registration.registration_date,
    }
    publish_event(event)

    return {"message": "Registration updated successfully"}

# Delete a registration
@router.delete("/{id}", response_description="Delete a registration", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registration(id: str):
    result = registrations_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Registration not found")

    # Publish event to RabbitMQ
    event = {
        "event": "RegistrationDeleted",
        "registration_id": id,
    }
    publish_event(event)

    return {"message": "Registration deleted successfully"}

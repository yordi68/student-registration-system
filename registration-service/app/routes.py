from fastapi import APIRouter, HTTPException, status, FastAPI
from app.models import Registration, PyObjectId
from app.database import registrations_collection
from bson import ObjectId
import pika
import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

# Define a dictionary to hold courses for each year
courses_by_year = {
    "1": [
        "Introduction to Programming",
        "Mathematics I",
        "Physics I",
        "English Composition",
        "Introduction to Psychology"
    ],
    "2": [
        "Data Structures and Algorithms",
        "Mathematics II",
        "Physics II",
        "Object-Oriented Programming",
        "Introduction to Sociology"
    ],
    "3": [
        "Database Management Systems",
        "Software Engineering",
        "Operating Systems",
        "Discrete Mathematics",
        "Web Development"
    ],
    "4": [
        "Machine Learning",
        "Computer Networks",
        "Mobile Application Development",
        "Human-Computer Interaction",
        "Capstone Project"
    ],
    "5": [
        "Advanced Topics in Artificial Intelligence",
        "Cloud Computing",
        "Cybersecurity",
        "Data Science and Big Data Analytics",
        "Entrepreneurship and Innovation"
    ]
}


router = APIRouter()
app = FastAPI()

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "registration_events"
STUDENT_API_URL="http://nginx/student/api/students/email/"
token = os.getenv("TOKEN")

async def fetch_student_by_email(email: str):
    headers = {
        "Authorization": f"Bearer {token}",
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{STUDENT_API_URL}{email}", headers=headers)
            print(f"Response: {response}")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors (e.g., 404, 500)
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        # Handle other errors (e.g., network issues)\
        print(f"Error fetching student: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Utility function to publish events to RabbitMQ
async def publish_event(event: dict):
    try:
        # Establish connection
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        # Declare the queue (idempotent operation)
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        print("fetching student")
        student = await fetch_student_by_email(event["student_email"]);
        print(student)

        if "error" in student:
            print(f"Error in student data: {student['error']}")
            return;
        event["student_name"] = student["name"]
        
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(event),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            ),
        )

        print(f"Published event: {event}")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        print(f"Error publishing message to RabbitMQ: {e}")
    finally:
        # Close the connection
        if 'connection' in locals() and connection.is_open:
            connection.close()

# Create a new registration
@router.post("/", response_description="Register a student", status_code=status.HTTP_201_CREATED)
async def create_registration(registration: Registration):

    # async with httpx.AsyncClient() as client:
    #     response = await client.get(f'http://localhost:8080/student/api/students/email/{registration.student_email}')
    #     response.raise_for_status()  # Raise an exception for HTTP errors
    #     student_info = response.json()

    # Insert the new registration data
    result = registrations_collection.insert_one(registration.model_dump(by_alias=True, exclude={"id"}))
    registration_id = str(result.inserted_id)

    # Publish event to RabbitMQ
    event = {
        "event": "RegistrationCreated",
        "registration_id": registration_id,
        "student_email": registration.student_email,
        "course_list": courses_by_year[registration.year],
        "registration_date": registration.registration_date,
    }
    print(event)
    await publish_event(event)

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
    await publish_event(event)

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
    await publish_event(event)

    return {"message": "Registration deleted successfully"}

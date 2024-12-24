from fastapi import APIRouter, HTTPException, status
from app.models import Registration, PyObjectId
from app.database import registrations_collection
from bson import ObjectId

router = APIRouter()

# Create a new registration
@router.post("/", response_description="Register a student", status_code=status.HTTP_201_CREATED)
async def create_registration(registration: Registration):
    result = registrations_collection.insert_one(registration.model_dump(by_alias=True, exclude={"id"}))
    return {"message": "Registration created successfully", "id": str(result.inserted_id)}

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
    return {"message": "Registration updated successfully"}

# Delete a registration
@router.delete("/{id}", response_description="Delete a registration", status_code=status.HTTP_204_NO_CONTENT)
async def delete_registration(id: str):
    result = registrations_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Registration not found")
    return {"message": "Registration deleted successfully"}

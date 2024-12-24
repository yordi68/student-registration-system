from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# Helper class for handling MongoDB ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

# Registration model
class Registration(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # Optional _id field with default None
    student_id: str  # Required student_id field
    course_id: str    # Required course_id field
    registration_date: str  # Required registration_date field in ISO 8601 format

    class Config:
        populate_by_name = True  # Allows population by both names and aliases
        json_encoders = {ObjectId: str}  # Converts ObjectId to string during JSON serialization
        json_schema_extra = {  # Example payload for documentation
            "example": {
                "student_id": "64123abcd567890123456789",
                "course_id": "CSC101",
                "registration_date": "2024-12-01"
            }
        }

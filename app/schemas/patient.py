import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import re

class PatientBase(BaseModel):
    """Base schema with shared attributes"""
    name: str = Field(..., min_length=2, max_length=100, description="Patient's full name")
    email: EmailStr = Field(..., description="Patient's email address")
    phone_number: str = Field(..., description="Patient's phone number")

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        """Validate phone number format"""
        pattern = r"^\+?[0-9\s\-\(\)]{8,20}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid phone number format. Examples: +1234567890, 123-456-7890, (123) 456-7890")
        return value

class PatientCreate(PatientBase):
    """Schema for creating a new patient - used for request validation"""
    pass

class PatientResponse(PatientBase):
    """Schema for patient response - used when returning patient data"""
    id: uuid.UUID
    document_photo_filename: str
    document_photo_content_type: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class PatientFormData(BaseModel):
    """Combined form data with both patient details and document"""
    patient_data: PatientCreate
    document_content: bytes
    document_filename: str
    document_content_type: str
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

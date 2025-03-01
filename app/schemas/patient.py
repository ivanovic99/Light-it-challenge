import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator
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
            raise ValueError("Invalid phone number format")
        return value

class PatientCreate(PatientBase):
    """Schema for creating a new patient - used for request validation"""
    # Document photo is being handled separately via UploadFile
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

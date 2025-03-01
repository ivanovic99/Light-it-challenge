import pytest
from pydantic import ValidationError

from app.schemas.patient import PatientCreate

def test_patient_create_valid_data():
    # Valid patient data should pass validation
    patient = PatientCreate(
        name="John Doe",
        email="john.doe@example.com",
        phone_number="+1234567890"
    )
    
    assert patient.name == "John Doe"
    assert patient.email == "john.doe@example.com"
    assert patient.phone_number == "+1234567890"

def test_patient_create_invalid_name():
    # Name too short should fail
    with pytest.raises(ValidationError) as exc_info:
        PatientCreate(
            name="J",  # Too short
            email="john.doe@example.com",
            phone_number="+1234567890"
        )
    
    assert "name" in str(exc_info.value)
    # Update this to match the current Pydantic error format
    assert "String should have at least 2 characters" in str(exc_info.value)

def test_patient_create_invalid_email():
    # Invalid email should fail
    with pytest.raises(ValidationError) as exc_info:
        PatientCreate(
            name="John Doe",
            email="not-an-email",  # Invalid format
            phone_number="+1234567890"
        )
    
    assert "email" in str(exc_info.value)

def test_patient_create_invalid_phone():
    # Invalid phone format should fail
    with pytest.raises(ValidationError) as exc_info:
        PatientCreate(
            name="John Doe",
            email="john.doe@example.com",
            phone_number="abc"  # Invalid format
        )
    
    assert "phone_number" in str(exc_info.value)
    assert "Invalid phone number format" in str(exc_info.value)

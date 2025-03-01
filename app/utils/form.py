from fastapi import Form, File, UploadFile, HTTPException, status
from pydantic import ValidationError

from app.schemas.patient import PatientCreate, PatientFormData
from app.services.file_handling import FileProcessingService

file_service = FileProcessingService()

async def get_patient_form(
    name: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    document_photo: UploadFile = File(...)
) -> PatientFormData:
    """
    Process and validate all form data including document.
    Returns a combined object with validated patient data and document content.
    """
    try:
        # 1. Validate patient data through Pydantic
        patient_data = PatientCreate(
            name=name,
            email=email,
            phone_number=phone_number
        )
        
        # 2. Validate document using service
        document_content = await file_service.validate_document(document_photo)
        
        # 3. Return combined validated data
        return PatientFormData(
            patient_data=patient_data,
            document_content=document_content,
            document_filename=document_photo.filename,
            document_content_type=document_photo.content_type
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )

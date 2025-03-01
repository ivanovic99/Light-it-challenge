from fastapi import APIRouter, Depends, UploadFile, File, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.notifications import NotificationFactory
from app.services.file_handling import FileProcessingService

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)

file_service = FileProcessingService()

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    *,
    background_tasks: BackgroundTasks,
    patient_data: PatientCreate,
    document_photo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new patient with document photo.
    """
    # Validate and process document photo
    document_content = await file_service.validate_document(document_photo)
    
    # Create patient object
    patient = Patient(
        name=patient_data.name,
        email=patient_data.email,
        phone_number=patient_data.phone_number,
        document_photo=document_content,
        document_photo_filename=document_photo.filename,
        document_photo_content_type=document_photo.content_type
    )
    
    # Save to database
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    
    # Send confirmation notification
    notifier = NotificationFactory.get_notifier("email")
    notifier.schedule_notification(
        background_tasks,
        patient.email,
        "Registration Confirmation",
        {
            "name": patient.name,
            "message": "Thank you for registering with our service. Your information has been received."
        }
    )
    
    return patient

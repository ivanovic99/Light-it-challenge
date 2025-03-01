from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientResponse, PatientFormData
from app.services.notifications import NotificationFactory
from app.services.file_handling import FileProcessingService
from app.utils.form import get_patient_form

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)

file_service = FileProcessingService()

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    *,
    background_tasks: BackgroundTasks,
    form_data: PatientFormData = Depends(get_patient_form),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new patient with document photo.
    All form data is pre-validated through dependencies.
    """
    # Create patient object using validated data
    patient = Patient(
        name=form_data.patient_data.name,
        email=form_data.patient_data.email,
        phone_number=form_data.patient_data.phone_number,
        document_photo=form_data.document_content,
        document_photo_filename=form_data.document_filename,
        document_photo_content_type=form_data.document_content_type
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

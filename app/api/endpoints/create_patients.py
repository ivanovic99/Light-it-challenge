from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

from app.db.base import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientResponse, PatientFormData
from app.services.notifications import NotificationFactory
from app.services.file_handling import FileProcessingService
from app.utils.form import get_patient_form

logger = logging.getLogger(__name__)

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
    logger.info("Starting patient creation process")
    logger.debug(f"Processing patient data for: {form_data.patient_data.name}")
    
    patient = Patient(
        name=form_data.patient_data.name,
        email=form_data.patient_data.email,
        phone_number=form_data.patient_data.phone_number,
        document_photo=form_data.document_content,
        document_photo_filename=form_data.document_filename,
        document_photo_content_type=form_data.document_content_type
    )
    
    try:
        logger.debug("Attempting to save patient to database")
        db.add(patient)
        await db.commit()
        await db.refresh(patient)
        logger.info(f"Patient {patient.id} created successfully")
        
    except IntegrityError as e:
        await db.rollback()
        error_msg = str(e).lower()
        logger.warning(f"IntegrityError during patient creation: {error_msg}")
        
        if "duplicate" in error_msg and "email" in error_msg:
            logger.info(f"Duplicate email attempt: {form_data.patient_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A patient with this email address already exists"
            )
        elif "duplicate" in error_msg:
            logger.info("Duplicate record attempt")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This record already exists in the system"
            )
        else:
            logger.error(f"Database constraint violation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data provided - database constraint violation"
            )
            
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"SQLAlchemy error while creating patient: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving the patient data"
        )
    
    try:
        logger.info(f"Scheduling notification for patient {patient.id}")
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
        logger.debug(f"Notification scheduled successfully for {patient.email}")
    except Exception as e:
        logger.error(f"Failed to schedule notification: {str(e)}")
    
    logger.info(f"Patient creation process completed for ID: {patient.id}")
    return patient

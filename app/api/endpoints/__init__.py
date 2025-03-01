from fastapi import APIRouter

from app.api.endpoints.create_patients import router as patients_router

# Main API router
router = APIRouter()

# Include all endpoint routers
router.include_router(patients_router)

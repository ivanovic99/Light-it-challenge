from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.endpoints import router as api_router
from app.utils.logger import setup_logging

setup_logging(logging.INFO)

app = FastAPI(
    title="Patient Registration API",
    description="API for registering patients and uploading their documents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Patient Registration API"}

logging.info("Patient Registration API started")
logging.debug("Debug logging enabled")

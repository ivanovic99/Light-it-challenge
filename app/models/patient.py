import uuid

from sqlalchemy import Column, DateTime, String, func, Index
from sqlalchemy.dialects.mysql import BINARY, MEDIUMBLOB

from app.db.base import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    
    document_photo = Column(MEDIUMBLOB, nullable=False)
    document_photo_filename = Column(String(255), nullable=False)
    document_photo_content_type = Column(String(100), nullable=False)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        Index('idx_patients_email_unique', email, unique=True),
    )
    
    @property
    def id_as_uuid(self):
        """Convert stored binary UUID to Python UUID object"""
        return uuid.UUID(bytes=self.id)
    
    def __str__(self):
        return f"Patient: {self.name} ({self.email})"

    def __repr__(self):
        return f"<Patient(id={self.id_as_uuid}, name={self.name}, email={self.email})>"

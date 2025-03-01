from fastapi import UploadFile, HTTPException, status

from app.services.file_handling.validators import (
    ContentTypeValidator,
    MagicNumberValidator,
    FileSizeValidator
)

class FileProcessingService:
    """Service for file validation and processing"""
    
    def __init__(self):
        # Default allowed types for document photos
        self.document_allowed_types = {"image/jpeg", "image/jpg", "image/png", "application/pdf"}
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        
        # Setup validation chain
        size_validator = FileSizeValidator(self.max_file_size)
        content_type_validator = ContentTypeValidator(self.document_allowed_types, size_validator)
        self.validator_chain = MagicNumberValidator(content_type_validator)
    
    async def validate_document(self, file: UploadFile) -> bytes:
        """
        Validate document file and return its contents
        Raises HTTPException if validation fails
        """
        # Read file content first so we can validate it
        file_content = await file.read()
        
        # Validate using chain
        is_valid, error_message = await self.validator_chain.validate(file, file_content)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Reset file pointer if needed for further processing
        await file.seek(0)
        
        return file_content

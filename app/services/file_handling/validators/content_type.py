from typing import Optional, Set

from fastapi import UploadFile

from app.services.file_handling.validators.base import FileValidator

class ContentTypeValidator(FileValidator):
    """Validates file's content type against allowed types"""
    
    def __init__(self, allowed_types: Set[str], next_validator: Optional[FileValidator] = None):
        super().__init__(next_validator)
        self.allowed_types = allowed_types
    
    async def _validate(self, file: UploadFile, file_content: bytes) -> tuple[bool, str]:
        if file.content_type not in self.allowed_types:
            return False, f"Invalid file type: {file.content_type}. Allowed types: {', '.join(self.allowed_types)}"
        return True, ""

from typing import Optional

from fastapi import UploadFile

from app.services.file_handling.validators.base import FileValidator

class FileSizeValidator(FileValidator):
    """Validates file doesn't exceed maximum size"""
    
    def __init__(self, max_size_bytes: int, next_validator: Optional[FileValidator] = None):
        super().__init__(next_validator)
        self.max_size_bytes = max_size_bytes
    
    async def _validate(self, file: UploadFile, file_content: bytes) -> tuple[bool, str]:
        if len(file_content) > self.max_size_bytes:
            max_mb = self.max_size_bytes / (1024 * 1024)
            return False, f"File exceeds maximum size of {max_mb:.1f}MB"
        return True, ""

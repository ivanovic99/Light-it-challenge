from abc import ABC, abstractmethod
from typing import Optional, Tuple

from fastapi import UploadFile

class FileValidator(ABC):
    """Base class for file validators"""
    
    def __init__(self, next_validator: Optional['FileValidator'] = None):
        self.next_validator = next_validator
    
    async def validate(self, file: UploadFile, file_content: bytes) -> Tuple[bool, str]:
        """
        Validate the file and pass to next validator if present
        Returns: (is_valid, error_message)
        """
        is_valid, message = await self._validate(file, file_content)
        
        if not is_valid:
            return False, message
            
        if self.next_validator:
            return await self.next_validator.validate(file, file_content)
            
        return True, ""
    
    @abstractmethod
    async def _validate(self, file: UploadFile, file_content: bytes) -> Tuple[bool, str]:
        """Concrete validation implementation"""
        pass

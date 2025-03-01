import magic

from fastapi import UploadFile

from app.services.file_handling.validators.base import FileValidator

class MagicNumberValidator(FileValidator):
    """Validates file's actual content using magic numbers"""
    
    async def _validate(self, file: UploadFile, file_content: bytes) -> tuple[bool, str]:
        detected_type = magic.from_buffer(file_content, mime=True)
        if detected_type != file.content_type:
            return False, f"File content ({detected_type}) doesn't match declared type ({file.content_type})"
        return True, ""

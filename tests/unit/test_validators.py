import pytest
from io import BytesIO

from app.services.file_handling.validators.file_size import FileSizeValidator
from app.services.file_handling.validators.content_type import ContentTypeValidator
from app.services.file_handling.validators.magic_number import MagicNumberValidator

# Create a mock UploadFile for testing
class MockUploadFile:
    def __init__(self, content: bytes, content_type: str, filename: str):
        self.file = BytesIO(content)
        self.content_type = content_type
        self.filename = filename
        
    async def read(self):
        self.file.seek(0)
        return self.file.read()
        
    async def seek(self, position):
        self.file.seek(position)

@pytest.fixture
def create_upload_file():
    def _create_file(content: bytes, content_type: str, filename: str) -> MockUploadFile:
        return MockUploadFile(content, content_type, filename)
    return _create_file

@pytest.mark.asyncio
async def test_file_size_validator_success(create_upload_file):
    # Arrange
    content = b"test file content" * 10  # Small file
    file = create_upload_file(content, "text/plain", "test.txt")
    validator = FileSizeValidator(max_size_bytes=1000)
    
    # Act
    is_valid, message = await validator._validate(file, content)
    
    # Assert
    assert is_valid is True
    assert message == ""

@pytest.mark.asyncio
async def test_file_size_validator_failure(create_upload_file):
    # Arrange
    content = b"test file content" * 100  # Large file
    file = create_upload_file(content, "text/plain", "test.txt")
    validator = FileSizeValidator(max_size_bytes=100)
    
    # Act
    is_valid, message = await validator._validate(file, content)
    
    # Assert
    assert is_valid is False
    assert "exceeds maximum size" in message

@pytest.mark.asyncio
async def test_content_type_validator(create_upload_file):
    # Arrange
    content = b"test content"
    allowed_types = {"text/plain", "application/json"}
    
    # Act & Assert - Valid type
    valid_file = create_upload_file(content, "text/plain", "test.txt")
    validator = ContentTypeValidator(allowed_types)
    is_valid, message = await validator._validate(valid_file, content)
    assert is_valid is True
    
    # Act & Assert - Invalid type
    invalid_file = create_upload_file(content, "image/png", "test.png")
    is_valid, message = await validator._validate(invalid_file, content)
    assert is_valid is False
    assert "Invalid file type" in message

# Fix the magic number validator test to match the actual implementation
@pytest.mark.asyncio
async def test_magic_number_validator(create_upload_file):
    # Arrange - Create a valid JPEG file
    jpeg_header = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C"
    
    # Act & Assert - Valid case: content_type matches the detected type
    valid_file = create_upload_file(jpeg_header, "image/jpeg", "test.jpg")
    validator = MagicNumberValidator()
    
    is_valid, message = await validator._validate(valid_file, jpeg_header)
    assert is_valid is True
    
    # Act & Assert - Invalid case: content_type doesn't match detected type
    # Using JPEG content but declaring it as PNG
    invalid_file = create_upload_file(jpeg_header, "image/png", "fake.png")
    
    is_valid, message = await validator._validate(invalid_file, jpeg_header)
    assert is_valid is False
    assert "doesn't match declared type" in message

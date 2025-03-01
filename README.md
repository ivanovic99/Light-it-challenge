# Patient Registration API
A robust FastAPI application for registering patients and securely handling their documents.

## Table of Contents
- Setup
- API Documentation
- Architecture
- Design Patterns
- Testing
- License
- Conclusion

## Setup

#### Prerequisites
- Docker and Docker Compose


### Configuration
Create a .env file in the project root with the following variables:

```plaintext
DATABASE_URL=mysql+asyncmy://user:password@db:3306/patient_db
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USER=eb23e02d772440
EMAIL_PASSWORD=278e526e98fee1
```

### Running the Application
To start the application, run:

```bash
# Build and start the containers
docker-compose up --build

# Application will be available at http://localhost:8080
```

And to stop the application (and remove volumes "-v"):

```bash
docker-compose down -v
```

## API Documentation
Once the application is running, you can access the interactive API documentation:

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc


### Endpoints
POST /api/patients/
Register a new patient with document photo.

#### Request:

- Format: multipart/form-data
- Fields:
    - name: Patient's full name (required)
    - email: Patient's email address (required)
    - phone_number: Patient's phone number (required)
    - document_photo: Image file of patient's document (required)

#### Response:

- Status: 201 Created
- Body: Patient information including ID and timestamps

#### Error Responses:

- 400 Bad Request: Invalid data or duplicate email
- 422 Unprocessable Entity: Validation errors
- 500 Internal Server Error: Server-side issues

## Architecture
The application follows a clean layered architecture:

1. *Presentation Layer*: API endpoints (FastAPI routes)
2. *Application Layer*: Form handling, service orchestration
3. *Domain Layer*: Business models and validation rules
4. *Infrastructure Layer*: Database, file storage, notifications

This separation ensures that each component has a single responsibility and can be modified independently.

### Project Structure
```plaintext
app/
├── api/
│   └── endpoints/      # API routes
├── core/              # Core configuration
├── db/                # Database connection and models
├── models/            # SQLAlchemy ORM models
├── schemas/           # Pydantic models for validation
├── services/          # Business logic and services
│   └── file_handling/  # File validation services
│       └── validators/ # Chain of validators
└── utils/             # Utility functions
```

## Design Patterns
This project demonstrates several design patterns to ensure maintainable, extensible code:

1. *Chain of Responsibility Pattern*
Used for file validation, allowing each validator to:

- Focus on a single validation aspect (content type, magic number, file size)
- Pass the file to the next validator if it passes
- Fail early when validation errors are detected
- Be easily extended with new validators

2. *Strategy Pattern*
Implemented in the notification system:

- Common interface (Notifier) for all notification methods
- Runtime selection of notification strategy (email, SMS)
- New notification types can be added without changing existing code

3. *Form Data Pattern*
Leverages FastAPI's dependency injection system:

- Separates form processing from business logic
- Combines Pydantic validation with file validation
- Returns pre-validated data to endpoints
- Keeps endpoint code focused on business operations

4. *Repository Pattern* (Partial)
DISCLAIMER: This is what the ORM already does, but it's worth mentioning though.
Used for database operations:

- Encapsulates database access logic
- Enforces model constraints
- Provides a clean API for database operations


### Benefits of This Architecture
- Clean Code: Endpoints contain only business logic, not validation or infrastructure concerns
- Separation of Concerns: Each component has a single responsibility
- Extensibility: Easy to add new validators, notifiers, or other components
- DRY Principle: Validation logic is defined once and reused
- Error Handling: Consistent error responses across the application (room for improvement here)
- Testability: Components can be tested in isolation

## Testing

To run tests:

```bash
# Run all tests
docker-compose run -e TEST_MODE=true api pytest

# Run with verbose output
docker-compose run -e TEST_MODE=true api pytest -v

# Run specific test file
docker-compose run -e TEST_MODE=true api pytest test/unit/test_validators.py
```

To remove test containers (and remove volumes "-v"):

```bash
docker-compose down -v
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Conclusion

This project demonstrates best practices for building maintainable, scalable APIs using modern Python frameworks and design patterns.

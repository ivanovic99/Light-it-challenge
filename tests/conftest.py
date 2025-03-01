import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

# Use test database
os.environ["DATABASE_URL"] = "mysql+asyncmy://user:password@db:3306/test_db"

# Import all models to ensure they're registered with the metadata
from app.db.base import Base, get_db
from app.models.patient import Patient
from app.main import app

# Create async test engine - but we won't use it for actual database operations in unit tests
engine_test = create_async_engine(
    os.environ["DATABASE_URL"], 
    poolclass=NullPool
)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a mock database session for unit tests.
    No actual DB operations will be performed since we're focusing on unit tests only.
    """
    async with async_session_maker() as session:
        yield session

@pytest.fixture(scope="function")
def client() -> TestClient:
    """Create a test client for the FastAPI app"""
    return TestClient(app)

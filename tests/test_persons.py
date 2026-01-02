import pytest
import uuid
from app.services.persons_impl import PersonServiceImpl
from app.models import PersonCreate, Person


@pytest.mark.asyncio
async def test_create_person_generates_uuid():
    """Test that creating a person generates a valid UUID."""
    service = PersonServiceImpl()
    data = PersonCreate(name="John Doe", email="john@example.com")
    
    result = await service.create_person(data)
    
    assert result.id is not None
    # Verify it's a valid UUID format
    uuid.UUID(result.id)


@pytest.mark.asyncio
async def test_create_person_preserves_name_and_email():
    """Test that person creation preserves name and email."""
    service = PersonServiceImpl()
    data = PersonCreate(name="Jane Smith", email="jane@example.com")
    
    result = await service.create_person(data)
    
    assert result.name == "Jane Smith"
    assert result.email == "jane@example.com"


@pytest.mark.asyncio
async def test_create_person_returns_person_model():
    """Test that create_person returns a Person model."""
    service = PersonServiceImpl()
    data = PersonCreate(name="Test User", email="test@example.com")
    
    result = await service.create_person(data)
    
    assert isinstance(result, Person)
    assert result.id is not None
    assert result.name == "Test User"
    assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_create_person_with_optional_fields():
    """Test that person creation works with optional fields."""
    service = PersonServiceImpl()
    data = PersonCreate(name=None, email=None)
    
    result = await service.create_person(data)
    
    assert isinstance(result, Person)
    assert result.id is not None
    assert result.name is None
    assert result.email is None


@pytest.mark.asyncio
async def test_create_person_generates_unique_ids():
    """Test that each person creation generates a unique ID."""
    service = PersonServiceImpl()
    data = PersonCreate(name="User", email="user@example.com")
    
    result1 = await service.create_person(data)
    result2 = await service.create_person(data)
    
    assert result1.id != result2.id


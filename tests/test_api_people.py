"""Tests for the People API endpoints."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.database import Base
from app.dependencies import get_db_session


# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db():
    """Override database dependency for testing."""
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session):
    """Create a test client with database override."""
    app.dependency_overrides[get_db_session] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_person_success(client: AsyncClient):
    """Test creating a person successfully."""
    person_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-01"
    }
    
    response = await client.post("/api/v1/parties/people/", json=person_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john.doe@example.com"
    assert data["phone"] == "+1234567890"
    assert data["is_active"] is True
    assert "id" in data
    assert "party" in data
    assert data["party"]["party_type"] == "person"
    assert data["party"]["status"] == "active"
    assert data["party"]["display_name"] == "John Doe"


@pytest.mark.asyncio
async def test_create_person_minimal_fields(client: AsyncClient):
    """Test creating a person with only required fields."""
    person_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com"
    }
    
    response = await client.post("/api/v1/parties/people/", json=person_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"
    assert data["email"] == "jane.smith@example.com"
    assert data["phone"] is None
    assert data["date_of_birth"] is None


@pytest.mark.asyncio
async def test_create_person_duplicate_email(client: AsyncClient):
    """Test that creating a person with duplicate email returns 409."""
    person_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "duplicate@example.com"
    }
    
    # Create first person
    response1 = await client.post("/api/v1/parties/people/", json=person_data)
    assert response1.status_code == 201
    
    # Try to create second person with same email
    response2 = await client.post("/api/v1/parties/people/", json=person_data)
    assert response2.status_code == 409
    error_data = response2.json()
    assert error_data["error"] == "DuplicateEmail"
    assert "Email already exists" in error_data["message"]


@pytest.mark.asyncio
async def test_create_person_validation_error(client: AsyncClient):
    """Test that invalid data returns validation error."""
    person_data = {
        "first_name": "",  # Empty first name
        "last_name": "Doe",
        "email": "invalid-email"  # Invalid email format
    }
    
    response = await client.post("/api/v1/parties/people/", json=person_data)
    assert response.status_code == 422
    error_data = response.json()
    assert error_data["error"] == "ValidationError"


@pytest.mark.asyncio
async def test_get_person_success(client: AsyncClient):
    """Test getting a person by ID."""
    # Create a person first
    person_data = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice@example.com"
    }
    create_response = await client.post("/api/v1/parties/people/", json=person_data)
    assert create_response.status_code == 201
    person_id = create_response.json()["id"]
    
    # Get the person
    response = await client.get(f"/api/v1/parties/people/{person_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == person_id
    assert data["first_name"] == "Alice"
    assert data["last_name"] == "Johnson"
    assert data["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_get_person_not_found(client: AsyncClient):
    """Test getting a non-existent person returns 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/api/v1/parties/people/{fake_id}")
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "NotFound"
    assert "Person not found" in error_data["message"]


@pytest.mark.asyncio
async def test_update_person_success(client: AsyncClient):
    """Test updating a person successfully."""
    # Create a person first
    person_data = {
        "first_name": "Bob",
        "last_name": "Williams",
        "email": "bob@example.com"
    }
    create_response = await client.post("/api/v1/parties/people/", json=person_data)
    person_id = create_response.json()["id"]
    
    # Update the person
    update_data = {
        "first_name": "Robert",
        "phone": "+9876543210"
    }
    response = await client.patch(f"/api/v1/parties/people/{person_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Robert"
    assert data["last_name"] == "Williams"  # Unchanged
    assert data["phone"] == "+9876543210"
    assert data["party"]["display_name"] == "Robert Williams"  # Display name updated


@pytest.mark.asyncio
async def test_update_person_not_found(client: AsyncClient):
    """Test updating a non-existent person returns 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    update_data = {"first_name": "Updated"}
    response = await client.patch(f"/api/v1/parties/people/{fake_id}", json=update_data)
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "NotFound"


@pytest.mark.asyncio
async def test_update_person_duplicate_email(client: AsyncClient):
    """Test that updating to a duplicate email returns 400."""
    # Create two people
    person1_data = {
        "first_name": "Person",
        "last_name": "One",
        "email": "person1@example.com"
    }
    person2_data = {
        "first_name": "Person",
        "last_name": "Two",
        "email": "person2@example.com"
    }
    create1 = await client.post("/api/v1/parties/people/", json=person1_data)
    create2 = await client.post("/api/v1/parties/people/", json=person2_data)
    person2_id = create2.json()["id"]
    
    # Try to update person2 with person1's email
    update_data = {"email": "person1@example.com"}
    response = await client.patch(f"/api/v1/parties/people/{person2_id}", json=update_data)
    assert response.status_code == 400
    error_data = response.json()
    assert error_data["error"] == "ValidationError"
    assert "Email already exists" in error_data["message"]


@pytest.mark.asyncio
async def test_delete_person_success(client: AsyncClient):
    """Test soft deleting a person successfully."""
    # Create a person first
    person_data = {
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie@example.com"
    }
    create_response = await client.post("/api/v1/parties/people/", json=person_data)
    person_id = create_response.json()["id"]
    
    # Delete the person
    response = await client.delete(f"/api/v1/parties/people/{person_id}")
    assert response.status_code == 204
    
    # Verify person is soft deleted (cannot be retrieved)
    get_response = await client.get(f"/api/v1/parties/people/{person_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_person_not_found(client: AsyncClient):
    """Test deleting a non-existent person returns 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.delete(f"/api/v1/parties/people/{fake_id}")
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["error"] == "NotFound"


@pytest.mark.asyncio
async def test_create_person_updates_party_display_name(client: AsyncClient):
    """Test that party display_name is correctly set from first and last name."""
    person_data = {
        "first_name": "Mary",
        "last_name": "Jane",
        "email": "mary.jane@example.com"
    }
    response = await client.post("/api/v1/parties/people/", json=person_data)
    assert response.status_code == 201
    data = response.json()
    assert data["party"]["display_name"] == "Mary Jane"


@pytest.mark.asyncio
async def test_update_person_name_updates_party_display_name(client: AsyncClient):
    """Test that updating first or last name updates party display_name."""
    # Create person
    person_data = {
        "first_name": "Initial",
        "last_name": "Name",
        "email": "initial@example.com"
    }
    create_response = await client.post("/api/v1/parties/people/", json=person_data)
    person_id = create_response.json()["id"]
    assert create_response.json()["party"]["display_name"] == "Initial Name"
    
    # Update first name
    update_response = await client.patch(
        f"/api/v1/parties/people/{person_id}",
        json={"first_name": "Updated"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["party"]["display_name"] == "Updated Name"
    
    # Update last name
    update_response2 = await client.patch(
        f"/api/v1/parties/people/{person_id}",
        json={"last_name": "Surname"}
    )
    assert update_response2.status_code == 200
    assert update_response2.json()["party"]["display_name"] == "Updated Surname"


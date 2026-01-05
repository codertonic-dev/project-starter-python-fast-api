from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List
from app.services.person_service import PersonService
from app.models.database import PersonCreate, PersonUpdate, PersonResponse
from app.models.errors import ErrorResponse
from app.dependencies import get_db_session

router = APIRouter(prefix="/parties/people", tags=["People"])


@router.get("/", response_model=List[PersonResponse])
async def list_people(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    List all active people.
    
    Returns a paginated list of all active people with their associated party details.
    """
    service = PersonService(db)
    return await service.list_people(skip=skip, limit=limit)


@router.post("/", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
async def create_person(
    person_data: PersonCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Create a new person.
    
    This endpoint creates both a Party record (with party_type='person') 
    and a linked Person record. The party's display_name is automatically 
    set to "FirstName LastName".
    
    Duplicate emails will be rejected with a 409 Conflict error.
    """
    service = PersonService(db)
    try:
        return await service.create_person(person_data)
    except ValueError as e:
        error_response = ErrorResponse(
            error="DuplicateEmail",
            message=str(e),
            status_code=status.HTTP_409_CONFLICT
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_response.model_dump()
        )
    except IntegrityError as e:
        error_response = ErrorResponse(
            error="DatabaseError",
            message="Database integrity constraint violated",
            status_code=status.HTTP_409_CONFLICT
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_response.model_dump()
        )

@router.get("/{person_id}", response_model=PersonResponse)
async def get_person(
    person_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get a person by ID.
    
    Returns the person record along with associated party details.
    Only active persons are returned.
    """
    service = PersonService(db)
    person = await service.get_person(person_id)
    if not person:
        error_response = ErrorResponse(
            error="NotFound",
            message="Person not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.model_dump()
        )
    return person


@router.patch("/{person_id}", response_model=PersonResponse)
async def update_person(
    person_id: str,
    update_data: PersonUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Update a person (partial update).
    
    Supports partial updates. Only provided fields will be updated.
    The party_id cannot be changed. If first_name or last_name 
    are updated, the party's display_name is automatically updated.
    """
    service = PersonService(db)
    try:
        person = await service.update_person(person_id, update_data)
        if not person:
            error_response = ErrorResponse(
                error="NotFound",
                message="Person not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response.model_dump()
            )
        return person
    except ValueError as e:
        error_response = ErrorResponse(
            error="ValidationError",
            message=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump()
        )


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(
    person_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Delete a person (soft delete).
    
    Performs a soft delete:
    - Person.is_active is set to False
    - Party.status is set to 'archived'
    - Records remain in the database for audit/compliance purposes
    """
    service = PersonService(db)
    deleted = await service.delete_person(person_id)
    if not deleted:
        error_response = ErrorResponse(
            error="NotFound",
            message="Person not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.model_dump()
        )

from fastapi import APIRouter, Depends
from app.models import PersonCreate, Person
from app.services.base import PersonService
from app.services.persons_impl import PersonServiceImpl

router = APIRouter()

def get_person_service() -> PersonService:
    return PersonServiceImpl()

@router.post(
    "/persons",
    response_model=Person,
    status_code=201,
)
async def create_person_endpoint(
    data: PersonCreate,
    service: PersonService = Depends(get_person_service),
) -> Person:
    return await service.create_person(data)

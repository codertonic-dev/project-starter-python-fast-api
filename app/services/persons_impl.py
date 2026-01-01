import uuid
from app.models import PersonCreate, Person
from app.services.person_service import PersonService

class PersonServiceImpl(PersonService):
    async def create_person(self, data: PersonCreate) -> Person:
        return Person(id=str(uuid.uuid4()), **data.model_dump())

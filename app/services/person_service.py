from abc import ABC, abstractmethod
from app.models import PersonCreate, Person

class PersonService(ABC):
    @abstractmethod
    async def create_person(self, data: PersonCreate) -> Person:
        """Create a new person entity."""
        raise NotImplementedError


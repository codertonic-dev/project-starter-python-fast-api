from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models.database import Party, Person, PersonCreate, PersonUpdate, PersonResponse, PartyOut

class PersonService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_person(self, person_data: PersonCreate) -> PersonResponse:
        # Check email uniqueness
        email_stmt = select(Person).where(Person.email == str(person_data.email))
        result = await self.db.execute(email_stmt)
        if result.scalar_one_or_none():
            raise ValueError("Email already exists")
        
        # Create Party
        party = Party(
            display_name=f"{person_data.first_name} {person_data.last_name}",
            party_type="person",
            status="active"
        )
        self.db.add(party)
        await self.db.flush()
        
        # Create Person (linked)
        person = Person(
            party_id=party.id,
            first_name=person_data.first_name,
            last_name=person_data.last_name,
            date_of_birth=person_data.date_of_birth,
            email=str(person_data.email),
            phone=person_data.phone
        )
        self.db.add(person)
        await self.db.commit()
        await self.db.refresh(person)
        await self.db.refresh(party)
        
        return PersonResponse(
            id=person.id,
            party=PartyOut.model_validate(party),
            first_name=person.first_name,
            last_name=person.last_name,
            date_of_birth=person.date_of_birth,
            email=person.email,
            phone=person.phone,
            is_active=person.is_active
        )
    
    async def get_person(self, person_id: str) -> Optional[PersonResponse]:
        stmt = select(Person).where(Person.id == person_id, Person.is_active == True)
        result = await self.db.execute(stmt)
        person = result.scalar_one_or_none()
        if person and person.party:
            return PersonResponse(
                id=person.id,
                party=PartyOut.model_validate(person.party),
                first_name=person.first_name,
                last_name=person.last_name,
                date_of_birth=person.date_of_birth,
                email=person.email,
                phone=person.phone,
                is_active=person.is_active
            )
        return None
    
    async def update_person(self, person_id: str, update_data: PersonUpdate) -> Optional[PersonResponse]:
        # Ensure party_id cannot be updated (explicitly exclude it)
        data = update_data.model_dump(exclude_unset=True, exclude_none=True)
        data.pop('party_id', None)  # Explicitly prevent party_id updates
        
        if not data:
            return await self.get_person(person_id)
        
        # Check if email is being updated and if it already exists
        if 'email' in data:
            email_stmt = select(Person).where(
                Person.email == str(data['email']),
                Person.id != person_id
            )
            result = await self.db.execute(email_stmt)
            if result.scalar_one_or_none():
                raise ValueError("Email already exists")
        
        # Get person first to check if it exists and is active
        person_stmt = select(Person).where(Person.id == person_id, Person.is_active == True)
        result = await self.db.execute(person_stmt)
        person = result.scalar_one_or_none()
        
        if not person:
            return None
        
        # Update person
        update_stmt = update(Person).where(Person.id == person_id, Person.is_active == True).values(**data)
        await self.db.execute(update_stmt)
        await self.db.commit()
        
        # Refresh person to get updated values
        await self.db.refresh(person)
        
        # Update party display_name if names changed
        if 'first_name' in data or 'last_name' in data:
            # Re-fetch to get updated names
            person_stmt = select(Person).where(Person.id == person_id)
            result = await self.db.execute(person_stmt)
            person = result.scalar_one_or_none()
            if person and person.party:
                person.party.display_name = f"{person.first_name} {person.last_name}"
                await self.db.commit()
        
        return await self.get_person(person_id)
    
    async def delete_person(self, person_id: str) -> bool:
        # Get person first to get party_id
        person_stmt = select(Person).where(Person.id == person_id)
        result = await self.db.execute(person_stmt)
        person = result.scalar_one_or_none()
        
        if not person:
            return False
        
        # Soft delete person
        update_person_stmt = update(Person).where(Person.id == person_id).values(is_active=False)
        result = await self.db.execute(update_person_stmt)
        
        # Soft delete party
        if person.party_id:
            party_stmt = update(Party).where(Party.id == person.party_id).values(status="archived")
            await self.db.execute(party_stmt)
        
        await self.db.commit()
        return result.rowcount > 0

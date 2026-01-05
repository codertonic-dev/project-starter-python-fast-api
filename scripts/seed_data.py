"""Script to seed the database with sample data."""
import asyncio
import sys
from pathlib import Path
from datetime import date
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import AsyncSessionLocal
from app.services.person_service import PersonService
from app.models.database import PersonCreate


async def seed_data():
    """Seed the database with sample people and party data."""
    async with AsyncSessionLocal() as session:
        service = PersonService(session)
        
        # Sample people data
        sample_people = [
            PersonCreate(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone="+1-555-0101",
                date_of_birth=date(1990, 5, 15)
            ),
            PersonCreate(
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                phone="+1-555-0102",
                date_of_birth=date(1985, 8, 22)
            ),
            PersonCreate(
                first_name="Michael",
                last_name="Johnson",
                email="michael.johnson@example.com",
                phone="+1-555-0103",
                date_of_birth=date(1992, 3, 10)
            ),
            PersonCreate(
                first_name="Emily",
                last_name="Williams",
                email="emily.williams@example.com",
                phone="+1-555-0104",
                date_of_birth=date(1988, 11, 30)
            ),
            PersonCreate(
                first_name="David",
                last_name="Brown",
                email="david.brown@example.com",
                phone="+1-555-0105",
                date_of_birth=date(1995, 7, 4)
            ),
            PersonCreate(
                first_name="Sarah",
                last_name="Davis",
                email="sarah.davis@example.com",
                phone="+1-555-0106",
                date_of_birth=date(1991, 12, 18)
            ),
            PersonCreate(
                first_name="Robert",
                last_name="Miller",
                email="robert.miller@example.com",
                phone="+1-555-0107",
                date_of_birth=date(1987, 2, 25)
            ),
            PersonCreate(
                first_name="Lisa",
                last_name="Wilson",
                email="lisa.wilson@example.com",
                phone="+1-555-0108",
                date_of_birth=date(1993, 9, 12)
            ),
            PersonCreate(
                first_name="James",
                last_name="Moore",
                email="james.moore@example.com",
                phone="+1-555-0109",
                date_of_birth=date(1989, 6, 8)
            ),
            PersonCreate(
                first_name="Patricia",
                last_name="Taylor",
                email="patricia.taylor@example.com",
                phone="+1-555-0110",
                date_of_birth=date(1994, 1, 20)
            ),
        ]
        
        print("Seeding database with sample data...")
        created_count = 0
        skipped_count = 0
        
        for person_data in sample_people:
            try:
                person = await service.create_person(person_data)
                created_count += 1
                print(f"[OK] Created: {person.first_name} {person.last_name} ({person.email})")
            except ValueError as e:
                if "Email already exists" in str(e):
                    skipped_count += 1
                    print(f"[SKIP] Skipped: {person_data.email} (already exists)")
                else:
                    print(f"[ERROR] Error creating {person_data.email}: {e}")
            except Exception as e:
                print(f"[ERROR] Unexpected error creating {person_data.email}: {e}")
        
        print(f"\n[SUCCESS] Seeding complete!")
        print(f"   Created: {created_count} people")
        print(f"   Skipped: {skipped_count} people (already exist)")


if __name__ == "__main__":
    asyncio.run(seed_data())


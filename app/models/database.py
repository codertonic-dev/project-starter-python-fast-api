from sqlalchemy import Column, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date, datetime
import uuid

Base = declarative_base()

class Party(Base):
    __tablename__ = "parties"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    party_type = Column(String, default="person", nullable=False)
    display_name = Column(String, nullable=False)
    status = Column(String, default="active")  # active, archived
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    person = relationship("Person", back_populates="party", uselist=False)

class Person(Base):
    __tablename__ = "people"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    party_id = Column(String, ForeignKey("parties.id"), unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    party = relationship("Party", back_populates="person")

# Pydantic schemas (will be generated + extended)
class PersonCreate(BaseModel):
    first_name: str = Field(..., min_length=1, description="First name is required")
    last_name: str = Field(..., min_length=1, description="Last name is required")
    date_of_birth: Optional[date] = Field(None, description="Date of birth (optional)")
    email: EmailStr = Field(..., description="Valid email address")
    phone: Optional[str] = Field(None, description="Phone number (optional)")
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class PersonUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, description="Last name")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    email: Optional[EmailStr] = Field(None, description="Valid email address")
    phone: Optional[str] = Field(None, description="Phone number")
    # Note: party_id is intentionally excluded - it cannot be updated
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError('Name cannot be empty')
        return v.strip() if v else None

class PartyOut(BaseModel):
    id: str
    party_type: str
    display_name: str
    status: str

class PersonResponse(BaseModel):
    id: str
    party: PartyOut
    first_name: str
    last_name: str
    date_of_birth: Optional[date]
    email: str
    phone: Optional[str]
    is_active: bool

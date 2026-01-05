"""Database configuration and session management."""
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.models.database import Base

# Load environment variables from .env file
# Try multiple paths to find .env file
project_root = Path(__file__).parent.parent.resolve()
env_path = project_root / ".env"
# Load from project root first, then try current directory as fallback
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)
else:
    load_dotenv(override=False)  # Try loading from current directory as fallback

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please set it in a .env file or as an environment variable. "
        "Example: postgresql+asyncpg://postgres:Shrutika2210@localhost:5432/onboarding_db"
    )

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DB_ECHO", "false").lower() == "true",  # Set via environment variable
    future=True,
    pool_pre_ping=True,  # Verify connections before using them
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


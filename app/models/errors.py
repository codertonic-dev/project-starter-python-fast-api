"""Error response models for consistent API error handling."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ErrorDetail(BaseModel):
    """Detail about a specific error."""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    status_code: int


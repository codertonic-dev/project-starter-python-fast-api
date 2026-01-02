from fastapi import APIRouter, Depends
from typing import Dict
from app.services.health_service import HealthService
from app.services.health_impl import HealthServiceImpl

router = APIRouter()

def get_health_service() -> HealthService:
    return HealthServiceImpl()

@router.get(
    "/health",
    response_model=Dict[str, str],
    status_code=200,
)
async def health_check_endpoint(
    service: HealthService = Depends(get_health_service),
) -> Dict[str, str]:
    return await service.check_health()


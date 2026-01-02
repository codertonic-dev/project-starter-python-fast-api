from typing import Dict
from app.services.health_service import HealthService

class HealthServiceImpl(HealthService):
    async def check_health(self) -> Dict[str, str]:
        return {"status": "ok"}


from abc import ABC, abstractmethod
from typing import Dict

class HealthService(ABC):
    @abstractmethod
    async def check_health(self) -> Dict[str, str]:
        """Check the health status of the service."""
        raise NotImplementedError


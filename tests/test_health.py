import pytest
from app.services.health_impl import HealthServiceImpl


@pytest.mark.asyncio
async def test_check_health_returns_ok_status():
    """Test that health check returns correct status."""
    service = HealthServiceImpl()
    result = await service.check_health()
    
    assert result == {"status": "ok"}
    assert isinstance(result, dict)
    assert "status" in result
    assert result["status"] == "ok"


@pytest.mark.asyncio
async def test_check_health_returns_dict():
    """Test that health check returns a dictionary."""
    service = HealthServiceImpl()
    result = await service.check_health()
    
    assert isinstance(result, dict)
    assert len(result) == 1


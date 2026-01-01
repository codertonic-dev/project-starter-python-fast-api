from fastapi import FastAPI
from app.api.persons import router as persons_router
from app.api.health import router as health_router

app = FastAPI(title="Contract First API")

app.include_router(persons_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")

from fastapi import FastAPI
from app.api.persons import router as persons_router

app = FastAPI(title="Contract First API")

app.include_router(persons_router, prefix="/api/v1")

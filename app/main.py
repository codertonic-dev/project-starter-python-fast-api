from fastapi import FastAPI
from generated.api.default import api_router  # Generated router
from app.api.impl.health import health_impl  # Custom logic

app = FastAPI(title="Service API", openapi_url="/openapi.json")

# Include generated routers
app.include_router(api_router, prefix="/api/v1")

# Override generated health handler with impl
@app.get("/api/v1/health")
async def health_check():
    return health_impl()

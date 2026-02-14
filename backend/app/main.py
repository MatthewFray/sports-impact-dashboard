from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.teams import router as teams_router

app = FastAPI(title="Sport Impact Dashboard API")

app.include_router(health_router)
app.include_router(teams_router, prefix="/api")

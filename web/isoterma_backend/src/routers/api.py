from fastapi import APIRouter

from src.routers import weather_routes, health_routes, farm_routes

router = APIRouter(prefix="/api/v1")

# Include all route modules
router.include_router(weather_routes.router)
router.include_router(health_routes.router)
router.include_router(farm_routes.router)
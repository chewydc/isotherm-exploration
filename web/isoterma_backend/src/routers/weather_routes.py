from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging

from src.models.weather_models import (
    WeatherRequest,
    WeatherResponse,
    ValidationRequest,
    ValidationResponse
)
from src.services.weather_service import WeatherService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/current")
async def get_current_weather(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude")
):
    """Get current weather for given coordinates"""
    try:
        data = await WeatherService.get_current_weather(latitude, longitude)
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_current_weather: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forecast")
async def get_forecast(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude"),
    forecast_days: int = Query(3, ge=1, le=7, description="Forecast days")
):
    """Get weather forecast for given coordinates"""
    try:
        data = await WeatherService.get_forecast(latitude, longitude, forecast_days)
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_forecast: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate")
async def validate_sensor(request: ValidationRequest):
    """Validate sensor reading against API data"""
    try:
        result = await WeatherService.validate_sensor(
            request.latitude,
            request.longitude,
            request.measured_temperature
        )
        
        return {
            "success": True,
            "sensor_id": request.sensor_id,
            "validation": result
        }
    except Exception as e:
        logger.error(f"Error in validate_sensor: {e}")
        raise HTTPException(status_code=500, detail=str(e))
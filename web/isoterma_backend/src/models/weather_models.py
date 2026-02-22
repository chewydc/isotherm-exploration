from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class WeatherRequest(BaseModel):
    """Request model for weather queries"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    forecast_days: Optional[int] = Field(3, ge=1, le=7, description="Forecast days")

class CurrentWeather(BaseModel):
    """Current weather data"""
    time: str
    temperature_2m: float
    relative_humidity_2m: int
    apparent_temperature: float
    precipitation: float
    rain: float
    cloud_cover: int
    pressure_msl: float
    wind_speed_10m: float
    wind_direction_10m: int
    wind_gusts_10m: float

class HourlyForecast(BaseModel):
    """Hourly forecast data"""
    time: List[str]
    temperature_2m: List[float]
    relative_humidity_2m: List[int]
    precipitation_probability: List[int]
    precipitation: List[float]
    wind_speed_10m: List[float]

class WeatherResponse(BaseModel):
    """Complete weather response"""
    latitude: float
    longitude: float
    timezone: str
    elevation: float
    current: CurrentWeather
    hourly: HourlyForecast

class ValidationRequest(BaseModel):
    """Request for sensor validation"""
    latitude: float
    longitude: float
    measured_temperature: float
    sensor_id: Optional[str] = None

class ValidationResponse(BaseModel):
    """Sensor validation response"""
    sensor_id: Optional[str]
    measured_temperature: float
    api_temperature: float
    difference: float
    status: str  # "OK", "WARNING", "ERROR"
    message: str
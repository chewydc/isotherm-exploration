import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for weather API interactions"""
    
    OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
    
    @staticmethod
    async def get_current_weather(latitude: float, longitude: float) -> Dict[str, Any]:
        """Get current weather from Open-Meteo API"""
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current': [
                    'temperature_2m',
                    'relative_humidity_2m',
                    'apparent_temperature',
                    'precipitation',
                    'rain',
                    'cloud_cover',
                    'pressure_msl',
                    'wind_speed_10m',
                    'wind_direction_10m',
                    'wind_gusts_10m'
                ],
                'timezone': 'America/Argentina/Buenos_Aires'
            }
            
            response = requests.get(
                WeatherService.OPEN_METEO_URL,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Weather data fetched for ({latitude}, {longitude})")
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            raise
    
    @staticmethod
    async def get_forecast(latitude: float, longitude: float, forecast_days: int = 3) -> Dict[str, Any]:
        """Get weather forecast from Open-Meteo API"""
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current': [
                    'temperature_2m',
                    'relative_humidity_2m',
                    'apparent_temperature',
                    'precipitation',
                    'rain',
                    'cloud_cover',
                    'pressure_msl',
                    'wind_speed_10m',
                    'wind_direction_10m',
                    'wind_gusts_10m'
                ],
                'hourly': [
                    'temperature_2m',
                    'relative_humidity_2m',
                    'precipitation_probability',
                    'precipitation',
                    'wind_speed_10m'
                ],
                'forecast_days': forecast_days,
                'timezone': 'America/Argentina/Buenos_Aires'
            }
            
            response = requests.get(
                WeatherService.OPEN_METEO_URL,
                params=params,
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Forecast data fetched for ({latitude}, {longitude}) - {forecast_days} days")
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching forecast data: {e}")
            raise
    
    @staticmethod
    async def validate_sensor(latitude: float, longitude: float, measured_temp: float) -> Dict[str, Any]:
        """Validate sensor reading against API data"""
        try:
            weather_data = await WeatherService.get_current_weather(latitude, longitude)
            api_temp = weather_data['current']['temperature_2m']
            difference = abs(api_temp - measured_temp)
            
            # Determine status
            if difference < 2:
                status = "OK"
                message = "Sensor calibrated correctly"
            elif difference < 5:
                status = "WARNING"
                message = "Review sensor calibration"
            else:
                status = "ERROR"
                message = "Sensor requires attention - significant deviation"
            
            return {
                'measured_temperature': measured_temp,
                'api_temperature': api_temp,
                'difference': round(difference, 2),
                'status': status,
                'message': message
            }
            
        except Exception as e:
            logger.error(f"Error validating sensor: {e}")
            raise
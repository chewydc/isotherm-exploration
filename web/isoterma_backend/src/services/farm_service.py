import json
import logging
from typing import List, Optional
from pathlib import Path

from src.models.farm_models import Farm

logger = logging.getLogger(__name__)

class FarmService:
    """Service for farm data management"""
    
    DATA_FILE = Path(__file__).parent.parent.parent / "data" / "fincas.json"
    
    @staticmethod
    def get_all_farms() -> List[Farm]:
        """Get all farms from JSON file"""
        try:
            with open(FarmService.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            farms = [Farm(**farm_data) for farm_data in data]
            logger.info(f"Loaded {len(farms)} farms")
            return farms
            
        except FileNotFoundError:
            logger.error(f"Farms data file not found: {FarmService.DATA_FILE}")
            return []
        except Exception as e:
            logger.error(f"Error loading farms: {e}")
            return []
    
    @staticmethod
    def get_farm_by_id(farm_id: str) -> Optional[dict]:
        """Get specific farm by ID"""
        try:
            with open(FarmService.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for farm in data:
                if farm["id"] == farm_id:
                    logger.info(f"Found farm: {farm['name']}")
                    return farm
            
            logger.warning(f"Farm not found: {farm_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error loading farm: {e}")
            return None
    
    @staticmethod
    def update_farm_settings(farm_id: str, settings: dict) -> dict:
        """Update farm settings"""
        try:
            with open(FarmService.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for farm in data:
                if farm["id"] == farm_id:
                    if "settings" not in farm:
                        farm["settings"] = {}
                    farm["settings"].update(settings)
                    
                    with open(FarmService.DATA_FILE, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    logger.info(f"Updated settings for farm {farm_id}")
                    return farm["settings"]
            
            raise ValueError(f"Farm not found: {farm_id}")
            
        except Exception as e:
            logger.error(f"Error updating farm settings: {e}")
            raise
    
    @staticmethod
    def check_temperature_alerts(farm_id: str) -> List[dict]:
        """Check for temperature alerts based on thresholds"""
        try:
            with open(FarmService.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            farm = next((f for f in data if f["id"] == farm_id), None)
            if not farm:
                raise ValueError(f"Farm not found: {farm_id}")
            
            settings = farm.get("settings", {})
            if not settings.get("alerts_enabled", False):
                return []
            
            min_temp = settings.get("temperature_threshold_min", 0)
            max_temp = settings.get("temperature_threshold_max", 50)
            
            alerts = []
            
            # Alertas de sensores actuales
            for sensor in farm.get("sensors", []):
                temp = sensor.get("temperature", 0)
                sensor_id = sensor.get("id", "unknown")
                
                if temp < min_temp:
                    alerts.append({
                        "type": "temperature_low",
                        "sensor_id": sensor_id,
                        "temperature": temp,
                        "threshold": min_temp,
                        "message": f"Temperatura baja detectada: {temp}°C (mín: {min_temp}°C)",
                        "severity": "warning",
                        "alert_type": "current"
                    })
                elif temp > max_temp:
                    alerts.append({
                        "type": "temperature_high",
                        "sensor_id": sensor_id,
                        "temperature": temp,
                        "threshold": max_temp,
                        "message": f"Temperatura alta detectada: {temp}°C (máx: {max_temp}°C)",
                        "severity": "warning",
                        "alert_type": "current"
                    })
            
            # Alertas de pronóstico
            forecast_alerts = FarmService._check_forecast_alerts(farm, min_temp, max_temp)
            alerts.extend(forecast_alerts)
            
            logger.info(f"Found {len(alerts)} alerts for farm {farm_id}")
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
            raise
    
    @staticmethod
    def _check_forecast_alerts(farm: dict, min_temp: float, max_temp: float) -> List[dict]:
        """Check forecast for temperature alerts"""
        try:
            from src.services.weather_service import WeatherService
            import asyncio
            
            # Obtener pronóstico
            lat = farm["location"]["latitude"]
            lon = farm["location"]["longitude"]
            
            # Ejecutar función async en contexto sync
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            forecast_data = loop.run_until_complete(
                WeatherService.get_forecast(lat, lon, 3)
            )
            loop.close()
            
            alerts = []
            hourly = forecast_data.get("hourly", {})
            times = hourly.get("time", [])
            temperatures = hourly.get("temperature_2m", [])
            
            # Revisar próximas 24 horas
            for i in range(min(24, len(temperatures))):
                temp = temperatures[i]
                time_str = times[i] if i < len(times) else "unknown"
                
                if temp < min_temp:
                    alerts.append({
                        "type": "forecast_temperature_low",
                        "sensor_id": "forecast",
                        "temperature": temp,
                        "threshold": min_temp,
                        "time": time_str,
                        "message": f"Pronóstico: {temp}°C a las {time_str[-5:]} (mín: {min_temp}°C)",
                        "severity": "info",
                        "alert_type": "forecast"
                    })
                elif temp > max_temp:
                    alerts.append({
                        "type": "forecast_temperature_high",
                        "sensor_id": "forecast",
                        "temperature": temp,
                        "threshold": max_temp,
                        "time": time_str,
                        "message": f"Pronóstico: {temp}°C a las {time_str[-5:]} (máx: {max_temp}°C)",
                        "severity": "info",
                        "alert_type": "forecast"
                    })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking forecast alerts: {e}")
            return []
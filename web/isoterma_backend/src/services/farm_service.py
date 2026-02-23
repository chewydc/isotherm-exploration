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
                if temp > max_temp:
                    alerts.append({
                        "type": "temperature_high",
                        "sensor_id": sensor_id,
                        "temperature": temp,
                        "threshold": max_temp,
                        "message": f"Temperatura alta detectada: {temp}°C (máx: {max_temp}°C)",
                        "severity": "warning",
                        "alert_type": "current"
                    })
            
            # Alertas de clima actual (API meteorológica)
            weather_alerts = FarmService._check_current_weather_alerts(farm, min_temp, max_temp)
            alerts.extend(weather_alerts)
            
            # Alertas de pronóstico
            forecast_alerts = FarmService._check_forecast_alerts(farm, min_temp, max_temp, settings)
            alerts.extend(forecast_alerts)
            
            logger.info(f"Found {len(alerts)} alerts for farm {farm_id}")
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
            raise
    
    @staticmethod
    def _check_forecast_alerts(farm: dict, min_temp: float, max_temp: float, settings: dict) -> List[dict]:
        """Check forecast for temperature alerts"""
        try:
            import requests
            
            # Obtener pronóstico directamente con requests
            lat = farm["location"]["latitude"]
            lon = farm["location"]["longitude"]
            
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'hourly': 'temperature_2m',
                'forecast_days': 3,
                'timezone': 'America/Argentina/Buenos_Aires'
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            forecast_data = response.json()
            
            alerts = []
            hourly = forecast_data.get("hourly", {})
            times = hourly.get("time", [])
            temperatures = hourly.get("temperature_2m", [])
            
            # Revisar próximas horas según configuración (por defecto 24h)
            forecast_hours = settings.get("forecast_alert_hours", 24)
            
            from datetime import datetime, timezone, timedelta
            
            # Obtener hora actual en Argentina (UTC-3)
            argentina_offset = timezone(timedelta(hours=-3))
            now = datetime.now(argentina_offset)
            
            for i in range(min(forecast_hours, len(temperatures))):
                temp = temperatures[i]
                time_str = times[i] if i < len(times) else "unknown"
                
                # Verificar que la hora sea futura
                try:
                    # Parsear como hora local de Argentina
                    dt_naive = datetime.fromisoformat(time_str)
                    dt = dt_naive.replace(tzinfo=argentina_offset)
                    
                    # Solo procesar si es una hora futura
                    if dt <= now:
                        continue
                        
                except Exception as e:
                    logger.error(f"Error parsing time {time_str}: {e}")
                    continue
                
                # Formatear fecha y hora más descriptiva
                try:
                    # Determinar si es hoy, mañana o pasado mañana
                    days_diff = (dt.date() - now.date()).days
                    if days_diff == 0:
                        day_label = "Hoy"
                    elif days_diff == 1:
                        day_label = "Mañana"
                    elif days_diff == 2:
                        day_label = "Pasado mañana"
                    else:
                        day_label = dt.strftime("%d/%m")
                    
                    time_label = dt.strftime("%H:%M")
                    full_time_label = f"{day_label} {time_label}"
                except Exception as e:
                    logger.error(f"Error formatting time: {e}")
                    full_time_label = time_str[-5:] if len(time_str) >= 5 else time_str
                
                if temp < min_temp:
                    alerts.append({
                        "type": "forecast_temperature_low",
                        "sensor_id": "forecast",
                        "temperature": temp,
                        "threshold": min_temp,
                        "time": time_str,
                        "message": f"Pronóstico: {temp}°C para {full_time_label} (mín: {min_temp}°C)",
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
                        "message": f"Pronóstico: {temp}°C para {full_time_label} (máx: {max_temp}°C)",
                        "severity": "info",
                        "alert_type": "forecast"
                    })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking forecast alerts: {e}")
            return []
    
    @staticmethod
    def _check_current_weather_alerts(farm: dict, min_temp: float, max_temp: float) -> List[dict]:
        """Check current weather API for temperature alerts"""
        try:
            import requests
            
            # Obtener clima actual directamente con requests
            lat = farm["location"]["latitude"]
            lon = farm["location"]["longitude"]
            
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m',
                'timezone': 'America/Argentina/Buenos_Aires'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            weather_data = response.json()
            
            alerts = []
            current = weather_data.get("current", {})
            temp = current.get("temperature_2m", 0)
            
            logger.info(f"Weather check: temp={temp}, min={min_temp}, max={max_temp}")
            
            if temp < min_temp:
                alerts.append({
                    "type": "weather_temperature_low",
                    "sensor_id": "weather_api",
                    "temperature": temp,
                    "threshold": min_temp,
                    "message": f"Clima actual: {temp}°C (mín: {min_temp}°C)",
                    "severity": "warning",
                    "alert_type": "weather"
                })
            if temp > max_temp:
                alerts.append({
                    "type": "weather_temperature_high",
                    "sensor_id": "weather_api",
                    "temperature": temp,
                    "threshold": max_temp,
                    "message": f"Clima actual: {temp}°C (máx: {max_temp}°C)",
                    "severity": "warning",
                    "alert_type": "weather"
                })
            
            logger.info(f"Weather alerts generated: {len(alerts)}")
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking weather alerts: {e}")
            return []
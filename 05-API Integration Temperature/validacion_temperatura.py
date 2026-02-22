import requests
import json
from datetime import datetime

print("=== VALIDACION DE TEMPERATURA - API vs MEDICION ===\n")

# PUNTO DE PRUEBA
lat = -39.164
lon = -67.035
temp_medida = 18.0  # Temperatura hardcodeada/medida

print(f"Coordenada: ({lat}, {lon})")
print(f"Temperatura MEDIDA: {temp_medida}°C")
print("-" * 60)

# ============================================
# 1. OPEN-METEO API (Gratuita, sin API key)
# ============================================
print("\n1. CONSULTANDO OPEN-METEO API...")
try:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m',
        'hourly': 'temperature_2m',
        'forecast_days': 3,
        'timezone': 'America/Argentina/Buenos_Aires'
    }
    
    response = requests.get(url, params=params, timeout=10)
    
    print(f"\nURL CONSULTADA:")
    print(f"{response.url}")
    print(f"\nSTATUS CODE: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        # LOGUEAR RESPUESTA COMPLETA
        print(f"\n{'='*60}")
        print("RESPUESTA COMPLETA DE LA API (JSON):")
        print(f"{'='*60}")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"{'='*60}\n")
        
        # ESTRUCTURA DE LA RESPUESTA
        print("ESTRUCTURA DE LA RESPUESTA:")
        print(f"  - Claves principales: {list(data.keys())}")
        if 'current' in data:
            print(f"  - Datos actuales: {list(data['current'].keys())}")
        if 'hourly' in data:
            print(f"  - Datos horarios: {list(data['hourly'].keys())}")
            print(f"  - Total horas en pronóstico: {len(data['hourly']['time'])}")
        print()
        
        # Temperatura actual
        temp_actual = data['current']['temperature_2m']
        humedad = data['current']['relative_humidity_2m']
        viento = data['current']['wind_speed_10m']
        
        print(f"✓ Temperatura ACTUAL: {temp_actual}°C")
        print(f"  Humedad: {humedad}%")
        print(f"  Viento: {viento} km/h")
        
        # Diferencia con medición
        diferencia = abs(temp_actual - temp_medida)
        print(f"\n  DIFERENCIA: {diferencia:.1f}°C")
        if diferencia < 2:
            print(f"  ✓ VALIDACION OK - Diferencia aceptable")
        else:
            print(f"  ⚠ ALERTA - Diferencia significativa")
        
        # Pronóstico próximas 24 horas
        print(f"\n  PRONOSTICO PROXIMAS 24 HORAS:")
        for i in range(0, 24, 6):  # Cada 6 horas
            hora = data['hourly']['time'][i]
            temp = data['hourly']['temperature_2m'][i]
            print(f"    {hora}: {temp}°C")
            
    else:
        print(f"✗ Error: {response.status_code}")
        
except Exception as e:
    print(f"✗ Error Open-Meteo: {e}")

# ============================================
# 2. WEATHERAPI.COM (Gratuita con registro)
# ============================================
print("\n2. CONSULTANDO WEATHERAPI.COM...")
print("  (Requiere API key gratuita - https://www.weatherapi.com/)")
# API_KEY = "TU_API_KEY_AQUI"  # Descomentar y agregar key
# try:
#     url = f"http://api.weatherapi.com/v1/forecast.json"
#     params = {
#         'key': API_KEY,
#         'q': f"{lat},{lon}",
#         'days': 3,
#         'aqi': 'no'
#     }
#     response = requests.get(url, params=params, timeout=10)
#     if response.status_code == 200:
#         data = response.json()
#         temp_actual = data['current']['temp_c']
#         print(f"✓ Temperatura ACTUAL: {temp_actual}°C")
# except Exception as e:
#     print(f"✗ Error WeatherAPI: {e}")

# ============================================
# 3. OPEN-WEATHER MAP (Gratuita con registro)
# ============================================
print("\n3. CONSULTANDO OPENWEATHERMAP...")
print("  (Requiere API key gratuita - https://openweathermap.org/api)")
# API_KEY = "TU_API_KEY_AQUI"  # Descomentar y agregar key
# try:
#     url = "https://api.openweathermap.org/data/2.5/weather"
#     params = {
#         'lat': lat,
#         'lon': lon,
#         'appid': API_KEY,
#         'units': 'metric'
#     }
#     response = requests.get(url, params=params, timeout=10)
#     if response.status_code == 200:
#         data = response.json()
#         temp_actual = data['main']['temp']
#         print(f"✓ Temperatura ACTUAL: {temp_actual}°C")
# except Exception as e:
#     print(f"✗ Error OpenWeatherMap: {e}")

# ============================================
# RESUMEN DE VALIDACION
# ============================================
print("\n" + "=" * 60)
print("RESUMEN DE VALIDACION")
print("=" * 60)
print(f"Ubicación: Río Negro, Argentina ({lat}, {lon})")
print(f"Temperatura MEDIDA (hardcoded): {temp_medida}°C")
print(f"Temperatura API (Open-Meteo): {temp_actual}°C")
print(f"Diferencia: {diferencia:.1f}°C")

if diferencia < 2:
    print("\n✓ SENSOR CALIBRADO CORRECTAMENTE")
elif diferencia < 5:
    print("\n⚠ REVISAR CALIBRACION DEL SENSOR")
else:
    print("\n✗ SENSOR DESCALIBRADO - REQUIERE ATENCION")

print("\n" + "=" * 60)
print("APIS DISPONIBLES:")
print("=" * 60)
print("1. Open-Meteo (GRATIS, sin registro)")
print("   https://open-meteo.com/")
print("\n2. WeatherAPI.com (GRATIS hasta 1M llamadas/mes)")
print("   https://www.weatherapi.com/")
print("\n3. OpenWeatherMap (GRATIS hasta 1000 llamadas/día)")
print("   https://openweathermap.org/api")
print("\n4. INTA Argentina (datos agrometeorológicos)")
print("   https://www.argentina.gob.ar/inta")
print("\n5. SMN Argentina (Servicio Meteorológico Nacional)")
print("   https://www.smn.gob.ar/")
print("=" * 60)
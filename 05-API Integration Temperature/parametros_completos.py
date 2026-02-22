import requests
import json

print("=== PARAMETROS COMPLETOS DISPONIBLES EN OPEN-METEO ===\n")

lat = -39.164
lon = -67.035

# ============================================
# CONSULTA CON TODOS LOS PARAMETROS AGRICOLAS
# ============================================
url = "https://api.open-meteo.com/v1/forecast"
params = {
    'latitude': lat,
    'longitude': lon,
    'timezone': 'America/Argentina/Buenos_Aires',
    'forecast_days': 3,
    
    # PARAMETROS ACTUALES
    'current': [
        'temperature_2m',           # Temperatura a 2m
        'relative_humidity_2m',     # Humedad relativa
        'apparent_temperature',     # Sensación térmica
        'precipitation',            # Precipitación
        'rain',                     # Lluvia
        'snowfall',                 # Nieve
        'weather_code',             # Código de clima
        'cloud_cover',              # Cobertura de nubes
        'pressure_msl',             # Presión atmosférica
        'surface_pressure',         # Presión superficial
        'wind_speed_10m',           # Velocidad viento 10m
        'wind_direction_10m',       # Dirección viento
        'wind_gusts_10m',           # Ráfagas de viento
    ],
    
    # PARAMETROS HORARIOS (72 valores)
    'hourly': [
        'temperature_2m',           # Temperatura
        'relative_humidity_2m',     # Humedad
        'dew_point_2m',            # Punto de rocío
        'apparent_temperature',     # Sensación térmica
        'precipitation_probability', # Probabilidad lluvia
        'precipitation',            # Precipitación
        'rain',                     # Lluvia
        'snowfall',                 # Nieve
        'weather_code',             # Código clima
        'cloud_cover',              # Nubes
        'visibility',               # Visibilidad
        'evapotranspiration',       # Evapotranspiración (CLAVE AGRICULTURA)
        'et0_fao_evapotranspiration', # ET0 FAO (RIEGO)
        'vapour_pressure_deficit',  # Déficit presión vapor (ESTRÉS PLANTAS)
        'wind_speed_10m',           # Viento
        'wind_direction_10m',       # Dirección viento
        'wind_gusts_10m',           # Ráfagas
        'soil_temperature_0cm',     # Temp suelo superficie
        'soil_temperature_6cm',     # Temp suelo 6cm
        'soil_temperature_18cm',    # Temp suelo 18cm
        'soil_temperature_54cm',    # Temp suelo 54cm
        'soil_moisture_0_to_1cm',   # Humedad suelo 0-1cm
        'soil_moisture_1_to_3cm',   # Humedad suelo 1-3cm
        'soil_moisture_3_to_9cm',   # Humedad suelo 3-9cm
        'soil_moisture_9_to_27cm',  # Humedad suelo 9-27cm
        'soil_moisture_27_to_81cm', # Humedad suelo 27-81cm
    ],
    
    # PARAMETROS DIARIOS (3 valores)
    'daily': [
        'temperature_2m_max',       # Temp máxima
        'temperature_2m_min',       # Temp mínima
        'apparent_temperature_max', # Sensación térmica máx
        'apparent_temperature_min', # Sensación térmica mín
        'sunrise',                  # Amanecer
        'sunset',                   # Atardecer
        'daylight_duration',        # Duración día
        'sunshine_duration',        # Duración sol
        'precipitation_sum',        # Precipitación total
        'rain_sum',                 # Lluvia total
        'precipitation_hours',      # Horas de lluvia
        'precipitation_probability_max', # Prob máx lluvia
        'wind_speed_10m_max',       # Viento máximo
        'wind_gusts_10m_max',       # Ráfaga máxima
        'wind_direction_10m_dominant', # Dirección dominante
        'et0_fao_evapotranspiration', # ET0 diario
    ]
}

print("Consultando API con TODOS los parámetros agrícolas...")
print(f"Coordenada: ({lat}, {lon})")
print("-" * 80)

try:
    response = requests.get(url, params=params, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n" + "="*80)
        print("DATOS ACTUALES")
        print("="*80)
        current = data['current']
        print(f"Hora: {current['time']}")
        print(f"Temperatura: {current['temperature_2m']}°C")
        print(f"Sensación térmica: {current['apparent_temperature']}°C")
        print(f"Humedad: {current['relative_humidity_2m']}%")
        print(f"Precipitación: {current['precipitation']} mm")
        print(f"Lluvia: {current['rain']} mm")
        print(f"Cobertura nubes: {current['cloud_cover']}%")
        print(f"Presión: {current['pressure_msl']} hPa")
        print(f"Viento: {current['wind_speed_10m']} km/h")
        print(f"Dirección viento: {current['wind_direction_10m']}°")
        print(f"Ráfagas: {current['wind_gusts_10m']} km/h")
        
        print("\n" + "="*80)
        print("RESUMEN DIARIO (Próximos 3 días)")
        print("="*80)
        daily = data['daily']
        for i in range(len(daily['time'])):
            print(f"\nDía {i+1}: {daily['time'][i]}")
            print(f"  Temp: {daily['temperature_2m_min'][i]}°C - {daily['temperature_2m_max'][i]}°C")
            print(f"  Precipitación: {daily['precipitation_sum'][i]} mm")
            print(f"  Prob. lluvia: {daily['precipitation_probability_max'][i]}%")
            print(f"  Horas de lluvia: {daily['precipitation_hours'][i]}h")
            print(f"  Viento máx: {daily['wind_speed_10m_max'][i]} km/h")
            print(f"  ET0 (evapotranspiración): {daily['et0_fao_evapotranspiration'][i]} mm")
            print(f"  Amanecer: {daily['sunrise'][i]}")
            print(f"  Atardecer: {daily['sunset'][i]}")
        
        print("\n" + "="*80)
        print("DATOS DE SUELO (Actual)")
        print("="*80)
        hourly = data['hourly']
        idx = 0  # Primera hora
        print(f"Temperatura suelo:")
        print(f"  Superficie: {hourly['soil_temperature_0cm'][idx]}°C")
        print(f"  6cm: {hourly['soil_temperature_6cm'][idx]}°C")
        print(f"  18cm: {hourly['soil_temperature_18cm'][idx]}°C")
        print(f"  54cm: {hourly['soil_temperature_54cm'][idx]}°C")
        print(f"\nHumedad suelo:")
        print(f"  0-1cm: {hourly['soil_moisture_0_to_1cm'][idx]} m³/m³")
        print(f"  1-3cm: {hourly['soil_moisture_1_to_3cm'][idx]} m³/m³")
        print(f"  3-9cm: {hourly['soil_moisture_3_to_9cm'][idx]} m³/m³")
        print(f"  9-27cm: {hourly['soil_moisture_9_to_27cm'][idx]} m³/m³")
        print(f"  27-81cm: {hourly['soil_moisture_27_to_81cm'][idx]} m³/m³")
        
        print("\n" + "="*80)
        print("PARAMETROS AGRICOLAS CLAVE")
        print("="*80)
        print(f"Punto de rocío: {hourly['dew_point_2m'][idx]}°C")
        print(f"Evapotranspiración: {hourly['evapotranspiration'][idx]} mm")
        print(f"ET0 FAO: {hourly['et0_fao_evapotranspiration'][idx]} mm")
        print(f"Déficit presión vapor: {hourly['vapour_pressure_deficit'][idx]} kPa")
        print(f"  (Indica estrés hídrico en plantas)")
        
        # Guardar respuesta completa
        with open('respuesta_completa.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("\n✓ Respuesta completa guardada en: respuesta_completa.json")
        
    else:
        print(f"✗ Error: {response.status_code}")
        
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*80)
print("PARAMETROS MAS UTILES PARA AGRICULTURA")
print("="*80)
print("""
1. TEMPERATURA
   - temperature_2m: Temperatura aire
   - soil_temperature_*: Temperatura suelo (germinación)
   
2. HUMEDAD
   - relative_humidity_2m: Humedad aire
   - soil_moisture_*: Humedad suelo (riego)
   - dew_point_2m: Punto rocío (enfermedades)
   
3. AGUA
   - precipitation: Precipitación
   - rain: Lluvia
   - et0_fao_evapotranspiration: Necesidad riego (FAO)
   - vapour_pressure_deficit: Estrés hídrico plantas
   
4. VIENTO
   - wind_speed_10m: Velocidad (aplicación fitosanitarios)
   - wind_gusts_10m: Ráfagas (daño cultivos)
   
5. RADIACION
   - sunshine_duration: Horas sol (fotosíntesis)
   - cloud_cover: Cobertura nubes
   
6. OTROS
   - weather_code: Código clima (0-99)
   - visibility: Visibilidad
   - pressure_msl: Presión atmosférica
""")
import pandas as pd
import numpy as np
import requests
import time

print("=== FINCA RIO NEGRO - SENSORES MULTINIVEL ===")

# Coordenadas exactas
lat_norte = -39.163552
lat_sur = -39.169029
lon_oeste = -67.038406
lon_este = -67.028948

# Generar cuadrícula menos densa
paso_lat = 0.0008   # ~88m
paso_lon = 0.0010   # ~88m

def obtener_altitud_real(lat, lon):
    """Obtiene altitud real usando API gratuita"""
    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['results'][0]['elevation']
        else:
            return 280  # Fallback
    except:
        return 280  # Fallback si falla la API

sensores = []
np.random.seed(2024)

print("Generando sensores con altitud real...")

lat_current = lat_norte
sensor_num = 1

while lat_current >= lat_sur:
    lon_current = lon_oeste
    while lon_current <= lon_este:
        
        # Obtener altitud real del terreno
        altitud_terreno = obtener_altitud_real(lat_current, lon_current)
        print(f"Sensor {sensor_num} -> Altitud: {altitud_terreno}m")
        time.sleep(0.1)  # Pausa para no saturar la API
        
        # Generar temperaturas a diferentes alturas
        temp_base = np.random.normal(15, 3)  # Temperatura base
        
        # Temperaturas a diferentes alturas (generalmente más frío arriba)
        temp_1m = round(temp_base + np.random.normal(0, 0.5), 1)
        temp_2m = round(temp_base + np.random.normal(-0.5, 0.5), 1)
        temp_5m = round(temp_base + np.random.normal(-1.0, 0.5), 1)
        temp_10m = round(temp_base + np.random.normal(-1.5, 0.5), 1)
        
        sensores.append({
            'latitude': lat_current,
            'longitude': lon_current,
            'altitude_terrain': altitud_terreno,  # Altitud del terreno
            'elevation_1m': 1,       # 1m sobre terreno
            'elevation_2m': 2,       # 2m sobre terreno
            'elevation_5m': 5,       # 5m sobre terreno
            'elevation_10m': 10,     # 10m sobre terreno
            'sensor_id': f'S_{sensor_num:03d}',
            'temp_1m': temp_1m,    # Temperatura a 1m
            'temp_2m': temp_2m,    # Temperatura a 2m
            'temp_5m': temp_5m,    # Temperatura a 5m
            'temp_10m': temp_10m,  # Temperatura a 10m
        })
        
        sensor_num += 1
        lon_current += paso_lon
    lat_current -= paso_lat

df = pd.DataFrame(sensores)
print(f"Total sensores: {len(df)}")

# Crear mapa con configuración automática
try:
    from keplergl import KeplerGl
    
    mapa = KeplerGl(height=700)
    mapa.add_data(data=df, name='sensores')
    
    # Configuración que fuerza la selección automática de elevation
    config = {
        'version': 'v1',
        'config': {
            'mapState': {
                'latitude': df['latitude'].mean(),
                'longitude': df['longitude'].mean(),
                'zoom': 15,
                'pitch': 50,
                'bearing': 0
            },
            'mapStyle': {'styleType': 'satellite'},
            'visState': {
                'filters': [],
                'layers': [
                    {
                        'id': 'temp_1m_layer',
                        'type': 'point',
                        'config': {
                            'dataId': 'sensores',
                            'label': 'Temperatura 1m',
                            'color': [255, 0, 0],
                            'columns': {
                                'lat': 'latitude',
                                'lng': 'longitude',
                                'altitude': 'elevation_1m'  # CLAVE: especificar columna altitude
                            },
                            'isVisible': True,
                            'visConfig': {
                                'radius': 10,
                                'opacity': 0.8,
                                'outline': False,
                                'thickness': 2,
                                'strokeColor': [255, 255, 255],
                                'colorRange': {
                                    'name': 'Global Warming',
                                    'type': 'sequential',
                                    'category': 'Uber',
                                    'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                                },
                                'strokeColorRange': {
                                    'name': 'Global Warming',
                                    'type': 'sequential',
                                    'category': 'Uber',
                                    'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                                },
                                'radiusRange': [0, 50],
                                'filled': True,
                                'enable3d': True,
                                'elevationScale': 5
                            }
                        },
                        'visualChannels': {
                            'colorField': {
                                'name': 'temp_1m',
                                'type': 'real'
                            },
                            'colorScale': 'quantile',
                            'heightField': {
                                'name': 'elevation_1m',
                                'type': 'real'
                            },
                            'heightScale': 'linear'
                        }
                    }
                ]
            }
        }
    }
    
    mapa.config = config
    mapa.save_to_html(file_name='finca_simple_mapa.html')
    print("Mapa guardado: finca_simple_mapa.html")
    
except ImportError:
    print("Keplergl no disponible")
except Exception as e:
    print(f"Error en mapa: {e}")

df.to_csv('finca_simple_datos.csv', index=False)
print("CSV guardado: finca_simple_datos.csv")
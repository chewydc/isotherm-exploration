import pandas as pd
import numpy as np
import requests
import time

print("=== HEATMAP MULTICAPA CON RELIEVE 3D ===")

# Coordenadas exactas
lat_norte = -39.163552
lat_sur = -39.169029
lon_oeste = -67.038406
lon_este = -67.028948

paso_lat = 0.0008
paso_lon = 0.0010

def obtener_altitud_real(lat, lon):
    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['results'][0]['elevation']
        else:
            return 280
    except:
        return 280

sensores = []
np.random.seed(2024)

print("Generando 80 sensores con altitud real y 4 capas térmicas...")

# Centros térmicos diferentes para cada altura
centros_1m = [(-39.164, -67.035, 18), (-39.167, -67.031, 16)]
centros_2m = [(-39.165, -67.036, 17), (-39.168, -67.032, 15)]
centros_5m = [(-39.166, -67.034, 16), (-39.164, -67.030, 14)]
centros_10m = [(-39.167, -67.035, 15), (-39.165, -67.031, 13)]

def calcular_temperatura(lat, lon, centros, temp_base):
    temp = temp_base
    for lat_c, lon_c, temp_c in centros:
        distancia = np.sqrt((lat - lat_c)**2 + (lon - lon_c)**2)
        influencia = np.exp(-distancia * 800)
        temp += (temp_c - temp_base) * influencia
    return temp + np.random.normal(0, 0.8)

lat_current = lat_norte
sensor_num = 1

while lat_current >= lat_sur:
    lon_current = lon_oeste
    while lon_current <= lon_este:
        
        # Obtener altitud real
        altitud_terreno = obtener_altitud_real(lat_current, lon_current)
        print(f"Sensor {sensor_num} -> Altitud: {altitud_terreno}m")
        time.sleep(0.05)
        
        temp_1m = round(calcular_temperatura(lat_current, lon_current, centros_1m, 12), 1)
        temp_2m = round(calcular_temperatura(lat_current, lon_current, centros_2m, 11.5), 1)
        temp_5m = round(calcular_temperatura(lat_current, lon_current, centros_5m, 11), 1)
        temp_10m = round(calcular_temperatura(lat_current, lon_current, centros_10m, 10.5), 1)
        
        sensores.append({
            'latitude': lat_current,
            'longitude': lon_current,
            'altitude_terrain': altitud_terreno,
            'temp_1m': temp_1m,
            'temp_2m': temp_2m,
            'temp_5m': temp_5m,
            'temp_10m': temp_10m,
            'sensor_id': f'S_{sensor_num:03d}'
        })
        
        sensor_num += 1
        lon_current += paso_lon
    lat_current -= paso_lat

df = pd.DataFrame(sensores)
print(f"Sensores: {len(df)}")
print(f"Altitud: {df['altitude_terrain'].min():.1f} - {df['altitude_terrain'].max():.1f}m")
print(f"Temp 1m: {df['temp_1m'].min():.1f} - {df['temp_1m'].max():.1f}°C")

try:
    from keplergl import KeplerGl
    
    mapa = KeplerGl(height=700)
    mapa.add_data(data=df, name='heatmap_3d')
    
    config = {
        'version': 'v1',
        'config': {
            'mapState': {
                'latitude': df['latitude'].mean(),
                'longitude': df['longitude'].mean(),
                'zoom': 15,
                'pitch': 45,  # Vista 3D
                'bearing': 0
            },
            'mapStyle': {'styleType': 'satellite'},
            'visState': {
                'layers': [
                    {
                        'id': 'heatmap_1m',
                        'type': 'heatmap',
                        'config': {
                            'dataId': 'heatmap_3d',
                            'label': 'Heatmap 1m altura',
                            'columns': {
                                'lat': 'latitude', 
                                'lng': 'longitude',
                                'altitude': 'altitude_terrain'  # RELIEVE 3D
                            },
                            'isVisible': True,
                            'visConfig': {
                                'opacity': 0.8,
                                'colorRange': {
                                    'colors': ['#0000FF', '#0080FF', '#00FFFF', '#80FF80', '#FFFF00', '#FF8000', '#FF0000']
                                },
                                'radius': 150,  # Radio mayor
                                'enable3d': True,  # Habilitar 3D
                                'elevationScale': 0.1  # Escala del relieve
                            }
                        },
                        'visualChannels': {
                            'weightField': {'name': 'temp_1m', 'type': 'real'},
                            'heightField': {'name': 'altitude_terrain', 'type': 'real'}
                        }
                    },
                    {
                        'id': 'heatmap_2m',
                        'type': 'heatmap',
                        'config': {
                            'dataId': 'heatmap_3d',
                            'label': 'Heatmap 2m altura',
                            'columns': {
                                'lat': 'latitude', 
                                'lng': 'longitude',
                                'altitude': 'altitude_terrain'
                            },
                            'isVisible': False,
                            'visConfig': {
                                'opacity': 0.8,
                                'colorRange': {
                                    'colors': ['#0000FF', '#0080FF', '#00FFFF', '#80FF80', '#FFFF00', '#FF8000', '#FF0000']
                                },
                                'radius': 150,
                                'enable3d': True,
                                'elevationScale': 0.1
                            }
                        },
                        'visualChannels': {
                            'weightField': {'name': 'temp_2m', 'type': 'real'},
                            'heightField': {'name': 'altitude_terrain', 'type': 'real'}
                        }
                    },
                    {
                        'id': 'heatmap_5m',
                        'type': 'heatmap',
                        'config': {
                            'dataId': 'heatmap_3d',
                            'label': 'Heatmap 5m altura',
                            'columns': {
                                'lat': 'latitude', 
                                'lng': 'longitude',
                                'altitude': 'altitude_terrain'
                            },
                            'isVisible': False,
                            'visConfig': {
                                'opacity': 0.8,
                                'colorRange': {
                                    'colors': ['#0000FF', '#0080FF', '#00FFFF', '#80FF80', '#FFFF00', '#FF8000', '#FF0000']
                                },
                                'radius': 150,
                                'enable3d': True,
                                'elevationScale': 0.1
                            }
                        },
                        'visualChannels': {
                            'weightField': {'name': 'temp_5m', 'type': 'real'},
                            'heightField': {'name': 'altitude_terrain', 'type': 'real'}
                        }
                    },
                    {
                        'id': 'heatmap_10m',
                        'type': 'heatmap',
                        'config': {
                            'dataId': 'heatmap_3d',
                            'label': 'Heatmap 10m altura',
                            'columns': {
                                'lat': 'latitude', 
                                'lng': 'longitude',
                                'altitude': 'altitude_terrain'
                            },
                            'isVisible': False,
                            'visConfig': {
                                'opacity': 0.8,
                                'colorRange': {
                                    'colors': ['#0000FF', '#0080FF', '#00FFFF', '#80FF80', '#FFFF00', '#FF8000', '#FF0000']
                                },
                                'radius': 150,
                                'enable3d': True,
                                'elevationScale': 0.1
                            }
                        },
                        'visualChannels': {
                            'weightField': {'name': 'temp_10m', 'type': 'real'},
                            'heightField': {'name': 'altitude_terrain', 'type': 'real'}
                        }
                    }
                ]
            }
        }
    }
    
    mapa.config = config
    mapa.save_to_html(file_name='heatmap_3d_final.html')
    print("Heatmap 3D final guardado: heatmap_3d_final.html")
    print("4 capas intercambiables con relieve del terreno")
    
except Exception as e:
    print(f"Error: {e}")

df.to_csv('heatmap_3d_final.csv', index=False)
print("CSV guardado: heatmap_3d_final.csv")
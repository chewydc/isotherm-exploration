import pandas as pd
import numpy as np
import requests
import time

print("=== FINCA RÍO NEGRO - SENSORES MULTINIVEL ===")

# Coordenadas exactas
lat_norte = -39.163552
lat_sur = -39.169029
lon_oeste = -67.038406
lon_este = -67.028948

# Generar cuadrícula menos densa
paso_lat = 0.0008   # ~88m
paso_lon = 0.0010   # ~88m

# CALCULAR TOTAL DE PUNTOS ANTES DE CREARLOS
num_filas = int((lat_norte - lat_sur) / paso_lat) + 1
num_cols = int((lon_este - lon_oeste) / paso_lon) + 1
total_puntos = num_filas * num_cols

print(f"📊 RESUMEN PREVIO:")
print(f"   Área: {abs(lat_norte-lat_sur)*111000:.0f}m x {abs(lon_este-lon_oeste)*111000*np.cos(np.radians(-39)):.0f}m")
print(f"   Espaciado: ~88m entre sensores")
print(f"   Cuadrícula: {num_filas} filas x {num_cols} columnas")
print(f"   🎯 TOTAL A GENERAR: {total_puntos} sensores")
print(f"   ⏱️ Tiempo estimado: ~{total_puntos*2/60:.1f} minutos (API + pausa)")
print(f"   📡 Consultando altitud real para cada punto...")
print()

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
        inicio = time.time()
        altitud_terreno = obtener_altitud_real(lat_current, lon_current)
        tiempo_api = time.time() - inicio
        print(f"Sensor {sensor_num}/{total_puntos} → Altitud: {altitud_terreno}m (API: {tiempo_api:.1f}s)")
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
            'altitude_1m': altitud_terreno + 1,   # Altitud a 1m
            'altitude_2m': altitud_terreno + 2,   # Altitud a 2m
            'altitude_5m': altitud_terreno + 5,   # Altitud a 5m
            'altitude_10m': altitud_terreno + 10, # Altitud a 10m
            # Elevaciones relativas para visualización 3D
            'elevation_terrain': 0,  # Terreno = base (0m)
            'elevation_1m': 1,       # 1m sobre terreno
            'elevation_2m': 2,       # 2m sobre terreno
            'elevation_5m': 5,       # 5m sobre terreno
            'elevation_10m': 10,     # 10m sobre terreno
            'sensor_id': f'S_{sensor_num:03d}',
            'temp_1m': temp_1m,    # Temperatura a 1m
            'temp_2m': temp_2m,    # Temperatura a 2m
            'temp_5m': temp_5m,    # Temperatura a 5m
            'temp_10m': temp_10m,  # Temperatura a 10m
            'temp_promedio': round((temp_1m + temp_2m + temp_5m + temp_10m) / 4, 1)
        })
        
        sensor_num += 1
        lon_current += paso_lon
    lat_current -= paso_lat

df = pd.DataFrame(sensores)
print(f"✓ Total sensores: {len(df)}")
print(f"✓ Altitud terreno: {df['altitude_terrain'].min():.1f}m - {df['altitude_terrain'].max():.1f}m")

# Calcular escala de elevación automática
# Kepler.gl usa elevación relativa - 1 metro = 1 unidad visual
escala_automatica = 1.0  # Sin escala - 1:1 real
print(f"✓ Escala de elevación: 1:1 (sin amplificación)")
print(f"✓ 1m real = 1m visual en el mapa")

# Crear mapa
try:
    from keplergl import KeplerGl
    
    mapa = KeplerGl(height=700)
    mapa.add_data(data=df, name='sensores_multinivel')
    
    config = {
        'version': 'v1',
        'config': {
            'mapState': {
                'latitude': df['latitude'].mean(),
                'longitude': df['longitude'].mean(),
                'zoom': 15,
                'pitch': 50,  # Vista 3D inclinada
                'bearing': 0
            },
            'mapStyle': {'styleType': 'satellite'},
            'visState': {
                'layers': [
                    # CAPA 1: Temperatura a 1m (visible por defecto)
                    {
                        'id': 'temp_1m',
                        'type': 'point',
                        'config': {
                            'dataId': 'sensores_multinivel',
                            'label': 'Temperatura 1m',
                            'columns': {'lat': 'latitude', 'lng': 'longitude'},
                            'isVisible': True,  # Visible por defecto
                            'visConfig': {
                                'radius': 8,
                                'opacity': 0.8,
                                'outline': False,
                                'filled': True,
                                'enable3d': True,  # Habilitar 3D
                                'elevationScale': escala_automatica,  # Escala calculada automáticamente
                                'colorRange': {
                                    'name': 'Temperatura',
                                    'colors': ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffcc', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                                }
                            }
                        },
                        'visualChannels': {
                            'colorField': {'name': 'temp_1m', 'type': 'real'},
                            'heightField': {'name': 'elevation_1m', 'type': 'real'}
                        }
                    },
                    # CAPA 2: Temperatura a 2m (oculta)
                    {
                        'id': 'temp_2m',
                        'type': 'point',
                        'config': {
                            'dataId': 'sensores_multinivel',
                            'label': 'Temperatura 2m',
                            'columns': {'lat': 'latitude', 'lng': 'longitude'},
                            'isVisible': False,
                            'visConfig': {
                                'radius': 8,
                                'opacity': 0.8,
                                'outline': False,
                                'filled': True,
                                'colorRange': {
                                    'name': 'Temperatura',
                                    'colors': ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffcc', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                                }
                            }
                        },
                        'visualChannels': {
                            'colorField': {'name': 'temp_2m', 'type': 'real'},
                            'heightField': {'name': 'elevation_2m', 'type': 'real'}
                        }
                    },
                    # CAPA 3: Temperatura a 5m (oculta)
                    {
                        'id': 'temp_5m',
                        'type': 'point',
                        'config': {
                            'dataId': 'sensores_multinivel',
                            'label': 'Temperatura 5m',
                            'columns': {'lat': 'latitude', 'lng': 'longitude'},
                            'isVisible': False,
                            'visConfig': {
                                'radius': 8,
                                'opacity': 0.8,
                                'outline': False,
                                'filled': True,
                                'colorRange': {
                                    'name': 'Temperatura',
                                    'colors': ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffcc', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                                }
                            }
                        },
                        'visualChannels': {
                            'colorField': {'name': 'temp_5m', 'type': 'real'},
                            'heightField': {'name': 'elevation_5m', 'type': 'real'}
                        }
                    },
                    # CAPA 4: Temperatura a 10m (oculta)
                    {
                        'id': 'temp_10m',
                        'type': 'point',
                        'config': {
                            'dataId': 'sensores_multinivel',
                            'label': 'Temperatura 10m',
                            'columns': {'lat': 'latitude', 'lng': 'longitude'},
                            'isVisible': False,
                            'visConfig': {
                                'radius': 8,
                                'opacity': 0.8,
                                'outline': False,
                                'filled': True,
                                'colorRange': {
                                    'name': 'Temperatura',
                                    'colors': ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffcc', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                                }
                            }
                        },
                        'visualChannels': {
                            'colorField': {'name': 'temp_10m', 'type': 'real'},
                            'heightField': {'name': 'elevation_10m', 'type': 'real'}
                        }
                    },
                    # CAPA 5: Altitud del terreno (oculta)
                    {
                        'id': 'altitud',
                        'type': 'point',
                        'config': {
                            'dataId': 'sensores_multinivel',
                            'label': 'Altitud Terreno',
                            'columns': {'lat': 'latitude', 'lng': 'longitude'},
                            'isVisible': False,
                            'visConfig': {
                                'radius': 8,
                                'opacity': 0.8,
                                'outline': False,
                                'filled': True,
                                'colorRange': {
                                    'name': 'Elevación',
                                    'colors': ['#0571b0', '#92c5de', '#f7f7f7', '#f4a582', '#ca0020']
                                }
                            }
                        },
                        'visualChannels': {
                            'colorField': {'name': 'altitude_terrain', 'type': 'real'}
                        }
                    }
                ]
            }
        }
    }
    
    mapa.config = config
    mapa.save_to_html(file_name='finca_altitude_mapa.html')
    print("✓ Mapa guardado: finca_altitude_mapa.html")
    print("✓ 5 capas configuradas:")
    print("  - Temperatura 1m (visible por defecto)")
    print("  - Temperatura 2m, 5m, 10m (ocultas)")
    print("  - Altitud terreno (oculta)")
    print("✓ Usa el panel de capas para alternar entre niveles")
    
except ImportError:
    print("⚠ Keplergl no disponible")
except Exception as e:
    print(f"Error en mapa: {e}")

df.to_csv('finca_altitude_datos.csv', index=False)
print("✓ CSV guardado con datos multinivel: finca_altitude_datos.csv")
print("\nDatos por sensor:")
print("- Altitud real del terreno")
print("- Temperatura a 1m, 2m, 5m y 10m de altura")
print("- Temperatura promedio")
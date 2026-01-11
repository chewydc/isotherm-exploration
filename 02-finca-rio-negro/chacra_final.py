import pandas as pd
import numpy as np

print("=== CHACRA 143 - VERSIÓN FINAL ===")

# Esquinas exactas con sensores
esquinas = [
    [-39.031090, -67.641083, "NOROESTE"],
    [-39.031584, -67.636841, "NORESTE"],
    [-39.035826, -67.637782, "SURESTE"],
    [-39.035328, -67.641930, "SUROESTE"]
]

def punto_dentro_poligono(lat, lon, esquinas_coords):
    x, y = lon, lat
    n = len(esquinas_coords)
    inside = False
    
    p1x, p1y = esquinas_coords[0][1], esquinas_coords[0][0]
    for i in range(1, n + 1):
        p2x, p2y = esquinas_coords[i % n][1], esquinas_coords[i % n][0]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Generar todos los sensores
sensores = []
np.random.seed(143)

# 1. SENSORES EN LAS 4 ESQUINAS EXACTAS
for i, (lat, lon, nombre) in enumerate(esquinas):
    sensores.append({
        'latitude': lat,
        'longitude': lon,
        'temperature': round(np.random.normal(16, 2.5), 1),
        'sensor_id': f'ESQ_{nombre}',
        'tipo': 'esquina'
    })

# 2. SENSORES INTERNOS CADA 100M
esquinas_coords = [[e[0], e[1]] for e in esquinas]
lats = [e[0] for e in esquinas]
lons = [e[1] for e in esquinas]
lat_min, lat_max = min(lats), max(lats)
lon_min, lon_max = min(lons), max(lons)

paso_lat, paso_lon = 0.0009, 0.0012
sensor_num = 1

lat_current = lat_min
while lat_current <= lat_max:
    lon_current = lon_min
    while lon_current <= lon_max:
        # Evitar duplicar las esquinas exactas
        es_esquina = any(abs(lat_current - e[0]) < 0.0001 and abs(lon_current - e[1]) < 0.0001 for e in esquinas)
        
        if not es_esquina and punto_dentro_poligono(lat_current, lon_current, esquinas_coords):
            sensores.append({
                'latitude': lat_current,
                'longitude': lon_current,
                'temperature': round(np.random.normal(16, 2.5), 1),
                'sensor_id': f'S_{sensor_num:03d}',
                'tipo': 'interno'
            })
            sensor_num += 1
        lon_current += paso_lon
    lat_current += paso_lat

df = pd.DataFrame(sensores)
print(f"✓ Total sensores: {len(df)}")
print(f"✓ Esquinas: {len(df[df['tipo']=='esquina'])}")
print(f"✓ Internos: {len(df[df['tipo']=='interno'])}")

# Crear mapa
try:
    from keplergl import KeplerGl
    
    mapa = KeplerGl(height=700)
    mapa.add_data(data=df, name='chacra143')
    
    config = {
        'version': 'v1',
        'config': {
            'mapState': {
                'latitude': df['latitude'].mean(),
                'longitude': df['longitude'].mean(),
                'zoom': 16
            },
            'mapStyle': {'styleType': 'satellite'},
            'visState': {
                'layers': [{
                    'type': 'point',
                    'config': {
                        'dataId': 'chacra143',
                        'columns': {'lat': 'latitude', 'lng': 'longitude'},
                        'visConfig': {
                            'radius': 10,
                            'opacity': 0.8,
                            'outline': False,
                            'filled': True,
                            'colorRange': {
                                'colors': ['#0571b0', '#92c5de', '#f7f7f7', '#f4a582', '#ca0020']
                            }
                        }
                    },
                    'visualChannels': {
                        'colorField': {'name': 'temperature', 'type': 'real'}
                    }
                }]
            }
        }
    }
    
    mapa.config = config
    mapa.save_to_html(file_name='chacra_143_final.html')
    print("✓ Mapa final: chacra_143_final.html")
    
except ImportError:
    print("⚠ Keplergl no disponible")

df.to_csv('chacra_143_final.csv', index=False)
print("✓ Datos finales: chacra_143_final.csv")
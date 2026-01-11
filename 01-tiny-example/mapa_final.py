import pandas as pd
from keplergl import KeplerGl

# Cargar datos
df = pd.read_csv('datos.csv')
print(f"Datos: {len(df)} puntos")
print(f"Lat range: {df['latitude'].min():.4f} - {df['latitude'].max():.4f}")
print(f"Lon range: {df['longitude'].min():.4f} - {df['longitude'].max():.4f}")

# Crear mapa
mapa = KeplerGl(height=600)
mapa.add_data(data=df, name='temperatura')

# Configuración con zoom apropiado
config = {
    'version': 'v1',
    'config': {
        'mapState': {
            'latitude': df['latitude'].mean(),
            'longitude': df['longitude'].mean(),
            'zoom': 10,
            'pitch': 0,
            'bearing': 0
        },
        'mapStyle': {
            'styleType': 'dark',
            'topLayerGroups': {},
            'visibleLayerGroups': {
                'label': True,
                'road': True,
                'border': False,
                'building': True,
                'water': True,
                'land': True
            }
        },
        'visState': {
            'layers': [{
                'id': 'puntos',
                'type': 'point',
                'config': {
                    'dataId': 'temperatura',
                    'columns': {
                        'lat': 'latitude',
                        'lng': 'longitude'
                    },
                    'isVisible': True,
                    'visConfig': {
                        'radius': 15,
                        'fixedRadius': False,
                        'opacity': 0.8,
                        'outline': False,
                        'thickness': 2,
                        'strokeColor': [255, 255, 255],
                        'colorRange': {
                            'name': 'Global Warming',
                            'type': 'sequential',
                            'category': 'Uber',
                            'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                        }
                    }
                },
                'visualChannels': {
                    'colorField': {
                        'name': 'temperature',
                        'type': 'real'
                    },
                    'sizeField': None
                }
            }]
        }
    }
}

mapa.config = config
mapa.save_to_html(file_name='mapa_madrid.html')
print("Mapa guardado: mapa_madrid.html")
print("Deberías ver Madrid con puntos de colores según temperatura")
import pandas as pd
from keplergl import KeplerGl

# Cargar datos
df = pd.read_csv('datos.csv')
print(f"Datos cargados: {len(df)} puntos")

# Crear mapa con configuración
mapa = KeplerGl(height=600)
mapa.add_data(data=df, name='temperatura')

# Configuración para mostrar puntos automáticamente
config = {
    'version': 'v1',
    'config': {
        'mapState': {
            'latitude': 40.4168,
            'longitude': -3.7038,
            'zoom': 11
        },
        'visState': {
            'layers': [{
                'id': 'temperatura',
                'type': 'point',
                'config': {
                    'dataId': 'temperatura',
                    'columns': {
                        'lat': 'latitude',
                        'lng': 'longitude'
                    },
                    'visConfig': {
                        'radius': 10,
                        'opacity': 0.8,
                        'colorRange': {
                            'colors': ['#440154', '#31688e', '#35b779', '#fde725']
                        }
                    }
                },
                'visualChannels': {
                    'colorField': {
                        'name': 'temperature',
                        'type': 'real'
                    }
                }
            }]
        }
    }
}

# Aplicar configuración
mapa.config = config

# Guardar HTML
mapa.save_to_html(file_name='mapa_configurado.html')
print("Mapa configurado guardado como: mapa_configurado.html")
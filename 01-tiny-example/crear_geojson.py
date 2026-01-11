import pandas as pd
import json

# Leer datos
df = pd.read_csv('datos.csv')

# Convertir a formato GeoJSON para Kepler.gl web
geojson = {
    "type": "FeatureCollection",
    "features": []
}

for _, row in df.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "temperature": row['temperature']
        }
    }
    geojson["features"].append(feature)

# Guardar GeoJSON
with open('datos.geojson', 'w') as f:
    json.dump(geojson, f, indent=2)

print("Archivo datos.geojson creado")
print("Ve a https://kepler.gl/demo y arrastra el archivo datos.geojson")
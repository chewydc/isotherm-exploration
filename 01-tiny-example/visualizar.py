import pandas as pd
from keplergl import KeplerGl

# Leer CSV
df = pd.read_csv('datos.csv')
print(f"Datos cargados: {len(df)} registros")

# Crear mapa
mapa = KeplerGl(height=600)
mapa.add_data(data=df, name='temperatura')

# Guardar HTML
mapa.save_to_html(file_name='mapa.html')
print("Mapa guardado: mapa.html")
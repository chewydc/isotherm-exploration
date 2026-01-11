import pandas as pd
from keplergl import KeplerGl

# Cargar datos
df = pd.read_csv('datos.csv')
print(f"Datos cargados: {len(df)} puntos")

# Crear mapa
mapa = KeplerGl(height=600)
mapa.add_data(data=df, name='temperatura')

# Guardar como HTML (funciona sin extensiones)
mapa.save_to_html(file_name='mapa_kepler.html')
print("Mapa guardado como: mapa_kepler.html")
print("Abre el archivo HTML en tu navegador")
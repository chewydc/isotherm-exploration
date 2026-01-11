import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer datos
df = pd.read_csv('datos.csv')
print(f"Datos: {len(df)} puntos")

# Crear mapa de calor
plt.figure(figsize=(10, 8))
plt.scatter(df['longitude'], df['latitude'], c=df['temperature'], 
           cmap='hot', s=100, alpha=0.7)
plt.colorbar(label='Temperatura °C')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.title('Mapa de Calor - Madrid')
plt.grid(True, alpha=0.3)
plt.savefig('mapa_calor.png', dpi=300, bbox_inches='tight')
plt.show()
print("Mapa guardado: mapa_calor.png")
import pandas as pd
import numpy as np

# Datos de ejemplo - Madrid
np.random.seed(42)
data = pd.DataFrame({
    'latitude': np.random.uniform(40.35, 40.50, 50),
    'longitude': np.random.uniform(-3.80, -3.60, 50),
    'temperature': np.random.uniform(15, 35, 50)
})

data.to_excel('datos.xlsx', index=False)
print("Excel creado: datos.xlsx")